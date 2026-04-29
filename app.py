import sys
import os

# ✅ FIX PYTHON PATH
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, jsonify, render_template, send_from_directory
from config import Config
from backend.ml_model.model_loader import ModelLoader
from flask_jwt_extended import JWTManager 

from backend.services.database_service import DatabaseService
from backend.ml_model.predict_service import PredictService

# ✅ CORRECT IMPORTS
from backend.api.auth_routes import auth_bp
from backend.api.user_routes import user_bp
from backend.api.scan_routes import scan_bp 
from backend.api.admin_routes import admin_bp
from backend.api.trash_routes import trash_bp
from backend.api.gallery_routes import gallery_bp 
from backend.api.chatbot_routes import chatbot_bp

# ✅ MODULE IMPORTS
import backend.api.scan_routes as scan_routes 
import backend.api.admin_routes as admin_routes_module
from backend.models.admin_model import AdminModel


def create_app(config_class=Config):
    app = Flask(__name__, 
                static_folder='src/static',
                template_folder='src/templates')
    
    app.config.from_object(config_class)

    # JWT CONFIG
    if 'SECRET_KEY' in app.config and 'JWT_SECRET_KEY' not in app.config:
        app.config['JWT_SECRET_KEY'] = app.config['SECRET_KEY']

    jwt = JWTManager(app)

    # CREATE UPLOAD FOLDER
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # DATABASE TEST
    try:
        db = DatabaseService.get_db()
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        print("✅ DATABASE CONNECTED SUCCESSFULLY")
    except Exception as e:
        print("❌ DATABASE CONNECTION FAILED:", e)

    # REGISTER APIs
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/user')
    app.register_blueprint(scan_bp, url_prefix='/api/scan')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(trash_bp, url_prefix='/api/trash')
    app.register_blueprint(gallery_bp, url_prefix='/api/gallery')
    app.register_blueprint(chatbot_bp, url_prefix='/api/chatbot')

    # =========================
    # ✅ LOAD ML MODEL
    # =========================
    model_loaded = False

    model_path = app.config['MODEL_PATH']
    print("📂 MODEL PATH:", model_path)

    if not os.path.exists(model_path):
        print("❌ MODEL FILE NOT FOUND!")
    else:
        print("✅ MODEL FILE FOUND")

    try:
        ModelLoader.load_model(model_path)
        print("✅ ML MODEL LOADED SUCCESSFULLY")
        model_loaded = True
    except Exception as e:
        import traceback
        print("❌ MODEL LOAD ERROR:")
        traceback.print_exc()
        model_loaded = False

    # =========================
    # ✅ INITIALIZE SERVICES
    # =========================
    with app.app_context():
        if model_loaded:
            print("✅ Predict service initialized")
            scan_routes.predict_service = PredictService()
        else:
            print("❌ Predict service NOT initialized")
            scan_routes.predict_service = None 

        admin_routes_module.admin_model = AdminModel(
            disease_classes=app.config.get('DISEASE_CLASSES')
        )

    # =========================
    # FRONTEND ROUTES
    # =========================
    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login')
    def login_page():
        return render_template('auth/login.html')

    @app.route('/signup')
    def signup_page():
        return render_template('auth/signup.html')

    @app.route('/dashboard')
    def dashboard_page():
        return render_template('user/dashboard.html')

    @app.route('/scan')
    def scan_page():
        return render_template('user/scan.html')

    @app.route('/gallery')
    def gallery_page():
        return render_template('user/gallery.html')

    @app.route('/uploads/<path:filename>')
    def serve_uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

    # ERROR HANDLING
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Not Found"}), 404

    app.teardown_appcontext(DatabaseService.close_db_connection)

    return app


# =========================
# RUN APP
# =========================
if __name__ == '__main__':
    os.environ['SECRET_KEY'] = 'dev-key'
    app = create_app(Config)
    app.run(host='0.0.0.0', port=5000, debug=True)