import json


def test_add_user(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/invited_user",
        data=json.dumps(
            {"email": "tkm@mail.com", "role_id": 1}
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert "tkm@mail.com was added" in data["message"]


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/invited_user", data=json.dumps({}), content_type="application/json"
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_invalid_json_keys(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        "/invited_user",
        data=json.dumps({"email": "mine@lol.com"}),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Input payload validation failed" in data["message"]


def test_add_user_duplicate_email(test_app, test_database):
    client = test_app.test_client()
    client.post(
        "/invited_user",
        data=json.dumps(
            {"email": "momo@mail.com", "role_id": 1}
        ),
        content_type="application/json",
    )
    resp = client.post(
        "/invited_user",
        data=json.dumps(
            {"email": "momo@mail.com", "role_id": 1}
        ),
        content_type="application/json",
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert "Sorry, That email already exists." in data["message"]
