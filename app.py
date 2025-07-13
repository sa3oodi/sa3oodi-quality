import os
import subprocess
from playsound import playsound  # Make sure to install with: pip install playsound

def has_nvidia_gpu():
    try:
        result = subprocess.run(["nvidia-smi"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def drag_and_drop_prompt():
    print("📁 Drag and drop the video file, then press Enter:")
    video_path = input("➡️ ").strip('"').strip()
    if not os.path.isfile(video_path):
        print("❌ File not found. Please try again.")
        exit()
    return video_path

def ask_itsscale():
    try:
        scale = float(input("🔢 Enter itsscale value (e.g., 2 for TikTok quality trick): "))
        return scale
    except ValueError:
        print("❌ Invalid number.")
        exit()

def apply_itsscale_with_encode(input_path, itsscale_value, output_path):
    use_gpu = has_nvidia_gpu()

    if use_gpu:
        print("🟢 NVIDIA GPU detected — using h264_nvenc for encoding (CPU decoding).")
        cmd = [
            "ffmpeg", "-y",
            "-itsscale", str(itsscale_value),
            "-i", input_path,
            "-vsync", "vfr",
            "-c:v", "h264_nvenc",
            "-preset", "fast",
            "-cq", "19",
            "-c:a", "copy",
            output_path
        ]
    else:
        print("🔵 No NVIDIA GPU found — using CPU for encoding.")
        cmd = [
            "ffmpeg", "-y",
            "-itsscale", str(itsscale_value),
            "-i", input_path,
            "-vsync", "vfr",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "18",
            "-c:a", "copy",
            output_path
        ]

    subprocess.run(cmd, check=True)

def main():
    print("🎬 FFmpeg Video Enhancer CLI")
    video_path = drag_and_drop_prompt()
    scale = ask_itsscale()
    base = os.path.splitext(os.path.basename(video_path))[0]
    final_output = f"{base}_final.mp4"
    apply_itsscale_with_encode(video_path, scale, final_output)
    print(f"✅ Done! Output saved to: {final_output}")
    playsound("sound/bell.mp3")

if __name__ == "__main__":
    main()
