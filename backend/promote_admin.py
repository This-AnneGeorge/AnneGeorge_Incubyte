import argparse

from sqlmodel import Session, select

from app.database import make_engine
from app.main import User


def main():
    parser = argparse.ArgumentParser(
        description="Promote an existing registered user to admin."
    )
    parser.add_argument("email", help="Email of the registered user")
    args = parser.parse_args()

    email = args.email.strip().lower()
    engine = make_engine()

    with Session(engine) as session:
        user = session.exec(
            select(User).where(User.email == email)
        ).first()

        if user is None:
            parser.error(
                f"No registered user found with email {email!r}. "
                "Register through the app first."
            )

        if user.role == "admin":
            print(f"{email} is already an admin.")
            return

        user.role = "admin"
        session.add(user)
        session.commit()

    print(f"{email} is now an admin.")


if __name__ == "__main__":
    main()