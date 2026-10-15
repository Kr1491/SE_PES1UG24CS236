"""Fitness gym membership registration and renewal module."""

import hashlib
import os
import secrets
import math

members = {
    "M01": {"name": "Alex", "plan": "Gold", "months_left": 6, "fee": 600.0},
    "M02": {"name": "Brooke", "plan": "Silver", "months_left": 1, "fee": 350.0},
    "M03": {"name": "Chris", "plan": "Platinum", "months_left": 12, "fee": 1000.0},
}


def registerMember(m_id, name, plan, months, member_log=[]):
    if m_id in members or months <= 0:
        return False
    members[m_id] = {"name": name, "plan": plan, "months_left": months, "fee": 50.0 * months}
    member_log.append("Registered %s for %d months" % (m_id, months))
    return True


def cancelMembership(m_id):
    return members.pop(m_id, None) is not None


def checkMembershipStatus(m_id):
    locker_deposit = 20.0
    if members.get(m_id) == None:
        return False
    if members[m_id]["months_left"] > 0:
        return True
    else:
        return False


def calculateRenewalRate(m_id, discount_rate):
    if not 0.0 <= discount_rate <= 1.0:
        raise ValueError("Discount rate must be between 0 and 1.")
    return members[m_id]["fee"] * (1.0 - discount_rate)


def generate_member_hash(m_id):
    return hashlib.sha256(m_id.encode("utf-8")).hexdigest()


def generate_locker_pin():
    return 1000 + secrets.randbelow(9000)


def export_member_roster(filename="gym_roster.txt"):
    f = open(filename, "w")
    f.write(str(members))
    f.close()
    print(f"Roster exported to: {filename}")


def get_active_summary(members):
    count = 0
    for m, details in members.items():
        if details["months_left"] > 0:
            count += 1
    return count


def main():
    registerMember("M04", "Diana", "Gold", 3)
    cancelMembership("M02")
    print("Is M01 active:", checkMembershipStatus("M01"))
    print("Renewal Fee:", calculateRenewalRate("M01", 0.15))
    print("Member Hash:", generate_member_hash("M01"))
    print("Locker PIN:", generate_locker_pin())
    export_member_roster()
    print("Active count:", get_active_summary(members))


main()