from flask import  request, jsonify, current_app, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from sqlalchemy import func
from datetime import datetime, timedelta
import os, json

from app.admin import bp
from app.extensions import db
from app.decorators import is_admin, is_moderator
from app.utils import AliApi, OpenStreetMap

from app.models.product import Product, Cart, OrderItem, Order, Availability, Media, Location
from app.models.user import User

aliapi = AliApi()
sendMail = g.sendMail
openstreetmap = OpenStreetMap()

account = current_app.config['ACCOUNT']
server_url = current_app.config['SERVER_URL']
frontend_url = current_app.config['FRONTEND_URL']

def orderAsDict(orders):
    orders_as_dict = []
    for order in orders:
        order_as_dict = order.as_dict()
        for item in order.order_items:
            order_as_dict['order_items'].append(item.as_dict())
        orders_as_dict.append(order_as_dict)
    return orders_as_dict

@bp.route('/order/fetch', methods=('GET','POST'))
@jwt_required()
@is_moderator
def fetchOrders():
    id = get_jwt_identity()
    # Fetch the orders
    orders = Order.query.filter_by(remove=False).order_by(Order.updated_on.desc()).all()
    orders = orderAsDict(orders)
    response = jsonify({"status": "success", "message": "Complete!", "orders": orders})
    return response, 200

@bp.route('/order/remove', methods=('GET','POST'))
@jwt_required()
@is_moderator
def removeOrder():
    id = get_jwt_identity()
    orderId = request.json.get("orderId", None)
    order = Order.query.filter_by(id=orderId).first()
    if not order:
        response = jsonify({"status": "error", "message": "Cette commande est introuvable"})
        return response, 404 
    if order.paid_confirmed == "confirmed" and not order.delivered:
        response = jsonify({"status": "error", "message": "Cette commande est payée et n'est pas encore livrée"})
        return response, 404 
    
    managed_by = User.query.filter_by(id=id).first()
    if not order.managed_by:
        order.managed_by = managed_by
    elif order.managed_by_id != managed_by.id and managed_by.status != 'admin':
        return jsonify({"status": "error", "message": "Vous n'êtes pas d'acte à manager cette commande"}), 200

    order.remove = True
    order.updated_on = datetime.utcnow()
    db.session.commit()
    
    # Fetch the orders
    orders = Order.query.filter_by(remove=False).order_by(Order.updated_on.desc()).all()
    orders = orderAsDict(orders)
    
    response = jsonify({"status": "success", "message": "Complete!", "orders": orders})
    return response, 200

@bp.route('/order/cancel', methods=('GET','POST'))
@jwt_required()
@is_moderator
def cancelOrder():
    id = get_jwt_identity()
    orderId = request.json.get("orderId", None)
    order = Order.query.filter_by(id=orderId).first()
    if not order:
        response = jsonify({"status": "error", "message": "Cette commande est introuvable"})
        return response, 404 
    if order.paid_confirmed == "confirmed" and not order.delivered:
        response = jsonify({"status": "error", "message": "Cette commande est payée et n'est pas encore livrée"})
        return response, 404 
    
    managed_by = User.query.filter_by(id=id).first()
    if not order.managed_by:
        order.managed_by = managed_by
    elif order.managed_by_id != managed_by.id and managed_by.status != 'admin':
        return jsonify({"status": "error", "message": "Vous n'êtes pas d'acte à manager cette commande"}), 200

    order.canceled = True
    order.updated_on = datetime.utcnow()
    db.session.commit()

    sendMail.orderCanceledEmail(url=frontend_url, order=order, user=order.ordered_by)

    # Fetch the orders
    orders = Order.query.filter_by(remove=False).order_by(Order.updated_on.desc()).all()
    orders = orderAsDict(orders)
    
    response = jsonify({"status": "success", "message": "Complete!", "orders": orders})
    return response, 200

@bp.route('/order/confirm_paid', methods=('GET','POST'))
@jwt_required()
@is_moderator
def confirmPaid():
    id = get_jwt_identity()
    orderId = request.json.get("orderId", None)
    paid_desc = request.json.get("paid_desc", None)
    paid_confirmed = request.json.get("paid_confirmed", None)

    order = Order.query.filter_by(id=orderId).first()
    if not order:
        response = jsonify({"status": "error", "message": "Cette commande est introuvable"})
        return response, 404 
    if order.paid_confirmed == "confirmed" and not order.delivered:
        response = jsonify({"status": "error", "message": "Cette commande est payée et n'est pas encore livrée"})
        return response, 404 
    
    managed_by = User.query.filter_by(id=id).first()
    if not order.managed_by:
        order.managed_by = managed_by
    elif order.managed_by_id != managed_by.id and managed_by.status != 'admin':
        return jsonify({"status": "error", "message": "Vous n'êtes pas d'acte à manager cette commande"}), 200

    if paid_confirmed == 'confirmed':
        coordinates = openstreetmap.getCoordinates(order.ordered_by.location)
        # Create locations
        delivery_to = Location(
            longitude=coordinates['longitude'], 
            latitude=coordinates['latitude'])
        db.session.add(delivery_to)
        db.session.commit()
        
        order.delivery_to_location = delivery_to
        db.session.commit()

    order.paid_desc = paid_desc
    order.paid_confirmed = paid_confirmed
    order.updated_on = datetime.utcnow()
    db.session.commit()
    
    sendMail.paymentConfirmEmail(decision=paid_desc, order=order, user=order.ordered_by)
    
    # Fetch the orders
    orders = Order.query.filter_by(remove=False).order_by(Order.updated_on.desc()).all()
    orders = orderAsDict(orders)
    
    response = jsonify({"status": "success", "message": "Complète!", "orders": orders})
    return response, 200

@bp.route('/order/delivery', methods=('GET','POST'))
@jwt_required()
@is_moderator
def orderDelivery():
    id = get_jwt_identity()
    orderId = request.json.get("orderId", None)
    delivery_number = request.json.get("delivery_number", None)
    delivery_center = request.json.get("delivery_center", None)

    order = Order.query.filter_by(id=orderId).first()
    if not order:
        response = jsonify({"status": "error", "message": "Cette commande est introuvable"})
        return response, 404 
    if order.paid_confirmed != "confirmed":
        response = jsonify({"status": "error", "message": "Cette commande n'est pas encore payée"})
        return response, 200 
    
    managed_by = User.query.filter_by(id=id).first()
    if not order.managed_by:
        order.managed_by = managed_by
    elif order.managed_by_id != managed_by.id and managed_by.status != 'admin':
        return jsonify({"status": "error", "message": "Vous n'êtes pas d'acte à manager cette commande"}), 200

    order.delivered = True
    order.delivery_number = delivery_number
    order.delivery_center = delivery_center
    order.updated_on = datetime.utcnow()
    db.session.commit()
    
    sendMail.orderDeliveryEmail(order=order, user=order.ordered_by)
    
    # Fetch the orders
    orders = Order.query.filter_by(remove=False).order_by(Order.updated_on.desc()).all()
    orders = orderAsDict(orders)
    
    response = jsonify({"status": "success", "message": "Complète!", "orders": orders})
    return response, 200

@bp.route('/aliexpress/search', methods=('POST',))
@jwt_required()
@is_moderator
def aliexpressSearchProducts():
    group = request.json.get("group", None)
    query = request.json.get("query", None)
    category = request.json.get("category", None)

    if not query and not category:
        response = jsonify({"status": "error", "message": "Format incorrect!"})
        return response, 401
    data = aliapi.getProductsbySearch(group, category, query)
    response = jsonify({"status": "success", "message": "Complete!", "searchItems": data['searchItems']})
    return response, 200

@bp.route('/aliexpress/item', methods=('POST',))
@jwt_required()
@is_moderator
def aliexpressProduct():
    itemId = request.json.get("itemId", None)

    if not itemId:
        response = jsonify({"status": "error", "message": "Format incorrect!"})
        return response, 401

    data = aliapi.getProductDetail(itemId)
    response = jsonify({"status": "success", "message": "Complete!", "item": data['item']})
    return response, 200

@bp.route('/aliexpress/categories', methods=('GET','PSOT'))
@jwt_required()
@is_moderator
def aliexpressCategoryProducts():
    data = aliapi.getProductCategories()
    response = jsonify({"status": "success", "message": "Complete!", "categories": data['categories']})
    return response, 200

@bp.route('/product/add', methods=('GET','POST'))
@jwt_required()
@is_moderator
def addProduct():
    id = get_jwt_identity()
    itemId = request.json.get('itemId', None)
    category = request.json.get('category', None)
    storeTitle = request.json.get('storeTitle', None)
    title = request.json.get('title', None)
    rating = request.json.get('rating', None)
    desc = request.json.get('desc', None)
    imgSrc = request.json.get('imgSrc', None)
    price = request.json.get('price', None)
    currency = request.json.get('currency', None)
    available_in = request.json.get('available_in', None)
    media = request.json.get('media', None)
    
    user = User.query.filter_by(id=id).first()
    product = Product.query.filter_by(itemId=itemId).first()
    
    if product:
        return jsonify({"status": "error", 
                        "message": "Ce produit est déjà disponible, vous pouvez le modifier dans la section mise à jour."}), 200

    availabilities = []
    for location in available_in:
        available = Availability.query.filter_by(location=location).first()
        if available:
            availabilities.append(available)
        else:
            new_location = Availability(location=location)
            availabilities.append(new_location)
            db.session.add(new_location)
            db.session.commit()
    medias = []
    for m in media:
        new_m = Media(type=m['type'], src=m['src'])
        medias.append(new_m)
        db.session.add(new_m)
        db.session.commit()
        
    new_product = Product(
        itemId=itemId,
        category=category, 
        storeTitle=storeTitle,
        title=title,
        rating=rating,
        desc=desc,
        imgSrc=imgSrc,
        price=price,
        currency=currency,
        created_by=user,
        available_in=availabilities,
        media=medias)
    db.session.add(new_product)
    db.session.commit()    
    return jsonify({"status": "success", "message": "Produit ajouté!"}), 200

@bp.route('/product/update', methods=('GET','POST'))
@jwt_required()
@is_moderator
def updateProduct():
    id = get_jwt_identity()
    prodId = request.json.get('prodId', None)
    itemId = request.json.get('itemId', None)
    category = request.json.get('category', None)
    storeTitle = request.json.get('storeTitle', None)
    title = request.json.get('title', None)
    rating = request.json.get('rating', None)
    desc = request.json.get('desc', None)
    imgSrc = request.json.get('imgSrc', None)
    price = request.json.get('price', None)
    currency = request.json.get('currency', None)
    available_in = request.json.get('available_in', None)
    media = request.json.get('media', None)
    
    user = User.query.filter_by(id=id).first()
    product = Product.query.filter_by(id=prodId).first()
    
    if not product:
        return jsonify({"status": "error", "message": "Product introuvable"}), 200

    availabilities = []
    for location in available_in:
        available = Availability.query.filter_by(location=location).first()
        if available:
            availabilities.append(available)
        else:
            new_location = Availability(location=location)
            availabilities.append(new_location)
            db.session.add(new_location)
            db.session.commit()
            
    for old_media in product.media:
        db.session.delete(old_media)
        
    medias = []
    for m in media:
        new_m = Media(type=m['type'], src=m['src'])
        medias.append(new_m)
        db.session.add(new_m)
        db.session.commit()
        
    product.itemId=itemId
    product.category=category
    product.storeTitle=storeTitle
    product.title=title
    product.rating=rating
    product.desc=desc
    product.imgSrc=imgSrc
    product.price=price
    product.currency=currency
    product.available_in=availabilities
    product.media=medias
    product.updated_on = datetime.utcnow()
    db.session.commit()    
    return jsonify({"status": "success", "message": "Produit modifié!"}), 200

@bp.route('/dashboard', methods=('GET','PSOT'))
@jwt_required()
@is_moderator
def fetchDashboard():
    numUser = User.query.count()
    numModerator = User.query.filter_by(status='moderator').count()
    numAdmin =  User.query.filter_by(status='admin').count()
    numClient = User.query.filter_by(status='user').count()
    numProduct = Product.query.count()
    numCart = Cart.query.filter_by(ordered=False).count()
    
    numPaidSubmitted = Order.query.filter((Order.paid_confirmed=='submitted') & (Order.remove==False) & (Order.canceled==False)).count()

    numPaidRejected = Order.query.filter((Order.paid_confirmed=='rejected') & (Order.delivered==False)).count()
    numPaidConfirmed = Order.query.filter((Order.paid_confirmed=='confirmed') & (Order.delivered==False)).count()
    
    numOrderDelivery = Order.query.filter_by(delivered=True).count()
    numOrderConfirmed = Order.query.filter_by(paid_confirmed='confirmed').count()
    users = [user.as_dict() for user in User.query.order_by(User.created_on.desc()).all()]
    
    # Define the date one month ago from now
    date = datetime.now() - timedelta(days=30)

    # Query to get the top 12 most bought products
    result = (
        db.session.query(
            Product.id,
            Product.title,
            func.sum(OrderItem.quantity).label('total_quantity')
        )
        .join(OrderItem, OrderItem.product_id == Product.id)
        .join(Order, Order.id == OrderItem.order_id)
        .filter(
            Order.delivered == True,
            Order.created_on >= date
        )
        .group_by(Product.id, Product.title)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(12)
        .all()
    )

    # Transform the result into a list of dictionaries
    top_products = [
        {
            "id": product_id,
            "title": product_title,
            "quantities": total_quantity
        }
        for product_id, product_title, total_quantity in result
    ]
    
    # Extract product IDs from top_products
    product_ids = [product["id"] for product in top_products]

    # Query the Cart table to get related cart items
    carts_result = db.session.query(
        Cart.product_id,
        func.sum(Cart.quantity).label('total_quantity')
    ).filter((Cart.product_id.in_(product_ids)) & (Cart.ordered==False)).group_by(Cart.product_id).all()

    # Create a list with related cart information
    related_carts = [
        {
            "id": product_id,
            "title": next((product["title"] for product in top_products if product["id"] == product_id), None),
            "quantities": total_quantity
        }
        for product_id, total_quantity in carts_result
    ]
    
    orders = [
        {
            "id": order.id,
            "price": order.total_price,
            "date": order.created_on
        }
        for order in Order.query.all()
    ]
    
    delivered_orders = [
        {
            "id": order.id,
            "price": order.total_price,
            "date": order.created_on
        }
        for order in Order.query.filter_by(delivered=True).all()
    ]

    dashboard = {
        "statistic": [
            {"name": "Utilisateurs", "icon": "fas fa-users", "value": numUser, "ratio": "" },
            {"name": "Produits", "icon": "fas fa-cubes", "value": numProduct, "ratio": "" },
            {"name": "Panier D'achat", "icon": "fas fa-shopping-cart", "value": numCart, "ratio": "" },
            {"name": "Payements Envoyés", "icon": "fas fa-file-invoice-dollar", "value": numPaidSubmitted, "ratio": "" },
            {"name": "Payement Ratio", "icon": "fas fa-money-check-alt", "value": numPaidConfirmed, "ratio": numPaidRejected, "labels": {"value": "approuvé(s)", "ratio": "rejeté(s)"} },
            {"name": "Commandes Ratio", "icon": "fas fa-shipping-fast", "value": numOrderConfirmed, "ratio": numOrderDelivery, "labels": {"value": "livrée(s)", "ratio": "payée(s)"} },
        ], 
        "user": [
            {"name": "Administrateurs", "value": numAdmin },
            {"name": "Modérateurs", "value": numModerator },
            {"name": "Clients", "value": numClient }
        ],
        "top_products": top_products,
        "related_carts": related_carts,
        "orders": orders,
        "delivered_orders": delivered_orders,
        "users": users
    }
    response = jsonify({"status": "success", "message": "Complete!", "dashboard": dashboard})
    return response, 200
