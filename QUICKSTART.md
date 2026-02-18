# 🚀 CPMS Quick Start Guide

Get your College Placement Management System up and running in minutes!

## ⚡ Quick Setup (5 Minutes)

### Step 1: Install Python and MongoDB

**Python** (if not installed):
- Windows: Download from [python.org](https://www.python.org/downloads/)
- Mac: `brew install python3`
- Linux: `sudo apt-get install python3 python3-pip`

**MongoDB** (if not installed):
- Windows: Download from [mongodb.com](https://www.mongodb.com/try/download/community)
- Mac: `brew tap mongodb/brew && brew install mongodb-community`
- Linux: `sudo apt-get install -y mongodb`

### Step 2: Start MongoDB

**Windows**: MongoDB starts automatically after installation
**Mac**: `brew services start mongodb-community`
**Linux**: `sudo systemctl start mongodb`

Verify MongoDB is running: Open new terminal and type `mongo` or `mongosh`

### Step 3: Setup Project

```bash
# Navigate to project folder
cd cpms

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Run the Application

```bash
python app.py
```

You should see:
```
🚀 Starting College Placement Management System
📁 Upload folder: static/uploads
🔐 JWT enabled
💾 MongoDB URI: mongodb://localhost:27017/cpms

✅ Server running on http://localhost:5000
```

### Step 5: Access the Application

Open your browser and go to: **http://localhost:5000**

---

## 👤 First Time Setup

### Create Test Accounts

1. **Go to Register Page**: http://localhost:5000/register

2. **Create a Student Account**:
   - Email: `student@test.com`
   - Password: `student123`
   - Role: Student

3. **Create a Company Account**:
   - Email: `company@test.com`
   - Password: `company123`
   - Role: Company

4. **Create an Admin Account**:
   - Email: `admin@test.com`
   - Password: `admin123`
   - Role: Admin

### Test the Complete Workflow

#### As Student:
1. Login → http://localhost:5000/login
2. Complete profile (name, roll no, branch, CGPA)
3. Upload resume (PDF only)
4. View available jobs
5. Apply for jobs
6. Check application status

#### As Company:
1. Login with company credentials
2. Complete company profile
3. Post a job drive (set CGPA, branches, salary)
4. View applicants
5. Shortlist or reject candidates

#### As Admin:
1. Login with admin credentials
2. View all students
3. View all companies
4. View all job drives
5. Check analytics and reports

---

## 📝 Sample Data for Testing

### Student Profile
```
Name: John Doe
Roll No: CSE101
Branch: CSE
CGPA: 8.5
Skills: Python, Java, Web Development
```

### Company Profile
```
Company Name: Google India
Contact Person: Jane Smith
Email: hr@google.com
Phone: 9876543210
```

### Job Posting
```
Job Title: Software Engineer
Description: Backend developer for cloud infrastructure
Min CGPA: 7.5
Branches: CSE, IT
Salary: 10-12 LPA
```

---

## 🔧 Common Issues & Solutions

### Issue 1: "ModuleNotFoundError"
**Solution**: Make sure virtual environment is activated and run:
```bash
pip install -r requirements.txt
```

### Issue 2: "Connection refused" (MongoDB)
**Solution**: Start MongoDB service:
- Windows: Start MongoDB service from Services
- Mac: `brew services start mongodb-community`
- Linux: `sudo systemctl start mongodb`

### Issue 3: "Port 5000 already in use"
**Solution**: 
- Kill the process using port 5000
- Or change port in `app.py`: `app.run(port=5001)`

### Issue 4: Can't upload resume
**Solution**: 
- Check file is PDF format
- Check file size is under 5MB
- Make sure `static/uploads` folder exists

### Issue 5: "Invalid token"
**Solution**: 
- Login again to get fresh token
- Clear browser localStorage
- Check token expiry time

---

## 🎯 Testing Checklist

Use this checklist to verify everything works:

### Student Flow
- [ ] Register as student
- [ ] Login successfully
- [ ] Complete profile
- [ ] Upload resume (PDF)
- [ ] View eligible jobs
- [ ] Apply for a job
- [ ] See "Already applied" error on duplicate application
- [ ] View application status

### Company Flow
- [ ] Register as company
- [ ] Login successfully
- [ ] Complete company profile
- [ ] Post a job drive
- [ ] View posted jobs
- [ ] See applicants list
- [ ] Shortlist a candidate
- [ ] Reject a candidate

### Admin Flow
- [ ] Register as admin
- [ ] Login successfully
- [ ] View all students
- [ ] View all companies
- [ ] View all jobs
- [ ] See analytics charts
- [ ] Check placement reports
- [ ] Verify statistics

---

## 📊 Verify in MongoDB

Open MongoDB shell and check data:

```bash
# Connect to MongoDB
mongo

# Use CPMS database
use cpms

# Check collections
show collections

# View users (should see 3 users)
db.users.find().pretty()

# View students
db.students.find().pretty()

# View companies
db.companies.find().pretty()

# View job drives
db.job_drives.find().pretty()

# View applications
db.applications.find().pretty()
```

---

## 🔍 API Testing with Postman

1. **Import Postman Collection**:
   - Refer to `API_TESTING.md` for detailed API documentation

2. **Test Flow**:
   - Register users
   - Login and get tokens
   - Create profiles
   - Post jobs
   - Apply for jobs
   - Update statuses

---

## 📱 URLs Reference

| Page | URL |
|------|-----|
| Home | http://localhost:5000/ |
| Login | http://localhost:5000/login |
| Register | http://localhost:5000/register |
| Student Dashboard | http://localhost:5000/student-dashboard |
| Company Dashboard | http://localhost:5000/company-dashboard |
| Admin Dashboard | http://localhost:5000/admin-dashboard |

---

## 🛑 Stopping the Application

1. In the terminal where Flask is running, press `Ctrl + C`
2. Deactivate virtual environment: `deactivate`
3. (Optional) Stop MongoDB:
   - Mac: `brew services stop mongodb-community`
   - Linux: `sudo systemctl stop mongodb`

---

## 📚 Next Steps

After quick start, explore:
1. **README.md** - Complete documentation
2. **API_TESTING.md** - API testing guide
3. **VIVA_GUIDE.md** - Viva preparation
4. Customize the code for your needs
5. Add more features
6. Deploy to cloud (Heroku/AWS)

---

## 💡 Pro Tips

1. **Use Different Browsers**: Test each role in different browsers or incognito windows
2. **Check Console**: Open browser DevTools to see API calls and errors
3. **MongoDB Compass**: Install MongoDB Compass for better database visualization
4. **Git**: Commit your changes regularly
5. **Backup**: Export MongoDB data before major changes
6. **Environment**: Use `.env` file for sensitive data (never commit it!)

---

## 🆘 Need Help?

- Check error messages in terminal
- Review browser console for frontend errors
- Verify MongoDB is running
- Check if all dependencies are installed
- Refer to detailed documentation in README.md
- Review API_TESTING.md for API examples

---

**Happy Coding! 🎉**

Your CPMS should now be fully functional. Test all features and customize as needed for your project requirements.
