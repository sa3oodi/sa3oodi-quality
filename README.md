# 🎬 SA3OODI Quality - FFmpeg Video Enhancer

A simple yet powerful command-line tool for enhancing video quality using FFmpeg's `itsscale` parameter. This tool automatically detects your GPU and optimizes encoding settings for the best performance.

## ✨ Features

- 🚀 **GPU Acceleration**: Automatically detects NVIDIA GPU and uses hardware encoding (h264_nvenc)
- 💻 **CPU Fallback**: Falls back to CPU encoding (libx264) when no GPU is detected
- 🎯 **Smart Quality Settings**: Optimized presets for both GPU and CPU encoding
- 📁 **Drag & Drop Interface**: Simple file input via drag and drop
- 🔔 **Audio Notification**: Plays a bell sound when processing is complete
- ⚡ **Variable Frame Rate**: Uses `vsync vfr` for optimal frame handling

## 🛠️ Requirements

- **FFmpeg**: Must be installed and available in your system PATH
- **Python 3.6+**
- **Dependencies**: 
  - `playsound` library for audio notifications

## 📦 Installation

1. **Install FFmpeg** (if not already installed):
   - Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
   - Make sure it's added to your system PATH

2. **Install Python dependencies**:
   ```bash
   pip install playsound
   ```

3. **Download the project**:
   ```bash
   git clone https://github.com/sa3oodi/sa3oodi-quality.git
   cd sa3oodi-quality
   ```

## 🚀 Usage

### Method 1: Run Python Script
```bash
python app.py
```

### Method 2: Use Executable (Windows)
```bash
./dist/app.exe
```

### Steps:
1. Run the application
2. Drag and drop your video file into the terminal
3. Press Enter
4. Enter the itsscale value (e.g., `2` for TikTok quality enhancement)
5. Wait for processing to complete
6. Find your enhanced video with `_final.mp4` suffix

## ⚙️ How It Works

The tool uses FFmpeg's `itsscale` parameter to modify the video's perceived frame rate, which can improve quality in certain scenarios:

- **GPU Mode**: Uses `h264_nvenc` encoder with CQ 19 for fast, high-quality encoding
- **CPU Mode**: Uses `libx264` encoder with CRF 18 for maximum quality
- **Audio**: Copies original audio stream without re-encoding

## 🎯 Use Cases

- **TikTok Quality Trick**: Use itsscale value of `2` to enhance video quality for social media
- **Frame Rate Adjustment**: Modify perceived playback speed without changing duration
- **Quality Enhancement**: Improve video quality through re-encoding with optimized settings

## 📁 Project Structure

```
sa3oodi-quality/
├── app.py              # Main Python script
├── app.spec            # PyInstaller spec file
├── dist/               # Compiled executable
│   └── app.exe
├── sound/              # Audio assets
│   └── bell.mp3
└── README.md           # This file
```

## 🔧 Building Executable

To build your own executable using PyInstaller:

```bash
pip install pyinstaller
pyinstaller app.spec
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🐛 Troubleshooting

- **FFmpeg not found**: Make sure FFmpeg is installed and added to your system PATH
- **GPU not detected**: Install NVIDIA drivers and ensure `nvidia-smi` command works
- **Audio issues**: Make sure the `sound/bell.mp3` file is present in the project directory

## 📞 Support

If you encounter any issues or have questions, please open an issue on GitHub.

---

Made with ❤️ by [sa3oodi](https://github.com/sa3oodi)
