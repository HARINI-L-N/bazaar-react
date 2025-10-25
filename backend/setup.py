#!/usr/bin/env python3
"""
Quick setup script for the E-commerce Backend
This script helps you get started quickly with the backend API
"""

import os
import sys
import subprocess
import shutil

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✓ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ {description} failed: {e.stderr}")
        return False

def main():
    print("🚀 E-commerce Backend Setup")
    print("=" * 50)
    
    # Check if Python is available
    if not shutil.which('python'):
        print("✗ Python is not installed or not in PATH")
        return False
    
    # Check if pip is available
    if not shutil.which('pip'):
        print("✗ pip is not installed or not in PATH")
        return False
    
    print("✓ Python and pip are available")
    
    # Create virtual environment
    if not run_command("python -m venv venv", "Creating virtual environment"):
        return False
    
    # Determine activation script based on OS
    if os.name == 'nt':  # Windows
        activate_script = "venv\\Scripts\\activate"
        pip_command = "venv\\Scripts\\pip"
        python_command = "venv\\Scripts\\python"
    else:  # Unix-like systems
        activate_script = "source venv/bin/activate"
        pip_command = "venv/bin/pip"
        python_command = "venv/bin/python"
    
    # Install requirements
    if not run_command(f"{pip_command} install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Create .env file if it doesn't exist
    if not os.path.exists('.env'):
        if os.path.exists('env.example'):
            shutil.copy('env.example', '.env')
            print("✓ Created .env file from template")
        else:
            print("⚠️  Please create a .env file with your configuration")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed successfully!")
    print("=" * 50)
    print("\nNext steps:")
    print("1. Make sure MongoDB is running on your system")
    print("2. Activate the virtual environment:")
    if os.name == 'nt':
        print("   venv\\Scripts\\activate")
    else:
        print("   source venv/bin/activate")
    print("3. Populate the database with sample data:")
    print(f"   {python_command} populate_db.py")
    print("4. Start the Flask application:")
    print(f"   {python_command} app.py")
    print("\nThe API will be available at http://localhost:5000")
    print("\nTest credentials:")
    print("- John Doe: john@example.com / password123")
    print("- Jane Smith: jane@example.com / password123")
    print("- Admin: admin@example.com / admin123")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)

