# 📧 Email Notification Setup Guide

## Quick Start

Your Student Life Organizer now sends **email notifications** for tasks due in 1 day!

## How It Works

- **Daily Check:** Every day at 9:00 AM, the system checks for tasks due tomorrow
- **Email Sent:** Users receive an email with a list of their upcoming tasks
- **Beautiful HTML:** Emails include color-coded priorities and task details

## Setup Instructions

### Step 1: Get Gmail App Password

1. Go to your Google Account: https://myaccount.google.com/
2. Click **Security** → **2-Step Verification** (enable if not already)
3. Scroll down to **App passwords**
4. Click **App passwords**
5. Select **Mail** and **Windows Computer**
6. Click **Generate**
7. **Copy the 16-character password** (you'll need this)

### Step 2: Create .env File

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Open `.env` and fill in your details:
   ```
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=abcd efgh ijkl mnop
   ```

### Step 3: Install python-dotenv

```bash
pip install python-dotenv
```

### Step 4: Restart the Server

Stop and restart your Flask server:
```bash
py app.py
```

## Testing Notifications

### Manual Test

You can test notifications manually by running:

```python
from app import app, mail
from notifications import check_and_send_notifications

with app.app_context():
    check_and_send_notifications(mail)
```

### Create Test Task

1. Register with your real email
2. Add a task with due date = tomorrow
3. Wait for 9:00 AM or run manual test
4. Check your email!

## Email Schedule

- **Default:** 9:00 AM daily
- **To change:** Modify `hour=9` in `app.py` scheduler configuration

## Troubleshooting

### "Authentication failed" error

- Make sure you're using an **App Password**, not your regular Gmail password
- Check that 2-Step Verification is enabled on your Google account

### No emails received

- Check spam folder
- Verify email is correct in user registration
- Check console for error messages
- Make sure `.env` file exists and has correct credentials

### Emails not sending at scheduled time

- Make sure the Flask server is running
- Check console for scheduler logs
- Verify timezone settings

## Disable Notifications

Users can disable notifications in their account (future feature), or you can:
- Set `email_notifications_enabled = False` in database
- Or remove email from user account

## Security Notes

- ✅ `.env` file is in `.gitignore` (credentials won't be pushed to GitHub)
- ✅ Never commit your email password to Git
- ✅ Use App Passwords, not your main Gmail password
- ✅ Email credentials stored as environment variables

## Alternative SMTP Providers

Instead of Gmail, you can use:
- **Outlook:** `smtp.office365.com:587`
- **Yahoo:** `smtp.mail.yahoo.com:587`
- **SendGrid:** Professional email service
- **Mailgun:** Developer-friendly email API

Just update the `.env` file with the appropriate SMTP settings.
