import copy


# =========================================================
# MUTATION TESTING FRAMEWORK
# =========================================================

DOCTORS = {
    "Dr. Ananya Sharma": "General Physician",
    "Dr. Rahul Mehta": "Cardiologist",
    "Dr. Priya Nair": "Dermatologist"
}

TIME_SLOTS = [
    "09:00",
    "10:00",
    "11:00",
    "14:00",
    "15:00",
    "16:00"
]


# ---------------------------------------------------------
# Original appointment validation logic
# ---------------------------------------------------------

ORIGINAL_CODE = '''
def validate_appointment(patient_name, patient_age, patient_email, doctor, date, time):

    if not patient_name.strip():
        return "Patient name is required."

    if not patient_age.isdigit():
        return "Age must be a valid number."

    age = int(patient_age)

    if age < 1 or age > 120:
        return "Age must be between 1 and 120."

    if "@" not in patient_email:
        return "Enter a valid email address."

    if doctor not in DOCTORS:
        return "Invalid doctor selected."

    if not date:
        return "Appointment date is required."

    if time not in TIME_SLOTS:
        return "Invalid time slot selected."

    if not is_slot_available(doctor, date, time):
        return "This appointment slot is already booked."

    return None
'''


# ---------------------------------------------------------
# Simulated appointment database
# ---------------------------------------------------------

BOOKED_SLOTS = {
    (
        "Dr. Ananya Sharma",
        "2030-12-01",
        "09:00"
    )
}


def is_slot_available(doctor, date, time):

    return (
        doctor,
        date,
        time
    ) not in BOOKED_SLOTS


# ---------------------------------------------------------
# Test cases
# ---------------------------------------------------------

TEST_CASES = [

    {
        "name": "",
        "age": "19",
        "email": "affan@test.com",
        "doctor": "Dr. Ananya Sharma",
        "date": "2030-11-01",
        "time": "09:00",
        "expected": "error"
    },

    {
        "name": "Affan",
        "age": "abc",
        "email": "affan@test.com",
        "doctor": "Dr. Ananya Sharma",
        "date": "2030-11-02",
        "time": "09:00",
        "expected": "error"
    },

    {
        "name": "Affan",
        "age": "130",
        "email": "affan@test.com",
        "doctor": "Dr. Ananya Sharma",
        "date": "2030-11-03",
        "time": "09:00",
        "expected": "error"
    },

    {
        "name": "Affan",
        "age": "19",
        "email": "affan",
        "doctor": "Dr. Ananya Sharma",
        "date": "2030-11-04",
        "time": "09:00",
        "expected": "error"
    },

    {
        "name": "Affan",
        "age": "19",
        "email": "Dr. Fake Doctor",
        "doctor": "Dr. Fake Doctor",
        "date": "2030-11-05",
        "time": "09:00",
        "expected": "error"
    },

    {
        "name": "Affan",
        "age": "19",
        "email": "affan@test.com",
        "doctor": "Dr. Ananya Sharma",
        "date": "",
        "time": "09:00",
        "expected": "error"
    },

    {
        "name": "Affan",
        "age": "19",
        "email": "affan@test.com",
        "doctor": "Dr. Ananya Sharma",
        "date": "2030-11-07",
        "time": "13:30",
        "expected": "error"
    },

    {
        "name": "Affan",
        "age": "19",
        "email": "affan@test.com",
        "doctor": "Dr. Ananya Sharma",
        "date": "2030-12-01",
        "time": "09:00",
        "expected": "error"
    },

    {
        "name": "Affan",
        "age": "19",
        "email": "affan@test.com",
        "doctor": "Dr. Ananya Sharma",
        "date": "2030-11-09",
        "time": "10:00",
        "expected": "success"
    },

    # Boundary-value test
    {
        "name": "Affan",
        "age": "1",
        "email": "affan@test.com",
        "doctor": "Dr. Ananya Sharma",
        "date": "2030-11-10",
        "time": "10:00",
        "expected": "success"
    }
]


# ---------------------------------------------------------
# Mutations
# ---------------------------------------------------------

MUTATIONS = [

    {
        "id": "M1",
        "description": "Reverse patient name validation",
        "original": "if not patient_name.strip():",
        "mutated": "if patient_name.strip():"
    },

    {
        "id": "M2",
        "description": "Reverse age numeric validation",
        "original": "if not patient_age.isdigit():",
        "mutated": "if patient_age.isdigit():"
    },

    {
        "id": "M3",
        "description": "Change age upper boundary",
        "original": "age > 120",
        "mutated": "age >= 120"
    },

    {
        "id": "M4",
        "description": "Reverse email validation",
        "original": 'if "@" not in patient_email:',
        "mutated": 'if "@" in patient_email:'
    },

    {
        "id": "M5",
        "description": "Reverse doctor validation",
        "original": "if doctor not in DOCTORS:",
        "mutated": "if doctor in DOCTORS:"
    },

    {
        "id": "M6",
        "description": "Reverse date validation",
        "original": "if not date:",
        "mutated": "if date:"
    },

    {
        "id": "M7",
        "description": "Reverse time-slot validation",
        "original": "if time not in TIME_SLOTS:",
        "mutated": "if time in TIME_SLOTS:"
    },

    {
        "id": "M8",
        "description": "Reverse slot availability check",
        "original": "if not is_slot_available(doctor, date, time):",
        "mutated": "if is_slot_available(doctor, date, time):"
    },

    {
        "id": "M9",
        "description": "Change minimum age boundary",
        "original": "age < 1",
        "mutated": "age < 2"
    },

    {
        "id": "M10",
        "description": "Change maximum age boundary",
        "original": "age > 120",
        "mutated": "age > 121"
    }
]


# ---------------------------------------------------------
# Run test cases against a function
# ---------------------------------------------------------

def run_test_suite(function):

    failures = []

    for test in TEST_CASES:

        try:

            result = function(
                test["name"],
                test["age"],
                test["email"],
                test["doctor"],
                test["date"],
                test["time"]
            )

            if test["expected"] == "error":

                test_passed = result is not None

            else:

                test_passed = result is None

            if not test_passed:
                failures.append(test)

        except Exception:

            failures.append(test)

    return failures


# ---------------------------------------------------------
# Create function from source code
# ---------------------------------------------------------

def create_function(source_code):

    namespace = {
        "DOCTORS": DOCTORS,
        "TIME_SLOTS": TIME_SLOTS,
        "is_slot_available": is_slot_available
    }

    exec(
        source_code,
        namespace
    )

    return namespace["validate_appointment"]


# ---------------------------------------------------------
# Run mutation testing
# ---------------------------------------------------------

def run_mutation_testing():

    results = []

    for mutation in MUTATIONS:

        mutated_code = ORIGINAL_CODE.replace(
            mutation["original"],
            mutation["mutated"]
        )

        mutant_function = create_function(
            mutated_code
        )

        failures = run_test_suite(
            mutant_function
        )

        if len(failures) > 0:

            status = "KILLED"

        else:

            status = "SURVIVED"

        results.append({
            "id": mutation["id"],
            "description": mutation["description"],
            "status": status,
            "failed_tests": len(failures)
        })

    return results


# ---------------------------------------------------------
# Display results
# ---------------------------------------------------------

def display_results(results):

    print()
    print("=" * 75)
    print("          HEALTHCARE MUTATION TESTING FRAMEWORK")
    print("=" * 75)

    print()
    print("MUTATION TEST RESULTS")
    print("-" * 75)

    for result in results:

        print(
            f'{result["id"]} | '
            f'{result["description"]:<40} | '
            f'{result["status"]}'
        )

    total_mutants = len(results)

    killed_mutants = sum(
        1
        for result in results
        if result["status"] == "KILLED"
    )

    survived_mutants = total_mutants - killed_mutants

    mutation_score = (
        killed_mutants /
        total_mutants
    ) * 100

    print("-" * 75)

    print(f"Total Mutants       : {total_mutants}")
    print(f"Killed Mutants      : {killed_mutants}")
    print(f"Surviving Mutants   : {survived_mutants}")
    print(f"Mutation Score      : {mutation_score:.2f}%")

    print("=" * 75)


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------

if __name__ == "__main__":

    results = run_mutation_testing()

    display_results(results)