"""
Email Notification System for Student Life Organizer
Sends daily email reminders for tasks due in 1 day
"""
from flask import render_template_string
from flask_mail import Message
from datetime import date, timedelta
from models import db, User, Task, Course


def check_and_send_notifications(mail):
    """
    Check all users for tasks due tomorrow and send email notifications
    This function is called by the scheduler daily
    """
    tomorrow = date.today() + timedelta(days=1)
    
    # Get all users with notifications enabled
    users = User.query.filter_by(email_notifications_enabled=True).all()
    
    for user in users:
        # Get tasks due tomorrow for this user
        tasks_due_tomorrow = Task.query.join(Course).filter(
            Course.user_id == user.id,
            Task.due_date == tomorrow,
            Task.status != 'completed'
        ).order_by(Task.priority.desc()).all()
        
        if tasks_due_tomorrow:
            send_notification_email(mail, user, tasks_due_tomorrow)
            print(f"Sent notification to {user.username} ({user.email}) for {len(tasks_due_tomorrow)} task(s)")


def send_notification_email(mail, user, tasks):
    """
    Send email notification to user with list of tasks due tomorrow
    """
    # Create email content
    subject = f"📚 Task Reminder: {len(tasks)} task{'s' if len(tasks) > 1 else ''} due tomorrow!"
    
    # HTML email template
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 8px 8px 0 0;
                text-align: center;
            }}
            .content {{
                background: #f9fafb;
                padding: 20px;
                border-radius: 0 0 8px 8px;
            }}
            .task {{
                background: white;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }}
            .task.high {{
                border-left-color: #ef4444;
            }}
            .task.medium {{
                border-left-color: #f59e0b;
            }}
            .task.low {{
                border-left-color: #10b981;
            }}
            .task-title {{
                font-weight: bold;
                font-size: 16px;
                margin-bottom: 5px;
            }}
            .task-meta {{
                color: #666;
                font-size: 14px;
            }}
            .priority {{
                display: inline-block;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
                margin-right: 5px;
            }}
            .priority.high {{
                background: #fee2e2;
                color: #991b1b;
            }}
            .priority.medium {{
                background: #fef3c7;
                color: #92400e;
            }}
            .priority.low {{
                background: #d1fae5;
                color: #065f46;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                color: #666;
                font-size: 14px;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                margin-top: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📚 Student Life Organizer</h1>
            <p>Task Reminder for {user.username}</p>
        </div>
        <div class="content">
            <p>Hi {user.username},</p>
            <p>You have <strong>{len(tasks)} task{'s' if len(tasks) > 1 else ''}</strong> due <strong>tomorrow</strong>:</p>
            
            {''.join([f'''
            <div class="task {task.priority}">
                <div class="task-title">{task.title}</div>
                <div class="task-meta">
                    <span class="priority {task.priority}">{task.priority.upper()}</span>
                    <strong>{task.course.name}</strong> • {task.task_type.title()}
                </div>
                {f'<p style="margin-top: 8px; color: #666;">{task.description}</p>' if task.description else ''}
            </div>
            ''' for task in tasks])}
            
            <div style="text-align: center;">
                <a href="http://127.0.0.1:5000" class="button">View Dashboard</a>
            </div>
        </div>
        <div class="footer">
            <p>This is an automated reminder from Student Life Organizer</p>
            <p style="font-size: 12px;">You can disable notifications in your account settings</p>
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    text_body = f"""
    Student Life Organizer - Task Reminder
    
    Hi {user.username},
    
    You have {len(tasks)} task{'s' if len(tasks) > 1 else ''} due tomorrow:
    
    {''.join([f'• {task.title} ({task.priority.upper()}) - {task.course.name}\n' for task in tasks])}
    
    Visit http://127.0.0.1:5000 to view your dashboard.
    
    ---
    This is an automated reminder from Student Life Organizer
    """
    
    # Create and send email
    msg = Message(
        subject=subject,
        sender='Student Life Organizer <noreply@studentorganizer.com>',
        recipients=[user.email],
        body=text_body,
        html=html_body
    )
    
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email to {user.email}: {str(e)}")
        return False


def send_notification_email_direct(mail, user_email, user_name, tasks):
    """
    Send email notification directly with email and name (for threading)
    """
    # Create email content
    subject = f"📚 Task Reminder: {len(tasks)} task{'s' if len(tasks) > 1 else ''} due tomorrow!"
    
    # HTML email template
    html_body = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 8px 8px 0 0;
                text-align: center;
            }}
            .content {{
                background: #f9fafb;
                padding: 20px;
                border-radius: 0 0 8px 8px;
            }}
            .task {{
                background: white;
                padding: 15px;
                margin: 10px 0;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }}
            .task.high {{
                border-left-color: #ef4444;
            }}
            .task.medium {{
                border-left-color: #f59e0b;
            }}
            .task.low {{
                border-left-color: #10b981;
            }}
            .task-title {{
                font-weight: bold;
                font-size: 16px;
                margin-bottom: 5px;
            }}
            .task-meta {{
                color: #666;
                font-size: 14px;
            }}
            .priority {{
                display: inline-block;
                padding: 2px 8px;
                border-radius: 4px;
                font-size: 12px;
                font-weight: bold;
                margin-right: 5px;
            }}
            .priority.high {{
                background: #fee2e2;
                color: #991b1b;
            }}
            .priority.medium {{
                background: #fef3c7;
                color: #92400e;
            }}
            .priority.low {{
                background: #d1fae5;
                color: #065f46;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                color: #666;
                font-size: 14px;
            }}
            .button {{
                display: inline-block;
                padding: 10px 20px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                margin-top: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📚 Student Life Organizer</h1>
            <p>Task Reminder for {user_name}</p>
        </div>
        <div class="content">
            <p>Hi {user_name},</p>
            <p>You have <strong>{len(tasks)} task{'s' if len(tasks) > 1 else ''}</strong> due <strong>tomorrow</strong>:</p>
            
            {''.join([f'''
            <div class="task {task.priority}">
                <div class="task-title">{task.title}</div>
                <div class="task-meta">
                    <span class="priority {task.priority}">{task.priority.upper()}</span>
                    <strong>{task.course.name}</strong> • {task.task_type.title()}
                </div>
                {f'<p style="margin-top: 8px; color: #666;">{task.description}</p>' if task.description else ''}
            </div>
            ''' for task in tasks])}
            
            <div style="text-align: center;">
                <a href="http://127.0.0.1:5000" class="button">View Dashboard</a>
            </div>
        </div>
        <div class="footer">
            <p>This is an automated reminder from Student Life Organizer</p>
            <p style="font-size: 12px;">You can disable notifications in your account settings</p>
        </div>
    </body>
    </html>
    """
    
    # Plain text version
    text_body = f"""
    Student Life Organizer - Task Reminder
    
    Hi {user_name},
    
    You have {len(tasks)} task{'s' if len(tasks) > 1 else ''} due tomorrow:
    
    {''.join([f'• {task.title} ({task.priority.upper()}) - {task.course.name}\\n' for task in tasks])}
    
    Visit http://127.0.0.1:5000 to view your dashboard.
    
    ---
    This is an automated reminder from Student Life Organizer
    """
    
    # Create and send email
    msg = Message(
        subject=subject,
        sender='Student Life Organizer <noreply@studentorganizer.com>',
        recipients=[user_email],
        body=text_body,
        html=html_body
    )
    
    try:
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email to {user_email}: {str(e)}")
        return False

