"""
Student Life Organizer - Main Flask Application
A simple web app for university students to organize courses and tasks
"""
from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
from models import db, Course, Task
from database import init_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student_organizer.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
init_db(app)


# ============================================================================
# DASHBOARD ROUTES
# ============================================================================

@app.route('/')
def dashboard():
    """Main dashboard showing all tasks sorted by due date"""
    tasks = Task.query.order_by(Task.due_date).all()
    courses = Course.query.all()
    return render_template('dashboard.html', tasks=tasks, courses=courses)


# ============================================================================
# COURSE ROUTES
# ============================================================================

@app.route('/courses')
def courses():
    """Course management page"""
    all_courses = Course.query.all()
    return render_template('courses.html', courses=all_courses)


@app.route('/courses', methods=['POST'])
def add_course():
    """Add a new course"""
    try:
        name = request.form.get('name')
        
        if not name:
            return jsonify({'error': 'Course name is required'}), 400
        
        course = Course(name=name)
        db.session.add(course)
        db.session.commit()
        
        return redirect(url_for('courses'))
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/courses/<int:course_id>', methods=['DELETE'])
def delete_course(course_id):
    """Delete a course (cascade deletes all associated tasks)"""
    try:
        course = Course.query.get_or_404(course_id)
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
def tasks():
    """Task management page"""
    all_tasks = Task.query.order_by(Task.due_date).all()
    all_courses = Course.query.all()
    return render_template('tasks.html', tasks=all_tasks, courses=all_courses)


@app.route('/tasks', methods=['POST'])
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
def update_task(task_id):
    """Update task status and priority only"""
    try:
        task = Task.query.get_or_404(task_id)
        
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
def delete_task(task_id):
    """Delete a task"""
    try:
        task = Task.query.get_or_404(task_id)
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
def api_get_tasks():
    """Get all tasks as JSON"""
    tasks = Task.query.order_by(Task.due_date).all()
    return jsonify([task.to_dict() for task in tasks])


@app.route('/api/courses')
def api_get_courses():
    """Get all courses as JSON"""
    courses = Course.query.all()
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
