"""
Professional Video Enhancer with Color Correction
A modular video enhancement tool supporting FFmpeg and HandBrake processing
"""
import os
import sys
from playsound import playsound

# Fix Windows console encoding for Unicode characters
if sys.platform == "win32":
    try:
        # Try to set UTF-8 encoding for Windows console
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        # Fallback: replace Unicode characters with ASCII equivalents
        pass

# Import our custom modules
from modules.system_checker import check_system_requirements
from modules.preset_manager import choose_color_preset
from modules.handbrake_processor import ask_handbrake_preprocessing, apply_handbrake_preprocessing
from modules.ffmpeg_processor import apply_itsscale_with_encode
from modules.user_interface import (
    drag_and_drop_prompt, 
    ask_itsscale, 
    generate_output_filename, 
    show_file_size_comparison
)

def main():
    """Main application workflow"""
    print("Professional Video Enhancer with Color Correction")
    print("=" * 55)
    
    # Check system requirements first
    if not check_system_requirements():
        print("\nCannot start application due to missing requirements.")
        input("Press Enter to exit...")
        return
    
    print("\n" + "=" * 55)
    print("Starting Video Enhancement Process...")
    print()
    
    # Step 1: Get user inputs
    original_video_path = drag_and_drop_prompt()
    use_handbrake = ask_handbrake_preprocessing()
    scale = ask_itsscale()
    color_presets = choose_color_preset()  # Returns a list of preset keys
    
    base = os.path.splitext(os.path.basename(original_video_path))[0]
    
    # Step 2: HandBrake preprocessing (if requested)
    if use_handbrake:
        print(f"\n🛠️  Step 1/2: HandBrake Compression...")
        handbrake_output = f"{base}_compressed.mp4"
        
        if apply_handbrake_preprocessing(original_video_path, handbrake_output):
            input_for_ffmpeg = handbrake_output
            print(f"📦 Compressed file: {handbrake_output}")
        else:
            print("⚠️  HandBrake failed, proceeding with original file...")
            input_for_ffmpeg = original_video_path
    else:
        input_for_ffmpeg = original_video_path
    
    # Step 3: FFmpeg processing with itsscale and color correction
    step_number = "2/2" if use_handbrake else "1/1"
    print(f"\n🎬 Step {step_number}: Video Enhancement...")
    
    # Generate output filename
    final_output = generate_output_filename(base, color_presets, use_handbrake)
    
    # Apply FFmpeg processing
    apply_itsscale_with_encode(input_for_ffmpeg, scale, color_presets, final_output)
    
    # Step 4: Cleanup and final reporting
    # Cleanup intermediate file if HandBrake was used
    if use_handbrake and os.path.exists(handbrake_output) and input_for_ffmpeg == handbrake_output:
        try:
            os.remove(handbrake_output)
            print(f"🗑️  Cleaned up intermediate file: {handbrake_output}")
        except:
            print(f"⚠️  Could not remove intermediate file: {handbrake_output}")
    
    print(f"✅ Done! Final output saved to: {final_output}")
    
    # Show file size comparison if HandBrake was used
    if use_handbrake:
        show_file_size_comparison(original_video_path, final_output)
    
    # Play completion sound
    playsound("sound/bell.mp3")

if __name__ == "__main__":
    main()
