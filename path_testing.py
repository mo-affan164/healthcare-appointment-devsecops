from app import validate_appointment
from database import initialize_database, create_appointment


# ---------------------------------------------------------
# Path Testing Framework
# ---------------------------------------------------------

PATHS = {
    "P1": "Invalid patient name",
    "P2": "Non-numeric age",
    "P3": "Age outside valid range",
    "P4": "Invalid email",
    "P5": "Invalid doctor",
    "P6": "Missing appointment date",
    "P7": "Invalid time slot",
    "P8": "Appointment slot already booked",
    "P9": "Valid appointment"
}


def run_path_tests():

    initialize_database()

    # -----------------------------------------------------
    # Create a booked slot for P8
    # -----------------------------------------------------

    booked_doctor = "Dr. Ananya Sharma"
    booked_date = "2030-12-01"
    booked_time = "09:00"

    create_appointment(
        "Booked Patient",
        30,
        "booked@test.com",
        booked_doctor,
        "General Physician",
        booked_date,
        booked_time
    )

    # -----------------------------------------------------
    # Test data for all independent paths
    # -----------------------------------------------------

    test_cases = [

        {
            "path": "P1",
            "name": "",
            "age": "19",
            "email": "affan@test.com",
            "doctor": "Dr. Ananya Sharma",
            "date": "2030-11-01",
            "time": "09:00"
        },

        {
            "path": "P2",
            "name": "Affan",
            "age": "abc",
            "email": "affan@test.com",
            "doctor": "Dr. Ananya Sharma",
            "date": "2030-11-02",
            "time": "09:00"
        },

        {
            "path": "P3",
            "name": "Affan",
            "age": "130",
            "email": "affan@test.com",
            "doctor": "Dr. Ananya Sharma",
            "date": "2030-11-03",
            "time": "09:00"
        },

        {
            "path": "P4",
            "name": "Affan",
            "age": "19",
            "email": "affan",
            "doctor": "Dr. Ananya Sharma",
            "date": "2030-11-04",
            "time": "09:00"
        },

        {
            "path": "P5",
            "name": "Affan",
            "age": "19",
            "email": "affan@test.com",
            "doctor": "Dr. Fake Doctor",
            "date": "2030-11-05",
            "time": "09:00"
        },

        {
            "path": "P6",
            "name": "Affan",
            "age": "19",
            "email": "affan@test.com",
            "doctor": "Dr. Ananya Sharma",
            "date": "",
            "time": "09:00"
        },

        {
            "path": "P7",
            "name": "Affan",
            "age": "19",
            "email": "affan@test.com",
            "doctor": "Dr. Ananya Sharma",
            "date": "2030-11-07",
            "time": "13:30"
        },

        {
            "path": "P8",
            "name": "Affan",
            "age": "19",
            "email": "affan@test.com",
            "doctor": booked_doctor,
            "date": booked_date,
            "time": booked_time
        },

        {
            "path": "P9",
            "name": "Affan",
            "age": "19",
            "email": "affan@test.com",
            "doctor": "Dr. Ananya Sharma",
            "date": "2030-11-09",
            "time": "10:00"
        }
    ]

    results = []

    # -----------------------------------------------------
    # Execute each path
    # -----------------------------------------------------

    for test in test_cases:

        result = validate_appointment(
            test["name"],
            test["age"],
            test["email"],
            test["doctor"],
            test["date"],
            test["time"]
        )

        # P9 is the successful path
        if test["path"] == "P9":
            passed = result is None

        # All other paths should return an error
        else:
            passed = result is not None

        results.append({
            "path": test["path"],
            "description": PATHS[test["path"]],
            "result": "PASS" if passed else "FAIL",
            "message": result if result else "Appointment accepted"
        })

    return results


def display_results(results):

    print("\n")
    print("=" * 70)
    print("       HEALTHCARE APPOINTMENT PATH TESTING FRAMEWORK")
    print("=" * 70)

    print("\nPATH TEST RESULTS")
    print("-" * 70)

    for result in results:

        print(
            f'{result["path"]} | '
            f'{result["description"]:<35} | '
            f'{result["result"]}'
        )

    total_paths = len(results)
    passed_paths = sum(
        1 for result in results
        if result["result"] == "PASS"
    )

    coverage = (passed_paths / total_paths) * 100

    print("-" * 70)

    print(f"Total Independent Paths : {total_paths}")
    print(f"Paths Successfully Tested: {passed_paths}")
    print(f"Path Coverage            : {coverage:.2f}%")

    print("=" * 70)

    if passed_paths == total_paths:
        print("RESULT: ALL INDEPENDENT PATHS COVERED")
    else:
        print("RESULT: SOME PATHS REQUIRE ADDITIONAL TESTING")

    print("=" * 70)


if __name__ == "__main__":

    results = run_path_tests()

    display_results(results)