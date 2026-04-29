import os

class Config:
    SECRET_KEY = "secret123"
    DEBUG = True

    MYSQL_HOST = "localhost"
    MYSQL_USER = "root"
    MYSQL_PASSWORD = "root123"
    MYSQL_DB = "leafguard_db"
    MYSQL_PORT = 3306

    # ✅ CORRECT MODEL PATH
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    MODEL_PATH = os.path.join(
        BASE_DIR,
        "ml_model_files",
        "mango_leaf_classifier_98_plus_final.h5"
    )

    DISEASE_CLASSES = [
        'Anthracnose',
        'Bacterial Canker',
        'Cutting Weevil',
        'die back',
        'Gall Midge',
        'Healthy',
        'Powdery Mildew',
        'Sooty Mould'
    ]

    IMAGE_SIZE = (224, 224)
    COLOR_MODE = 'rgb'

    UPLOAD_FOLDER = os.path.join(BASE_DIR, "backend", "uploads", "images")
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}