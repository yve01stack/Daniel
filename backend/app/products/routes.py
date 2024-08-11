from flask import  request, jsonify, current_app, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from datetime import datetime
import os

from app.products import bp
from app.extensions import db
from app.utils import generateUniqueId

from app.models.product import Product, Cart, OrderItem, Order, Location, Availability
from app.models.user import User

sendMail = g.sendMail

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


@bp.route('/fetch_products', methods=('GET','PSOT'))
def fetchProducts():
    products = [product.as_dict() for product in Product.query.all()]
    countries = [country.as_dict() for country in Availability.query.all()]
    
    categories = db.session.query(Product.category).distinct().all()
    unique_categories = [category[0] for category in categories]

    response = jsonify({"status": "success", "message": "Complete!", "products": products, 
                        "countries": countries, "categories": unique_categories})
    return response, 200

@bp.route('/fetch_carts', methods=('GET','POST'))
@jwt_required()
def fetchCarts():
    id = get_jwt_identity()
    carts = Cart.query.filter((Cart.created_by_id==id) & (Cart.ordered==False)).all() 
    carts = [cart.as_dict() for cart in carts]
    response = jsonify({"status": "success", "message": "Complete!", "carts": carts})
    return response, 200

@bp.route('/add_to_cart', methods=('GET','POST'))
@jwt_required()
def addToCart():
    id = get_jwt_identity()
    prodId = request.json.get("prodId", None)
    user = User.query.filter_by(id=id).first()
    product = Product.query.filter_by(id=prodId).first()
    if not user or not product:
        return jsonify({"status": "error", "message": "Le format ne correspond pas"}), 400
    
    cart = Cart.query.filter((Cart.created_by_id == id) & (Cart.product_id == prodId) & (Cart.ordered==False)).first()
    if cart:
        cart.quantity += 1
    else:
        new_cart = Cart(quantity=1, product=product, created_by=user, ordered=False)
        db.session.add(new_cart)
    db.session.commit()

    carts = Cart.query.filter((Cart.created_by_id==id) & (Cart.ordered==False)).all()
    carts = [cart.as_dict() for cart in carts]
    response = jsonify({"status": "success", "message": "Complete!", "carts": carts})
    return response, 200

@bp.route('/remove_from_cart', methods=('GET','POST'))
@jwt_required()
def removeFromCart():
    id = get_jwt_identity()
    cartId = request.json.get("cartId", None)
    cart = Cart.query.filter((Cart.created_by_id == id) & (Cart.id == cartId)).first()

    if not cart:
        return jsonify({"status": "error", "message": "Le format ne correspond pas"}), 400
    db.session.delete(cart)
    db.session.commit()

    carts = Cart.query.filter((Cart.created_by_id==id) & (Cart.ordered==False)).all()
    carts = [cart.as_dict() for cart in carts]
    response = jsonify({"status": "success", "message": "Complete!", "carts": carts})
    return response, 200

@bp.route('/increase_qty', methods=('GET','POST'))
@jwt_required()
def increaseQty():
    id = get_jwt_identity()
    cartId = request.json.get("cartId", None)
    cart = Cart.query.filter((Cart.created_by_id == id) & (Cart.id == cartId)).first()

    if not cart:
        return jsonify({"status": "error", "message": "Le format ne correspond pas"}), 400
    cart.quantity += 1
    cart.updated_on = datetime.utcnow()
    db.session.commit()

    carts = Cart.query.filter((Cart.created_by_id==id) & (Cart.ordered==False)).all()
    carts = [cart.as_dict() for cart in carts]
    response = jsonify({"status": "success", "message": "Complete!", "carts": carts})
    return response, 200

@bp.route('/decrease_qty', methods=('GET','POST'))
@jwt_required()
def decreaseQty():
    id = get_jwt_identity()
    cartId = request.json.get("cartId", None)
    cart = Cart.query.filter((Cart.created_by_id == id) & (Cart.id == cartId)).first()

    if not cart:
        return jsonify({"status": "error", "message": "Le format ne correspond pas"}), 400
    if cart.quantity > 1:
        cart.quantity -= 1
        cart.updated_on = datetime.utcnow()
        db.session.commit()

    carts = Cart.query.filter((Cart.created_by_id==id) & (Cart.ordered==False)).all()
    carts = [cart.as_dict() for cart in carts]
    response = jsonify({"status": "success", "message": "Complete!", "carts": carts})
    return response, 200

@bp.route('/order/fetch', methods=('GET','POST'))
@jwt_required()
def fetchOrders():
    id = get_jwt_identity()

    # Fetch the orders
    orders = Order.query.filter((Order.ordered_by_id==id) & (Order.remove==False)).order_by(Order.updated_on.desc()).all()
    orders = orderAsDict(orders)

    response = jsonify({"status": "success", "message": "Complete!", "orders": orders})
    return response, 200

@bp.route('/order/cart', methods=('GET','POST'))
@jwt_required()
def orderCart():
    id = get_jwt_identity()
    carts = Cart.query.filter((Cart.created_by_id==id) & (Cart.ordered==False)).all()

    user = User.query.filter_by(id=id).first()
    # Create locations
    delivery_from = Location(
        longitude=account['Gabon']['coordinates']['longitude'], 
        latitude=account['Gabon']['coordinates']['latitude'])
    db.session.add(delivery_from)
    db.session.commit()
    
    order_number = 'C'+generateUniqueId()

    order = Order(account_number=account['Gabon']['account_number'], 
                  account_name=account['Gabon']['account_name'], 
                  delivery_from_location=delivery_from,
                  ordered_by=user, order_number=order_number) # Create an order 
    db.session.add(order)
    db.session.commit()

    for cart in carts:
        # Add items to the order
        order_item = OrderItem(order_id=order.id, product_id=cart.product_id, quantity=cart.quantity)
        cart.ordered = True
        db.session.add(order_item)
        db.session.commit()
        
    sendMail.orderEmail(url=frontend_url, order=order, user=user)

    # Fetch the orders
    orders = Order.query.filter((Order.ordered_by_id==id) & (Order.remove==False)).order_by(Order.updated_on.desc()).all()
    orders = orderAsDict(orders)

    carts = Cart.query.filter((Cart.created_by_id==id) & (Cart.ordered==False)).all()
    carts = [cart.as_dict() for cart in carts]
    response = jsonify({"status": "success", "message": "Complete!", "carts": carts, "orders": orders})
    return response, 200

@bp.route('/order/product', methods=('GET','POST'))
@jwt_required()
def orderProduct():
    id = get_jwt_identity()
    prodId = request.json.get("prodId", None)

    user = User.query.filter_by(id=id).first()
    
    # Create locations
    delivery_from = Location(
        longitude=account['Gabon']['coordinates']['longitude'], 
        latitude=account['Gabon']['coordinates']['latitude'])
    db.session.add(delivery_from)
    db.session.commit()

    order_number = 'C'+generateUniqueId()
    
    order = Order(account_number=account['Gabon']['account_number'], 
                  account_name=account['Gabon']['account_name'], 
                  delivery_from_location=delivery_from,
                  ordered_by=user, order_number=order_number) # Create an order    
    db.session.add(order)
    db.session.commit()
    
    # Add item to the order
    product = Product.query.filter_by(id=prodId).first()
    if product:
        order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=1)
        db.session.add(order_item)
        db.session.commit()
    else:
        response = jsonify({"status": "error", "message": "Produit commandé n'est pas disponible!"})
        return response, 404 

    sendMail.orderEmail(url=frontend_url, order=order, user=user)

    # Fetch the orders
    orders = Order.query.filter((Order.ordered_by_id==id) & (Order.remove==False)).order_by(Order.updated_on.desc()).all()
    orders = orderAsDict(orders)

    carts = Cart.query.filter((Cart.created_by_id==id) & (Cart.ordered==False)).all()
    carts = [cart.as_dict() for cart in carts]
    response = jsonify({"status": "success", "message": "Complete!", "carts": carts, "orders": orders})
    return response, 200

@bp.route('/order/remove', methods=('GET','POST'))
@jwt_required()
def removeOrder():
    id = get_jwt_identity()
    orderId = request.json.get("orderId", None)
    order = Order.query.filter((Order.id==orderId) & (Order.ordered_by_id==id)).first()
    if not order:
        response = jsonify({"status": "error", "message": "Cette commande est introuvable"})
        return response, 404 
    if order.paid_confirmed == "confirmed" and not order.delivered:
        response = jsonify({"status": "error", "message": "Cette commande est payée et n'est pas encore livrée"})
        return response, 404 
    
    order.remove = True
    order.updated_on = datetime.utcnow()
    db.session.commit()
    
    # Fetch the orders
    orders = Order.query.filter((Order.ordered_by_id==id) & (Order.remove==False)).order_by(Order.updated_on.desc()).all()
    orders = orderAsDict(orders)

    carts = Cart.query.filter((Cart.created_by_id==id) & (Cart.ordered==False)).all()
    carts = [cart.as_dict() for cart in carts]
    response = jsonify({"status": "success", "message": "Complete!", "carts": carts, "orders": orders})
    return response, 200

@bp.route('/order/remove_from_order', methods=('GET','POST'))
@jwt_required()
def removeFromOrder():
    id = get_jwt_identity()
    orderItemId = request.json.get("orderItemId", None)
    item = OrderItem.query.filter_by(id=orderItemId).first()
    order = Order.query.filter((Order.id==item.order_id) & (Order.ordered_by_id==id)).first()
    if not order:
        response = jsonify({"status": "error", "message": "Cette commande est introuvable"})
        return response, 404 
    
    if order.paid_confirmed == "confirmed":
        response = jsonify({"status": "error", "message": "La commande ne peut plus être modifier, le paiement a déjà été confirmé."})
        return response, 401
    
    if len(order.order_items) == 1:
        db.session.delete(order)
        db.session.commit()
    else:
        db.session.delete(item)
        db.session.commit()

    # Fetch the orders
    orders = Order.query.filter((Order.ordered_by_id==id) & (Order.remove==False)).order_by(Order.updated_on.desc()).all()
    orders = orderAsDict(orders)

    carts = Cart.query.filter((Cart.created_by_id==id) & (Cart.ordered==False)).all()
    carts = [cart.as_dict() for cart in carts]
    response = jsonify({"status": "success", "message": "Complete!", "carts": carts, "orders": orders})
    return response, 200

@bp.route('/order/increase_qty', methods=('GET','POST'))
@jwt_required()
def increaseOrderItemQuantity():
    id = get_jwt_identity()
    orderItemId = request.json.get("orderItemId", None)
    item = OrderItem.query.filter_by(id=orderItemId).first()
    order = Order.query.filter((Order.id==item.order_id) & (Order.ordered_by_id==id)).first()
    if not order:
        response = jsonify({"status": "error", "message": "Cette commande est introuvable"})
        return response, 404 

    if order.paid_confirmed == "confirmed":
        response = jsonify({"status": "error", "message": "La commande ne peut plus être modifier, le paiement a déjà été confirmé."})
        return response, 401
    
    item.quantity += 1
    db.session.commit()

    # Fetch the orders
    orders = Order.query.filter((Order.ordered_by_id==id) & (Order.remove==False)).order_by(Order.updated_on.desc()).all()
    orders = orderAsDict(orders)

    carts = Cart.query.filter((Cart.created_by_id==id) & (Cart.ordered==False)).all()
    carts = [cart.as_dict() for cart in carts]
    response = jsonify({"status": "success", "message": "Complete!", "carts": carts, "orders": orders})
    return response, 200

@bp.route('/order/decrease_qty', methods=('GET','POST'))
@jwt_required()
def decreaseOrderItemQuantity():
    id = get_jwt_identity()
    orderItemId = request.json.get("orderItemId", None)
    item = OrderItem.query.filter_by(id=orderItemId).first()
    order = Order.query.filter((Order.id==item.order_id) & (Order.ordered_by_id==id)).first()
    if not order:
        response = jsonify({"status": "error", "message": "Cette commande est introuvable"})
        return response, 404 
    
    if order.paid_confirmed == "confirmed":
        response = jsonify({"status": "error", "message": "La commande ne peut plus être modifier, le paiement a déjà été confirmé."})
        return response, 401
    
    if item.quantity > 1:
        item.quantity -= 1
        db.session.commit()

    # Fetch the orders
    orders = Order.query.filter((Order.ordered_by_id==id) & (Order.remove==False)).order_by(Order.updated_on.desc()).all()
    orders = orderAsDict(orders)

    carts = Cart.query.filter((Cart.created_by_id==id) & (Cart.ordered==False)).all()
    carts = [cart.as_dict() for cart in carts]
    response = jsonify({"status": "success", "message": "Complete!", "carts": carts, "orders": orders})
    return response, 200

@bp.route('/order/paid', methods=('GET','POST'))
@jwt_required()
def paidProofOrder():
    id = get_jwt_identity()
    orderId = request.form.get("orderId", None)
    location = request.form.get("location", None)
        
    order = Order.query.filter((Order.id==orderId) & (Order.ordered_by_id==id)).first()
    ordered_by = User.query.filter_by(id=order.ordered_by_id).first()

    if not order:
        response = jsonify({"status": "error", "message": "Cette commande est introuvable"})
        return response, 404 
    
    if order.paid_confirmed == "confirmed":
        response = jsonify({"status": "error", "message": "La commande ne peut plus être modifier, le paiement a déjà été confirmé."})
        return response, 401
    
    if not ordered_by.confirmed:
        return jsonify({"status": "error", 'message': 'Veuillez ajouter/vérifier votre adresse email pour continuer'}), 201
    
    if 'file' not in request.files:
        return jsonify({"status": "error", 'message': 'No selected file'}), 400
    file = request.files.get('file')
    if file.filename == '':
        return jsonify({"status": "error", 'message': 'No file part'}), 400
    if file:
        ext = file.filename.rsplit(".", 1)[1]
        file.filename = secure_filename(str(datetime.timestamp(datetime.now()))+'.'+ext)
        filepath = os.path.join('app', 'static', 'uploads', file.filename)
        file.save(filepath)
        filepath = os.path.join(server_url, 'static', 'uploads', file.filename).replace("\\", '/')

    if location:
        ordered_by.location = location
    if file:
        order.paid_proof = filepath 
        order.paid_confirmed = "submitted"    
    order.updated_on = datetime.utcnow()   
    db.session.commit()
    
    account_email = account['Gabon']['account_email']
    admin = User.query.filter_by(email=account_email).first()
    if admin:
        sendMail.paymentSubmittedEmail(order=order, user=admin)

    # Fetch the orders
    orders = Order.query.filter((Order.ordered_by_id==id) & (Order.remove==False)).order_by(Order.updated_on.desc()).all()
    orders = orderAsDict(orders)

    carts = Cart.query.filter((Cart.created_by_id==id) & (Cart.ordered==False)).all()
    carts = [cart.as_dict() for cart in carts]
    response = jsonify({"status": "success", "message": "Complète! Vous recevrez un mail après la vérification de votre paiement", "carts": carts, "orders": orders})
    return response, 200
