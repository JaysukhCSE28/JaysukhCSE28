#!/usr/bin/env python3
"""
Dot-Matrix Portrait Generator: Converts images to dot-matrix SVG.
"""

import argparse
from PIL import Image, ImageOps, ImageEnhance
import sys

def image_to_dot_matrix(input_path, output_path, cols=50, equalize=True, detail=0.5, color="#a78bfa"):
    """
    Convert an image to a dot-matrix SVG.
    
    Args:
        input_path: Path to input image
        output_path: Path to output SVG
        cols: Number of columns in the dot matrix
        equalize: Whether to equalize histogram
        detail: Detail level (0-1) for brightness threshold
        color: Hex color for dots
    """
    try:
        img = Image.open(input_path).convert("L")
        
        # Equalize if requested
        if equalize:
            img = ImageOps.equalize(img)
        
        # Resize to match column count
        aspect = img.size[1] / img.size[0]
        rows = int(cols * aspect)
        img = img.resize((cols, rows), Image.Resampling.LANCZOS)
        
        # Get pixel data
        pixels = img.getdata()
        width, height = img.size
        
        # Threshold
        threshold = int(255 * (1 - detail))
        
        # Generate SVG
        dot_radius = 4
        svg_width = cols * dot_radius * 2 + 20
        svg_height = rows * dot_radius * 2 + 20
        
        svg = f'<svg width="{svg_width}" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">\n'
        svg += '<rect width="{}" height="{}" fill="#1e1e2e"/>\n'.format(svg_width, svg_height)
        
        for y in range(height):
            for x in range(width):
                pixel = pixels[y * width + x]
                if pixel < threshold:
                    cx = 10 + x * dot_radius * 2 + dot_radius
                    cy = 10 + y * dot_radius * 2 + dot_radius
                    svg += f'<circle cx="{cx}" cy="{cy}" r="{dot_radius}" fill="{color}" opacity="{1 - pixel/255}"/>\n'
        
        svg += '</svg>'
        
        with open(output_path, 'w') as f:
            f.write(svg)
        
        print(f"✅ Generated dot-matrix SVG: {output_path}")
        
    except FileNotFoundError:
        print(f"❌ Input file not found: {input_path}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate dot-matrix SVG from image")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("-o", "--output", default="assets/portrait.svg", help="Output SVG path")
    parser.add_argument("--cols", type=int, default=50, help="Number of columns")
    parser.add_argument("--equalize", action="store_true", default=True, help="Equalize histogram")
    parser.add_argument("--detail", type=float, default=0.5, help="Detail level (0-1)")
    parser.add_argument("--color", default="#a78bfa", help="Hex color for dots")
    
    args = parser.parse_args()
    image_to_dot_matrix(args.input, args.output, args.cols, args.equalize, args.detail, args.color)
