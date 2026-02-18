import os
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def save_resume(file, user_id):
    """Save uploaded resume file"""
    if file and allowed_file(file.filename):
        filename = secure_filename(f"{user_id}_{file.filename}")
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        
        # Create upload directory if it doesn't exist
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        
        file.save(filepath)
        return filepath
    return None

def validate_email(email):
    """Basic email validation"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_cgpa(cgpa):
    """Validate CGPA range"""
    try:
        cgpa_float = float(cgpa)
        return 0 <= cgpa_float <= 10
    except (ValueError, TypeError):
        return False
