from flask import request, jsonify, g
from app.extensions import db

from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies
from flask_jwt_extended import unset_jwt_cookies, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

from app.auth import bp
from app.models.user import User

sendMail = g.sendMail


@bp.route('/signup', methods=('POST',))
def signup():
    phone = request.json.get("phone", None)
    name = request.json.get("name", None)
    password = request.json.get("password", None)
    email = request.json.get("email", None)
    location = request.json.get("location", "")

    if not phone or not name or not password:
        return jsonify({"status": "error", "message": "Le format ne correspond pas"}), 400
    
    user = User.query.filter((User.phone == phone) | (User.name == name)).first()
    if not user: 
        user = User(phone=phone, 
                    name=name, 
                    location=location, 
                    password=generate_password_hash(password))
        if email is not None:
            emailCheck = User.query.filter_by(email=email).first()
            if emailCheck:
                return jsonify({"status": "error", "message": "Cette adresse e-mail ne peut pas être utilisée"}), 400
            else:
                user = User(phone=phone, 
                            name=name, 
                            email=email, 
                            location=location, 
                            password=generate_password_hash(password))
        
        db.session.add(user)
        db.session.commit()
        user = User.query.filter_by(phone=phone).first()
        if not user:
            return jsonify({"status": "error", "message": "Quelque chose ne va pas, réessayez"}), 400
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        response = jsonify({"status": "success", "access_token": access_token, 
                            "refresh_token": refresh_token,
                            "user_info": user.as_dict(), "message": "Completed"})
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response, 200
    else:
        return jsonify({"status": "error", "message": "Ce numéro de téléphone ou ce nom ne peut pas être utilisé"}), 400
  
@bp.route('/signin', methods=('POST',))
def signin():
    phone = request.json.get("phone", None)
    password = request.json.get("password", None)

    user = User.query.filter_by(phone=phone).first()
    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        return jsonify({"status": "error", "message": "Mot de passe ou numéro de téléphone incorrect"}), 200
    
    if user:
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        response = jsonify({"status": "success", "access_token": access_token, 
                            "refresh_token": refresh_token,
                            "user_info": user.as_dict(), "message": "Completed!"})
        set_access_cookies(response, access_token)
        set_refresh_cookies(response, refresh_token)
        return response, 201
    else:
        return jsonify({"status": "error", "message": "Unauthorized"}), 401

@bp.route('/user', methods=('GET','POST'))
@jwt_required()
def fetchUser():
    id = get_jwt_identity()
    user = User.query.filter_by(id=id).first()
    if not user:
        return jsonify({"status": "error", "message": "Bad access token"}), 401
    
    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)

    response = jsonify({"status": "success", "access_token": access_token, 
                        "refresh_token": refresh_token,
                        "user_info": user.as_dict(), "message": "Completed!"})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 201

@bp.route('/refresh', methods=('POST','GET'))
@jwt_required(refresh=True)
def refresh():
    id = get_jwt_identity()
    access_token = create_access_token(identity=id)
    set_access_cookies(response, access_token)
    response = jsonify({"status": "success", "access_token": access_token})
    return response, 201

@bp.route('/logout', methods=('POST','GET'))
@jwt_required()
def logout():
    response = jsonify({"status": "success", "message": ""})
    unset_jwt_cookies(response)
    return response, 200

@bp.route('/edict_email', methods=('GET','POST'))
@jwt_required()
def edictEmail():
    id = get_jwt_identity()
    email = request.json.get("email", None)
    phone = request.json.get("phone", None)
    
    current_user = User.query.filter_by(id=id).first()
    
    if not email or not phone or not current_user:
        return jsonify({"status": "error", "message": "Mauvaise requête"}), 201

    user = User.query.filter_by(email=email).first()
    if user and user != current_user:
        return jsonify({"status": "error", "message": "Cette adresse email n\'est pas disponible"}), 201
    
    user = User.query.filter_by(phone=phone).first()
    if user and user != current_user:
        return jsonify({"status": "error", "message": "Ce numéro de téléphone n\'est pas disponible"}), 201
    
    if email and email != '':
        if email != current_user.email:
            current_user.email = email
            current_user.confirmed = False
    if phone != current_user.phone and phone != '':
        current_user.phone = phone
    user.updated_on = datetime.utcnow()
    db.session.commit()

    response = jsonify({"status": "success", "message": "Votre adresse a bien été modifiée!",
                        "user_info": current_user.as_dict()})
    return response, 201

@bp.route('/change_pwd', methods=('GET','POST'))
@jwt_required()
def changePwd():
    id = get_jwt_identity()
    password = request.json.get("password", None)
    current_user = User.query.filter_by(id=id).first()
    if not current_user:
        return jsonify({"status": "error", "message": "Mauvaise requête"}), 401
    if not password:
        return jsonify({"status": "error", "message": "Mauvaise requête"}), 201
    
    current_user.password = generate_password_hash(password)
    current_user.updated_on = datetime.utcnow()
    db.session.commit()
    
    response = jsonify({"status": "success", "message": "Mot de passe modifié!",
                        "user_info": current_user.as_dict()})
    return response, 201

@bp.route('/check_email', methods=('POST','GET'))
@jwt_required()
def checkEmail():
    id = get_jwt_identity()
    baseUrl = request.json.get("baseUrl", None)

    current_user = User.query.filter_by(id=id).first()
    if current_user.confirmed:
        return jsonify({"status": "error", "message": "Votre adresse est déjà été vérifiée"}), 201
    sendMail.checkEmailRequest(current_user, baseUrl)
    response = jsonify({"status": "success", "message": "Vérifiez votre e-mail (ou spam) pour obtenir les instructions pour confirmer votre adresse mail.",
                        "user_info": current_user.as_dict()})
    return response, 201

@bp.route('/checked_email', methods=('POST','GET'))
def checkedEmail():
    token = request.json.get("token", None)
    current_user = User.verify_confirm_email_token(token)
    if not current_user:
        return jsonify({"status": "error", "message": "Le lien est expiré, veuillez réessayer!"}), 201
    current_user.set_confirmed(True)
    current_user.updated_on = datetime.utcnow()
    response = jsonify({"status": "success", "message": "Votre adresse mail a bien été vérifiée.",
                        "user_info": current_user.as_dict()})
    return response, 201

@bp.route('/forgot_password', methods=('GET', 'POST'))
def forgotPassword():
    email = request.json.get("email", None)
    baseUrl = request.json.get("baseUrl", None)

    if not email:
        return jsonify({"status": "error", "message": "Mauvaise requête, réessayer plus tard"}), 201
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"status": "error", "message": "Mauvaise requête, réessayer plus tard"}), 201
    sendMail.resetPasswordRequest(user, baseUrl)
    response = jsonify({"status": "success", 
                        "message": "Vérifiez votre e-mail (ou spam) pour obtenir les instructions pour réinitialiser votre mot de passe"})
    return response, 201

@bp.route('/reset_password', methods=('POST','GET'))
def reset_password():
    token = request.json.get("token", None)
    current_user = User.verify_reset_password_token(token)
    if not current_user:
        return jsonify({"status": "error", "message": "Le lien est expiré, veuillez réessayer!"}), 201
    access_token = create_access_token(identity=current_user.id)
    refresh_token = create_refresh_token(identity=current_user.id)

    response = jsonify({"status": "success", "access_token": access_token, 
                        "refresh_token": refresh_token,
                        "user_info": current_user.as_dict(), 
                        "message": "Veuillez accéder à votre profil, cliquez modifier et définir un nouveau mot de passe!"})
    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)
    return response, 201

