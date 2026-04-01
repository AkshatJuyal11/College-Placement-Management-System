from datetime import datetime
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

class Quiz:
    """Quiz model for job screenings"""
    @staticmethod
    def create(db, job_id, company_id, data):
        quiz = {
            'job_id': ObjectId(job_id),
            'company_id': ObjectId(company_id),
            'title': data.get('title'),
            'questions': data.get('questions'), # Array of {question, options, correct}
            'duration': int(data.get('duration', 10)), # in minutes
            'created_at': datetime.utcnow()
        }
        return db.quizzes.insert_one(quiz).inserted_id

    @staticmethod
    def get_by_job(db, job_id):
        return db.quizzes.find_one({'job_id': ObjectId(job_id)})

class QuizResult:
    """Model to store student quiz performance"""
    @staticmethod
    def save_result(db, quiz_id, student_id, score, total):
        result = {
            'quiz_id': ObjectId(quiz_id),
            'student_id': ObjectId(student_id),
            'score': score,
            'total': total,
            'completed_at': datetime.utcnow()
        }
        return db.quiz_results.insert_one(result).inserted_id
class User:
    """User model for authentication"""
    
    @staticmethod
    def create(db, email, password, role):
        """Create a new user"""
        if db.users.find_one({'email': email}):
            return None, "Email already exists"
        
        user = {
            'email': email,
            'password': generate_password_hash(password),
            'role': role,
            'created_at': datetime.utcnow()
        }
        
        result = db.users.insert_one(user)
        return result.inserted_id, None
    
    @staticmethod
    def authenticate(db, email, password):
        """Authenticate user"""
        user = db.users.find_one({'email': email})
        
        if user and check_password_hash(user['password'], password):
            return user
        return None
    
    @staticmethod
    def get_by_id(db, user_id):
        """Get user by ID"""
        return db.users.find_one({'_id': ObjectId(user_id)})


class Student:
    """Student model"""
    
    @staticmethod
    def create_or_update(db, user_id, data):
        """Create or update student profile"""
        student_data = {
            'user_id': ObjectId(user_id),
            'name': data.get('name'),
            'roll_no': data.get('roll_no'),
            'branch': data.get('branch'),
            'cgpa': float(data.get('cgpa', 0)),
            'skills': data.get('skills', []),
            'resume_url': data.get('resume_url', ''),
            'placed': data.get('placed', False),
            'updated_at': datetime.utcnow()
        }
        
        result = db.students.update_one(
            {'user_id': ObjectId(user_id)},
            {'$set': student_data},
            upsert=True
        )
        return result
    
    @staticmethod
    def get_by_user_id(db, user_id):
        """Get student by user ID"""
        return db.students.find_one({'user_id': ObjectId(user_id)})
    
    @staticmethod
    def get_all(db):
        """Get all students"""
        return list(db.students.find())
    
    @staticmethod
    def update_placement_status(db, student_id, placed):
        """Update placement status"""
        return db.students.update_one(
            {'_id': ObjectId(student_id)},
            {'$set': {'placed': placed}}
        )


class Company:
    """Company model"""
    
    @staticmethod
    def create_or_update(db, user_id, data):
        """Create or update company profile"""
        company_data = {
            'user_id': ObjectId(user_id),
            'company_name': data.get('company_name'),
            'contact_person': data.get('contact_person'),
            'email': data.get('email'),
            'phone': data.get('phone'),
            'updated_at': datetime.utcnow()
        }
        
        result = db.companies.update_one(
            {'user_id': ObjectId(user_id)},
            {'$set': company_data},
            upsert=True
        )
        return result
    
    @staticmethod
    def get_by_user_id(db, user_id):
        """Get company by user ID"""
        return db.companies.find_one({'user_id': ObjectId(user_id)})
    
    @staticmethod
    def get_all(db):
        """Get all companies"""
        return list(db.companies.find())


class JobDrive:
    """Job Drive model"""
    
    @staticmethod
    def create(db, company_id, data):
        """Create a new job drive"""
        job = {
            'company_id': ObjectId(company_id),
            'job_title': data.get('job_title'),
            'job_description': data.get('job_description'),
            'criteria': {
                'min_cgpa': float(data.get('min_cgpa', 0)),
                'branches': data.get('branches', [])
            },
            'salary': data.get('salary'),
            'deadline': datetime.fromisoformat(data.get('deadline')) if data.get('deadline') else None,
            'posted_at': datetime.utcnow(),
            'active': True
        }
        
        result = db.job_drives.insert_one(job)
        return result.inserted_id
    
    @staticmethod
    def get_eligible_jobs(db, student_cgpa, student_branch):
        """Get jobs eligible for a student"""
        jobs = db.job_drives.find({
            'active': True,
            'criteria.min_cgpa': {'$lte': student_cgpa},
            'criteria.branches': student_branch
        })
        return list(jobs)
    
    @staticmethod
    def get_by_company(db, company_id):
        """Get jobs posted by a company"""
        return list(db.job_drives.find({'company_id': ObjectId(company_id)}))
    
    @staticmethod
    def get_all(db):
        """Get all job drives"""
        return list(db.job_drives.find())
    
    @staticmethod
    def get_by_id(db, job_id):
        """Get job by ID"""
        return db.job_drives.find_one({'_id': ObjectId(job_id)})


class Application:
    """Application model"""
    
    @staticmethod
    def create(db, student_id, job_id):
        """Create a new application"""
        # Check if already applied
        existing = db.applications.find_one({
            'student_id': ObjectId(student_id),
            'job_id': ObjectId(job_id)
        })
        
        if existing:
            return None, "Already applied to this job"
        
        # Check if job has a quiz
        quiz = db.quizzes.find_one({'job_id': ObjectId(job_id)})
        quiz_required = quiz is not None
        
        application = {
            'student_id': ObjectId(student_id),
            'job_id': ObjectId(job_id),
            'status': 'applied',
            'quiz_required': quiz_required,
            'quiz_completed': False,
            'applied_at': datetime.utcnow()
        }
        
        result = db.applications.insert_one(application)
        return result.inserted_id, None
    
    @staticmethod
    def get_by_student(db, student_id):
        """Get applications by student"""
        pipeline = [
            {'$match': {'student_id': ObjectId(student_id)}},
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
            {'$unwind': '$company'}
        ]
        return list(db.applications.aggregate(pipeline))
    
    @staticmethod
    def get_by_job(db, job_id):
        """Get applicants for a job"""
        pipeline = [
            {'$match': {'job_id': ObjectId(job_id)}},
            {'$lookup': {
                'from': 'students',
                'localField': 'student_id',
                'foreignField': '_id',
                'as': 'student'
            }},
            {'$unwind': '$student'}
        ]
        return list(db.applications.aggregate(pipeline))
    
    @staticmethod
    def update_status(db, application_id, status):
        """Update application status"""
        result = db.applications.update_one(
            {'_id': ObjectId(application_id)},
            {'$set': {'status': status, 'updated_at': datetime.utcnow()}}
        )
        return result
    
    @staticmethod
    def get_all(db):
        """Get all applications"""
        return list(db.applications.find())
