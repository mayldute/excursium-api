from app.core.security import hash_password, verify_password


def test_password_hashing_and_verification() -> None:
    password = "StrongPassword123!"
    hashed = hash_password(password)

    assert hashed != password
    assert verify_password(password, hashed)
    assert not verify_password("WrongPassword123!", hashed)
