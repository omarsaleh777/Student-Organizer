# 📚 Student Life Organizer

A simple, clean web application for university students to organize courses, assignments, quizzes, and exams.

## ✨ Features

- **Course Management**: Add and manage your courses
- **Task Organization**: Create assignments, quizzes, and exams
- **Priority & Status Tracking**: Set priority levels and track task status
- **Days Remaining**: Automatic calculation of days until due date
- **Color-Coded Urgency**: Visual indicators for urgent, soon, and later tasks
- **Mobile-Friendly**: Responsive design works on all devices
- **Frontend Filtering**: Filter tasks by type (assignment/quiz/exam)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Navigate to the project directory**
   ```bash
   cd student-life-organizer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Open your browser**
   
   Navigate to: `http://127.0.0.1:5000`

That's it! The database will be created automatically on first run.

## 📖 Usage Guide

### Adding a Course

1. Go to the **Courses** page
2. Enter the course name (e.g., "Data Structures")
3. Click **Add Course**

### Adding a Task

1. Go to the **Tasks** page
2. Fill in the task details:
   - **Title**: Name of the assignment/quiz/exam
   - **Description**: Optional details
   - **Due Date**: When it's due
   - **Course**: Select from your courses
   - **Task Type**: Assignment, Quiz, or Exam
   - **Priority**: Low, Medium, or High
   - **Status**: Pending, In Progress, or Completed
3. Click **Add Task**

### Dashboard

The dashboard shows all your tasks sorted by due date with:
- **Color-coded urgency**:
  - 🔴 Red: Overdue or due in 3 days or less
  - 🟡 Yellow: Due in 4-7 days
  - 🟢 Green: Due in more than 7 days
- **Quick status/priority updates**: Use dropdowns to change task status or priority
- **Filter by type**: Filter tasks by assignment, quiz, or exam

### Deleting Items

- **Delete Course**: Deletes the course and ALL associated tasks (cascade delete)
- **Delete Task**: Deletes only the specific task

## 🗂️ Project Structure

```
student-life-organizer/
├── app.py                 # Main Flask application with routes
├── models.py              # Database models (Course, Task)
├── database.py            # Database initialization
├── seed.py               # Optional seed script for testing
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   └── style.css         # Custom CSS (no framework)
└── templates/
    ├── base.html         # Base template with navigation
    ├── dashboard.html    # Main dashboard view
    ├── courses.html      # Course management page
    └── tasks.html        # Task management page
```

## 🧪 Optional: Seed Sample Data

For testing purposes, you can populate the database with sample data:

```bash
python seed.py
```

This will create:
- 3 sample courses
- 5 sample tasks with various due dates, priorities, and statuses

**Note**: This will clear existing data, so only use it for testing!

## 🔧 Technical Details

### Backend
- **Framework**: Flask 3.0.0
- **Database**: SQLite (file-based, no setup required)
- **ORM**: SQLAlchemy

### Frontend
- **HTML5** with Jinja2 templating
- **Custom CSS** (no framework for speed and clarity)
- **Vanilla JavaScript** for interactivity

### Database Models

**Course**
- `id`: Primary key
- `name`: Course name

**Task**
- `id`: Primary key
- `title`: Task title
- `description`: Optional description
- `due_date`: Due date
- `task_type`: assignment, quiz, or exam
- `status`: pending, in-progress, or completed
- `priority`: low, medium, or high
- `course_id`: Foreign key to Course (cascade delete)

### API Routes

**Courses**
- `GET /courses` - View courses page
- `POST /courses` - Add new course
- `DELETE /courses/<id>` - Delete course (cascade deletes tasks)

**Tasks**
- `GET /tasks` - View tasks page
- `POST /tasks` - Add new task
- `PUT /tasks/<id>` - Update task (status & priority only)
- `DELETE /tasks/<id>` - Delete task

**Dashboard**
- `GET /` - Main dashboard

## 📱 Mobile Responsiveness

The application is fully responsive and tested on:
- Mobile (320px)
- Tablet (768px)
- Desktop (1024px+)

## 🎯 MVP Boundaries

This is a **Minimum Viable Product** with the following intentional limitations:

- ✅ **No authentication**: Single user, local deployment
- ✅ **No notifications**: Manual checking only
- ✅ **Single semester**: No multi-semester support
- ✅ **Local only**: SQLite database, not production-ready

## 🚀 Production Considerations

If you want to deploy this for production use, consider:

1. **Authentication**: Add user login/registration (Flask-Login)
2. **Database**: Migrate from SQLite to PostgreSQL
3. **Security**: Add CSRF protection, input validation
4. **Deployment**: Use a production WSGI server (Gunicorn)
5. **Cloud Hosting**: Deploy to Heroku, AWS, or similar
6. **Multi-semester**: Add semester field to courses
7. **Notifications**: Email or push notifications for upcoming deadlines

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Feel free to fork, modify, and improve this project!

---

**Built with ❤️ for students who want to stay organized**
