import sys
import os

sys.path.insert(
    0,
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

from app import validate_appointment


def test_valid_appointment():
    result = validate_appointment(
        "Affan",
        "19",
        "affan@test.com",
        "Dr. Ananya Sharma",
        "2026-10-20",
        "09:00"
    )

    assert result is None


def test_empty_patient_name():
    result = validate_appointment(
        "",
        "19",
        "affan@test.com",
        "Dr. Ananya Sharma",
        "2026-10-20",
        "09:00"
    )

    assert result == "Patient name is required."


def test_non_numeric_age():
    result = validate_appointment(
        "Affan",
        "abc",
        "affan@test.com",
        "Dr. Ananya Sharma",
        "2026-10-20",
        "09:00"
    )

    assert result == "Age must be a valid number."


def test_age_below_one():
    result = validate_appointment(
        "Affan",
        "0",
        "affan@test.com",
        "Dr. Ananya Sharma",
        "2026-10-20",
        "09:00"
    )

    assert result == "Age must be between 1 and 120."


def test_age_above_120():
    result = validate_appointment(
        "Affan",
        "130",
        "affan@test.com",
        "Dr. Ananya Sharma",
        "2026-10-20",
        "09:00"
    )

    assert result == "Age must be between 1 and 120."


def test_invalid_email():
    result = validate_appointment(
        "Affan",
        "19",
        "affan",
        "Dr. Ananya Sharma",
        "2026-10-20",
        "09:00"
    )

    assert result == "Enter a valid email address."


def test_invalid_doctor():
    result = validate_appointment(
        "Affan",
        "19",
        "affan@test.com",
        "Dr. Fake Doctor",
        "2026-10-20",
        "09:00"
    )

    assert result == "Invalid doctor selected."


def test_missing_date():
    result = validate_appointment(
        "Affan",
        "19",
        "affan@test.com",
        "Dr. Ananya Sharma",
        "",
        "09:00"
    )

    assert result == "Appointment date is required."


def test_invalid_time():
    result = validate_appointment(
        "Affan",
        "19",
        "affan@test.com",
        "Dr. Ananya Sharma",
        "2026-10-20",
        "13:30"
    )

    assert result == "Invalid time slot selected."


def test_booked_slot():
    from database import (
        initialize_database,
        create_appointment
    )

    initialize_database()

    doctor = "Dr. Ananya Sharma"
    date = "2026-12-01"
    time = "09:00"

    # Book the slot first
    create_appointment(
        "Test Patient",
        25,
        "test@test.com",
        doctor,
        "General Physician",
        date,
        time
    )

    # Now test the validation function
    result = validate_appointment(
        "Affan",
        "19",
        "affan@test.com",
        doctor,
        date,
        time
    )

    assert result == "This appointment slot is already booked."