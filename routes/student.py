from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from models.database import Student, JobDrive, Application, Quiz, QuizResult
from utils.helpers import save_resume, validate_cgpa
from bson import ObjectId
from datetime import datetime

student_bp = Blueprint('student', __name__)

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

def require_student():
    """Decorator helper to check student role"""
    claims = get_jwt()
    if claims.get('role') != 'student':
        return jsonify({'error': 'Student access required'}), 403
    return None


@student_bp.route('/profile', methods=['GET', 'POST'])
@jwt_required()
def profile():
    """Get or update student profile"""
    # Check role
    check = require_student()
    if check:
        return check
    
    user_id = get_jwt_identity()
    from flask import current_app
    db = current_app.config['db']
    
    if request.method == 'GET':
        student = Student.get_by_user_id(db, user_id)
        if not student:
            return jsonify({'error': 'Profile not found'}), 404
        
        student['_id'] = str(student['_id'])
        student['user_id'] = str(student['user_id'])
        return jsonify(student), 200
    
    elif request.method == 'POST':
        try:
            data = request.get_json()
            
            # Validation
            if not data.get('name') or not data.get('roll_no') or not data.get('branch'):
                return jsonify({'error': 'Name, roll number, and branch are required'}), 400
            
            if not validate_cgpa(data.get('cgpa', 0)):
                return jsonify({'error': 'CGPA must be between 0 and 10'}), 400
            
            # Update profile
            Student.create_or_update(db, user_id, data)
            
            return jsonify({'message': 'Profile updated successfully'}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@student_bp.route('/upload-resume', methods=['POST'])
@jwt_required()
def upload_resume():
    """Upload resume"""
    check = require_student()
    if check:
        return check
    
    try:
        user_id = get_jwt_identity()
        
        if 'resume' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['resume']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        filepath = save_resume(file, user_id)
        
        if not filepath:
            return jsonify({'error': 'Invalid file type. Only PDF allowed'}), 400
        
        # Update student record
        from flask import current_app
        db = current_app.config['db']
        db.students.update_one(
            {'user_id': ObjectId(user_id)},
            {'$set': {'resume_url': filepath}}
        )
        
        return jsonify({
            'message': 'Resume uploaded successfully',
            'resume_url': filepath
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@student_bp.route('/jobs', methods=['GET'])
@jwt_required()
def get_eligible_jobs():
    """Get eligible job drives"""
    check = require_student()
    if check:
        return check
    
    try:
        user_id = get_jwt_identity()
        
        from flask import current_app
        db = current_app.config['db']
        
        # Get student profile
        student = Student.get_by_user_id(db, user_id)
        
        if not student:
            return jsonify({'error': 'Please complete your profile first'}), 400
        
        # Get eligible jobs
        jobs = JobDrive.get_eligible_jobs(db, student['cgpa'], student['branch'])
        
        # Add company details
        for job in jobs:
            company = db.companies.find_one({'_id': job['company_id']})
            if company:
                job['company_name'] = company.get('company_name', 'N/A')
        
        # Convert all ObjectId fields to strings
        jobs = convert_objectid_to_str(jobs)
        
        return jsonify(jobs), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@student_bp.route('/apply', methods=['POST'])
@jwt_required()
def apply_job():
    """Apply for a job"""
    check = require_student()
    if check:
        return check
    
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data.get('job_id'):
            return jsonify({'error': 'Job ID is required'}), 400
        
        from flask import current_app
        db = current_app.config['db']
        
        # Get student
        student = Student.get_by_user_id(db, user_id)
        
        if not student:
            return jsonify({'error': 'Please complete your profile first'}), 400
        
        if not student.get('resume_url'):
            return jsonify({'error': 'Please upload your resume first'}), 400
        
        # Create application
        app_id, error = Application.create(db, str(student['_id']), data['job_id'])
        
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({
            'message': 'Application submitted successfully',
            'application_id': str(app_id)
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@student_bp.route('/applications', methods=['GET'])
@jwt_required()
def get_applications():
    """Get student's applications"""
    check = require_student()
    if check:
        return check
    
    try:
        user_id = get_jwt_identity()
        
        from flask import current_app
        db = current_app.config['db']
        
        # Get student
        student = Student.get_by_user_id(db, user_id)
        
        if not student:
            return jsonify({'error': 'Profile not found'}), 404
        
        # Get applications
        applications = Application.get_by_student(db, str(student['_id']))

        # Enrich with quiz status
        for app in applications:
            quiz = db.quizzes.find_one({'job_id': ObjectId(app['job_id'])})
            app['quiz_required'] = bool(quiz)
            if quiz:
                quiz_result = db.quiz_results.find_one({
                    'quiz_id': quiz['_id'],
                    'student_id': ObjectId(student['_id'])
                })
                app['quiz_completed'] = bool(quiz_result)
            else:
                app['quiz_completed'] = False

        # Convert all ObjectId fields to strings
        applications = convert_objectid_to_str(applications)
        
        return jsonify(applications), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500  

@student_bp.route('/quiz/<job_id>', methods=['GET'])
@jwt_required()
def get_quiz(job_id):
    from flask import current_app
    db = current_app.config['db']
    quiz = Quiz.get_by_job(db, job_id)
    if not quiz:
        return jsonify({'error': 'No quiz found for this job'}), 404
    return jsonify(convert_objectid_to_str(quiz)), 200 #

@student_bp.route('/submit-quiz', methods=['POST'])
@jwt_required()
def submit_quiz():
    data = request.get_json()
    from flask import current_app
    db = current_app.config['db']
    
    # Simple server-side grading logic
    quiz = db.quizzes.find_one({'_id': ObjectId(data['quiz_id'])})
    if not quiz:
        return jsonify({'error': 'Quiz not found'}), 404

    score = 0
    for i, q in enumerate(quiz['questions']):
        if i < len(data.get('answers', [])) and data['answers'][i] == q['correct']:
            score += 1

    student = Student.get_by_user_id(db, get_jwt_identity())
    result_id = QuizResult.save_result(db, data['quiz_id'], student['_id'], score, len(quiz['questions']))

    # Mark application quiz completed
    db.applications.update_one(
        {'student_id': student['_id'], 'job_id': quiz['job_id']},
        {'$set': {'quiz_completed': True}}
    )

    return jsonify({'message': 'Quiz submitted', 'score': score, 'total': len(quiz['questions']), 'result_id': str(result_id)}), 200