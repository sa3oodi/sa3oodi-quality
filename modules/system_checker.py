"""
System Requirements Checker
Validates all dependencies and system components before application startup
"""
import os
import subprocess
import sys

def check_system_requirements():
    """Check all system requirements before starting the application"""
    print("🔍 Checking System Requirements...")
    print("=" * 40)
    
    all_good = True
    issues = []
    
    # 1. Check Python version
    python_version = sys.version_info
    if python_version.major >= 3 and python_version.minor >= 6:
        print("✅ Python version: OK (Python {}.{}.{})".format(python_version.major, python_version.minor, python_version.micro))
    else:
        print("❌ Python version: FAILED (Need Python 3.6+)")
        issues.append("Upgrade to Python 3.6 or higher")
        all_good = False
    
    # 2. Check FFmpeg
    try:
        result = subprocess.run(["ffmpeg", "-version"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            # Extract version from output
            version_line = result.stdout.split('\n')[0]
            print(f"✅ FFmpeg: OK ({version_line.split()[2]})")
        else:
            print("❌ FFmpeg: FAILED (Command error)")
            issues.append("Install FFmpeg from https://ffmpeg.org/download.html")
            all_good = False
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("❌ FFmpeg: NOT FOUND")
        issues.append("Install FFmpeg and add it to your system PATH")
        all_good = False
    
    # 3. Check NVIDIA GPU (optional)
    try:
        result = subprocess.run(["nvidia-smi"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5)
        if result.returncode == 0:
            print("✅ NVIDIA GPU: Detected (Hardware acceleration available)")
        else:
            print("ℹ️  NVIDIA GPU: Not detected (Will use CPU encoding)")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("ℹ️  NVIDIA GPU: Not available (Will use CPU encoding)")
    
    # 4. Check HandBrake CLI (optional)
    try:
        result = subprocess.run(["HandBrakeCLI", "--version"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            # Extract version from output
            version_line = result.stdout.split('\n')[0]
            print(f"✅ HandBrake CLI: OK ({version_line.split()[0]} {version_line.split()[1]})")
        else:
            print("⚠️  HandBrake CLI: FAILED (Command error)")
            print("   Note: HandBrake compression will not be available")
    except (FileNotFoundError, subprocess.TimeoutExpired):
        print("⚠️  HandBrake CLI: NOT FOUND")
        print("   Note: You can still use the app without compression")
        print("   Download from: https://handbrake.fr/downloads.php")
    
    # 5. Check Python dependencies
    try:
        import playsound
        print("✅ Python dependencies: OK (playsound available)")
    except ImportError:
        print("❌ Python dependencies: MISSING (playsound)")
        issues.append("Install playsound: pip install playsound")
        all_good = False
    
    # 6. Check required files
    required_files = ["color_presets.json", "sound/bell.mp3"]
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ Required file: {file_path}")
        else:
            print(f"❌ Required file: {file_path} NOT FOUND")
            issues.append(f"Ensure {file_path} exists in the application directory")
            all_good = False
    
    print("\n" + "=" * 40)
    
    if all_good:
        print("🎉 All requirements satisfied! Ready to enhance videos!")
        return True
    else:
        print("❌ Some requirements are missing. Please fix the following issues:")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
        print("\n💡 Fix these issues and restart the application.")
        return False

def has_nvidia_gpu():
    """Check if NVIDIA GPU is available for hardware acceleration"""
    try:
        result = subprocess.run(["nvidia-smi"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def has_handbrake():
    """Check if HandBrakeCLI is available"""
    try:
        result = subprocess.run(["HandBrakeCLI", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except FileNotFoundError:
        return False
