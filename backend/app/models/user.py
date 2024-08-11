from flask import current_app
from app.extensions import db
from datetime import datetime
from time import time
import logging as lg
import jwt

from app.models import product

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), unique=True)
    phone = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200))
    confirmed = db.Column(db.Boolean, default=False)
    password = db.Column(db.String(200))
    location = db.Column(db.String(500))
    country = db.Column(db.String(500))
    avatar = db.Column(db.String(500), default="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png")
    status = db.Column(db.String(10), default="user") # user, admin, moderator
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, default=datetime.utcnow())
    # Define a relationship to Product and Cart
    products = db.relationship('Product', back_populates='created_by')
    carts = db.relationship('Cart', back_populates='created_by')
    # Define a relationship to Order 
    orders_placed = db.relationship('Order', back_populates='ordered_by', foreign_keys='Order.ordered_by_id')
    orders_managed = db.relationship('Order', back_populates='managed_by', foreign_keys='Order.managed_by_id')

    def __repr__(self):
        return '<User {}>'.format(self.name)

    def __init__(self, name, phone, password, location, email="", status='user'):
        self.name = name
        self.email = email
        self.phone = phone
        self.password = password
        self.location = location
        self.status = status
        self.created_on = datetime.now()
        self.updated_on = datetime.now()
        
    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in}, 
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def get_confirm_email_token(self, expires_in=600):
        return jwt.encode(
            {'confirm_email': self.id, 'exp': time() + expires_in}, 
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_confirm_email_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])['confirm_email']
        except:
            return
        return User.query.get(id)
    
    def set_confirmed(self, confirmed):
        self.confirmed = confirmed
        db.session.commit()
    
    def as_dict(self):
        return {'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'location': self.location,
            'country': self.country,
            'avatar': self.avatar,
            'confirmed': self.confirmed,
            'status': self.status,
            'created_on': self.created_on.strftime("%m-%d-%Y"),
            'updated_on': self.updated_on.strftime("%m/%d/%Y, %H:%M")
            }

#database initialized
def init_db():
    db.drop_all()
    db.create_all()
    db.session.add(User(name='Mark Darius', email='admin@gmail.com', location = '121 rue saint Louis',
                        phone='12345678', password='pbkdf2:sha256:260000$y3iRZHjCrAPnYNeP$786b16cf4d73c5c02061ecdda95afb75f1a00c763e77bce5cca95e75dbce4598', 
                        status='admin'))
    db.session.add(User(name='Moro Lapoule', email='moderator@gmail.com', location = '121 rue saint Louis',
                        phone='13245678', password='pbkdf2:sha256:260000$y3iRZHjCrAPnYNeP$786b16cf4d73c5c02061ecdda95afb75f1a00c763e77bce5cca95e75dbce4598', 
                        status='moderator'))
    db.session.add(User(name='Ado Doflato', email='user@gmail.com', location = '121 rue saint Louis',
                        phone='14235678', password='pbkdf2:sha256:260000$y3iRZHjCrAPnYNeP$786b16cf4d73c5c02061ecdda95afb75f1a00c763e77bce5cca95e75dbce4598', 
                        status='user'))
    db.session.commit()
    lg.warning('Database initialized!')