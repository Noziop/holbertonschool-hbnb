def test_login_valid(client, normal_user):
    """Test POST /login avec des identifiants valides 🔑"""
    print("\n=== Debug test_login_valid ===")
    credentials = {"email": normal_user.email, "password": "User123!"}
    print(f"Credentials: {credentials}")

    response = client.post("/api/v1/login", json=credentials)
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json}")

    assert response.status_code == 200
    assert "token" in response.json


def test_login_invalid_email(client):
    """Test POST /login avec un email invalide ❌"""
    print("\n=== Debug test_login_invalid_email ===")
    credentials = {"email": "ghost@nowhere.com", "password": "User123!"}
    print(f"Credentials: {credentials}")

    response = client.post("/api/v1/login", json=credentials)
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json}")

    assert response.status_code == 401
    assert "message" in response.json


def test_login_invalid_password(client, normal_user):
    """Test POST /login avec un mot de passe invalide ❌"""
    print("\n=== Debug test_login_invalid_password ===")
    credentials = {"email": normal_user.email, "password": "WrongPass123!"}
    print(f"Credentials: {credentials}")

    response = client.post("/api/v1/login", json=credentials)
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json}")

    assert response.status_code == 401
    assert "message" in response.json


def test_login_inactive_user(client, normal_user):
    """Test POST /login avec un utilisateur inactif 👻"""
    print("\n=== Debug test_login_inactive_user ===")
    # Désactiver l'utilisateur
    normal_user.is_active = False
    normal_user.save()

    credentials = {"email": normal_user.email, "password": "User123!"}
    print(f"Credentials: {credentials}")

    response = client.post("/api/v1/login", json=credentials)
    print(f"Response status: {response.status_code}")
    print(f"Response data: {response.json}")

    assert response.status_code == 401
    assert "message" in response.json


def test_login_missing_fields(client):
    """Test POST /login avec des champs manquants ❌"""
    print("\n=== Debug test_login_missing_fields ===")

    # Email manquant
    response = client.post("/api/v1/login", json={"password": "User123!"})
    print(f"Missing email - Response status: {response.status_code}")
    print(f"Missing email - Response data: {response.json}")
    assert response.status_code == 400

    # Password manquant
    response = client.post("/api/v1/login", json={"email": "user@test.com"})
    print(f"Missing password - Response status: {response.status_code}")
    print(f"Missing password - Response data: {response.json}")
    assert response.status_code == 400
