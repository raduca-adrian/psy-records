from PIL import Image, ImageDraw
import os

def create_app_icon():
    """Create a simple application icon"""
    # Create a 256x256 image
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Draw shield background
    shield_color = (52, 152, 219)  # Blue
    border_color = (41, 128, 185)  # Darker blue
    
    # Shield points (scaled to 256x256)
    center_x, center_y = size // 2, size // 2
    width, height = int(size * 0.6), int(size * 0.7)
    
    # Shield shape coordinates
    top = center_y - height // 2 + 20
    bottom = center_y + height // 2 - 20
    left = center_x - width // 2
    right = center_x + width // 2
    
    # Draw shield
    shield_points = [
        (center_x, top),
        (right, top + 30),
        (right, bottom - 40),
        (center_x, bottom),
        (left, bottom - 40),
        (left, top + 30)
    ]
    
    # Draw border
    draw.polygon(shield_points, fill=border_color)
    
    # Draw inner shield
    inner_points = [(x + (3 if i % 2 == 0 else -3), y + 3) for i, (x, y) in enumerate(shield_points)]
    draw.polygon(inner_points, fill=shield_color)
    
    # Draw lock symbol
    lock_x, lock_y = center_x, center_y
    lock_size = 40
    
    # Lock body
    draw.rectangle([
        lock_x - lock_size//2, lock_y,
        lock_x + lock_size//2, lock_y + lock_size
    ], fill=(255, 255, 255))
    
    # Lock shackle
    draw.arc([
        lock_x - lock_size//3, lock_y - lock_size//2,
        lock_x + lock_size//3, lock_y + lock_size//4
    ], start=0, end=180, fill=(255, 255, 255), width=8)
    
    # Lock hole
    draw.ellipse([
        lock_x - 6, lock_y + 10,
        lock_x + 6, lock_y + 22
    ], fill=shield_color)
    
    return img

if __name__ == "__main__":
    try:
        icon = create_app_icon()
        
        # Save as different formats
        icon.save("app_icon.png", "PNG")
        
        # Create ICO file for Windows
        icon.save("app_icon.ico", "ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
        
        print("✓ Icon files created successfully!")
        print("  - app_icon.png")
        print("  - app_icon.ico")
        
    except ImportError:
        print("PIL (Pillow) not installed. Creating a simple text-based icon description instead...")
        
        # Create a simple text description
        with open("icon_description.txt", "w") as f:
            f.write("""
Application Icon Description:
- A blue shield shape (security symbol)
- White lock icon in the center
- Colors: Blue (#3498db), Dark Blue (#2980b9), White (#ffffff)
- Represents security and data protection

To create an actual icon:
1. Install Pillow: pip install Pillow
2. Run this script again
3. Or use any icon creation tool with the description above
            """)
        print("✓ Icon description created: icon_description.txt")
