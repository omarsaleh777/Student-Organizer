"""
Simple launcher for Student Life Organizer
"""
import os
import sys

# Change to the correct directory
os.chdir(r'C:\Users\mrsal\.gemini\antigravity\scratch\student-life-organizer')

try:
    # Import and run the app
    from app import app
    print("=" * 60)
    print("Student Life Organizer - Starting...")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5000)
except Exception as e:
    print(f"Error starting application: {e}")
    import traceback
    traceback.print_exc()
    input("Press Enter to exit...")
