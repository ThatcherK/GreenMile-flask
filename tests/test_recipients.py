import json
from app import db
from app.api.models import User,Recipient,Invited_user

def test_add_recipient(test_app,test_database):
    client = test_app.test_client()
    client = test_app.test_client()
    invited_user = Invited_user(email='momo@mail.com',invite_code='that1',role_id=2)
    db.session.add(invited_user)
    db.session.commit()
    client.post(
        '/users',
        data = json.dumps({'name':'Thatcher','email':'momo@mail.com','password':'real','invite_code':'that1'}),
        content_type='application/json'
    )
    resp1 = client.post(
            '/login',
            data=json.dumps({'email':'momo@mail.com','password':'real'}),
            content_type = 'application/json'
            )
    login_data = json.loads(resp1.data.decode())
    auth_token = login_data['auth_token']
    resp = client.post(
        '/recipients',
        data = json.dumps({'name':'Will','email':'will@mail.com','address':'Wilson road plot 50'}),
        content_type = 'application/json',
        headers= { 'Authorization': f'Bearer {auth_token}'}
    )

    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert 'will@mail.com has been added' in data['message']

def test_add_recipient_invalid_json(test_app,test_database):
    client = test_app.test_client()
    resp = client.post(
        '/recipients',
        data = json.dumps({}),
        content_type = 'application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']

def test_add_recipient_invalid_json_keys(test_app,test_database):
    client = test_app.test_client()
    resp = client.post(
        '/recipients',
        data = json.dumps({'email':'mine@lol.com','name':'tkm'}),
        content_type = 'application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']