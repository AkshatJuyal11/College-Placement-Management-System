# CPMS API Testing Guide

This guide provides step-by-step instructions for testing the CPMS APIs using Postman.

## Prerequisites

1. Install Postman from [postman.com](https://www.postman.com/downloads/)
2. Ensure the Flask application is running on `http://localhost:5000`
3. Ensure MongoDB is running

## API Base URL

```
http://localhost:5000/api
```

## Testing Flow

### 1. Register Users

#### Register a Student
```
POST http://localhost:5000/api/auth/register

Headers:
Content-Type: application/json

Body (JSON):
{
    "email": "student@college.edu",
    "password": "student123",
    "role": "student"
}

Expected Response (201):
{
    "message": "User registered successfully",
    "user_id": "..."
}
```

#### Register a Company
```
POST http://localhost:5000/api/auth/register

Body (JSON):
{
    "email": "hr@google.com",
    "password": "company123",
    "role": "company"
}
```

#### Register an Admin
```
POST http://localhost:5000/api/auth/register

Body (JSON):
{
    "email": "admin@college.edu",
    "password": "admin123",
    "role": "admin"
}
```

### 2. Login and Get JWT Token

#### Student Login
```
POST http://localhost:5000/api/auth/login

Headers:
Content-Type: application/json

Body (JSON):
{
    "email": "student@college.edu",
    "password": "student123"
}

Expected Response (200):
{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "role": "student",
    "user_id": "..."
}
```

**Important**: Copy the `token` value. You'll need it for authenticated requests.

### 3. Student APIs (Use Student Token)

#### Get/Update Student Profile
```
POST http://localhost:5000/api/student/profile

Headers:
Content-Type: application/json
Authorization: Bearer {STUDENT_TOKEN}

Body (JSON):
{
    "name": "John Doe",
    "roll_no": "CSE101",
    "branch": "CSE",
    "cgpa": 8.5,
    "skills": ["Python", "Java", "MongoDB"]
}

Expected Response (200):
{
    "message": "Profile updated successfully"
}
```

#### Upload Resume
```
POST http://localhost:5000/api/student/upload-resume

Headers:
Authorization: Bearer {STUDENT_TOKEN}

Body (form-data):
resume: [Select PDF file]

Expected Response (200):
{
    "message": "Resume uploaded successfully",
    "resume_url": "static/uploads/..."
}
```

#### Get Eligible Jobs
```
GET http://localhost:5000/api/student/jobs

Headers:
Authorization: Bearer {STUDENT_TOKEN}

Expected Response (200):
[
    {
        "_id": "...",
        "job_title": "Software Engineer",
        "company_name": "Google",
        "criteria": {
            "min_cgpa": 7.5,
            "branches": ["CSE", "IT"]
        },
        ...
    }
]
```

#### Apply for Job
```
POST http://localhost:5000/api/student/apply

Headers:
Content-Type: application/json
Authorization: Bearer {STUDENT_TOKEN}

Body (JSON):
{
    "job_id": "{JOB_ID}"
}

Expected Response (201):
{
    "message": "Application submitted successfully",
    "application_id": "..."
}
```

#### Get My Applications
```
GET http://localhost:5000/api/student/applications

Headers:
Authorization: Bearer {STUDENT_TOKEN}

Expected Response (200):
[
    {
        "job": {
            "job_title": "Software Engineer"
        },
        "company": {
            "company_name": "Google"
        },
        "status": "applied",
        "applied_at": "2024-01-15T10:30:00"
    }
]
```

### 4. Company APIs (Use Company Token)

#### Update Company Profile
```
POST http://localhost:5000/api/company/profile

Headers:
Content-Type: application/json
Authorization: Bearer {COMPANY_TOKEN}

Body (JSON):
{
    "company_name": "Google India",
    "contact_person": "Jane Smith",
    "email": "hr@google.com",
    "phone": "9876543210"
}

Expected Response (200):
{
    "message": "Profile updated successfully"
}
```

#### Create Job Drive
```
POST http://localhost:5000/api/company/job

Headers:
Content-Type: application/json
Authorization: Bearer {COMPANY_TOKEN}

Body (JSON):
{
    "job_title": "Software Engineer",
    "job_description": "Backend developer role for cloud infrastructure",
    "min_cgpa": 7.5,
    "branches": ["CSE", "IT"],
    "salary": "10-12 LPA",
    "deadline": "2024-12-31T23:59:59"
}

Expected Response (201):
{
    "message": "Job drive created successfully",
    "job_id": "..."
}
```

#### Get Posted Jobs
```
GET http://localhost:5000/api/company/jobs

Headers:
Authorization: Bearer {COMPANY_TOKEN}

Expected Response (200):
[
    {
        "_id": "...",
        "job_title": "Software Engineer",
        "criteria": {
            "min_cgpa": 7.5,
            "branches": ["CSE", "IT"]
        },
        "posted_at": "2024-01-15T10:00:00"
    }
]
```

#### Get Applicants for a Job
```
GET http://localhost:5000/api/company/applicants/{JOB_ID}

Headers:
Authorization: Bearer {COMPANY_TOKEN}

Expected Response (200):
[
    {
        "student": {
            "name": "John Doe",
            "roll_no": "CSE101",
            "branch": "CSE",
            "cgpa": 8.5
        },
        "status": "applied",
        "applied_at": "2024-01-15T11:00:00"
    }
]
```

#### Update Application Status
```
POST http://localhost:5000/api/company/update-status

Headers:
Content-Type: application/json
Authorization: Bearer {COMPANY_TOKEN}

Body (JSON):
{
    "application_id": "{APPLICATION_ID}",
    "status": "shortlisted"
}

Status options: "applied", "shortlisted", "rejected"

Expected Response (200):
{
    "message": "Application status updated successfully"
}
```

### 5. Admin APIs (Use Admin Token)

#### Get All Students
```
GET http://localhost:5000/api/admin/students

Headers:
Authorization: Bearer {ADMIN_TOKEN}

Expected Response (200):
[
    {
        "name": "John Doe",
        "roll_no": "CSE101",
        "branch": "CSE",
        "cgpa": 8.5,
        "placed": false
    }
]
```

#### Get All Companies
```
GET http://localhost:5000/api/admin/companies

Headers:
Authorization: Bearer {ADMIN_TOKEN}

Expected Response (200):
[
    {
        "company_name": "Google",
        "contact_person": "Jane Smith",
        "email": "hr@google.com"
    }
]
```

#### Get All Jobs
```
GET http://localhost:5000/api/admin/jobs

Headers:
Authorization: Bearer {ADMIN_TOKEN}

Expected Response (200):
[
    {
        "company_name": "Google",
        "job_title": "Software Engineer",
        "criteria": {
            "min_cgpa": 7.5,
            "branches": ["CSE", "IT"]
        }
    }
]
```

#### Get Placement Reports
```
GET http://localhost:5000/api/admin/reports

Headers:
Authorization: Bearer {ADMIN_TOKEN}

Expected Response (200):
{
    "overview": {
        "total_students": 100,
        "placed_students": 75,
        "placement_percentage": 75.0,
        "total_companies": 20,
        "total_jobs": 30,
        "total_applications": 250
    },
    "applications_by_status": [...],
    "company_wise_selections": [...],
    "branch_wise_stats": [...]
}
```

## Common Error Responses

### 400 Bad Request
```json
{
    "error": "Validation error message"
}
```

### 401 Unauthorized
```json
{
    "error": "Invalid credentials"
}
```

### 403 Forbidden
```json
{
    "error": "Student access required"
}
```

### 404 Not Found
```json
{
    "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
    "error": "Internal server error"
}
```

## Postman Collection

You can import this collection into Postman for easier testing:

1. Create a new Collection named "CPMS API"
2. Add an Environment variable `base_url` = `http://localhost:5000/api`
3. Add Environment variables for tokens:
   - `student_token`
   - `company_token`
   - `admin_token`
4. Create folders for each role (Auth, Student, Company, Admin)
5. Add requests as documented above

## Testing Tips

1. **Always login first** to get the JWT token
2. **Use environment variables** in Postman to store tokens
3. **Test in sequence**: Register → Login → Create Profile → Post Job → Apply → Review
4. **Check MongoDB** using MongoDB Compass to verify data
5. **Clear database** between test runs if needed
6. **Use different emails** for different test users

## MongoDB Verification

After API calls, verify data in MongoDB:

```bash
# Connect to MongoDB
mongo

# Use CPMS database
use cpms

# View collections
show collections

# View users
db.users.find().pretty()

# View students
db.students.find().pretty()

# View companies
db.companies.find().pretty()

# View jobs
db.job_drives.find().pretty()

# View applications
db.applications.find().pretty()
```

## Troubleshooting

### Token Expired
- Login again to get a new token

### "Profile not found"
- Create profile first using POST /student/profile or /company/profile

### "Please complete your profile first"
- Student must have profile before applying
- Company must have profile before posting jobs

### "Already applied to this job"
- Cannot apply to the same job twice

### Upload fails
- Check file is PDF format
- Check file size is under 5MB

---

For more details, refer to the main README.md file.
