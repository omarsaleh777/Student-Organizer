"""
Student Life Organizer - Main Flask Application with Authentication
A simple web app for university students to organize courses and tasks
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from models import db, User, Course, Task
from database import init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_organizer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key-change-this-in-production'

# Initialize database
init_db(app)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Username and password are required', 'error')
            return render_template('register.html')
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return render_template('register.html')
        
        # Create new user
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out', 'success')
    return redirect(url_for('login'))


# ============================================================================
# DASHBOARD ROUTES
# ============================================================================

@app.route('/')
@login_required
def dashboard():
    """Main dashboard showing all tasks sorted by due date"""
    # Only show tasks from current user's courses
    tasks = Task.query.join(Course).filter(Course.user_id == current_user.id).order_by(Task.due_date).all()
    courses = Course.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks, courses=courses)


# ============================================================================
# COURSE ROUTES
# ============================================================================

@app.route('/courses')
@login_required
def courses():
    """Course management page"""
    all_courses = Course.query.filter_by(user_id=current_user.id).all()
    return render_template('courses.html', courses=all_courses)


@app.route('/courses', methods=['POST'])
@login_required
def add_course():
    """Add a new course"""
    try:
        name = request.form.get('name')
        
        if not name:
            return jsonify({'error': 'Course name is required'}), 400
        
        course = Course(name=name, user_id=current_user.id)
        db.session.add(course)
        db.session.commit()
        
        return redirect(url_for('courses'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/courses/<int:course_id>', methods=['DELETE'])
@login_required
def delete_course(course_id):
    """Delete a course (cascade deletes all associated tasks)"""
    try:
        course = Course.query.filter_by(id=course_id, user_id=current_user.id).first_or_404()
        db.session.delete(course)
        db.session.commit()
        
        return jsonify({'message': 'Course and associated tasks deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============================================================================
# TASK ROUTES
# ============================================================================

@app.route('/tasks')
@login_required
def tasks():
    """Task management page"""
    all_tasks = Task.query.join(Course).filter(Course.user_id == current_user.id).order_by(Task.due_date).all()
    all_courses = Course.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks.html', tasks=all_tasks, courses=all_courses)


@app.route('/tasks', methods=['POST'])
@login_required
def add_task():
    """Add a new task"""
    try:
        title = request.form.get('title')
        description = request.form.get('description', '')
        due_date_str = request.form.get('due_date')
        task_type = request.form.get('task_type')
        status = request.form.get('status', 'pending')
        priority = request.form.get('priority', 'medium')
        course_id = request.form.get('course_id')
        
        # Validation
        if not all([title, due_date_str, task_type, course_id]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Verify course belongs to current user
        course = Course.query.filter_by(id=int(course_id), user_id=current_user.id).first()
        if not course:
            return jsonify({'error': 'Invalid course'}), 403
        
        # Parse date
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()
        
        task = Task(
            title=title,
            description=description,
            due_date=due_date,
            task_type=task_type,
            status=status,
            priority=priority,
            course_id=int(course_id)
        )
        
        db.session.add(task)
        db.session.commit()
        
        return redirect(url_for('tasks'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/tasks/<int:task_id>', methods=['PUT'])
@login_required
def update_task(task_id):
    """Update task status and priority only"""
    try:
        task = Task.query.join(Course).filter(
            Task.id == task_id,
            Course.user_id == current_user.id
        ).first_or_404()
        
        data = request.get_json()
        
        # Only allow status and priority updates
        if 'status' in data:
            task.status = data['status']
        if 'priority' in data:
            task.priority = data['priority']
        
        db.session.commit()
        
        return jsonify(task.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    """Delete a task"""
    try:
        task = Task.query.join(Course).filter(
            Task.id == task_id,
            Course.user_id == current_user.id
        ).first_or_404()
        db.session.delete(task)
        db.session.commit()
        
        return jsonify({'message': 'Task deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# ============================================================================
# API ROUTES (for AJAX requests)
# ============================================================================

@app.route('/api/tasks')
@login_required
def api_get_tasks():
    """Get all tasks as JSON"""
    tasks = Task.query.join(Course).filter(Course.user_id == current_user.id).order_by(Task.due_date).all()
    return jsonify([task.to_dict() for task in tasks])


@app.route('/api/courses')
@login_required
def api_get_courses():
    """Get all courses as JSON"""
    courses = Course.query.filter_by(user_id=current_user.id).all()
    return jsonify([course.to_dict() for course in courses])


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("Student Life Organizer")
    print("=" * 60)
    print("Starting server at http://127.0.0.1:5000")
    print("Press CTRL+C to quit")
    print("=" * 60)
    app.run(debug=False, host='127.0.0.1', port=5000, use_reloader=False)
