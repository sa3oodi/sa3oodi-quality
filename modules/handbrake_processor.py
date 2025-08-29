"""
HandBrake Processor
Handles video compression using HandBrake CLI with Production Standard preset
"""
import subprocess
from .system_checker import has_handbrake

def ask_handbrake_preprocessing():
    """Ask user if they want to use HandBrake preprocessing"""
    print("\n🛠️  HandBrake Preprocessing (Optional)")
    print("=" * 45)
    print("📦 This will compress the video first to reduce file size while maintaining quality")
    print("⚙️  Settings: Production Standard preset, RF 27, Slower encoder")
    print("⏰ Note: This adds extra processing time but significantly reduces file size")
    print()
    
    while True:
        choice = input("Do you want to use HandBrake preprocessing? (y/n): ").lower().strip()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("❌ Please enter 'y' for yes or 'n' for no.")

def apply_handbrake_preprocessing(input_path, output_path):
    """Apply HandBrake preprocessing with Production Standard preset"""
    if not has_handbrake():
        print("❌ HandBrakeCLI not found! Please install HandBrake and ensure HandBrakeCLI is in your PATH.")
        print("💡 You can download HandBrake from: https://handbrake.fr/downloads.php")
        return False
    
    print("🛠️  Applying HandBrake preprocessing...")
    print("⚙️  Preset: Production Standard | Quality: RF 27 | Encoder: Slower")
    
    cmd = [
        "HandBrakeCLI",
        "-i", input_path,
        "-o", output_path,
        "--preset", "Production Standard",
        "--quality", "27",
        "--encoder-preset", "slower",
        "--audio-copy-mask", "aac,ac3,eac3,truehd,dts,dtshd,mp3,flac",
        "--audio-fallback", "av_aac"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("✅ HandBrake preprocessing completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ HandBrake preprocessing failed: {e}")
        return False
