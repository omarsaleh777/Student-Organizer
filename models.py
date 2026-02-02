"""
Database models for Student Life Organizer
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy()


class Course(db.Model):
    """Course model - represents a university course"""
    __tablename__ = 'courses'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    # Relationship: One course has many tasks (cascade delete)
    tasks = db.relationship('Task', backref='course', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        """Convert course to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'task_count': len(self.tasks)
        }


class Task(db.Model):
    """Task model - represents an assignment, quiz, or exam"""
    __tablename__ = 'tasks'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date, nullable=False)
    task_type = db.Column(db.String(20), nullable=False)  # assignment, quiz, exam
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, in-progress, completed
    priority = db.Column(db.String(20), nullable=False, default='medium')  # low, medium, high
    
    # Foreign key to Course (with cascade delete)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id', ondelete='CASCADE'), nullable=False)
    
    def days_remaining(self):
        """Calculate days remaining until due date"""
        today = date.today()
        delta = self.due_date - today
        return delta.days
    
    def urgency_level(self):
        """Determine urgency level based on days remaining"""
        days = self.days_remaining()
        if days < 0:
            return 'overdue'
        elif days <= 3:
            return 'urgent'
        elif days <= 7:
            return 'soon'
        else:
            return 'later'
    
    def to_dict(self):
        """Convert task to dictionary"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat(),
            'task_type': self.task_type,
            'status': self.status,
            'priority': self.priority,
            'course_id': self.course_id,
            'course_name': self.course.name,
            'days_remaining': self.days_remaining(),
            'urgency_level': self.urgency_level()
        }
