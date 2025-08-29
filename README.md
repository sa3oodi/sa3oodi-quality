# Professional Video Enhancer with Color Correction

A powerful Python-based video enhancement tool that combines FFmpeg processing with professional color correction presets. Features intelligent preset combination, HandBrake compression integration, and hardware acceleration support.

## 🌟 Key Features

- **Multi-Preset Color Correction**: Combine multiple professional presets (HDR-Vivid Colors, Sharpness levels, Brightness enhancement)
- **HandBrake Integration**: Optional compression preprocessing with Production Standard settings
- **Hardware Acceleration**: Automatic NVIDIA GPU detection with fallback to CPU encoding
- **Intelligent Filter Combination**: Smart merging of multiple color correction filters
- **Professional Presets**: 10 carefully crafted enhancement presets for various video styles
- **itsscale Enhancement**: Built-in support for quality improvement techniques
- **Modular Architecture**: Clean, maintainable code structure with separated concerns

## 🎨 Available Presets

1. **No Color Correction** - Keep original video colors
2. **HDR - Vivid Colors** - Enhanced contrast and vibrant saturation
3. **Colors - Low** - Subtle color enhancement
4. **Colors - Medium** - Balanced color improvement  
5. **Colors - High** - Strong color enhancement
6. **Sharpness and Clarity - Low** - Gentle sharpening
7. **Sharpness and Clarity - Medium** - Moderate sharpening
8. **Sharpness and Clarity - High** - Strong sharpening
9. **High Brightness Locations** - Enhance bright areas
10. **Dark Shadow Areas** - Improve dark regions

## 🚀 Usage

1. Run the application: `python main.py`
2. Drag and drop your video file
3. Choose HandBrake preprocessing (optional)
4. Enter itsscale value (recommended: 2)
5. Select color preset(s) - supports combinations like "2,8,6"
6. Wait for processing to complete

## 📋 System Requirements

- Python 3.6+
- FFmpeg (with PATH configuration)
- HandBrake CLI (optional, for compression)
- NVIDIA GPU (optional, for hardware acceleration)

### Required Python Packages
```bash
pip install playsound
```

## 📦 Installation

1. Install FFmpeg: Download from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Install HandBrake (optional): Download from [https://handbrake.fr/downloads.php](https://handbrake.fr/downloads.php)
3. Install Python dependencies: `pip install playsound`
4. Run: `python main.py`

## 🔧 Technical Details

- **GPU Encoding**: h264_nvenc with CQ 20 for NVIDIA GPUs
- **CPU Encoding**: libx264 with CRF 20 for compatibility
- **HandBrake Settings**: Production Standard preset, RF 27, Slower encoder
- **Filter Intelligence**: Automatic odd matrix size conversion for unsharp filters
- **Preset Combination**: Multiplicative blending for contrast/saturation, additive for brightness/colorbalance

## 📁 Project Structure

```
project/
├── main.py                      # Main application entry point
├── modules/                     # Modular components
│   ├── __init__.py             # Module initialization
│   ├── system_checker.py       # System requirements validation
│   ├── preset_manager.py       # Color preset management
│   ├── handbrake_processor.py  # HandBrake compression handling
│   ├── ffmpeg_processor.py     # FFmpeg video processing
│   └── user_interface.py       # User interaction components
├── color_presets.json          # Color correction presets
├── sound/bell.mp3              # Completion notification
├── app.py                      # Legacy monolithic version
└── README.md                   # This file
```

## 🏗️ Architecture

The application follows a modular design pattern:

- **main.py**: Application entry point and workflow orchestration
- **system_checker**: Validates dependencies and system requirements
- **preset_manager**: Handles color preset loading, selection, and intelligent combination
- **handbrake_processor**: Manages video compression with HandBrake CLI
- **ffmpeg_processor**: Core video enhancement using FFmpeg with hardware acceleration
- **user_interface**: User input handling and output filename generation

## 🔄 Migration from Legacy Version

The legacy `app.py` file contains all functionality in a single file. The new modular structure provides:

- **Better Maintainability**: Each module has a specific responsibility
- **Easier Testing**: Individual components can be tested separately
- **Code Reusability**: Modules can be imported and used independently
- **Cleaner Code**: Better organization and separation of concerns

To continue using the legacy version, run `python app.py`. For the new modular version, use `python main.py`.

## 🐛 Troubleshooting

- **FFmpeg not found**: Ensure FFmpeg is installed and added to your system PATH
- **HandBrake not found**: Download HandBrake CLI from the official website
- **GPU encoding issues**: Update NVIDIA drivers or fallback will use CPU encoding
- **Audio playback error**: Ensure `playsound` package is installed properly

## 📈 Performance Tips

- Use NVIDIA GPU for faster encoding when available
- HandBrake preprocessing reduces final file size but adds processing time
- Multiple preset combinations may increase processing time
- Higher itsscale values improve quality but increase file size
