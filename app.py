from flask import Flask, render_template, request

from database import (
    initialize_database,
    is_slot_available,
    create_appointment
)

app = Flask(__name__)

initialize_database()


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


def validate_appointment(
    patient_name,
    patient_age,
    patient_email,
    doctor,
    date,
    time
):
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


@app.route("/")
def index():
    return render_template(
        "index.html",
        doctors=DOCTORS
    )


@app.route("/book", methods=["GET", "POST"])
def book():

    if request.method == "POST":

        patient_name = request.form.get("patient_name", "")
        patient_age = request.form.get("patient_age", "")
        patient_email = request.form.get("patient_email", "")
        doctor = request.form.get("doctor", "")
        date = request.form.get("date", "")
        time = request.form.get("time", "")

        error = validate_appointment(
            patient_name,
            patient_age,
            patient_email,
            doctor,
            date,
            time
        )

        if error:
            return render_template(
                "book.html",
                doctors=DOCTORS,
                time_slots=TIME_SLOTS,
                error=error
            )

        appointment_id = create_appointment(
            patient_name,
            int(patient_age),
            patient_email,
            doctor,
            DOCTORS[doctor],
            date,
            time
        )

        return render_template(
            "confirmation.html",
            appointment_id=appointment_id,
            patient_name=patient_name,
            doctor=doctor,
            specialization=DOCTORS[doctor],
            date=date,
            time=time
        )

    return render_template(
        "book.html",
        doctors=DOCTORS,
        time_slots=TIME_SLOTS,
        error=None
    )


if __name__ == "__main__":
    app.run(debug=True)

