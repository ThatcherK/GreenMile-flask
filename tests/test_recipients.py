import json
from app import db

def test_add_recipient(test_app,test_database):
    client = test_app.test_client()
    resp = client.post(
        '/recipients',
        data = json.dumps({'name':'Will','email':'will@mail.com','address':'Wilson road plot 50'}),
        content_type = 'application/json'
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