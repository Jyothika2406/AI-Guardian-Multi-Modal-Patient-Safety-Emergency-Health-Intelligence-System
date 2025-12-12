#!/usr/bin/env python3
"""
Installation and setup helper for AI Guardian
"""

import os
import sys
import subprocess
import platform

def run_command(cmd, description=""):
    """Run a shell command"""
    if description:
        print(f"\n📦 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        return False

def main():
    print("=" * 70)
    print("🛡️  AI GUARDIAN - Setup Script")
    print("=" * 70)
    
    # Check Python version
    print(f"\n✅ Python {sys.version.split()[0]}")
    
    # Check OS
    os_name = platform.system()
    print(f"✅ OS: {os_name}")
    
    # Create virtual environment
    venv_path = "venv" if os_name != "Windows" else "venv"
    if not os.path.exists(venv_path):
        print(f"\n📦 Creating virtual environment...")
        if os_name == "Windows":
            run_command("python -m venv venv")
        else:
            run_command("python3 -m venv venv")
    else:
        print(f"✅ Virtual environment already exists")
    
    # Determine pip command
    if os_name == "Windows":
        pip_cmd = "venv\\Scripts\\pip"
    else:
        pip_cmd = "venv/bin/pip"
    
    # Upgrade pip
    print(f"\n📦 Upgrading pip...")
    run_command(f"{pip_cmd} install --upgrade pip")
    
    # Install requirements
    print(f"\n📦 Installing dependencies...")
    run_command(f"{pip_cmd} install -r backend/requirements.txt")
    
    print("\n" + "=" * 70)
    print("✅ Setup Complete!")
    print("=" * 70)
    
    # Instructions
    if os_name == "Windows":
        activate_cmd = "venv\\Scripts\\activate"
    else:
        activate_cmd = "source venv/bin/activate"
    
    print(f"\n📝 Next steps:")
    print(f"1. Activate virtual environment:")
    print(f"   {activate_cmd}")
    print(f"\n2. Run the demo:")
    print(f"   cd backend")
    print(f"   python demo.py")
    print(f"\n3. Or run the web server:")
    print(f"   cd backend")
    print(f"   python run.py")
    print(f"   Then open: http://localhost:5000/dashboard")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
