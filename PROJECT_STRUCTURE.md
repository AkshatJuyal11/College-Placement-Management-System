# CPMS Project Structure

Complete file and folder organization for the College Placement Management System.

## 📁 Directory Structure

```
cpms/
│
├── app.py                          # Main Flask application entry point
├── config.py                       # Application configuration
├── requirements.txt                # Python dependencies
├── .env                           # Environment variables (SECRET KEYS)
│
├── README.md                       # Project documentation
├── QUICKSTART.md                   # Quick setup guide
├── API_TESTING.md                  # API testing documentation
├── VIVA_GUIDE.md                   # Viva preparation questions & answers
│
├── models/                         # Database models
│   └── database.py                # MongoDB models (User, Student, Company, JobDrive, Application)
│
├── routes/                         # API route blueprints
│   ├── auth.py                    # Authentication routes (/api/auth/*)
│   ├── student.py                 # Student routes (/api/student/*)
│   ├── company.py                 # Company routes (/api/company/*)
│   └── admin.py                   # Admin routes (/api/admin/*)
│
├── utils/                          # Utility functions
│   └── helpers.py                 # Helper functions (file upload, validation)
│
├── templates/                      # HTML templates
│   ├── index.html                 # Landing page
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   ├── student_dashboard.html     # Student dashboard
│   ├── company_dashboard.html     # Company dashboard
│   └── admin_dashboard.html       # Admin dashboard
│
└── static/                         # Static files
    ├── css/
    │   └── style.css              # Custom CSS styles
    ├── js/
    │   └── main.js                # JavaScript utilities
    └── uploads/                    # Resume upload directory
```

## 📄 File Descriptions

### Core Application Files

**app.py** (Main Application)
- Flask app initialization
- Database connection setup
- JWT configuration
- Blueprint registration
- Route definitions for frontend pages
- Error handlers

**config.py** (Configuration)
- Environment variable loading
- Application settings
- JWT settings
- File upload configuration
- Database URI

**requirements.txt** (Dependencies)
- Flask 3.0.0
- Flask-PyMongo 2.3.0
- Flask-JWT-Extended 4.6.0
- PyMongo 4.6.1
- Werkzeug 3.0.1
- Python-dotenv 1.0.0

**.env** (Environment Variables)
- MONGO_URI
- SECRET_KEY
- JWT_SECRET_KEY
- UPLOAD_FOLDER
- MAX_FILE_SIZE

### Models Layer

**models/database.py**
- `User` class: Authentication and user management
- `Student` class: Student profile operations
- `Company` class: Company profile operations
- `JobDrive` class: Job posting management
- `Application` class: Application tracking
- All CRUD operations for each entity

### Routes Layer (API Endpoints)

**routes/auth.py**
- POST `/api/auth/register` - User registration
- POST `/api/auth/login` - User login
- GET `/api/auth/me` - Get current user info

**routes/student.py**
- GET/POST `/api/student/profile` - Profile management
- POST `/api/student/upload-resume` - Resume upload
- GET `/api/student/jobs` - Get eligible jobs
- POST `/api/student/apply` - Apply for job
- GET `/api/student/applications` - Get applications

**routes/company.py**
- GET/POST `/api/company/profile` - Profile management
- POST `/api/company/job` - Create job drive
- GET `/api/company/jobs` - Get posted jobs
- GET `/api/company/applicants/<job_id>` - Get applicants
- POST `/api/company/update-status` - Update application status

**routes/admin.py**
- GET `/api/admin/students` - Get all students
- GET `/api/admin/companies` - Get all companies
- GET `/api/admin/jobs` - Get all jobs
- GET `/api/admin/applications` - Get all applications
- GET `/api/admin/reports` - Get analytics & reports

### Utilities

**utils/helpers.py**
- `allowed_file()` - File extension validation
- `save_resume()` - Resume file handling
- `validate_email()` - Email format validation
- `validate_cgpa()` - CGPA range validation

### Frontend Templates

**templates/index.html** - Landing Page
- Hero section
- Features showcase
- How it works
- About section
- Responsive navbar

**templates/login.html** - Login Page
- Email/password form
- Role-based redirection
- Error handling
- Form validation

**templates/register.html** - Registration Page
- User registration form
- Role selection
- Password confirmation
- Input validation

**templates/student_dashboard.html** - Student Dashboard
- Profile management tab
- Resume upload tab
- Available jobs tab
- My applications tab
- Real-time status updates

**templates/company_dashboard.html** - Company Dashboard
- Company profile tab
- Post job tab
- My jobs tab
- Applicant management modal
- Status update functionality

**templates/admin_dashboard.html** - Admin Dashboard
- Overview with stats cards
- All students table
- All companies table
- All jobs table
- Reports with charts
- Analytics visualizations

### Static Assets

**static/css/style.css**
- Modern design system
- Custom color palette
- Typography styles
- Component styles (cards, buttons, forms, tables)
- Responsive grid layouts
- Animations and transitions
- Dashboard layouts
- Utility classes

**static/js/main.js**
- API client functions
- Token management
- Authentication helpers
- Form validation utilities
- Toast notifications
- Date formatting
- Loading indicators

## 🗄️ Database Collections

### users
```javascript
{
  _id: ObjectId,
  email: String,
  password: String (hashed),
  role: String,
  created_at: Date
}
```

### students
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  name: String,
  roll_no: String,
  branch: String,
  cgpa: Number,
  skills: [String],
  resume_url: String,
  placed: Boolean
}
```

### companies
```javascript
{
  _id: ObjectId,
  user_id: ObjectId,
  company_name: String,
  contact_person: String,
  email: String,
  phone: String
}
```

### job_drives
```javascript
{
  _id: ObjectId,
  company_id: ObjectId,
  job_title: String,
  job_description: String,
  criteria: {
    min_cgpa: Number,
    branches: [String]
  },
  salary: String,
  deadline: Date,
  posted_at: Date,
  active: Boolean
}
```

### applications
```javascript
{
  _id: ObjectId,
  student_id: ObjectId,
  job_id: ObjectId,
  status: String,
  applied_at: Date
}
```

## 🔄 Request Flow

### Student Applies for Job

```
1. Frontend (student_dashboard.html)
   ↓
2. JavaScript (main.js) - API.post('/student/apply', {job_id})
   ↓
3. Flask Route (routes/student.py) - @jwt_required
   ↓
4. Model (models/database.py) - Application.create()
   ↓
5. MongoDB (applications collection)
   ↓
6. Response back to frontend
   ↓
7. UI update with status
```

### Company Posts Job

```
1. Frontend (company_dashboard.html)
   ↓
2. JavaScript - API.post('/company/job', data)
   ↓
3. Flask Route (routes/company.py) - @jwt_required
   ↓
4. Model - JobDrive.create()
   ↓
5. MongoDB (job_drives collection)
   ↓
6. Response confirmation
```

## 🎯 Feature Implementation Mapping

| Feature | Frontend | Backend Route | Model | Database |
|---------|----------|---------------|-------|----------|
| User Registration | register.html | auth.py | User | users |
| User Login | login.html | auth.py | User | users |
| Student Profile | student_dashboard.html | student.py | Student | students |
| Resume Upload | student_dashboard.html | student.py | Student | students |
| Job Browsing | student_dashboard.html | student.py | JobDrive | job_drives |
| Job Application | student_dashboard.html | student.py | Application | applications |
| Job Posting | company_dashboard.html | company.py | JobDrive | job_drives |
| Applicant Review | company_dashboard.html | company.py | Application | applications |
| Analytics | admin_dashboard.html | admin.py | Multiple | Multiple |

## 🔐 Security Implementation

| Layer | Implementation |
|-------|----------------|
| Authentication | JWT tokens with user_id and role |
| Password | Werkzeug hashing (pbkdf2:sha256) |
| Authorization | Role-based access control in routes |
| Input Validation | Email, CGPA, file type checks |
| File Upload | Extension check, size limit, secure filename |
| API Protection | @jwt_required decorator on all protected routes |

## 📊 Code Statistics

- **Total Lines of Code**: ~3000+
- **Python Files**: 7
- **HTML Templates**: 6
- **CSS Lines**: ~600
- **JavaScript Lines**: ~300
- **API Endpoints**: 20+
- **Database Collections**: 5
- **Routes/Blueprints**: 4

## 🚀 Deployment Structure

For production deployment:

```
cpms/
├── app.py
├── config.py
├── requirements.txt
├── Procfile                  # For Heroku
├── runtime.txt              # Python version
├── .gitignore              # Git ignore file
├── models/
├── routes/
├── utils/
├── templates/
└── static/
```

## 📝 Documentation Files

- **README.md**: Complete project documentation
- **QUICKSTART.md**: Fast setup guide
- **API_TESTING.md**: API testing with Postman
- **VIVA_GUIDE.md**: Viva questions and answers
- **PROJECT_STRUCTURE.md**: This file

---

This structure follows MVC architecture principles and Flask best practices for maintainability and scalability.
