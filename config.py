class Config:
    SECRET_KEY = 'your-secret-key'  
    SQLALCHEMY_DATABASE_URI = 'sqlite:///payment_gateway.db'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = True
