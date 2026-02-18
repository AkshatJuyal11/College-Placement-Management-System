# 🎓 College Placement Management System (CPMS)

A comprehensive full-stack web application for managing college placement activities, built with Flask, MongoDB, and Bootstrap.

## 📋 Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [System Architecture](#system-architecture)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Documentation](#api-documentation)
- [Database Schema](#database-schema)
- [Team Members](#team-members)
- [Screenshots](#screenshots)

## ✨ Features

### For Students
- Create and manage profile with academic details
- Upload resume (PDF format)
- Browse eligible job opportunities based on CGPA and branch
- Apply for jobs with one click
- Track application status in real-time
- View placement history

### For Companies
- Create company profile
- Post job drives with eligibility criteria
- Set minimum CGPA and branch requirements
- View all applicants for each job
- Shortlist or reject candidates
- Manage multiple job postings

### For Administrators (TPO)
- Monitor all students and companies
- View all job drives and applications
- Generate comprehensive placement reports
- Analytics dashboard with charts
- Track placement statistics by branch
- Company-wise selection reports

## 🛠️ Technology Stack

### Frontend
- HTML5, CSS3, JavaScript (ES6)
- Bootstrap 5.3.0
- Chart.js (for analytics)
- Google Fonts (Poppins, Inter)

### Backend
- Python 3.8+
- Flask 3.0.0
- Flask-PyMongo 2.3.0
- Flask-JWT-Extended 4.6.0
- Werkzeug (password hashing)

### Database
- MongoDB 4.0+
- PyMongo driver

### Development Tools
- VS Code
- Postman (API testing)
- Git/GitHub

## 🏗️ System Architecture

```
┌─────────────────┐
│   Web Browser   │
│  (Client Side)  │
└────────┬────────┘
         │
         │ HTTP/HTTPS
         │
┌────────┴────────┐
│  Flask Server   │
│   (Backend)     │
│                 │
│  - Routes       │
│  - Auth (JWT)   │
│  - Business     │
│    Logic        │
└────────┬────────┘
         │
         │ PyMongo
         │
┌────────┴────────┐
│    MongoDB      │
│   (Database)    │
│                 │
│  - users        │
│  - students     │
│  - companies    │
│  - job_drives   │
│  - applications │
└─────────────────┘
```

## 💻 Installation

### Prerequisites
- Python 3.8 or higher
- MongoDB 4.0 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/cpms.git
cd cpms
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Install and Start MongoDB

#### Windows
1. Download MongoDB Community Server from [mongodb.com](https://www.mongodb.com/try/download/community)
2. Install and start MongoDB service
3. MongoDB will run on `mongodb://localhost:27017` by default

#### macOS (using Homebrew)
```bash
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get install -y mongodb
sudo systemctl start mongodb
sudo systemctl enable mongodb
```

### Step 5: Configure Environment Variables

Edit the `.env` file in the project root:

```env
MONGO_URI=mongodb://localhost:27017/cpms
SECRET_KEY=your-secret-key-change-this-in-production
JWT_SECRET_KEY=your-jwt-secret-key-change-this
UPLOAD_FOLDER=static/uploads
MAX_FILE_SIZE=5242880
```

### Step 6: Run the Application

```bash
python app.py
```

The application will start on `http://localhost:5000`

## 🔧 Configuration

### Database Configuration

The database name is `cpms` by default. To change it, modify the `MONGO_URI` in `.env`:

```env
MONGO_URI=mongodb://localhost:27017/your_database_name
```

### File Upload Configuration

Configure upload settings in `.env`:

```env
UPLOAD_FOLDER=static/uploads    # Upload directory
MAX_FILE_SIZE=5242880           # 5MB in bytes
```

### JWT Configuration

JWT tokens are used for authentication. Configure token settings in `config.py`:

```python
JWT_TOKEN_LOCATION = ['headers']
JWT_HEADER_NAME = 'Authorization'
JWT_HEADER_TYPE = 'Bearer'
```

## 📖 Usage

### For Students

1. **Register**: Go to `/register` and create account with role "Student"
2. **Login**: Login at `/login`
3. **Complete Profile**: Fill in academic details, CGPA, branch, skills
4. **Upload Resume**: Upload your resume in PDF format
5. **Browse Jobs**: View eligible job opportunities
6. **Apply**: Click "Apply Now" for desired positions
7. **Track Status**: Monitor application status in "My Applications" tab

### For Companies

1. **Register**: Create account with role "Company"
2. **Login**: Access company dashboard
3. **Setup Profile**: Add company details and contact information
4. **Post Job**: Create job drive with eligibility criteria
5. **Review Applicants**: View all applications for your jobs
6. **Shortlist/Reject**: Update candidate status

### For Admin (TPO)

1. **Register**: Create account with role "Admin"
2. **Login**: Access admin dashboard
3. **Monitor**: View all students, companies, and job drives
4. **Analytics**: Check placement statistics and charts
5. **Reports**: Generate comprehensive placement reports

## 🔌 API Documentation

### Authentication APIs

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123",
  "role": "student"
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "password123"
}

Response:
{
  "token": "JWT_TOKEN",
  "role": "student",
  "user_id": "..."
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer {JWT_TOKEN}
```

### Student APIs

#### Create/Update Profile
```http
POST /api/student/profile
Authorization: Bearer {JWT_TOKEN}
Content-Type: application/json

{
  "name": "John Doe",
  "roll_no": "CSE101",
  "branch": "CSE",
  "cgpa": 8.5,
  "skills": ["Python", "Java", "React"]
}
```

#### Upload Resume
```http
POST /api/student/upload-resume
Authorization: Bearer {JWT_TOKEN}
Content-Type: multipart/form-data

resume: [PDF_FILE]
```

#### Get Eligible Jobs
```http
GET /api/student/jobs
Authorization: Bearer {JWT_TOKEN}
```

#### Apply for Job
```http
POST /api/student/apply
Authorization: Bearer {JWT_TOKEN}
Content-Type: application/json

{
  "job_id": "..."
}
```

#### Get My Applications
```http
GET /api/student/applications
Authorization: Bearer {JWT_TOKEN}
```

### Company APIs

#### Create/Update Profile
```http
POST /api/company/profile
Authorization: Bearer {JWT_TOKEN}
Content-Type: application/json

{
  "company_name": "Google",
  "contact_person": "Jane Smith",
  "email": "contact@google.com",
  "phone": "1234567890"
}
```

#### Create Job Drive
```http
POST /api/company/job
Authorization: Bearer {JWT_TOKEN}
Content-Type: application/json

{
  "job_title": "Software Engineer",
  "job_description": "Backend developer role",
  "min_cgpa": 7.5,
  "branches": ["CSE", "IT"],
  "salary": "10-12 LPA",
  "deadline": "2024-12-31T23:59:59"
}
```

#### Get Posted Jobs
```http
GET /api/company/jobs
Authorization: Bearer {JWT_TOKEN}
```

#### Get Applicants for Job
```http
GET /api/company/applicants/{job_id}
Authorization: Bearer {JWT_TOKEN}
```

#### Update Application Status
```http
POST /api/company/update-status
Authorization: Bearer {JWT_TOKEN}
Content-Type: application/json

{
  "application_id": "...",
  "status": "shortlisted"
}
```

### Admin APIs

#### Get All Students
```http
GET /api/admin/students
Authorization: Bearer {JWT_TOKEN}
```

#### Get All Companies
```http
GET /api/admin/companies
Authorization: Bearer {JWT_TOKEN}
```

#### Get All Jobs
```http
GET /api/admin/jobs
Authorization: Bearer {JWT_TOKEN}
```

#### Get Reports
```http
GET /api/admin/reports
Authorization: Bearer {JWT_TOKEN}

Response includes:
- Overview statistics
- Applications by status
- Company-wise selections
- Branch-wise placement stats
```

## 💾 Database Schema

### users Collection
```javascript
{
  _id: ObjectId,
  email: String,
  password: String (hashed),
  role: String (student|company|admin),
  created_at: Date
}
```

### students Collection
```javascript
{
  _id: ObjectId,
  user_id: ObjectId (ref: users),
  name: String,
  roll_no: String,
  branch: String,
  cgpa: Number,
  skills: [String],
  resume_url: String,
  placed: Boolean
}
```

### companies Collection
```javascript
{
  _id: ObjectId,
  user_id: ObjectId (ref: users),
  company_name: String,
  contact_person: String,
  email: String,
  phone: String
}
```

### job_drives Collection
```javascript
{
  _id: ObjectId,
  company_id: ObjectId (ref: companies),
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

### applications Collection
```javascript
{
  _id: ObjectId,
  student_id: ObjectId (ref: students),
  job_id: ObjectId (ref: job_drives),
  status: String (applied|shortlisted|rejected),
  applied_at: Date
}
```

## 👥 Team Members

| Name | Roll Number | Responsibility |
|------|-------------|----------------|
| Member 1 | CSE001 | Frontend Development & UI/UX |
| Member 2 | CSE002 | Backend APIs & Flask Development |
| Member 3 | CSE003 | Database Design & MongoDB |
| Member 4 | CSE004 | Testing & Documentation |

## 📸 Screenshots

*Add screenshots of your application here*

## 🚀 Future Enhancements

- Email notifications for application status updates
- AI-based resume screening
- Interview scheduling system
- Video interview integration
- Mobile application
- Advanced analytics with ML predictions
- Export reports to PDF/Excel
- Real-time chat between students and companies
- Multi-college support
- Alumni network integration

## 📝 License

This project is created for academic purposes as part of the 6th Semester Full Stack Web Development course.

## 🤝 Contributing

This is an academic project. For suggestions or improvements, please contact the team members.

## 📞 Support

For any queries or issues, please contact:
- Email: support@cpms.edu
- GitHub Issues: [Create an issue](https://github.com/your-username/cpms/issues)

---

**Note**: This project is built for educational purposes and demonstrates full-stack web development skills using Flask and MongoDB.
