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
- **Job Screening Quizzes**: Attempt screening quizzes assigned to specific job drives with real-time countdown timers
- Complete timed MCQ quizzes and receive instant score feedback after submission
- Track application and quiz submission statuses in real-time
- View placement history

### For Companies
- Create company profile
- Post job drives with eligibility criteria
- Set minimum CGPA and branch requirements
- **Screening Quiz Creation**: Build customized multiple-choice questionnaires linked to specific job postings, configure durations, and specify correct answers
- **Quiz Performance Monitoring**: Track and view real-time scores for applicants attempting screening quizzes
- Review applicant quiz results per job drive to shortlist candidates more effectively
- Shortlist or reject candidates based on application profiles and quiz metrics
- Manage multiple job postings

### For Administrators (TPO)
- Monitor all students, companies, and placement workflows
- View all job drives, applications, and **global quiz results** across all companies
- Generate comprehensive placement reports
- Analytics dashboard with charts (Applications by status, branch-wise metrics)
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
- Werkzeug (password hashing and secure filenames)

### Database
- MongoDB 4.0+
- PyMongo driver

### Development Tools
- VS Code
- Postman (API testing)
- Git/GitHub

## 🏗️ System Architecture