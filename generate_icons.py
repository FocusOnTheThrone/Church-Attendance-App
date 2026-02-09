#!/usr/bin/env python3
"""
Generate PWA app icons using PIL (Python Imaging Library).
Requires: pip install Pillow
"""

from PIL import Image, ImageDraw, ImageFont
import os

def generate_icon(size, maskable=False):
    """Generate a simple icon with app name and optional padding for maskable icons."""
    # Create image
    if maskable:
        # Maskable icons need padding (safe zone is ~80% of the image)
        bg_color = (13, 110, 253)  # Bootstrap primary blue
    else:
        bg_color = (13, 110, 253)  # Bootstrap primary blue
    
    img = Image.new('RGB', (size, size), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw a simple cross or church symbol in the center
    padding = size // 6
    
    # Draw a simple church/cross shape
    # Center circle
    circle_radius = size // 6
    cx, cy = size // 2, size // 2
    draw.ellipse(
        [(cx - circle_radius, cy - circle_radius), (cx + circle_radius, cy + circle_radius)],
        fill=(255, 255, 255)
    )
    
    # Vertical line of cross
    line_thickness = size // 20
    draw.rectangle(
        [(cx - line_thickness, cy - size // 3), (cx + line_thickness, cy + size // 3)],
        fill=(255, 255, 255)
    )
    
    # Horizontal line of cross
    draw.rectangle(
        [(cx - size // 3, cy - line_thickness), (cx + size // 3, cy + line_thickness)],
        fill=(255, 255, 255)
    )
    
    return img

def main():
    """Generate all required PWA icons."""
    icons_dir = 'static/icons'
    os.makedirs(icons_dir, exist_ok=True)
    
    print("Generating PWA app icons...")
    
    # Generate standard icons
    sizes = [192, 512]
    for size in sizes:
        print(f"  Creating icon-{size}.png...", end=" ")
        icon = generate_icon(size)
        icon.save(os.path.join(icons_dir, f'icon-{size}.png'))
        print("✓")
    
    # Generate maskable icons (with safe zone padding)
    for size in sizes:
        print(f"  Creating icon-{size}-maskable.png...", end=" ")
        icon = generate_icon(size, maskable=True)
        icon.save(os.path.join(icons_dir, f'icon-{size}-maskable.png'))
        print("✓")
    
    print("\n✅ Icons generated successfully!")
    print(f"📁 Icons saved to: {icons_dir}/")
    print("\nGenerated files:")
    print("  - icon-192.png (standard icon)")
    print("  - icon-192-maskable.png (adaptive icon for Android)")
    print("  - icon-512.png (splash screen icon)")
    print("  - icon-512-maskable.png (adaptive icon for Android)")
    print("\n💡 Tip: For production, replace these with your actual app logo.")

if __name__ == '__main__':
    main()
