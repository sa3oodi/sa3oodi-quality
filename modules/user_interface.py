"""
User Interface
Handles all user interactions and input validation
"""
import os

def drag_and_drop_prompt():
    """Get video file path from user with drag-and-drop support"""
    print("📁 Drag and drop the video file, then press Enter:")
    video_path = input("➡️ ").strip('"').strip()
    if not os.path.isfile(video_path):
        print("❌ File not found. Please try again.")
        exit()
    return video_path

def ask_itsscale():
    """Get itsscale value from user with input validation"""
    try:
        scale = float(input("🔢 Enter itsscale value (e.g., 2 for TikTok quality trick): "))
        return scale
    except ValueError:
        print("❌ Invalid number.")
        exit()

def generate_output_filename(base_name, color_presets, use_handbrake):
    """Generate appropriate output filename based on selected options"""
    # Create filename suffix based on selected presets
    if color_presets == ["none"] or not color_presets:
        preset_suffix = ""
    elif len(color_presets) == 1:
        preset_suffix = f"_{color_presets[0]}"
    else:
        # For multiple presets, create a shorter combined name
        preset_suffix = "_enhanced"
    
    # Add compression suffix if used
    compression_suffix = "_compressed" if use_handbrake else ""
    return f"{base_name}_final{preset_suffix}{compression_suffix}.mp4"

def show_file_size_comparison(original_path, final_path):
    """Display file size comparison if both files exist"""
    if os.path.exists(original_path) and os.path.exists(final_path):
        original_size = os.path.getsize(original_path) / (1024 * 1024)  # MB
        final_size = os.path.getsize(final_path) / (1024 * 1024)  # MB
        reduction = ((original_size - final_size) / original_size) * 100
        print(f"📊 File size: {original_size:.1f}MB → {final_size:.1f}MB ({reduction:.1f}% reduction)")
