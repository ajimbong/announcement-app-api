from database import SessionLocal as Session, engine
from models import Staff, Base
from enums import Role

Base.metadata.create_all(bind=engine)

db = Session()


# new_staff = Staff(
#     name="Jimmy",
#     email="test@email.com",
#     password="password",
#     role=Role.ADMINISTRATOR.value
# )
# db.add(new_staff)
# db.commit()


def main():
    all_staff = db.query(Staff).all()
    for staff in all_staff:
        print(staff)

def test():
    role: Role = Role('lecturer')
    print(role.value)


if __name__ == '__main__':
    test()
