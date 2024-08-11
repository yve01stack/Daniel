from flask import Flask, g
import logging, os
from logging.handlers import SMTPHandler
from logging.handlers import RotatingFileHandler

from config import Config
from app.extensions import db, migrate, jwt, cors, migrate, mail
from app.models import user, product
from app.utils import MailSender

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Flask extensions here
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)
    migrate.init_app(app, db, render_as_batch=True)
    mail.init_app(app)
    
    
    
    if not app.debug:
        if app.config['MAIL_SERVER']:
            auth = None
            if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
                auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
            secure = None
            if app.config['MAIL_USE_TLS']:
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
                fromaddr='no-reply@' + app.config['MAIL_SERVER'],
                toaddrs=app.config['HANDLER_EMAILS'], subject='Web Application Failure',
                credentials=auth, secure=secure)
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/mesachatsenchine.log', maxBytes=10240,
                                        backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Contact the developer')

    
    @app.cli.command("init_db")
    def init_db():
        user.init_db()
        product.init_db()
    
    @app.shell_context_processor
    def make_shell_context():
        return {'db': db, 'User': user.User, 'Product': product.Product, 'Order': product.Order, 'Cart': product.Cart }

    with app.app_context():    
        g.sendMail = MailSender(app) 
        
        # Register blueprints here
        from .main import bp as main_bp
        app.register_blueprint(main_bp)

        from .auth import bp as auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')

        from .products import bp as product_bp
        app.register_blueprint(product_bp, url_prefix='/product')

        from .admin import bp as admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

    @app.route('/test/')
    def test_page():
        return '<h1>Testing the Flask Application Factory Pattern</h1>'

    return app
