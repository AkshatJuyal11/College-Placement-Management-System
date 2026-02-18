from flask import Flask, render_template, send_from_directory
from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from config import Config
import os

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize MongoDB
mongo = PyMongo(app)
app.config['db'] = mongo.db

# Initialize JWT
jwt = JWTManager(app)

# Import routes
from routes.auth import auth_bp
from routes.student import student_bp
from routes.company import company_bp
from routes.admin import admin_bp

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(student_bp, url_prefix='/api/student')
app.register_blueprint(company_bp, url_prefix='/api/company')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

# Frontend routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/student-dashboard')
def student_dashboard():
    return render_template('student_dashboard.html')

@app.route('/company-dashboard')
def company_dashboard():
    return render_template('company_dashboard.html')

@app.route('/admin-dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')

# Serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return {'error': 'Not found'}, 404

@app.errorhandler(500)
def internal_error(error):
    return {'error': 'Internal server error'}, 500

if __name__ == '__main__':
    # Create upload directory if it doesn't exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    print("🚀 Starting College Placement Management System")
    print(f"📁 Upload folder: {app.config['UPLOAD_FOLDER']}")
    print(f"🔐 JWT enabled")
    print(f"💾 MongoDB URI: {app.config['MONGO_URI']}")
    print("\n✅ Server running on http://localhost:5000")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
