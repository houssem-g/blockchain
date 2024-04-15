from app.core.hashing import AuthService

# from app.db.models.brand import Brand


def test_password_hashing():
    # this test is using mocked database connection.
    response = AuthService.create_salt_and_hashed_password(plaintext_password="test")
    assert len(response.password) > len("test")
    assert response.salt != ""
