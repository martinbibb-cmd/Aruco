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
    
    args = parser.parse_args()
    
    if args.multiple:
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
