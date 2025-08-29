"""
Preset Manager
Handles loading, combining, and managing color correction presets
"""
import json

def load_color_presets():
    """Load color presets from JSON file, with fallback to built-in presets"""
    try:
        with open("color_presets.json", "r") as f:
            data = json.load(f)
            return data["presets"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError):
        # Fallback to built-in presets if file doesn't exist or is corrupted
        return {
            "none": {
                "name": "No Color Correction",
                "description": "Apply no color effects - keep original video colors",
                "filter": ""
            },
            "cinematic": {
                "name": "Cinematic Look",
                "description": "Film-like color grading with enhanced contrast and cooler tones",
                "filter": "eq=contrast=1.2:brightness=0.05:saturation=1.1,colorbalance=rs=-0.1:gs=0.05:bs=0.15"
            },
            "vibrant": {
                "name": "Vibrant Colors",
                "description": "Increased saturation and sharpness for bold, eye-catching videos",
                "filter": "eq=contrast=1.3:saturation=1.4:gamma=1.1,unsharp=5:5:1.0:5:5:0.0"
            }
        }

def choose_color_preset():
    """Interactive preset selection interface with multi-selection support"""
    color_presets = load_color_presets()
    print("\n🎨 Available Video Enhancement Presets:")
    print("=" * 50)
    print("💡 You can select multiple presets by entering numbers separated by commas")
    print("   Example: 2,8,6 to combine Colors-Medium + Sharpness-High + Bright Areas")
    print()
    
    preset_keys = list(color_presets.keys())
    for i, key in enumerate(preset_keys, 1):
        preset = color_presets[key]
        print(f"{i:2d}. {preset['name']}")
        print(f"     {preset['description']}")
        print()
    
    try:
        user_input = input(f"Choose preset(s) (1-{len(preset_keys)}) or comma-separated (e.g., 2,8,6): ").strip()
        
        if ',' in user_input:
            # Multiple presets selected
            choices = [int(x.strip()) - 1 for x in user_input.split(',')]
            selected_keys = []
            selected_names = []
            
            for choice in choices:
                if 0 <= choice < len(preset_keys):
                    key = preset_keys[choice]
                    if key != "none":  # Skip "none" in combinations
                        selected_keys.append(key)
                        selected_names.append(color_presets[key]['name'])
            
            if selected_keys:
                print(f"✅ Selected combination: {' + '.join(selected_names)}")
                return selected_keys
            else:
                print("❌ No valid presets selected. Using no color correction.")
                return ["none"]
        else:
            # Single preset selected
            choice = int(user_input) - 1
            if 0 <= choice < len(preset_keys):
                selected_key = preset_keys[choice]
                selected_preset = color_presets[selected_key]
                print(f"✅ Selected: {selected_preset['name']}")
                return [selected_key]
            else:
                print("❌ Invalid choice. Using no color correction.")
                return ["none"]
    except ValueError:
        print("❌ Invalid input. Using no color correction.")
        return ["none"]

def combine_preset_filters(color_presets, preset_keys):
    """Intelligently combine multiple preset filters into one optimized filter chain"""
    if not preset_keys or preset_keys == ["none"]:
        return ""
    
    # Separate different types of adjustments
    eq_params = {
        'contrast': 1.0,
        'brightness': 0.0,
        'saturation': 1.0,
        'gamma': 1.0
    }
    
    colorbalance_params = {
        'rs': 0.0,
        'gs': 0.0,
        'bs': 0.0
    }
    
    unsharp_settings = None
    curves_settings = []
    
    # Process each selected preset
    for key in preset_keys:
        if key == "none":
            continue
            
        preset_filter = color_presets[key]["filter"]
        if not preset_filter:
            continue
        
        # Parse the filter string to extract parameters
        parts = preset_filter.split(',')
        
        for part in parts:
            part = part.strip()
            
            if part.startswith('eq='):
                # Parse eq parameters
                eq_part = part[3:]  # Remove 'eq='
                params = eq_part.split(':')
                for param in params:
                    if '=' in param:
                        name, value = param.split('=', 1)
                        if name in eq_params:
                            # Combine values intelligently
                            if name in ['contrast', 'saturation', 'gamma']:
                                # Multiply factors (1.2 * 1.1 = 1.32)
                                eq_params[name] *= float(value)
                            else:  # brightness
                                # Add brightness values
                                eq_params[name] += float(value)
            
            elif part.startswith('colorbalance='):
                # Parse colorbalance parameters
                cb_part = part[13:]  # Remove 'colorbalance='
                params = cb_part.split(':')
                for param in params:
                    if '=' in param:
                        name, value = param.split('=', 1)
                        if name in colorbalance_params:
                            # Add colorbalance values
                            colorbalance_params[name] += float(value)
            
            elif part.startswith('unsharp='):
                # Take the strongest unsharp setting and ensure odd matrix sizes
                unsharp_part = part[8:]  # Remove 'unsharp='
                params = unsharp_part.split(':')
                if len(params) >= 3:
                    strength = float(params[2])
                    if unsharp_settings is None or strength > float(unsharp_settings.split(':')[2]):
                        # Ensure matrix sizes are odd numbers
                        luma_x = int(params[0])
                        luma_y = int(params[1])
                        chroma_x = int(params[3]) if len(params) > 3 else luma_x
                        chroma_y = int(params[4]) if len(params) > 4 else luma_y
                        
                        # Convert even numbers to odd
                        if luma_x % 2 == 0:
                            luma_x = luma_x - 1 if luma_x > 1 else 3
                        if luma_y % 2 == 0:
                            luma_y = luma_y - 1 if luma_y > 1 else 3
                        if chroma_x % 2 == 0:
                            chroma_x = chroma_x - 1 if chroma_x > 1 else 3
                        if chroma_y % 2 == 0:
                            chroma_y = chroma_y - 1 if chroma_y > 1 else 3
                        
                        # Rebuild unsharp parameters with odd matrix sizes
                        luma_amount = params[2]
                        chroma_amount = params[5] if len(params) > 5 else "0.0"
                        unsharp_settings = f"{luma_x}:{luma_y}:{luma_amount}:{chroma_x}:{chroma_y}:{chroma_amount}"
            
            elif part.startswith('curves='):
                # Collect curves settings
                curves_settings.append(part)
    
    # Build the combined filter
    filter_parts = []
    
    # Add eq filter
    eq_filter = f"eq=contrast={eq_params['contrast']:.3f}:brightness={eq_params['brightness']:.3f}:saturation={eq_params['saturation']:.3f}:gamma={eq_params['gamma']:.3f}"
    filter_parts.append(eq_filter)
    
    # Add colorbalance if any adjustments
    if any(abs(v) > 0.001 for v in colorbalance_params.values()):
        cb_filter = f"colorbalance=rs={colorbalance_params['rs']:.3f}:gs={colorbalance_params['gs']:.3f}:bs={colorbalance_params['bs']:.3f}"
        filter_parts.append(cb_filter)
    
    # Add curves (combine if multiple)
    if curves_settings:
        # For simplicity, just use the first curves setting
        # In practice, you might want to combine them more intelligently
        filter_parts.append(curves_settings[0])
    
    # Add unsharp
    if unsharp_settings:
        filter_parts.append(f"unsharp={unsharp_settings}")
    
    return ','.join(filter_parts)
