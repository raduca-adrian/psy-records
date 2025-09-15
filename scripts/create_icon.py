import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageDraw, ImageFont
import os

def create_psychological_records_icon():
    """Create a suggestive app icon for Psychological Records application"""
    
    # Icon dimensions (multiple sizes for .ico format)
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
        padding = max(2, size // 16)
        
        # Draw background circle (professional badge style)
        circle_radius = size // 2 - padding
        circle_center = (size // 2, size // 2)
        draw.ellipse([
            circle_center[0] - circle_radius,
            circle_center[1] - circle_radius,
            circle_center[0] + circle_radius,
            circle_center[1] + circle_radius
        ], fill=bg_color, outline=accent_color, width=max(1, size // 32))
        
        # Draw document/clipboard representation
        doc_width = size // 3
        doc_height = size // 2
        doc_x = circle_center[0] - doc_width // 2
        doc_y = circle_center[1] - doc_height // 2
        
        # Document background
        draw.rectangle([
            doc_x, doc_y,
            doc_x + doc_width, doc_y + doc_height
        ], fill=paper_color, outline=text_color, width=1)
        
        # Draw lines on document (suggesting text/records)
        line_spacing = max(2, size // 20)
        line_width = doc_width - 4
        for i in range(3):
            line_y = doc_y + (size // 10) + (i * line_spacing)
            if line_y < doc_y + doc_height - 4:
                draw.rectangle([
                    doc_x + 2, line_y,
                    doc_x + 2 + line_width - (i * 2), line_y + 1
                ], fill=bg_color)
        
        # Add psychological symbol (stylized brain/mind icon)
        if size >= 32:
            # Draw a simple brain-like symbol in the top-right
            brain_x = circle_center[0] + size // 8
            brain_y = circle_center[1] - size // 8
            brain_size = max(3, size // 10)
            
            # Left hemisphere
            draw.ellipse([
                brain_x - brain_size, brain_y - brain_size // 2,
                brain_x + 1, brain_y + brain_size // 2
            ], fill=highlight_color)
            
            # Right hemisphere  
            draw.ellipse([
                brain_x, brain_y - brain_size // 2,
                brain_x + brain_size, brain_y + brain_size // 2
            ], fill=highlight_color)
        
        # Add a small plus/cross symbol (medical association)
        if size >= 24:
            cross_size = max(2, size // 15)
            cross_x = circle_center[0] - size // 6
            cross_y = circle_center[1] + size // 6
            cross_thickness = max(1, size // 32)
            
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

def save_icon_files():
    """Save the icon in both PNG and ICO formats"""
    try:
        # Create the icons
        icon_images = create_psychological_records_icon()
        
        # Save PNG version (largest size)
        png_path = "D:/Code/testpy/assets/app_icon_new.png"
        icon_images[-1].save(png_path, "PNG")
        print(f"✅ PNG icon saved: {png_path}")
        
        # Save ICO version (multi-size)
        ico_path = "D:/Code/testpy/assets/app_icon_new.ico"
        icon_images[0].save(ico_path, "ICO", sizes=[(img.size[0], img.size[1]) for img in icon_images])
        print(f"✅ ICO icon saved: {ico_path}")
        
        # Create a preview window
        create_preview_window(icon_images)
        
    except Exception as e:
        print(f"❌ Error creating icon: {e}")

def create_preview_window(icon_images):
    """Create a preview window to show the new icon"""
    root = tk.Tk()
    root.title("Psychological Records - New App Icon Preview")
    root.geometry("600x400")
    root.configure(bg="#f0f0f0")
    
    # Title
    title_label = tk.Label(root, 
                          text="New App Icon Preview", 
                          font=("Arial", 16, "bold"),
                          bg="#f0f0f0")
    title_label.pack(pady=10)
    
    # Description
    desc_label = tk.Label(root, 
                         text="Suggestive icon design for Psychological Records application\nFeatures: Professional medical badge, document clipboard, brain symbol, medical cross",
                         font=("Arial", 10),
                         bg="#f0f0f0",
                         justify="center")
    desc_label.pack(pady=5)
    
    # Create frame for icon previews
    icon_frame = tk.Frame(root, bg="#f0f0f0")
    icon_frame.pack(pady=20, fill="both", expand=True)
    
    # Show different sizes
    sizes_to_show = [32, 48, 64, 128]
    for i, size in enumerate(sizes_to_show):
        if i < len(icon_images):
            # Get the corresponding icon image
            icon_idx = next((j for j, img in enumerate(icon_images) if img.size[0] == size), -1)
            if icon_idx >= 0:
                icon_img = icon_images[icon_idx]
                
                # Save temporary file and load as PhotoImage
                temp_path = f"temp_icon_{size}.png"
                icon_img.save(temp_path, "PNG")
                photo = tk.PhotoImage(file=temp_path)
                
                # Create label with icon
                icon_label = tk.Label(icon_frame, image=photo, bg="#f0f0f0")
                icon_label.image = photo  # Keep a reference
                icon_label.grid(row=0, column=i, padx=20, pady=10)
                
                # Size label
                size_label = tk.Label(icon_frame, text=f"{size}x{size}", font=("Arial", 8), bg="#f0f0f0")
                size_label.grid(row=1, column=i, padx=20)
                
                # Clean up temp file
                try:
                    os.remove(temp_path)
                except OSError:
                    pass
    
    # Buttons frame
    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(pady=20)
    
    def apply_icon():
        try:
            # Replace the old icon files
            import shutil
            shutil.copy("D:/Code/testpy/assets/app_icon_new.png", "D:/Code/testpy/assets/app_icon.png")
            shutil.copy("D:/Code/testpy/assets/app_icon_new.ico", "D:/Code/testpy/assets/app_icon.ico")
            messagebox.showinfo("Success", "New icon applied successfully!\nThe icon will be used in the next build.")
            root.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to apply icon: {e}")
    
    def close_preview():
        root.destroy()
    
    apply_btn = tk.Button(button_frame, text="Apply New Icon", command=apply_icon, 
                         bg="#4A90A4", fg="white", font=("Arial", 10, "bold"),
                         padx=20, pady=5)
    apply_btn.pack(side="left", padx=10)
    
    close_btn = tk.Button(button_frame, text="Close Preview", command=close_preview,
                         bg="#6c757d", fg="white", font=("Arial", 10),
                         padx=20, pady=5)
    close_btn.pack(side="left", padx=10)
    
    root.mainloop()

if __name__ == "__main__":
    print("🎨 Creating suggestive app icon for Psychological Records...")
    save_icon_files()
