from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.database import Student, Company, JobDrive, Application, Quiz, QuizResult
from bson import ObjectId
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

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

def require_admin():
    """Decorator helper to check admin role"""
    claims = get_jwt()
    if claims.get('role') != 'admin':
        return jsonify({'error': 'Admin access required'}), 403
    return None


@admin_bp.route('/students', methods=['GET'])
@jwt_required()
def get_students():
    """Get all students"""
    check = require_admin()
    if check:
        return check
    
    try:
        from flask import current_app
        db = current_app.config['db']
        
        students = Student.get_all(db)
        students = convert_objectid_to_str(students)
        
        return jsonify(students), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/companies', methods=['GET'])
@jwt_required()
def get_companies():
    """Get all companies"""
    check = require_admin()
    if check:
        return check
    
    try:
        from flask import current_app
        db = current_app.config['db']
        
        companies = Company.get_all(db)
        companies = convert_objectid_to_str(companies)
        
        return jsonify(companies), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/jobs', methods=['GET'])
@jwt_required()
def get_all_jobs():
    """Get all job drives"""
    check = require_admin()
    if check:
        return check
    
    try:
        from flask import current_app
        db = current_app.config['db']
        
        jobs = JobDrive.get_all(db)
        
        # Add company details
        for job in jobs:
            company = db.companies.find_one({'_id': ObjectId(job['company_id'])})
            if company:
                job['company_name'] = company.get('company_name', 'N/A')
        
        jobs = convert_objectid_to_str(jobs)
        
        return jsonify(jobs), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/applications', methods=['GET'])
@jwt_required()
def get_all_applications():
    """Get all applications"""
    check = require_admin()
    if check:
        return check
    
    try:
        from flask import current_app
        db = current_app.config['db']
        
        applications = Application.get_all(db)
        applications = convert_objectid_to_str(applications)
        
        return jsonify(applications), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/reports', methods=['GET'])
@jwt_required()
def get_reports():
    """Get placement reports and statistics"""
    check = require_admin()
    if check:
        return check
    
    try:
        from flask import current_app
        db = current_app.config['db']
        
        # Total students
        total_students = db.students.count_documents({})
        
        # Placed students
        placed_students = db.students.count_documents({'placed': True})
        
        # Total companies
        total_companies = db.companies.count_documents({})
        
        # Total job drives
        total_jobs = db.job_drives.count_documents({})
        
        # Total applications
        total_applications = db.applications.count_documents({})
        
        # Applications by status
        status_pipeline = [
            {'$group': {
                '_id': '$status',
                'count': {'$sum': 1}
            }}
        ]
        applications_by_status = list(db.applications.aggregate(status_pipeline))
        
        # Company-wise selections (shortlisted students)
        company_pipeline = [
            {'$match': {'status': 'shortlisted'}},
            {'$lookup': {
                'from': 'job_drives',
                'localField': 'job_id',
                'foreignField': '_id',
                'as': 'job'
            }},
            {'$unwind': '$job'},
            {'$lookup': {
                'from': 'companies',
                'localField': 'job.company_id',
                'foreignField': '_id',
                'as': 'company'
            }},
            {'$unwind': '$company'},
            {'$group': {
                '_id': '$company.company_name',
                'count': {'$sum': 1}
            }},
            {'$sort': {'count': -1}}
        ]
        company_selections = list(db.applications.aggregate(company_pipeline))
        
        # Branch-wise placement
        branch_pipeline = [
            {'$group': {
                '_id': '$branch',
                'total': {'$sum': 1},
                'placed': {
                    '$sum': {'$cond': [{'$eq': ['$placed', True]}, 1, 0]}
                }
            }},
            {'$sort': {'_id': 1}}
        ]
        branch_stats = list(db.students.aggregate(branch_pipeline))
        
        report = {
            'overview': {
                'total_students': total_students,
                'placed_students': placed_students,
                'placement_percentage': round((placed_students / total_students * 100), 2) if total_students > 0 else 0,
                'total_companies': total_companies,
                'total_jobs': total_jobs,
                'total_applications': total_applications
            },
            'applications_by_status': applications_by_status,
            'company_wise_selections': company_selections,
            'branch_wise_stats': branch_stats
        }
        
        # Convert all ObjectIds to strings
        report = convert_objectid_to_str(report)
        
        return jsonify(report), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/quiz-results', methods=['GET'])
@jwt_required()
def get_all_quiz_results():
    """Get all quiz results for admin"""
    check = require_admin()
    if check:
        return check
    
    try:
        from flask import current_app
        db = current_app.config['db']
        
        # Aggregate quiz results with student and job details
        pipeline = [
            {'$lookup': {
                'from': 'quizzes',
                'localField': 'quiz_id',
                'foreignField': '_id',
                'as': 'quiz'
            }},
            {'$unwind': '$quiz'},
            {'$lookup': {
                'from': 'job_drives',
                'localField': 'quiz.job_id',
                'foreignField': '_id',
                'as': 'job'
            }},
            {'$unwind': '$job'},
            {'$lookup': {
                'from': 'companies',
                'localField': 'job.company_id',
                'foreignField': '_id',
                'as': 'company'
            }},
            {'$unwind': '$company'},
            {'$lookup': {
                'from': 'students',
                'localField': 'student_id',
                'foreignField': '_id',
                'as': 'student'
            }},
            {'$unwind': '$student'},
            {'$sort': {'completed_at': -1}}
        ]
        
        results = list(db.quiz_results.aggregate(pipeline))
        results = convert_objectid_to_str(results)
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@admin_bp.route('/student-placement', methods=['POST'])
@jwt_required()
def admin_set_student_placed():
    check = require_admin()
    if check:
        return check

    try:
        data = request.get_json()
        if not data.get('student_id') or 'placed' not in data:
            return jsonify({'error': 'student_id and placed are required'}), 400

        from flask import current_app
        db = current_app.config['db']

        Student.update_placement_status(db, data['student_id'], bool(data['placed']))

        return jsonify({'message': 'Student placed status updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500