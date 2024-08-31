import re
import colorsys
import numpy as np

def detect_color_type(color):
    """Detect the color format based on the input."""
    if isinstance(color, str):
        if color.startswith('#'):
            return 'hex'
        elif 'hsl' in color:
            return 'hsl'
    elif isinstance(color, (list, tuple)):
        if len(color) == 3:
            return 'rgb'
        elif len(color) == 4:
            return 'rgba'
    return None

def parse_hsl_string(hsl_string):
    """Parse HSL string into a tuple of (h, s, l)."""
    hsl_values = re.findall(r'\d+', hsl_string)
    return int(hsl_values[0]), int(hsl_values[1]), int(hsl_values[2])

def hex_to_rgb(hex_color):
    """Convert HEX to RGB."""
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    return tuple(int(hex_color[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

def rgb_to_hex(rgb_color):
    """Convert RGB to HEX."""
    return '#{:02x}{:02x}{:02x}'.format(*rgb_color)

def rgba_to_hex(rgba_color):
    """Convert RGBA to HEX (including alpha)."""
    return '#{:02x}{:02x}{:02x}{:02x}'.format(rgba_color[0], rgba_color[1], rgba_color[2], int(rgba_color[3] * 255))

def hex_to_rgba(hex_color, alpha=1):
    """Convert HEX to RGBA. If HEX has an alpha value, use it; otherwise, use the default."""
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 8:
        r, g, b, a = tuple(int(hex_color[i:i+2], 16) for i in range(0, 8, 2))
        return r, g, b, a
    else:
        r, g, b = hex_to_rgb(hex_color)
        return r, g, b, alpha

def rgb_to_hsl(rgb_color):
    """Convert RGB to HSL."""
    r, g, b = [x / 255.0 for x in rgb_color]
    h, l, s = colorsys.rgb_to_hls(r, g, b)
    return int(h * 360), int(s * 100), int(l * 100)

def hsl_to_rgb(hsl_color):
    """Convert HSL to RGB."""
    h, s, l = hsl_color
    r, g, b = colorsys.hls_to_rgb(h / 360, l / 100, s / 100)
    return int(r * 255), int(g * 255), int(b * 255)

def convert_color(color, to_format, alpha=1):
    """Convert the color to the desired format."""
    from_format = detect_color_type(color)
    
    if not from_format:
        raise ValueError("Unsupported color format.")
    
    has_alpha = False
    
    if from_format == 'hex':
        rgba_color = hex_to_rgba(color, alpha)
        rgb_color = rgba_color[:3]
        has_alpha = len(color) == 9  # HEX with alpha has 9 characters (including #)
    elif from_format == 'rgb':
        rgb_color = color
        rgba_color = rgb_color + (alpha,)
    elif from_format == 'rgba':
        rgb_color = color[:3]
        rgba_color = color
        has_alpha = True
    elif from_format == 'hsl':
        hsl_color = parse_hsl_string(color)
        rgb_color = hsl_to_rgb(hsl_color)
        rgba_color = rgb_color + (alpha,)
    
    if has_alpha:
        alpha = rgba_color[3]  # Use the alpha from the input color

    if to_format == 'hex':
        return np.array(rgb_to_hex(rgb_color))
    elif to_format == 'rgba':
        return np.array(rgba_color[:3] + (alpha,))
    elif to_format == 'rgb':
        return np.array(rgb_color)
    elif to_format == 'hsl':
        return np.array(rgb_to_hsl(rgb_color))
    
    raise ValueError(f"Unsupported target format: {to_format}")







if __name__ == "__main__":
    # Example usage:
    print(convert_color("#34a1eb", "rgba", alpha=0.8))  # HEX to RGBA
    print(convert_color((52, 161, 235), "hex"))         # RGB to HEX
    print(convert_color("#34a1eb1b", "rgba"))           # HEX to RGBA
    print(convert_color((52, 161, 235, 100), "hex"))    # RGBA to HEX
    print(convert_color("#34a1ebff", "rgba"))           # HEX with alpha to RGBA
    print(convert_color((52, 161, 235, 0.5), "rgba"))   # RGBA input, ignore default alpha