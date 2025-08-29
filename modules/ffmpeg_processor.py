"""
FFmpeg Processor
Handles video enhancement using FFmpeg with itsscale and color correction filters
"""
import subprocess
from .system_checker import has_nvidia_gpu
from .preset_manager import load_color_presets, combine_preset_filters

def apply_itsscale_with_encode(input_path, itsscale_value, preset_keys, output_path):
    """Apply itsscale and color correction using FFmpeg with optimal encoder selection"""
    use_gpu = has_nvidia_gpu()
    color_presets = load_color_presets()
    
    # Combine multiple presets into one filter
    combined_filter = combine_preset_filters(color_presets, preset_keys)
    
    # Build video filter chain
    video_filters = []
    
    # Add combined color correction filter if specified
    if combined_filter:
        video_filters.append(combined_filter)
    
    # Combine all filters
    filter_string = ",".join(video_filters) if video_filters else None

    if use_gpu:
        print("🟢 NVIDIA GPU detected — using h264_nvenc for encoding (CPU decoding).")
        cmd = [
            "ffmpeg", "-y",
            "-itsscale", str(itsscale_value),
            "-i", input_path,
            "-c:v", "h264_nvenc",
            "-preset", "fast",
            "-profile:v", "main",
            "-cq", "20",
            "-pix_fmt", "yuv420p",
            "-c:a", "copy"
        ]
        
        # Add video filter if we have any
        if filter_string:
            cmd.extend(["-vf", filter_string])
            
        cmd.append(output_path)
    else:
        print("🔵 No NVIDIA GPU found — using CPU for encoding.")
        cmd = [
            "ffmpeg", "-y",
            "-itsscale", str(itsscale_value),
            "-i", input_path,
            "-c:v", "libx264",
            "-preset", "medium",
            "-profile:v", "main",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            "-movflags", "+faststart",
            "-c:a", "copy"
        ]
        
        # Add video filter if we have any
        if filter_string:
            cmd.extend(["-vf", filter_string])
            
        cmd.append(output_path)

    # Display what's being applied
    if len(preset_keys) > 1 and preset_keys != ["none"]:
        preset_names = [color_presets[key]['name'] for key in preset_keys if key != "none"]
        print(f"🎬 Applying combination: {' + '.join(preset_names)}")
    elif preset_keys and preset_keys[0] != "none":
        print(f"🎬 Applying: {color_presets[preset_keys[0]]['name']}")
    
    if combined_filter:
        print(f"🔧 Combined Filter: {combined_filter}")
    
    subprocess.run(cmd, check=True)
