# How to Push Student Life Organizer to GitHub

## Step 1: Create a GitHub Repository

1. Go to [GitHub](https://github.com) and log in
2. Click the **"+"** icon in the top right → **"New repository"**
3. Repository name: `student-life-organizer` (or your preferred name)
4. Description: `A simple Flask web app for university students to organize courses and tasks`
5. Choose **Public** or **Private**
6. **DO NOT** initialize with README, .gitignore, or license (we already have these)
7. Click **"Create repository"**

## Step 2: Initialize Git and Push

Open a terminal in the project directory and run these commands:

```bash
# Navigate to project directory
cd C:\Users\mrsal\.gemini\antigravity\scratch\student-life-organizer

# Initialize Git repository
git init

# Add all files
git add .

# Create first commit
git commit -m "Initial commit: Student Life Organizer MVP"

# Add your GitHub repository as remote (replace YOUR_USERNAME and REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 3: Replace Placeholders

In the command above, replace:
- `YOUR_USERNAME` with your GitHub username
- `REPO_NAME` with your repository name

**Example:**
```bash
git remote add origin https://github.com/johndoe/student-life-organizer.git
```

## Alternative: Using GitHub Desktop

If you prefer a GUI:

1. Download [GitHub Desktop](https://desktop.github.com/)
2. Install and sign in
3. Click **"Add"** → **"Add existing repository"**
4. Browse to: `C:\Users\mrsal\.gemini\antigravity\scratch\student-life-organizer`
5. Click **"Publish repository"** to push to GitHub

## What Gets Pushed

✅ **Included:**
- All Python source code (app.py, models.py, etc.)
- HTML templates
- CSS files
- README.md
- requirements.txt
- .gitignore

❌ **Excluded (via .gitignore):**
- Database files (*.db)
- Python cache (__pycache__)
- Test files
- IDE settings

## Verify Your Push

After pushing, visit your GitHub repository URL to see your code online!

---

**Need help?** Check the [GitHub Docs](https://docs.github.com/en/get-started/importing-your-projects-to-github/importing-source-code-to-github/adding-locally-hosted-code-to-github)
