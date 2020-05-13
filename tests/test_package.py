import json
from app import db
from app.api.models import User,Recipient

def test_add_package(test_app,test_database):
    client = test_app.test_client()
    client.post(
        '/invited_user',
        data=json.dumps({'email':'momo@mail.com','invite_code':'that1','role_id':2}),
        content_type = 'application/json'
        )
    client.post(
        '/users',
        data=json.dumps({'name':'Thatcher','email':'momo@mail.com','password':'real','invite_code':'that1'}),
        content_type = 'application/json'
        )
    client.post(
        '/recipients',
        data = json.dumps({'name':'Pearl','email':'pally@mail.com','address':'plot 94 Seeta'}),
        content_type = 'application/json'
    )
    supplier = User.query.filter_by(email='momo@mail.com').first()
    recipient = Recipient.query.filter_by(email='pally@mail.com').first()
    resp = client.post(
        '/packages',
        data = json.dumps({'name':'Flat iron','description':'240V,600W','supplier_id':supplier.id,'weight':'0.5kg','recipient_id':recipient.id}),
        content_type = 'application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert 'Flat iron has been added' in data['message']

    def test_add_package_invalid_json(test_app,test_database):
        client = test_app.test_client()
        client.post(
            '/invited_user',
            data=json.dumps({'email':'dem@mail.com','invite_code':'that1','role_id':2}),
            content_type = 'application/json'
            )
        client.post(
            '/users',
            data=json.dumps({'name':'dem','email':'dem@mail.com','password':'real','invite_code':'that1'}),
            content_type = 'application/json'
            )
        client.post(
            '/recipients',
            data = json.dumps({'name':'Pearl','email':'pally@mail.com','address':'plot 94 Seeta'}),
            content_type = 'application/json'
        )
        supplier = User.query.filter_by(email='dem@mail.com').first()
        recipient = Recipient.query.filter_by(email='pally@mail.com').first()
        resp = client.post(
            '/packages',
            data = json.dumps({}),
            content_type = 'application/json'
        )
        data = json.loads(resp.data.decode())
        assert resp.status_code == 400
        assert 'Input payload validation failed' in data['message']