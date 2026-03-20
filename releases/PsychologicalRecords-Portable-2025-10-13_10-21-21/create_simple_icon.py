from PIL import Image, ImageDraw
import os

def create_simple_psychological_icon():
    """Create a simple but suggestive app icon for Psychological Records"""
    
    # Icon dimensions
    sizes = [16, 24, 32, 48, 64, 128, 256]
    
    # Color scheme - professional medical/psychological theme
    bg_color = "#2E4B6B"      # Professional blue
    accent_color = "#4A90A4"   # Light blue accent
    highlight_color = "#87CEEB" # Sky blue highlight
    text_color = "#FFFFFF"     # White text
    paper_color = "#F8F9FA"    # Off-white paper
    
    images = []
    
    for size in sizes:
        # Create new image with transparency
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Scale elements based on icon size
        padding = max(1, size // 16)
        
        # Draw background circle (professional badge style)
        circle_radius = size // 2 - padding
        circle_center = (size // 2, size // 2)
        
        # Ensure valid coordinates
        x1 = max(0, circle_center[0] - circle_radius)
        y1 = max(0, circle_center[1] - circle_radius)
        x2 = min(size, circle_center[0] + circle_radius)
        y2 = min(size, circle_center[1] + circle_radius)
        
        draw.ellipse([x1, y1, x2, y2], fill=bg_color, outline=accent_color, width=max(1, size // 32))
        
        # Draw document/clipboard representation (center)
        doc_width = max(4, size // 4)
        doc_height = max(6, size // 3)
        doc_x = circle_center[0] - doc_width // 2
        doc_y = circle_center[1] - doc_height // 2
        
        # Ensure document is within bounds
        doc_x = max(padding, min(doc_x, size - doc_width - padding))
        doc_y = max(padding, min(doc_y, size - doc_height - padding))
        
        # Document background
        draw.rectangle([
            doc_x, doc_y,
            doc_x + doc_width, doc_y + doc_height
        ], fill=paper_color, outline=accent_color, width=1)
        
        # Draw lines on document (suggesting text/records)
        if size >= 16:
            line_spacing = max(1, size // 20)
            for i in range(min(3, doc_height // (line_spacing + 1))):
                line_y = doc_y + 2 + (i * (line_spacing + 1))
                line_width = max(2, doc_width - 4 - i)
                if line_y < doc_y + doc_height - 2 and line_width > 0:
                    draw.rectangle([
                        doc_x + 2, line_y,
                        doc_x + 2 + line_width, line_y + 1
                    ], fill=bg_color)
        
        # Add psychological symbol (stylized mind/brain dots)
        if size >= 24:
            # Three small dots suggesting neural connections/thoughts
            dot_radius = max(1, size // 20)
            dots_x = circle_center[0] + size // 6
            dots_y = circle_center[1] - size // 6
            
            for i, (dx, dy) in enumerate([(0, 0), (-3, 3), (3, 3)]):
                dot_x = dots_x + dx
                dot_y = dots_y + dy
                if (0 <= dot_x - dot_radius and dot_x + dot_radius < size and 
                    0 <= dot_y - dot_radius and dot_y + dot_radius < size):
                    draw.ellipse([
                        dot_x - dot_radius, dot_y - dot_radius,
                        dot_x + dot_radius, dot_y + dot_radius
                    ], fill=highlight_color)
        
        # Add a small medical cross
        if size >= 20:
            cross_size = max(2, size // 15)
            cross_x = circle_center[0] - size // 6
            cross_y = circle_center[1] + size // 6
            cross_thickness = max(1, size // 40)
            
            # Ensure cross is within bounds
            if (cross_x - cross_size >= 0 and cross_x + cross_size < size and
                cross_y - cross_size >= 0 and cross_y + cross_size < size):
                
                # Horizontal line
                draw.rectangle([
                    cross_x - cross_size, cross_y - cross_thickness,
                    cross_x + cross_size, cross_y + cross_thickness
                ], fill=highlight_color)
                
                # Vertical line
                draw.rectangle([
                    cross_x - cross_thickness, cross_y - cross_size,
                    cross_x + cross_thickness, cross_y + cross_size
                ], fill=highlight_color)
        
        images.append(img)
    
    return images

def save_icons():
    """Save the new icons"""
    try:
        print("🎨 Creating suggestive app icon for Psychological Records...")
        
        # Create the icons
        icon_images = create_simple_psychological_icon()
        
        # Save PNG version (largest size)
        png_path = "assets/app_icon_new.png"
        icon_images[-1].save(png_path, "PNG")
        print(f"✅ PNG icon saved: {png_path}")
        
        # Save ICO version (multi-size)
        ico_path = "assets/app_icon_new.ico"
        icon_images[0].save(ico_path, "ICO", sizes=[(img.size[0], img.size[1]) for img in icon_images])
        print(f"✅ ICO icon saved: {ico_path}")
        
        # Show preview of largest size
        print(f"\n📋 Icon Description:")
        print(f"   • Professional medical blue color scheme")
        print(f"   • Document/clipboard representing records")
        print(f"   • Neural dots suggesting psychological/mental health")
        print(f"   • Medical cross for healthcare association")
        print(f"   • Clean, modern design suitable for professional use")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating icon: {e}")
        return False

def apply_new_icon():
    """Replace the current icon with the new one"""
    try:
        import shutil
        
        # Backup original icons
        if os.path.exists("assets/app_icon.png"):
            shutil.copy("assets/app_icon.png", "assets/app_icon_backup.png")
            print("📁 Backed up original PNG icon")
        
        if os.path.exists("assets/app_icon.ico"):
            shutil.copy("assets/app_icon.ico", "assets/app_icon_backup.ico")
            print("📁 Backed up original ICO icon")
        
        # Apply new icons
        shutil.copy("assets/app_icon_new.png", "assets/app_icon.png")
        shutil.copy("assets/app_icon_new.ico", "assets/app_icon.ico")
        
        print("✅ New icon applied successfully!")
        print("🔄 The new icon will be used in the next application build.")
        
        return True
        
    except Exception as e:
        print(f"❌ Error applying icon: {e}")
        return False

if __name__ == "__main__":
    if save_icons():
        print("\n" + "="*50)
        print("🎨 ICON CREATION COMPLETE")
        print("="*50)
        
        while True:
            choice = input("\nWould you like to apply this new icon? (y/n): ").lower().strip()
            if choice in ['y', 'yes']:
                apply_new_icon()
                break
            elif choice in ['n', 'no']:
                print("📝 New icon files saved as app_icon_new.png and app_icon_new.ico")
                print("   You can manually replace the original files when ready.")
                break
            else:
                print("Please enter 'y' for yes or 'n' for no.")
    else:
        print("❌ Icon creation failed.")
