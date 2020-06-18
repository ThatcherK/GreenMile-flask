import json
from app import db
from app.api.models import User,Recipient,Invited_user

def test_add_package(test_app,test_database):
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
    client.post(
        '/recipients',
        data = json.dumps({'name':'Pearl','email':'pally@mail.com','address':'plot 94 Seeta'}),
        content_type = 'application/json',
        headers= { 'Authorization': f'Bearer {auth_token}'}
    )
    supplier = User.query.filter_by(email='momo@mail.com').first()
    recipient = Recipient.query.filter_by(email='pally@mail.com').first()
    resp = client.post(
        '/packages',
        data = json.dumps({'name':'Flat iron','description':'240V,600W','supplier_id':supplier.id,'weight':'0.5kg','recipient_id':recipient.id}),
        headers= { 'Authorization': f'Bearer {auth_token}'} ,
        content_type = 'application/json'
    )
    data = json.loads(resp.data.decode())
    print(data)
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
    resp1 = client.post(
            '/login',
            data=json.dumps({'email':'dem@mail.com','password':'real'}),
            content_type = 'application/json'
            )
    login_data = json.loads(resp1.data.decode())
    auth_token = login_data['auth_token']
    client.post(
        '/recipients',
        data = json.dumps({'name':'Pearl','email':'paly@mail.com','address':'plot 94 Seeta'}),
        content_type = 'application/json',
        headers= { 'Authorization': f'Bearer {auth_token}'} 
        )
    supplier = User.query.filter_by(email='dem@mail.com').first()
    recipient = Recipient.query.filter_by(email='paly@mail.com').first()
    resp = client.post(
        '/packages',
        data = json.dumps({}),
        content_type = 'application/json',
        headers= { 'Authorization': f'Bearer {auth_token}'} 
        )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']

def test_supplier_packages(test_app,test_database):
    client = test_app.test_client()
    client.post(
        '/invited_user',
        data=json.dumps({'email':'dis@mail.com','invite_code':'that1','role_id':2}),
        content_type = 'application/json'
        )
    client.post(
        '/users',
        data=json.dumps({'name':'Thatcher','email':'dis@mail.com','password':'real','invite_code':'that1'}),
        content_type = 'application/json'
        )

    resp1 = client.post(
            '/login',
            data=json.dumps({'email':'dis@mail.com','password':'real'}),
            content_type = 'application/json'
            )
    login_data = json.loads(resp1.data.decode())
    auth_token = login_data['auth_token']
    client.post(
        '/recipients',
        data = json.dumps({'name':'Pearl','email':'pall@mail.com','address':'plot 94 Seeta'}),
        content_type = 'application/json',
        headers= { 'Authorization': f'Bearer {auth_token}'}
    )
    supplier = User.query.filter_by(email='dis@mail.com').first()
    recipient = Recipient.query.filter_by(email='pall@mail.com').first()
    client.post(
        '/packages',
        data = json.dumps({'name':'Flat iron','description':'240V,600W','supplier_id':supplier.id,'weight':'0.5kg','recipient_id':recipient.id}),
        headers= { 'Authorization': f'Bearer {auth_token}'} ,
        content_type = 'application/json'
    )
    resp = client.get(
        '/packages',headers= { 'Authorization': f'Bearer {auth_token}'}
        )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'Flat iron' in data.get('packages')[0].get('name')