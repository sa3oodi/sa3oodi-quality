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
from modules.ffmpeg_processor import apply_itsscale_with_encode, apply_filters_only, apply_itsscale_only
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
    
    if use_handbrake:
        # New workflow: 1) Apply filters, 2) HandBrake, 3) itsscale
        print(f"\n🎬 Step 1/3: Applying Color Filters...")
        
        # Apply filters first without itsscale
        filtered_output = f"{base}_filtered.mp4"
        apply_filters_only(original_video_path, color_presets, filtered_output)
        
        print(f"\n🛠️  Step 2/3: HandBrake Compression...")
        handbrake_output = f"{base}_compressed.mp4"
        
        if apply_handbrake_preprocessing(filtered_output, handbrake_output):
            print(f"📦 Compressed file: {handbrake_output}")
            
            print(f"\n⚡ Step 3/3: Applying itsscale trick...")
            final_output = generate_output_filename(base, color_presets, use_handbrake)
            apply_itsscale_only(handbrake_output, scale, final_output)
            
            # Cleanup intermediate files
            try:
                os.remove(filtered_output)
                os.remove(handbrake_output)
                print(f"🗑️  Cleaned up intermediate files")
            except:
                print(f"⚠️  Could not remove some intermediate files")
        else:
            print("⚠️  HandBrake failed, proceeding with filtered file and itsscale...")
            final_output = generate_output_filename(base, color_presets, False)
            apply_itsscale_only(filtered_output, scale, final_output)
            
            # Cleanup
            try:
                os.remove(filtered_output)
            except:
                pass
    else:
        # Original workflow: Apply filters and itsscale together
        print(f"\n🎬 Step 1/1: Video Enhancement...")
        final_output = generate_output_filename(base, color_presets, use_handbrake)
        apply_itsscale_with_encode(original_video_path, scale, color_presets, final_output)
    
    print(f"✅ Done! Final output saved to: {final_output}")
    
    # Show file size comparison if HandBrake was used
    if use_handbrake:
        show_file_size_comparison(original_video_path, final_output)
    
    # Play completion sound
    playsound("sound/bell.mp3")

if __name__ == "__main__":
    main()
