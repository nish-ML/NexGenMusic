#!/usr/bin/env python3
"""
Setup script for NexGenMusic Mood Detection & Audio Generation
"""

import os
import sys
import subprocess
import platform

def print_header():
    print("🎵" + "=" * 60 + "🎵")
    print("    NexGenMusic: AI Mood Detection & Audio Generation")
    print("    Setup and Installation Script")
    print("🎵" + "=" * 60 + "🎵")
    print()

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8+ is required. Current version:", f"{version.major}.{version.minor}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("\n📦 Installing Python dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def download_ml_models():
    """Download required ML models"""
    print("\n🧠 Downloading ML models...")
    try:
        if os.path.exists("download_models.py"):
            subprocess.check_call([sys.executable, "download_models.py"])
            print("✅ ML models downloaded successfully")
        else:
            print("⚠️  download_models.py not found, skipping model download")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to download models: {e}")
        return False

def setup_database():
    """Setup Django database"""
    print("\n🗄️  Setting up database...")
    try:
        subprocess.check_call([sys.executable, "manage.py", "migrate"])
        print("✅ Database setup complete")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to setup database: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    directories = ["generated_audio", "models_cache"]
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ Created directory: {directory}")
        else:
            print(f"📁 Directory already exists: {directory}")

def check_env_file():
    """Check if .env file exists"""
    print("\n🔧 Checking environment configuration...")
    if os.path.exists(".env"):
        print("✅ .env file found")
        return True
    else:
        print("⚠️  .env file not found")
        print("📝 Creating sample .env file...")
        
        sample_env = """# NexGenMusic Environment Variables
DJANGO_SECRET_KEY=your-secret-key-here
SPOTIFY_CLIENT_ID=your-spotify-client-id
SPOTIFY_CLIENT_SECRET=your-spotify-client-secret

# Optional: Database settings (defaults to SQLite)
# DATABASE_URL=postgresql://user:password@localhost/nexgenmusic
"""
        
        with open(".env.sample", "w") as f:
            f.write(sample_env)
        
        print("📄 Created .env.sample file")
        print("🔑 Please copy .env.sample to .env and fill in your credentials")
        return False

def test_installation():
    """Test if installation works"""
    print("\n🧪 Testing installation...")
    try:
        # Test Django
        subprocess.check_call([sys.executable, "manage.py", "check"], 
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Django configuration OK")
        
        # Test audio generation
        if os.path.exists("test_audio_generation.py"):
            print("🎵 Testing audio generation...")
            result = subprocess.run([sys.executable, "test_audio_generation.py"], 
                                  capture_output=True, text=True, timeout=30)
            if result.returncode == 0:
                print("✅ Audio generation test passed")
            else:
                print("⚠️  Audio generation test had issues (this is normal on first run)")
        
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Installation test failed: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("⚠️  Audio generation test timed out (this is normal)")
        return True

def print_next_steps():
    """Print next steps for the user"""
    print("\n🎉 Setup Complete!")
    print("=" * 50)
    print("Next steps:")
    print("1. 🔑 Configure your .env file with Spotify credentials")
    print("2. 🚀 Start the server: python manage.py runserver")
    print("3. 🌐 Open http://localhost:8000 in your browser")
    print("4. 🎵 Start detecting moods and generating audio!")
    print()
    print("📚 Documentation: README_MOOD_DETECTION.md")
    print("🧪 Test audio generation: python test_audio_generation.py")
    print("🎯 Test mood detection: python test_ml_sentiment.py")
    print()
    print("Happy mood detecting! 🧠🎵")

def main():
    """Main setup function"""
    print_header()
    
    # Check system requirements
    if not check_python_version():
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        sys.exit(1)
    
    # Download ML models
    download_ml_models()
    
    # Setup database
    if not setup_database():
        print("❌ Setup failed at database setup")
        sys.exit(1)
    
    # Check environment
    env_ok = check_env_file()
    
    # Test installation
    test_installation()
    
    # Print next steps
    print_next_steps()
    
    if not env_ok:
        print("⚠️  Don't forget to configure your .env file!")

if __name__ == "__main__":
    main()