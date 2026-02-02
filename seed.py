"""
Optional developer seed script for Student Life Organizer
Run manually with: python seed.py
"""
from app import app
from models import db, Course, Task
from datetime import date, timedelta


def seed_data():
    """Seed the database with sample data for testing"""
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        Task.query.delete()
        Course.query.delete()
        
        # Create sample courses
        print("Creating sample courses...")
        course1 = Course(name='Data Structures')
        course2 = Course(name='Web Development')
        course3 = Course(name='Database Systems')
        
        db.session.add_all([course1, course2, course3])
        db.session.commit()
        
        # Create sample tasks
        print("Creating sample tasks...")
        today = date.today()
        
        tasks = [
            Task(
                title='Binary Tree Assignment',
                description='Implement AVL tree with rotation',
                due_date=today + timedelta(days=2),
                task_type='assignment',
                status='in-progress',
                priority='high',
                course_id=course1.id
            ),
            Task(
                title='Midterm Exam',
                description='Covers chapters 1-5',
                due_date=today + timedelta(days=5),
                task_type='exam',
                status='pending',
                priority='high',
                course_id=course1.id
            ),
            Task(
                title='React Project',
                description='Build a todo app with React',
                due_date=today + timedelta(days=10),
                task_type='assignment',
                status='pending',
                priority='medium',
                course_id=course2.id
            ),
            Task(
                title='CSS Quiz',
                description='Flexbox and Grid layout',
                due_date=today + timedelta(days=1),
                task_type='quiz',
                status='pending',
                priority='medium',
                course_id=course2.id
            ),
            Task(
                title='SQL Homework',
                description='Complex JOIN queries',
                due_date=today + timedelta(days=14),
                task_type='assignment',
                status='pending',
                priority='low',
                course_id=course3.id
            ),
        ]
        
        db.session.add_all(tasks)
        db.session.commit()
        
        print(f"Seeded {len(tasks)} tasks across {3} courses")
        print("Database seeding completed successfully")


if __name__ == '__main__':
    seed_data()
