from app import db,bcrypt
from flask import current_app

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    email = db.Column(db.String(64),unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'),nullable=False)

    def __init__(self,name,email,password,role_id):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password,current_app.config.get('BCRYPT_LOG_ROUNDS')).decode()
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
    def __repr__(self):
        return f'<User, {self.email,self.password,self.name,self.role_id}>'
class Invited_user(db.Model):
    __tablename__ = "invited_user"
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),nullable=False,unique=True)
    invite_code = db.Column(db.String(64),nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'),nullable=False)

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

    def __repr__(self):
        return f'<Invited_user, {self.email,self.invite_code,self.role_id}>'

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer,primary_key=True)
    role_name = db.Column(db.String(64),nullable=False)

    def __init__(self,role_name):
        self.role_name = role_name

    def json(self):
        data ={'role_name':self.role_name}
        return data
    def __repr__(self):
        return f'<Role, {self.role_name,self.id}>'

class Recipient(db.Model):
    __tablename__="recipients"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    email = db.Column(db.String(64),unique=True,nullable=False)
    address = db.Column(db.String(128),nullable=False)

    def __init__(self,name,email,address):
        self.name  = name
        self.email = email
        self.address = address
    def json(self):
        data = {
            'name': self.name,
            'email':self.email,
            'address':self.address
        }
        return data

class Package(db.Model):
    __tablename__ = "packages"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    description = db.Column(db.String(128),nullable=False)
    supplier_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    weight = db.Column(db.String(64),nullable=False)
    recipient_id = db.Column(db.Integer,db.ForeignKey('recipients.id'),nullable=False)


    def __init__(self,name,description,supplier_id,weight,recipient_id):
        self.name = name
        self.description = description
        self.supplier_id = supplier_id
        self.weight = weight
        self.recipient_id = recipient_id

    def save(self):
        db.session.add(self)
        db.session.commit()
    def json(self):
        supplier =User.query.filter_by(self.supplier_id).first()
        recipient = Recipient.query.filter_by(self.recipient_id).first()

        data = {
            'name':self.name,
            'supplier':supplier.email,
            'weight':self.weight,
            'recipient':recipient.email
        }
        return data

