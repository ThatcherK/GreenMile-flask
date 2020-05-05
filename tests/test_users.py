import json
from app import db
from app.api.models import User

def test_add_user(test_app,test_database):
    client = test_app.test_client()
    resp =client.post(
        '/users',
        data=json.dumps({'role':0,'name':'Thatcher','email':'momo@mail.com','password':'real'}),content_type='application/json',
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 201
    assert 'momo@mail.com was added!' in data['message']

def test_add_user_invalid_json(test_app,test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data = json.dumps({}),
        content_type = 'application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']

def test_add_user_invalid_json_keys(test_app,test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data = json.dumps({'role':2,'email':'mine@lol.com','name':'tkm'}),
        content_type = 'application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']

def test_add_user_duplicate_email(test_app,test_database):
    client = test_app.test_client()
    client.post(
        '/users',
        data = json.dumps({
            'role':0,'name':'Thatcher','email':'momo@mail.com','password':'real'
        }),
        content_type = 'application/json'
    )
    resp = client.post(
        '/users',
        data = json.dumps({
            'role':0,'name':'Thatcher','email':'momo@mail.com','password':'real'
        }),
        content_type = 'application/json'
    )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Sorry, That email already exists.' in data['message']

def test_single_user(test_app,test_database):
    user = User(name='momo',role=0,email='momo@dop.com',password='like')
    db.session.add(user)
    db.session.commit()
    client =test_app.test_client()
    resp = client.get(f'/users/{user.id}')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 200
    assert 'momo' in data['name']
    assert data['role'] == 0
    assert 'momo@dop.com' in data['email']
    assert 'like' in data['password']

def test_single_user_incorrect_id(test_app,test_database):
    client =test_app.test_client()
    resp = client.get('/users/50')
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert 'User 50 does not exist' in data['message']

def test_user_logIn(test_app,test_database):
    client = test_app.test_client()
    user = User(name='mygirl',role=1,email='paul@dop.com',password='nope')
    db.session.add(user)
    db.session.commit()
    resp = client.post(
        '/login',
        data = json.dumps({'email': 'paul@dop.com','password':'nope'}),
        content_type = 'application/json'
        )
    data = json.loads(resp.data.decode())
    print(resp.status_code)
    assert resp.status_code == 201
    assert 'nope' == data['password']
    assert 'paul@dop.com' == data['email']

def test_user_login_invalid_fields(test_app,test_database):
    client = test_app.test_client()
    user = User(name='boo',role=2,email='boo@dop.com',password='yap')
    db.session.add(user)
    db.session.commit()
    resp = client.post(
        'login',
        data = json.dumps({'email': 'paul@dop.com'}),
        content_type = 'application/json'
        )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']

def test_user_login_incorrect_email(test_app,test_database):
    client = test_app.test_client()
    user = User(name='bae',role=2,email='bae@dop.com',password='nap')
    db.session.add(user)
    db.session.commit()
    resp = client.post(
        '/login',
        data = json.dumps({'email': 'bad@dop.com','password':'nap'}),
        content_type = 'application/json'
        )
    data = json.loads(resp.data.decode())
    assert resp.status_code == 404
    assert  'bad@dop.com does not exist'
    
# def test_user_login_incorrect_password(test_app,test_database):
#     client = test_app.test_client()
#     user = User(name='bitch',role=2,email='bad@dop.com',password='pap')
#     db.session.add(user)
#     db.session.commit()
#     resp = client.post(
#         '/login',
#         data = json.dumps({'email': 'bad@dop.com','password':'nap'}),
#         content_type = 'application/json'
#         )
#     data = json.loads(resp.data.decode())
#     assert resp.status_code == 404
#     assert  'Wrong password'