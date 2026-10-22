from app import create_app, db, security
from app.repos import orders as orders_repo
from app.repos import patients as patients_repo
from app.repos import users as users_repo

USERS = [
    ("admin", "admin-pass", "admin", "Site Administrator"),
    ("tech", "tech-pass", "lab_tech", "Lab Technician"),
    ("dr.meyer", "doctor-pass", "doctor", "Dr. Meyer"),
]

PATIENTS = [
    ("10000001", "Anna Schmidt", "1984-03-12", "Cardiology"),
    ("10000002", "Jonas Weber", "1971-11-02", "Nephrology"),
    ("10000003", "Mira Hoffmann", "1999-07-25", "Oncology"),
]

ORDERS = [
    (1, "GLU", ),
    (2, "CREA", ),
    (3, "CBC", ),
]


def seed():
    app = create_app()
    with app.app_context():
        db.init_db()
        for username, password, role, display_name in USERS:
            users_repo.create(username, security.hash_password(password), role, display_name)
        for mrn, name, birth, ward in PATIENTS:
            patients_repo.create(mrn, name, birth, ward)
        for patient_id, code in ORDERS:
            orders_repo.create(patient_id, code, 2)


if __name__ == "__main__":
    seed()
