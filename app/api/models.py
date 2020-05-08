from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    email = db.Column(db.String(64),unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self,name,email,password,role_id):
        self.name = name
        self.email = email
        self.password = password
        self.role_id = role_id

    def save(self):
        db.session.add(self)
        db.session.commit()
    def json(self):
        role = Role.query.filter_by(id=self.role_id).first()
        data= {
            'id': self.id,
            'email':self.email,
            'password':self.password,
            'name':self.name,
            'role':role.role_name
        }
        return data

class Invited_user(db.Model):
    __tablename__ = "invited_user"
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),nullable=False)
    invite_code = db.Column(db.String(64),nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))

    def __init__(self,email,invite_code,role_id):
        self.email = email
        self.invite_code = invite_code
        self.role_id = role_id
        
    def save(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        role = Role.query.filter_by(id=self.role_id).first()
        data={
            'email':self.email,
            'invite_code':self.invite_code,
            'role':role.role_name
        }
        return data

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    role_name = db.Column(db.String(64),nullable=False)

    def __init__(self,role_name):
        self.role_name = role_name

    def json(self):
        data ={'role_name':self.role_name}
        return data

class Package(db.Model):
    __tablename__ = "packages"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    supplier_id = db.Column(db.Integer,db.ForeignKey('users.id'))
    weight = db.Column(db.String(64),nullable=False)
    recipient = db.Column(db.String(64),nullable=False)

    def __init__(self,name,supplier_id,weight,recipient):
        self.name = name
        self.supplier_id = supplier_id
        self.weight = weight
        self.recipient = recipient

    def save(self):
        db.session.add(self)
        db.session.commit()
