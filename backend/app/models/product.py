from app.extensions import db
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
import logging as lg

from .user import User

# Association table
product_availability = db.Table('product_availability', db.Model.metadata,
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('availability_id', db.Integer, db.ForeignKey('availability.id'), primary_key=True)
)

product_media = db.Table('product_media', db.Model.metadata,
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True),
    db.Column('media_id', db.Integer, db.ForeignKey('medias.id'), primary_key=True)
)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    itemId = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(200), nullable=False)
    storeTitle = db.Column(db.String(500))
    title = db.Column(db.String(1000), nullable=False)
    rating = db.Column(db.Float, default=0)
    desc = db.Column(db.Text)
    imgSrc = db.Column(db.String(500), nullable=False)
    price = db.Column(db.Float, default=0)
    currency = db.Column(db.String(10), nullable=False)
    seen = db.Column(db.Integer, default=0)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, default=datetime.utcnow())

    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = db.relationship('User', back_populates='products')
    # Define a relationship to Cart
    carts = db.relationship('Cart', back_populates='product')
    # Relationship to Availability
    available_in = db.relationship('Availability', secondary=product_availability, back_populates='products')
    # Relationship to Availability
    media = db.relationship('Media', secondary=product_media, back_populates='products')

    def __repr__(self):
        return f'<Product "{self.title}">'   

    def __init__(self, itemId, category, storeTitle, title, rating, desc, imgSrc, price, currency, created_by, available_in, media):
        self.itemId = itemId
        self.category = category
        self.storeTitle = storeTitle
        self.title = title
        self.rating = rating
        self.desc = desc
        self.imgSrc = imgSrc
        self.price = price
        self.currency = currency
        self.created_by = created_by
        self.available_in = available_in
        self.media = media
        self.created_on = datetime.now()
        self.updated_on = datetime.now()
    
    def as_dict(self):
        return {'id': self.id,
            'itemId': self.itemId,
            'category': self.category,
            'storeTitle': self.storeTitle,
            'title': self.title,
            'rating': self.rating,
            'desc': self.desc,
            'imgSrc': self.imgSrc,
            'price': self.price,
            'currency': self.currency,
            'created_by': self.created_by.as_dict(),
            'available_in': [l.as_dict() for l in self.available_in],
            'media': [m.as_dict() for m in self.media],
            'created_on': self.created_on.strftime("%m/%d/%Y, %H:%M"),
            'updated_on': self.updated_on.strftime("%m/%d/%Y, %H:%M")
            }
    
class Availability(db.Model):
    __tablename__ = 'availability'
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String, unique=True)

    # Relationship to Product
    products = db.relationship('Product', secondary='product_availability', back_populates='available_in')

    def __repr__(self):
        return f'<Availability "{self.location}">' 
    
    def as_dict(self):
        return self.location

class Media(db.Model):
    __tablename__ = 'medias'
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    src = db.Column(db.String)

    # Relationship to Product
    products = db.relationship('Product', secondary='product_media', back_populates='media')

    def __repr__(self):
        return f'<Media "{self.id}">' 
    
    def as_dict(self):
        return {'id': self.id,
            'type': self.type,
            'src': self.src
            }

class Cart(db.Model):
    __tablename__ = 'carts'
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, default=0)
    ordered = db.Column(db.Boolean, nullable=False, default=False)
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, default=datetime.utcnow())

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    product = db.relationship('Product', back_populates='carts')
    created_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_by = db.relationship('User', back_populates='carts')

    def __repr__(self):
        return f'<Cart "{self.quantity}">' 
    
    def as_dict(self):
        return {'id': self.id,
            'quantity': self.quantity,
            'product': self.product.as_dict(),
            'created_by': self.created_by.as_dict(),
            'created_on': self.created_on.strftime("%m/%d/%Y, %H:%M"),
            'updated_on': self.updated_on.strftime("%m/%d/%Y, %H:%M")
            }

class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    
    product = db.relationship("Product", backref=db.backref("order_items", cascade="all, delete-orphan"))
    order = db.relationship("Order", backref=db.backref("order_items", cascade="all, delete-orphan"))

    def as_dict(self):
        return {'id': self.id,
            'quantity': self.quantity,
            'product': self.product.as_dict(),
            }
    
class Order(db.Model):
    __tablename__ = 'orders'
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(200), default="")
    currency = db.Column(db.String(10), default="Fcfa")
    account_number = db.Column(db.String(500), default="")
    account_name = db.Column(db.String(500), default="")
    paid_proof = db.Column(db.String(500), default="")
    paid_confirmed = db.Column(db.String(30), default="none") # submitted, confirmed, rejected
    paid_desc = db.Column(db.String(2000), default="")
    canceled = db.Column(db.Boolean, default=False)
    delivered = db.Column(db.Boolean, default=False)
    remove = db.Column(db.Boolean, default=False)
    delivery_number = db.Column(db.String(500), default="")
    delivery_center = db.Column(db.String(500), default="")

    ordered_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    ordered_by = db.relationship('User', back_populates='orders_placed', foreign_keys=[ordered_by_id])
    
    managed_by_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    managed_by = db.relationship('User', back_populates='orders_managed', foreign_keys=[managed_by_id])
    
    created_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())
    updated_on = db.Column(db.DateTime, default=datetime.utcnow())

    delivery_to = db.Column(db.Integer, db.ForeignKey('locations.id'))
    delivery_from = db.Column(db.Integer, db.ForeignKey('locations.id'))
    
    # Define the relationship to Location
    delivery_to_location = db.relationship('Location', back_populates='delivery_to_orders', foreign_keys=[delivery_to])
    delivery_from_location = db.relationship('Location', back_populates='delivery_from_orders', foreign_keys=[delivery_from])
   
    @hybrid_property
    def total_price(self):
        return sum(item.product.price * item.quantity for item in self.order_items)
    
    def __repr__(self):
        return f"<Order(id={self.id}, total_price={self.total_price})>"
    
    def as_dict(self):
        return {'id': self.id,
                'total_price': self.total_price,
                'currency': self.currency,
                'account_number': self.account_number,
                'account_name': self.account_name,
                'paid_proof': self.paid_proof,
                'paid_confirmed': self.paid_confirmed,
                'paid_desc': self.paid_desc,
                'canceled': self.canceled,
                'delivered': self.delivered,
                'delivery_to': self.delivery_to_location.as_dict() if self.delivery_to_location else {},
                'delivery_from': self.delivery_from_location.as_dict() if self.delivery_from_location else {},
                'order_items': [],
                'delivery_number': self.delivery_number,
                'delivery_center': self.delivery_center,
                'order_number': self.order_number,
                'ordered_by': self.ordered_by.as_dict(),
                'managed_by': self.managed_by.as_dict() if self.managed_by else {},
                'created_on': self.created_on.strftime("%m/%d/%Y"),
                'updated_on': self.updated_on.strftime("%m/%d/%Y")
            }
         
class Location(db.Model):
    __tablename__ = 'locations'
    id = db.Column(db.Integer, primary_key=True)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    
    # Define the relationship to Order
    delivery_to_orders = db.relationship('Order', back_populates='delivery_to_location', foreign_keys='Order.delivery_to')
    delivery_from_orders = db.relationship('Order', back_populates='delivery_from_location', foreign_keys='Order.delivery_from')

    def as_dict(self):
        return {'id': self.id, 
                'longitude': self.longitude, 
                'latitude': self.latitude
        }

products = [{
            'id': 1,
            'category': "Tshirts",
            'storeTitle': "Zara",
            'title': "Carton Astronault Tshirts",
            'rating': 3.7,
            'desc': "official Discord server, or StackOverflow. You should also subscribe to our mailing list and follow the official @vuejs twitter account for latest news in the Vue world.",
            'imgSrc': "https://i.postimg.cc/kg9YYbTn/f1.jpg",
            'price': 999,
            'currency': "Fcfa",
            'available_in': ['Bénin', 'Gabon', 'Togo'],
            'media': [
                { 'type': 'image', 'src': 'https://i.postimg.cc/L86BZByZ/f7.jpg' },
                { 'type': 'image', 'src': 'https://i.postimg.cc/L86BZByZ/f7.jpg' }
            ]
          },
          {
            'id': 2,
            'category': "Tshirts",
            'storeTitle': "Adidas",
            'title': "Carton Leave Tshirts",
            'rating': 4,
            'desc': "official Discord server, or StackOverflow. You should also subscribe to our mailing list and follow the official @vuejs twitter account for latest news in the Vue world.",
            'imgSrc': "https://i.postimg.cc/2yhT2kvb/f2.jpg",
            'price': 99,
            'currency': "Fcfa",
            'available_in': ['Gabon', 'Togo'],
            'media': [
                { 'type': 'video', 'src': 'https://www.w3schools.com/html/mov_bbb.mp4' },
                { 'type': 'image', 'src': 'https://i.postimg.cc/L86BZByZ/f7.jpg' }
            ]
          },
          {
            'id': 3,
            'category': "Tshirts",
            'storeTitle': "Adidas",
            'title': "Rose Multicolor Tshirts",
            'rating': 3.2,
            'desc': "official Discord server, or StackOverflow. You should also subscribe to our mailing list and follow the official @vuejs twitter account for latest news in the Vue world.",
            'imgSrc': "https://i.postimg.cc/VL9DtNm2/f3.jpg",
            'price': 99,
            'currency': "Fcfa",
            'available_in': ['Bénin', 'Gabon'],
            'media': [
                { 'type': 'image', 'src': 'https://i.postimg.cc/L86BZByZ/f7.jpg' },
                { 'type': 'video', 'src': 'https://www.w3schools.com/html/mov_bbb.mp4' },
            ]
          },
          {
            'id': 4,
            'category': "Tshirts",
            'storeTitle': "Zara",
            'title': "Pink Flower Tshirts",
            'rating': 4,
            'desc': "official Discord server, or StackOverflow. You should also subscribe to our mailing list and follow the official @vuejs twitter account for latest news in the Vue world.",
            'imgSrc': "https://i.postimg.cc/vZ3hPS1z/f4.jpg",
            'price': 99,
            'currency': "Fcfa",
            'available_in': ['Gabon'],
            'media': [
                { 'type': 'image', 'src': 'https://i.postimg.cc/L86BZByZ/f7.jpg' },
                { 'type': 'video', 'src': 'https://www.w3schools.com/html/mov_bbb.mp4' },
                { 'type': 'image', 'src': 'https://i.postimg.cc/L86BZByZ/f7.jpg' }
            ]
          },
          {
            'id': 5,
            'category': "Tshirts",
            'storeTitle': "Adidas",
            'title': "Purple Flowering Tshirts",
            'rating': 4.7,
            'desc': "official Discord server, or StackOverflow. You should also subscribe to our mailing list and follow the official @vuejs twitter account for latest news in the Vue world.",
            'imgSrc': "https://i.postimg.cc/q7FLrhx6/f5.jpg",
            'price': 99,
            'currency': "Fcfa",
            'available_in': ['Togo'],
            'media': [
                { 'type': 'video', 'src': 'https://www.w3schools.com/html/mov_bbb.mp4' },
            ]
          },
          {
            'id': 6,
            'category': "Short",
            'storeTitle': "Adidas",
            'title': "Short Knicker",
            'rating': 4,
            'desc': "official Discord server, or StackOverflow. You should also subscribe to our mailing list and follow the official @vuejs twitter account for latest news in the Vue world.",
            'imgSrc': "https://i.postimg.cc/L86BZByZ/f7.jpg",
            'price': 99,
            'currency': "Fcfa",
            'available_in': ['Bénin', 'Gabon', 'Togo'],
            'media': [
                { 'type': 'image', 'src': 'https://i.postimg.cc/L86BZByZ/f7.jpg' },
                { 'type': 'video', 'src': 'https://www.w3schools.com/html/mov_bbb.mp4' },
            ]
          },
          {
            'id': 7,
            'category': "Short",
            'storeTitle': "Zara",
            'title': "2 in 1 Double Routed with bag T",
            'rating': 3,
            'desc': "official Discord server, or StackOverflow. You should also subscribe to our mailing list and follow the official @vuejs twitter account for latest news in the Vue world.",
            'imgSrc': "https://i.postimg.cc/zDxJ2f0H/f6.jpg",
            'price': 99,
            'currency': "Fcfa",
            'available_in': ['Bénin'],
            'media': [
                { 'type': 'image', 'src': 'https://i.postimg.cc/L86BZByZ/f7.jpg' },
                { 'type': 'video', 'src': 'https://www.w3schools.com/html/mov_bbb.mp4' },
                { 'type': 'image', 'src': 'https://i.postimg.cc/L86BZByZ/f7.jpg' }
            ]
          },
          {
            'id': 8,
            'category': "Short",
            'storeTitle': "Adidas",
            'title': "Ash Short",
            'rating': 4,
            'desc': "official Discord server, or StackOverflow. You should also subscribe to our mailing list and follow the official @vuejs twitter account for latest news in the Vue world.",
            'imgSrc': "https://i.postimg.cc/x8qcBrpP/n6.jpg",
            'price': 99,
            'currency': "Fcfa",
            'available_in': ['Togo'],
            'media': [
                { 'type': 'image', 'src': 'https://i.postimg.cc/L86BZByZ/f7.jpg' },
                { 'type': 'image', 'src': 'https://i.postimg.cc/L86BZByZ/f7.jpg' }
            ]
          }]

#database initialized
def init_db(products):
    user = User.query.filter_by(id=1).first()
    for product in products:
        new_product = product
        availability = []
        for location in new_product['available_in']:
            available = Availability.query.filter_by(location=location).first()
            if available:
                availability.append(available)
            else:
                new_location = Availability(location=location)
                availability.append(new_location)
                db.session.add(new_location)
                db.session.commit()
        medias = []
        for m in new_product['media']:
            new_m = Media(type=m['type'], src=m['src'])
            medias.append(new_m)
            db.session.add(new_m)
            db.session.commit()

        new = Product(itemId=new_product['id'],category=new_product['category'], 
                    storeTitle=new_product['storeTitle'],
                    title=new_product['title'],
                    rating=new_product['rating'],
                    desc=new_product['desc'],
                    imgSrc=new_product['imgSrc'],
                    price=new_product['price'],
                    currency=new_product['currency'],
                    created_by=user,
                    available_in=availability,
                    media=medias)
        db.session.add(new)
        db.session.commit()
    p = Product.query.filter_by(id=1).first()
    print(p)
    


