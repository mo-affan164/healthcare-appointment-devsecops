import sqlite3

DATABASE = "database.db"


def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def initialize_database():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_name TEXT NOT NULL,
            patient_age INTEGER NOT NULL,
            patient_email TEXT NOT NULL,
            doctor TEXT NOT NULL,
            specialization TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            appointment_time TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def is_slot_available(doctor, date, time):
    conn = get_db_connection()

    appointment = conn.execute("""
        SELECT id
        FROM appointments
        WHERE doctor = ?
        AND appointment_date = ?
        AND appointment_time = ?
        AND status = 'Confirmed'
    """, (doctor, date, time)).fetchone()

    conn.close()

    return appointment is None


def create_appointment(
    patient_name,
    patient_age,
    patient_email,
    doctor,
    specialization,
    date,
    time
):
    conn = get_db_connection()

    conn.execute("""
        INSERT INTO appointments
        (
            patient_name,
            patient_age,
            patient_email,
            doctor,
            specialization,
            appointment_date,
            appointment_time,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        patient_name,
        patient_age,
        patient_email,
        doctor,
        specialization,
        date,
        time,
        "Confirmed"
    ))

    conn.commit()
    appointment_id = conn.execute(
        "SELECT last_insert_rowid()"
    ).fetchone()[0]

    conn.close()

    return appointment_id