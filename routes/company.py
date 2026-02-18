from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.database import Company, JobDrive, Application
from bson import ObjectId
from datetime import datetime

company_bp = Blueprint('company', __name__)

def convert_objectid_to_str(obj):
    """Convert ObjectId to string recursively"""
    if isinstance(obj, ObjectId):
        return str(obj)
    elif isinstance(obj, dict):
        return {key: convert_objectid_to_str(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_objectid_to_str(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    return obj

def require_company():
    """Decorator helper to check company role"""
    claims = get_jwt()
    if claims.get('role') != 'company':
        return jsonify({'error': 'Company access required'}), 403
    return None


@company_bp.route('/profile', methods=['GET', 'POST'])
@jwt_required()
def profile():
    """Get or update company profile"""
    check = require_company()
    if check:
        return check
    
    user_id = get_jwt_identity()
    from flask import current_app
    db = current_app.config['db']
    
    if request.method == 'GET':
        company = Company.get_by_user_id(db, user_id)
        if not company:
            return jsonify({'error': 'Profile not found'}), 404
        
        company['_id'] = str(company['_id'])
        company['user_id'] = str(company['user_id'])
        return jsonify(company), 200
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            # Validation
            if not data.get('company_name'):
                return jsonify({'error': 'Company name is required'}), 400
            
            # Update profile
            Company.create_or_update(db, user_id, data)
            
            return jsonify({'message': 'Profile updated successfully'}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@company_bp.route('/job', methods=['POST'])
@jwt_required()
def create_job():
    """Create a new job drive"""
    check = require_company()
    if check:
        return check
    
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validation
        if not data.get('job_title') or not data.get('min_cgpa') or not data.get('branches'):
            return jsonify({'error': 'Job title, minimum CGPA, and branches are required'}), 400
        
        from flask import current_app
        db = current_app.config['db']
        
        # Get company
        company = Company.get_by_user_id(db, user_id)
        
        if not company:
            return jsonify({'error': 'Please complete your company profile first'}), 400
        
        # Create job
        job_id = JobDrive.create(db, str(company['_id']), data)
        
        return jsonify({
            'message': 'Job drive created successfully',
            'job_id': str(job_id)
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@company_bp.route('/jobs', methods=['GET'])
@jwt_required()
def get_jobs():
    """Get jobs posted by company"""
    check = require_company()
    if check:
        return check
    
    try:
        user_id = get_jwt_identity()
        
        from flask import current_app
        db = current_app.config['db']
        
        # Get company
        company = Company.get_by_user_id(db, user_id)
        
        if not company:
            return jsonify({'error': 'Profile not found'}), 404
        
        # Get jobs
        jobs = JobDrive.get_by_company(db, str(company['_id']))
        
        # Convert all ObjectId fields to strings
        jobs = convert_objectid_to_str(jobs)
        
        return jsonify(jobs), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@company_bp.route('/applicants/<job_id>', methods=['GET'])
@jwt_required()
def get_applicants(job_id):
    """Get applicants for a specific job"""
    check = require_company()
    if check:
        return check
    
    try:
        user_id = get_jwt_identity()
        
        from flask import current_app
        db = current_app.config['db']
        
        # Verify job belongs to this company
        job = JobDrive.get_by_id(db, job_id)
        
        if not job:
            return jsonify({'error': 'Job not found'}), 404
        
        company = Company.get_by_user_id(db, user_id)
        
        if str(job['company_id']) != str(company['_id']):
            return jsonify({'error': 'Unauthorized'}), 403
        
        # Get applicants
        applicants = Application.get_by_job(db, job_id)
        
        # Convert all ObjectId fields to strings
        applicants = convert_objectid_to_str(applicants)
        
        return jsonify(applicants), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@company_bp.route('/update-status', methods=['POST'])
@jwt_required()
def update_application_status():
    """Update application status (shortlist/reject)"""
    check = require_company()
    if check:
        return check
    
    try:
        data = request.get_json()
        
        if not data.get('application_id') or not data.get('status'):
            return jsonify({'error': 'Application ID and status are required'}), 400
        
        if data['status'] not in ['applied', 'shortlisted', 'rejected']:
            return jsonify({'error': 'Invalid status'}), 400
        
        from flask import current_app
        db = current_app.config['db']
        
        # Update status
        result = Application.update_status(db, data['application_id'], data['status'])
        
        if result.modified_count == 0:
            return jsonify({'error': 'Application not found'}), 404
        
        return jsonify({'message': 'Application status updated successfully'}), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500