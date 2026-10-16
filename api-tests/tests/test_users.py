import pytest

REQUIRED_USER_FIELDS = {"id", "email", "username", "firstName", "lastName", "address", "phone"}


@pytest.mark.smoke
def test_get_all_users_returns_200(session, api_base_url):
    resp = session.get(f"{api_base_url}/users")
    assert resp.status_code == 200
    body = resp.json()
    assert "users" in body
    assert isinstance(body["users"], list)


@pytest.mark.regression
def test_user_schema_has_required_fields(session, api_base_url):
    resp = session.get(f"{api_base_url}/users/1")
    assert resp.status_code == 200
    body = resp.json()
    missing = REQUIRED_USER_FIELDS - body.keys()
    assert not missing, f"Response missing fields: {missing}"


@pytest.mark.smoke
def test_create_user_returns_201(session, api_base_url):
    payload = {
        "firstName": "QA",
        "lastName": "Tester",
        "email": "qa.automation.test@example.com",
        "username": "qa_auto_tester",
        "password": "TestPass123!",
    }
    resp = session.post(f"{api_base_url}/users/add", json=payload)
    assert resp.status_code in (200, 201)
    body = resp.json()
    assert "id" in body


@pytest.mark.smoke
def test_login_with_valid_credentials_returns_token(session, api_base_url):
    resp = session.post(
        f"{api_base_url}/auth/login",
        json={"username": "emilys", "password": "emilyspass"},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert "accessToken" in body


@pytest.mark.negative
def test_login_with_invalid_credentials_is_rejected(session, api_base_url):
    resp = session.post(
        f"{api_base_url}/auth/login",
        json={"username": "not_a_real_user", "password": "wrong_password"},
    )
    assert resp.status_code in (400, 401, 404)


@pytest.mark.negative
def test_login_with_missing_password_field(session, api_base_url):
    resp = session.post(f"{api_base_url}/auth/login", json={"username": "emilys"})
    assert resp.status_code in (400, 401, 404, 422)
