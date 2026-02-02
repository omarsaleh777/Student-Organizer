# Render Deployment Guide for Student Life Organizer

## 🚀 Deploy to Render

### Step 1: Push Your Code to GitHub
Your code is already on GitHub! ✅

### Step 2: Create Render Account
1. Go to https://render.com
2. Sign up (you can use GitHub to sign in)

### Step 3: Create New Web Service
1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub account
3. Select your repository: `Student-Organizer`
4. Click **"Connect"**

### Step 4: Configure Your Service

**Basic Settings:**
- **Name:** `student-life-organizer` (or any name you want)
- **Region:** Choose closest to you
- **Branch:** `main`
- **Root Directory:** Leave empty
- **Runtime:** `Python 3`
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`

### Step 5: Add Environment Variables (IMPORTANT!)

This is where you add your `.env` variables **without pushing them to GitHub**:

Click **"Environment"** tab or scroll to **"Environment Variables"** section, then add:

```
MAIL_SERVER = smtp.gmail.com
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = mrok730@gmail.com
MAIL_PASSWORD = your-16-char-app-password-here
MAIL_DEFAULT_SENDER = noreply@studentorganizer.com
SECRET_KEY = your-secret-key-here-change-this
```

**Important Notes:**
- Replace `your-16-char-app-password-here` with your actual Gmail App Password
- Replace `your-secret-key-here-change-this` with a random string (e.g., `mysecretkey12345`)
- These variables are stored securely on Render's servers
- They are NOT in your GitHub repository

### Step 6: Deploy!
1. Click **"Create Web Service"**
2. Render will automatically:
   - Pull your code from GitHub
   - Install dependencies
   - Start your app
3. Wait 2-5 minutes for deployment

### Step 7: Get Your URL
Once deployed, Render gives you a URL like:
```
https://student-life-organizer.onrender.com
```

You can share this URL with anyone!

---

## 🔄 Auto-Deploy

Render automatically redeploys when you push to GitHub:
1. Make changes locally
2. `git push origin main`
3. Render detects the change and redeploys automatically

---

## 🗄️ Database on Render

Your SQLite database will work, but it resets on every deploy. For production, consider:
- **PostgreSQL** (Render offers free tier)
- Or keep SQLite for testing

---

## 🔒 Security on Render

✅ Environment variables are encrypted
✅ Not visible in logs
✅ Not in GitHub
✅ Only accessible by your app

---

## 🐛 Troubleshooting

**If deployment fails:**
1. Check Render logs (click "Logs" tab)
2. Common issues:
   - Missing dependencies in `requirements.txt`
   - Wrong start command
   - Database issues

**If email doesn't work:**
1. Check environment variables are set correctly
2. Make sure `MAIL_PASSWORD` is your App Password (not regular password)
3. Check Render logs for errors

---

## 💰 Pricing

**Render Free Tier:**
- ✅ Free web service
- ✅ Automatic HTTPS
- ⚠️ Sleeps after 15 min of inactivity (wakes up on request)
- ⚠️ 750 hours/month free

**For always-on service:** Upgrade to paid plan ($7/month)

---

## 📝 Summary

1. Push code to GitHub ✅ (already done)
2. Create Render account
3. Connect GitHub repo
4. Add environment variables in Render dashboard
5. Deploy!

Your `.env` file stays on your computer and Render's servers only. Never on GitHub! 🔒
