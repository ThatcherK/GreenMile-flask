from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False)
    email = db.Column(db.String(64),unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self,email,password):
        self.email = email
        self.password = password
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()
    def json(self):
        data= {
            'id': self.id,
            'email':self.email,
            'password':self.password
            'name':self.name
        }
        return data

class Invited_user(db.Model):
    __tablename__ = "invited_user"
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(64),nullable=False)
    invite_code = db.Column(db.String(64),nullable=False)
    role = db.Column(db.String(64),nullable=False)

    def __init__(self,name):
        self.email = email
        self.invite_code = invite_code
        self.role = role

    def save(self):
        db.session.add(self)
        db.session.commit()

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
