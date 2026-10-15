"""Behavior and security regression tests for the cleaned lab program."""

import ast
import contextlib
import copy
import importlib.util
import io
from pathlib import Path
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1] / "gym_membership_system.py"
SPEC = importlib.util.spec_from_file_location("gym", SOURCE)
gym = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gym)


class MembershipTests(unittest.TestCase):
    """Verify supported behavior and former unsafe input paths."""

    def setUp(self):
        self.original = copy.deepcopy(gym.members)

    def tearDown(self):
        gym.members.clear()
        gym.members.update(self.original)

    def test_registration_and_caller_log(self):
        log = []
        self.assertTrue(gym.register_member("M04", "Diana", "Gold", 3, log))
        self.assertEqual(gym.members["M04"]["fee"], 150.0)
        self.assertEqual(log, ["Registered M04 for 3 months"])
        self.assertFalse(gym.register_member("M04", "Other", "Gold", 3))
        self.assertFalse(gym.register_member("M05", "Other", "Gold", 0))
        self.assertFalse(gym.register_member("M05", "Other", "Gold", -1))
        self.assertNotIn("M05", gym.members)

    def test_default_logging_does_not_leak_between_calls(self):
        gym.register_member("M04", "Diana", "Gold", 3)
        log = []
        gym.register_member("M05", "Evan", "Silver", 2, log)
        self.assertEqual(log, ["Registered M05 for 2 months"])
        self.assertEqual(gym.register_member.__defaults__, (None,))

    def test_cancel_existing_and_missing_member(self):
        self.assertTrue(gym.cancel_membership("M02"))
        self.assertFalse(gym.cancel_membership("M02"))
        self.assertFalse(gym.check_membership_status("M02"))

    def test_status_and_active_count(self):
        self.assertTrue(gym.check_membership_status("M01"))
        gym.members["M01"]["months_left"] = 0
        self.assertFalse(gym.check_membership_status("M01"))
        self.assertFalse(gym.check_membership_status("unknown"))
        self.assertEqual(gym.get_active_summary(gym.members), 2)
        self.assertEqual(gym.get_active_summary({}), 0)

    def test_discount_bounds_and_missing_member(self):
        self.assertEqual(gym.calculate_renewal_rate("M01", 0.15), 510.0)
        self.assertEqual(gym.calculate_renewal_rate("M01", 0), 600.0)
        self.assertEqual(gym.calculate_renewal_rate("M01", 1), 0.0)
        for rate in [-0.01, 1.01, float("nan")]:
            with self.assertRaises(ValueError):
                gym.calculate_renewal_rate("M01", rate)
        with self.assertRaises(KeyError):
            gym.calculate_renewal_rate("unknown", 0.15)

    def test_expression_input_is_rejected_without_execution(self):
        with tempfile.TemporaryDirectory() as directory:
            marker = Path(directory) / "executed"
            payload = f"__import__('pathlib').Path({str(marker)!r}).touch()"
            with self.assertRaises(TypeError):
                gym.calculate_renewal_rate("M01", payload)
            self.assertFalse(marker.exists())

    def test_hash_and_pin(self):
        digest = gym.generate_member_hash("M01")
        self.assertEqual(len(digest), 64)
        self.assertEqual(digest, gym.generate_member_hash("M01"))
        self.assertNotEqual(digest, gym.generate_member_hash("M02"))
        for _ in range(100):
            pin = gym.generate_locker_pin()
            self.assertIsInstance(pin, int)
            self.assertGreaterEqual(pin, 1000)
            self.assertLessEqual(pin, 9999)

    def test_export_treats_shell_metacharacters_as_filename(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "roster; touch INJECTED"
            with contextlib.redirect_stdout(io.StringIO()):
                gym.export_member_roster(path)
            self.assertEqual(ast.literal_eval(path.read_text()), gym.members)
            self.assertEqual(list(Path(directory).iterdir()), [path])
            with self.assertRaises(OSError):
                gym.export_member_roster(Path(directory) / "missing" / "file")

    def test_import_has_no_demo_side_effects(self):
        module = importlib.util.module_from_spec(SPEC)
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            SPEC.loader.exec_module(module)
        self.assertEqual(output.getvalue(), "")
        self.assertNotIn("M04", module.members)

    def test_demo_still_works_without_exposing_secret(self):
        output = io.StringIO()
        with tempfile.TemporaryDirectory() as directory:
            # Keep exports isolated without changing the process directory.
            from unittest.mock import patch
            export = gym.export_member_roster
            target = Path(directory) / "gym_roster.txt"
            with patch.object(gym, "export_member_roster",
                              side_effect=lambda: export(target)):
                with contextlib.redirect_stdout(output):
                    gym.main()
            self.assertTrue(target.exists())
        self.assertIn("Renewal Fee: 510.0", output.getvalue())
        self.assertIn("Active count: 3", output.getvalue())
        self.assertNotIn("Portal secret:", output.getvalue())


if __name__ == "__main__":
    unittest.main()
