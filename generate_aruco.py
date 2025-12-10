#!/usr/bin/env python3
"""
ArUco Marker Generator

This script generates ArUco markers for computer vision applications.
ArUco markers are square fiducial markers commonly used for camera calibration,
pose estimation, and augmented reality.
"""

import cv2
import numpy as np
import argparse
import os
from PIL import Image, ImageDraw, ImageFont


def generate_aruco_marker(marker_id, dictionary_name='DICT_4X4_50', size=200, output_path=None):
    """
    Generate an ArUco marker.
    
    Args:
        marker_id (int): The ID of the marker to generate (0-based)
        dictionary_name (str): The ArUco dictionary to use (default: DICT_4X4_50)
        size (int): The size of the marker in pixels (default: 200)
        output_path (str): Path to save the marker image. If None, displays the marker.
    
    Returns:
        numpy.ndarray: The generated marker image
    """
    # Map dictionary names to OpenCV constants and their max IDs
    aruco_dict_map = {
        'DICT_4X4_50': (cv2.aruco.DICT_4X4_50, 49),
        'DICT_4X4_100': (cv2.aruco.DICT_4X4_100, 99),
        'DICT_4X4_250': (cv2.aruco.DICT_4X4_250, 249),
        'DICT_4X4_1000': (cv2.aruco.DICT_4X4_1000, 999),
        'DICT_5X5_50': (cv2.aruco.DICT_5X5_50, 49),
        'DICT_5X5_100': (cv2.aruco.DICT_5X5_100, 99),
        'DICT_5X5_250': (cv2.aruco.DICT_5X5_250, 249),
        'DICT_5X5_1000': (cv2.aruco.DICT_5X5_1000, 999),
        'DICT_6X6_50': (cv2.aruco.DICT_6X6_50, 49),
        'DICT_6X6_100': (cv2.aruco.DICT_6X6_100, 99),
        'DICT_6X6_250': (cv2.aruco.DICT_6X6_250, 249),
        'DICT_6X6_1000': (cv2.aruco.DICT_6X6_1000, 999),
        'DICT_7X7_50': (cv2.aruco.DICT_7X7_50, 49),
        'DICT_7X7_100': (cv2.aruco.DICT_7X7_100, 99),
        'DICT_7X7_250': (cv2.aruco.DICT_7X7_250, 249),
        'DICT_7X7_1000': (cv2.aruco.DICT_7X7_1000, 999),
    }
    
    if dictionary_name not in aruco_dict_map:
        raise ValueError(f"Invalid dictionary name. Choose from: {list(aruco_dict_map.keys())}")
    
    dict_constant, max_id = aruco_dict_map[dictionary_name]
    
    # Validate marker ID is within valid range for the dictionary
    if marker_id < 0 or marker_id > max_id:
        raise ValueError(f"Marker ID {marker_id} is out of range for {dictionary_name}. Valid range: 0-{max_id}")
    
    # Get the ArUco dictionary
    aruco_dict = cv2.aruco.getPredefinedDictionary(dict_constant)
    
    # Generate the marker
    marker_image = cv2.aruco.generateImageMarker(aruco_dict, marker_id, size)
    
    # Save or display the marker
    if output_path:
        cv2.imwrite(output_path, marker_image)
        print(f"ArUco marker {marker_id} saved to {output_path}")
    
    return marker_image


def generate_multiple_markers(start_id, count, dictionary_name='DICT_4X4_50', 
                              size=200, output_dir='aruco_markers'):
    """
    Generate multiple ArUco markers.
    
    Args:
        start_id (int): Starting marker ID
        count (int): Number of markers to generate
        dictionary_name (str): The ArUco dictionary to use
        size (int): The size of each marker in pixels
        output_dir (str): Directory to save the markers
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    for i in range(count):
        marker_id = start_id + i
        output_path = os.path.join(output_dir, f'aruco_marker_{marker_id}.png')
        generate_aruco_marker(marker_id, dictionary_name, size, output_path)
    
    print(f"\nGenerated {count} markers in '{output_dir}' directory")


def mm_to_pixels(mm, dpi=300):
    """
    Convert millimeters to pixels at a given DPI.
    
    Args:
        mm (float): Size in millimeters
        dpi (int): Dots per inch (default: 300 for print quality)
    
    Returns:
        int: Size in pixels
    """
    inches = mm / 25.4
    return int(inches * dpi)


def generate_print_layout(marker_ids, dictionary_name='DICT_4X4_50', 
                          format_type='a4', output_path='aruco_print_layout.png',
                          dpi=300, margin_mm=10):
    """
    Generate a print layout with multiple ArUco markers for specific paper formats.
    
    Args:
        marker_ids (list): List of marker IDs to include in the layout
        dictionary_name (str): The ArUco dictionary to use
        format_type (str): Paper format - 'creditcard', 'a4', or 'a5'
        output_path (str): Path to save the layout image
        dpi (int): Resolution in dots per inch (default: 300 for print quality)
        margin_mm (float): Margin in millimeters (default: 10mm)
    """
    # Define paper dimensions in millimeters (width x height)
    format_sizes = {
        'creditcard': (85.60, 53.98),  # Standard credit card size
        'a4': (210, 297),               # A4 paper
        'a5': (148, 210),               # A5 paper
    }
    
    if format_type not in format_sizes:
        raise ValueError(f"Invalid format type. Choose from: {list(format_sizes.keys())}")
    
    # Get paper dimensions in pixels
    paper_width_mm, paper_height_mm = format_sizes[format_type]
    paper_width_px = mm_to_pixels(paper_width_mm, dpi)
    paper_height_px = mm_to_pixels(paper_height_mm, dpi)
    margin_px = mm_to_pixels(margin_mm, dpi)
    
    # Create white background
    layout_image = Image.new('RGB', (paper_width_px, paper_height_px), 'white')
    draw = ImageDraw.Draw(layout_image)
    
    # Calculate marker size and spacing based on format
    available_width = paper_width_px - (2 * margin_px)
    available_height = paper_height_px - (2 * margin_px)
    
    num_markers = len(marker_ids)
    
    if format_type == 'creditcard':
        # For credit card, place one large marker centered
        marker_size_px = min(available_width, available_height) - mm_to_pixels(10, dpi)
        cols, rows = 1, 1
    elif format_type == 'a5':
        # For A5, arrange in 2 columns
        cols = 2
        rows = (num_markers + cols - 1) // cols  # Ceiling division
        marker_size_px = min(
            (available_width - mm_to_pixels(10, dpi) * (cols - 1)) // cols,
            (available_height - mm_to_pixels(10, dpi) * (rows - 1)) // rows
        )
    else:  # a4
        # For A4, arrange in 3 columns
        cols = 3
        rows = (num_markers + cols - 1) // cols  # Ceiling division
        marker_size_px = min(
            (available_width - mm_to_pixels(10, dpi) * (cols - 1)) // cols,
            (available_height - mm_to_pixels(10, dpi) * (rows - 1)) // rows
        )
    
    # Limit marker size for readability
    marker_size_px = min(marker_size_px, mm_to_pixels(80, dpi))
    
    spacing_px = mm_to_pixels(10, dpi)
    
    # Generate and place markers
    for idx, marker_id in enumerate(marker_ids):
        if idx >= rows * cols:
            print(f"Warning: Not all markers fit on the page. Only showing first {rows * cols} markers.")
            break
        
        # Generate marker
        marker_img_cv = generate_aruco_marker(marker_id, dictionary_name, marker_size_px, None)
        
        # Convert from OpenCV (numpy array) to PIL Image
        marker_img_pil = Image.fromarray(marker_img_cv)
        
        # Calculate position
        col = idx % cols
        row = idx // cols
        
        # Center the grid on the page
        total_width = cols * marker_size_px + (cols - 1) * spacing_px
        total_height = rows * marker_size_px + (rows - 1) * spacing_px
        start_x = margin_px + (available_width - total_width) // 2
        start_y = margin_px + (available_height - total_height) // 2
        
        x = start_x + col * (marker_size_px + spacing_px)
        y = start_y + row * (marker_size_px + spacing_px)
        
        # Paste marker onto layout
        layout_image.paste(marker_img_pil, (x, y))
        
        # Add marker ID label below the marker
        try:
            # Try to use a default font, fall back to basic if not available
            font_size = max(12, marker_size_px // 20)
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", font_size)
            except:
                font = ImageFont.load_default()
        except:
            font = None
        
        label_text = f"ID: {marker_id}"
        
        # Get text bounding box for centering
        if font:
            bbox = draw.textbbox((0, 0), label_text, font=font)
            text_width = bbox[2] - bbox[0]
        else:
            text_width = len(label_text) * 6  # Rough estimate for default font
        
        label_x = x + (marker_size_px - text_width) // 2
        label_y = y + marker_size_px + 5
        
        draw.text((label_x, label_y), label_text, fill='black', font=font)
    
    # Add border for crop marks
    draw.rectangle(
        [(margin_px // 2, margin_px // 2), 
         (paper_width_px - margin_px // 2, paper_height_px - margin_px // 2)],
        outline='lightgray',
        width=1
    )
    
    # Save the layout
    layout_image.save(output_path, dpi=(dpi, dpi))
    print(f"\nPrint layout saved to {output_path}")
    print(f"Format: {format_type.upper()}, DPI: {dpi}, Paper size: {paper_width_mm}mm x {paper_height_mm}mm")
    print(f"Number of markers: {min(num_markers, rows * cols)}")
    
    return layout_image


def main():
    parser = argparse.ArgumentParser(
        description='Generate ArUco markers for computer vision applications',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a single marker with ID 0
  python generate_aruco.py --id 0
  
  # Generate marker with ID 5 and save to custom path
  python generate_aruco.py --id 5 --output my_marker.png
  
  # Generate 10 markers starting from ID 0
  python generate_aruco.py --multiple 10
  
  # Generate markers with custom dictionary and size
  python generate_aruco.py --id 0 --dict DICT_6X6_250 --size 300
  
  # Generate print layout for A4 paper with markers 0-8
  python generate_aruco.py --print-layout a4 --id 0 --count 9
  
  # Generate print layout for credit card with marker 0
  python generate_aruco.py --print-layout creditcard --id 0
  
  # Generate print layout for A5 paper with markers 10-13
  python generate_aruco.py --print-layout a5 --id 10 --count 4
        """
    )
    
    parser.add_argument('--id', type=int, default=0,
                       help='Marker ID to generate (default: 0)')
    parser.add_argument('--dict', type=str, default='DICT_4X4_50',
                       choices=['DICT_4X4_50', 'DICT_4X4_100', 'DICT_4X4_250', 'DICT_4X4_1000',
                               'DICT_5X5_50', 'DICT_5X5_100', 'DICT_5X5_250', 'DICT_5X5_1000',
                               'DICT_6X6_50', 'DICT_6X6_100', 'DICT_6X6_250', 'DICT_6X6_1000',
                               'DICT_7X7_50', 'DICT_7X7_100', 'DICT_7X7_250', 'DICT_7X7_1000'],
                       help='ArUco dictionary to use (default: DICT_4X4_50)')
    parser.add_argument('--size', type=int, default=200,
                       help='Marker size in pixels (default: 200)')
    parser.add_argument('--output', type=str,
                       help='Output file path (default: aruco_marker_<ID>.png)')
    parser.add_argument('--multiple', type=int,
                       help='Generate multiple markers starting from --id')
    parser.add_argument('--output-dir', type=str, default='aruco_markers',
                       help='Output directory for multiple markers (default: aruco_markers)')
    
    # Print layout options
    parser.add_argument('--print-layout', type=str,
                       choices=['creditcard', 'a4', 'a5'],
                       help='Generate a print layout for specific paper format (creditcard, a4, or a5)')
    parser.add_argument('--count', type=int,
                       help='Number of markers to include in print layout (default: auto based on format)')
    parser.add_argument('--dpi', type=int, default=300,
                       help='DPI resolution for print layout (default: 300)')
    parser.add_argument('--margin', type=float, default=10,
                       help='Margin in millimeters for print layout (default: 10mm)')
    
    args = parser.parse_args()
    
    if args.print_layout:
        # Generate print layout
        if args.count is None:
            # Auto-determine count based on format
            format_defaults = {
                'creditcard': 1,
                'a5': 4,
                'a4': 9
            }
            args.count = format_defaults.get(args.print_layout, 1)
        
        marker_ids = list(range(args.id, args.id + args.count))
        output_path = args.output or f'aruco_print_{args.print_layout}.png'
        
        generate_print_layout(
            marker_ids=marker_ids,
            dictionary_name=args.dict,
            format_type=args.print_layout,
            output_path=output_path,
            dpi=args.dpi,
            margin_mm=args.margin
        )
    elif args.multiple:
        # Generate multiple markers
        generate_multiple_markers(
            start_id=args.id,
            count=args.multiple,
            dictionary_name=args.dict,
            size=args.size,
            output_dir=args.output_dir
        )
    else:
        # Generate a single marker
        output_path = args.output or f'aruco_marker_{args.id}.png'
        generate_aruco_marker(
            marker_id=args.id,
            dictionary_name=args.dict,
            size=args.size,
            output_path=output_path
        )


if __name__ == '__main__':
    main()
