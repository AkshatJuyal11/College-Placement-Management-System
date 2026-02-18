import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'dev-jwt-secret')
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/cpms')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'static/uploads')
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 5242880))  # 5MB
    ALLOWED_EXTENSIONS = {'pdf'}
    JWT_TOKEN_LOCATION = ['headers']
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
