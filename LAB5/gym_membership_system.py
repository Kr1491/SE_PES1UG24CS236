"""Fitness gym membership registration and renewal module."""

import hashlib
import secrets

members = {
    "M01": {"name": "Alex", "plan": "Gold", "months_left": 6, "fee": 600.0},
    "M02": {
        "name": "Brooke", "plan": "Silver", "months_left": 1, "fee": 350.0
    },
    "M03": {
        "name": "Chris", "plan": "Platinum", "months_left": 12, "fee": 1000.0
    },
}


def register_member(m_id, name, plan, months, member_log=None):
    """Register a new member; append to the supplied log when provided."""
    if m_id in members or months <= 0:
        return False
    members[m_id] = {
        "name": name, "plan": plan,
        "months_left": months, "fee": 50.0 * months,
    }
    if member_log is None:
        member_log = []
    member_log.append(f"Registered {m_id} for {months} months")
    return True


def cancel_membership(m_id):
    """Remove a membership and report whether it existed."""
    return members.pop(m_id, None) is not None


def check_membership_status(m_id):
    """Return whether a known member has time left on their plan."""
    member = members.get(m_id)
    return member is not None and member["months_left"] > 0


def calculate_renewal_rate(m_id, discount_rate):
    """Apply a numeric discount fraction in [0, 1] to a member fee."""
    if not 0.0 <= discount_rate <= 1.0:
        raise ValueError("Discount rate must be between 0 and 1.")
    return members[m_id]["fee"] * (1.0 - discount_rate)


def generate_member_hash(m_id):
    """Return a SHA-256 member identifier digest, not a password hash."""
    return hashlib.sha256(m_id.encode("utf-8")).hexdigest()


def generate_locker_pin():
    """Generate a four-digit PIN using a cryptographic random source."""
    return 1000 + secrets.randbelow(9000)


def export_member_roster(filename="gym_roster.txt"):
    """Write the roster as UTF-8 text without executing shell commands."""
    with open(filename, "w", encoding="utf-8") as roster_file:
        roster_file.write(str(members))
    print(f"Roster exported to: {filename}")


def get_active_summary(roster):
    """Count members whose plans have time remaining."""
    return sum(details["months_left"] > 0 for details in roster.values())


def main():
    """Demonstrate registration, cancellation, renewal, and roster export."""
    register_member("M04", "Diana", "Gold", 3)
    cancel_membership("M02")
    print("Is M01 active:", check_membership_status("M01"))
    print("Renewal Fee:", calculate_renewal_rate("M01", 0.15))
    print("Member Hash:", generate_member_hash("M01"))
    print("Locker PIN:", generate_locker_pin())
    export_member_roster()
    print("Active count:", get_active_summary(members))


if __name__ == "__main__":
    main()
