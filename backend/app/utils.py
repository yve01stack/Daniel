from flask import render_template, current_app
from app.extensions import mail
from threading import Thread
from flask_mail import Message
from datetime import datetime
import random
import string
import requests
import os
import json
 
class MailSender(object):
    def __init__(self, app):
        self.app = app
        self.send_via_api = current_app.config['SEND_VIA_API']
        # headers
        self.headers = {
            "x-rapidapi-key": current_app.config['RAPIDAPI_KEY'],
            "x-rapidapi-host": current_app.config['FIREBASE_MAILER_URL'],
            "Content-Type": "application/json"
        }
        
        self.from_email = current_app.config['SENDER_EMAIL']
        self.reply_to_email = current_app.config['REPLY_TO_EMAIL']
        self.from_name = current_app.config['SENDER_NAME']
        self.flask_mail_sender = current_app.config['MAIL_USERNAME']
        self.url = "https://send-mail-serverless.p.rapidapi.com/send"

    def async_send(self, app, msg):
        with app.app_context():
            try:
                if self.send_via_api:
                    response = requests.post(self.url, json=msg, headers=self.headers)
                    print(response.json())
                else:  
                    mail.send(msg)
            except Exception as e:
                print(e)

    def send(self, subject, receiver, html_body):
        if self.send_via_api:
            
            msg = {
                "personalizations": [
                    { 
                    "to": [
                            {
                                "email": receiver.email,
                                "name": receiver.name
                            }
                        ] 
                    }
                ],
                "from": {
                    "email": self.from_email,
                    "name": self.from_name
                },
                "reply_to": {
                    "email": self.reply_to_email,
                    "name": self.from_name
                },
                "subject": subject,
                "content": [
                    {
                        "type": "text/html",
                        "value": html_body
                    },
                    {
                        "type": "text/plan",
                        "value": "Hello You!"
                    }
                ],
                "headers": { "List-Unsubscribe": "<mailto: unsubscribe@firebese.com?subject=unsubscribe>, <https://firebese.com/unsubscribe/id>" }
            }
            
        else:
            msg = Message(subject, 
                          sender=self.flask_mail_sender, 
                          recipients=[receiver])
            msg.body = "Hello You!"
            msg.html = html_body
        Thread(target=self.async_send, args=(self.app, msg)).start()

    # Email templates
    def resetPasswordRequest(self, user, baseUrl):
        year = datetime.utcnow().year
        
        token = user.get_reset_password_token()
        url = str(baseUrl)+str(token)
        self.send('Réinitialisez votre mot de passe',
                   receiver=user, 
                   html_body=render_template('email/reset_password.html', user=user, url=url, year=year))
        print(url)

    def checkEmailRequest(self, user, baseUrl):
        year = datetime.utcnow().year
        
        token = user.get_confirm_email_token()
        url = str(baseUrl)+str(token)
        self.send('Confirmez votre adresse e-mail',
                   receiver=user, 
                   html_body=render_template('email/confirm_email.html', user=user, url=url, year=year))
        print(url)
    
    def orderEmail(self, url, order, user):
        year = datetime.utcnow().year
        
        subject = f"Votre commande {order.order_number} - Paiement en attente"
        body = f"""
            <p>Merci d'avoir passé une commande sur notre site. Nous sommes ravis de vous compter parmi nos clients !</p>
            <p>Pour finaliser votre commande, veuillez effectuer le paiement via mobile à l'aide des informations ci-dessous :</p>
            <p style="background-color: #f8f8f8; padding: 10px; border: 1px solid #ddd;">
                <strong>Montant total :</strong> {order.total_price} {order.currency}<br>
                <strong>Référence de commande :</strong> {order.order_number}<br>
                <strong>Détails du paiement mobile :</strong> {order.account_number}, {order.account_name}
            </p>
            <p>Une fois le paiement effectué, nous vous invitons à soumettre une capture d'écran de la transaction dans votre espace client. Pour ce faire, <a href="{url}" style="text-decoration: none;">connectez-vous</a> à votre profil sur notre site, allez dans la section "Mes commandes", puis téléchargez votre capture d'écran sous la commande correspondante.</p>
        """
        self.send(subject, receiver=user,
                   html_body=render_template('email/email_to_client.html', user=user, body=body, year=year))
    
    def orderCanceledEmail(self, url, order, user):
        year = datetime.utcnow().year
        
        subject = f"Votre commande {order.order_number} - annuelée"
        body = f"""
            <p>Nous vous informons que votre commande <strong>{order.order_number}</strong> a été annulée. Si vous avez des questions ou souhaitez obtenir plus de détails, n'hésitez pas à nous contacter.</p>
            <p>Nous comprenons que cette situation puisse être décevante, mais sachez que vous êtes toujours le bienvenu sur notre site <strong>Mes Achats en Chine</strong>. Nous restons à votre disposition pour vous offrir la meilleure expérience possible.</p>
            <p>Explorez notre site pour découvrir nos derniers produits et offres spéciales. Nous espérons vous revoir très bientôt et vous aider à trouver exactement ce que vous cherchez.</p>
        """
        self.send(subject, receiver=user,
                   html_body=render_template('email/email_to_client.html', user=user, body=body, year=year))    

    def paymentConfirmEmail(self, decision, order, user):
        year = datetime.utcnow().year
        
        subject = f"Votre commande {order.order_number} - Paiement en confirmation"
        body = f"""
            <p>Ce mail a été envoyé concernant le paiement de votre commande <strong>{order.order_number}</strong>.</p>
            <p>{decision}</p>
        """
        self.send(subject, receiver=user,
                   html_body=render_template('email/email_to_client.html', user=user, body=body, year=year))    
    
    def orderDeliveryEmail(self, order, user):
        year = datetime.utcnow().year
        
        subject = f"Votre commande {order.order_number} - livrée"
        body = f"""
            <p>Nous sommes heureux de vous informer que votre commande <strong>{order.order_number}</strong> a été livrée avec succès. Vous pouvez récupérer votre commande en utilisant les informations suivantes :</p>
            <p style="background-color: #f8f8f8; padding: 10px; border: 1px solid #ddd;">
                <strong>Numéro de livraison :</strong> {order.delivery_number}<br>
                <strong>Centre de livraison :</strong> {order.delivery_center}
            </p>
        """
        self.send(subject, receiver=user,
                   html_body=render_template('email/email_to_client.html', user=user, body=body, year=year))    

    def paymentSubmittedEmail(self, order, user):
        year = datetime.utcnow().year
        
        subject = f"Votre commande {order.order_number} - Paiement en enrégistré"
        body = f"""
            <p>Nous souhaitons vous informer qu'un client a téléchargé un justificatif de paiement pour sa commande <strong>{order.order_number}</strong>.</p>
            <p>Voici les détails :</p>
            <p style="background-color: #f8f8f8; padding: 10px; border: 1px solid #ddd;">
                <strong>Client :</strong> {order.ordered_by.name}<br>
                <strong>Numéro de commande :</strong> {order.order_number}<br>
                <strong>Date du téléchargement :</strong> {order.updated_on.strftime("%m/%d/%Y")}
            </p>
            <p>Nous vous invitons à vérifier le justificatif de paiement et à procéder à la validation de la commande si tout est en ordre.</p>
            <p>Pour plus de détails, veuillez vous connecter à votre tableau de bord d'administration.</p>
        """
        self.send(subject, receiver=user,
                   html_body=render_template('email/email_to_admin.html', user=user, body=body, year=year))                   

#Class to consume RapiApi - Aliexpress
class AliApi:
    #constructor
    def __init__(self):
        self.loc = 'CN'
        self.locale = 'fr_FR'
        self.region = 'US'
        self.currency = 'USD'
        # headers 
        self.headers = {
            "x-rapidapi-key": current_app.config['RAPIDAPI_KEY'],
            "x-rapidapi-host": current_app.config['ALIEXPRESS_URL']
        }

    #GET Products Searching
    def getProductsbySearch(self, group, category, searchWord):
        url = "https://aliexpress-datahub.p.rapidapi.com/item_search"
        headers=self.headers
        querystring = {"q": searchWord,"page":"1","sort":"default", 'loc':self.loc, 'locale':self.locale, 'region':self.region, 'currency':self.currency}
        response = requests.get(url, headers=headers, params=querystring)
        
        data = response.json()
        return {"searchItems": data['result']['resultList']}
    
    #Product Detail 
    def getProductDetail(self, itemId):
        url = "https://aliexpress-datahub.p.rapidapi.com/item_detail"
        headers=self.headers
        querystring = {"itemId": itemId, 'loc':self.loc, 'locale':self.locale, 'region':self.region, 'currency':self.currency}
        response = requests.get(url, headers=headers, params=querystring)
        
        data = response.json()
        item = data['result']['item']
        item["storeTitle"] = data['result']['seller']['storeTitle']
        return {"item": item}

    #GET Product category
    def getProductCategories(self):
        url = "https://aliexpress-datahub.p.rapidapi.com/category_list_1"
        headers=self.headers
        querystring = {'loc':self.loc, 'locale':self.locale, 'region':self.region, 'currency':self.currency}
        # response = requests.get(url, headers=headers, params=querystring)
        # data = response.json()
        
        # path = os.path.join('app', 'static', 'data', 'aliexpress_categories.json')
        # with open(path, 'w') as outfile: 
        #     json.dump({"categories": data['result']['resultList']}, outfile)
        
        path = os.path.join('app', 'static', 'data', 'aliexpress_categories.json')
        with open(path, 'r', encoding='utf-8') as fp:
            data = json.load(fp)
        return {"categories": data['categories']}
    

class OpenStreetMap:
    def __init__(self):
        self.url = "https://nominatim.openstreetmap.org/search?"

    def getCoordinates(self, address):
        querystring = {"q": address, "format": "json", "addressdetails": 1, "limit": 1, "polygon_svg": 1 }
        response = requests.get(self.url, params=querystring)
        print(response)
        
        if response.status_code == 200:
            data = response.json()
        else:
            data = [] 
    
        if len(data) > 0:
            return { "longitude": float(data[0]['lon']), "latitude": float(data[0]['lat']) }
        return {'longitude': 9.4418849, "latitude": 0.4086518 }


def generateUniqueId():
    # Get current date
    now = datetime.now()
    
    # Date component: year (2 digits) + month (2 digits) + day (2 digits)
    date_component = now.strftime("%y%m%d")  # e.g., '240806' for August 6, 2024
    
    # Random alphanumeric component: 4 characters long
    random_component = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    
    # Combine components to create the order number
    order_number = date_component + random_component
    
    return order_number




