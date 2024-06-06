from sqlalchemy.orm import Session

from api.db.models import Student
from api.schemas.student import StudentCreate, StudentUpdate
from api.utils.hashing import get_password_hash


def get_student(db: Session, student_id: int):
    return db.query(Student).filter(Student.id == student_id).first()


def get_student_by_email(db: Session, email: str):
    return db.query(Student).filter(Student.email == email).first()


def get_student_by_matricule(db: Session, matricule: str):
    return db.query(Student).filter(Student.matricule == matricule).first()


# TODO: Do research on FastAPI pagination
def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Student).offset(skip).limit(limit).all()


def create_student(db: Session, student: StudentCreate):
    hashed_password = get_password_hash(student.password)
    db_student: Student = Student(
        name=student.name,
        email=student.email,
        matricule=student.matricule,
        password=hashed_password,
    )
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def update_student(db: Session, student: StudentUpdate, student_id: int):
    """
    For the update operation, we won't be able to update the password
    """
    db_student: Student = db.query(Student).filter(Student.id==student_id).first()

    db_student.name = student.name
    db_student.email = student.email
    db_student.matricule = student.matricule
    db.commit()
    db.refresh(db_student)
    return db_student


def other_student_with_same_email(db: Session, student_id: int, student: StudentUpdate) -> bool:
    student_with_same_email: Student = get_student_by_email(db=db, email=student.email)
    if student_with_same_email is not None and student_with_same_email.id != student_id:
        return True
    return False


def other_student_with_same_matricule(db: Session, student_id: int, student: StudentUpdate) -> bool:
    student_with_same_matricule: Student = get_student_by_matricule(db=db, matricule=student.matricule)
    if student_with_same_matricule is not None and student_with_same_matricule.id != student_id:
        return True
    return False


def delete_student(db: Session, student_id: int):
    db_student: Student = db.query(Student).filter_by(id=student_id).first()

    db.delete(db_student)
    db.commit()
