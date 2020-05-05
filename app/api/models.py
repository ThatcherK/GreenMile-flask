from app import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer,primary_key=True)
    role = db.Column(db.Integer,db.ForeignKey('roles.id'))
    name = db.Column(db.String(128),nullable=False)
    email = db.Column(db.String(64),unique=True, index=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self,role,name,email,password):
        self.role = role
        self.name = name
        self.email = email
        self.password = password

    def save(self):
        db.session.add(self)
        db.session.commit()
    def json(self):
        data= {
            'id': self.id,
            'role':self.role,
            'name':self.name,
            'email':self.email,
            'password':self.password
        }
        return data

class Role(db.Model):
    __tablename__ = "roles"
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64),nullable=False)

    def __init__(self,name):
        self.name = name

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
