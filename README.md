# ArUco Marker Generator

Generate ArUco markers for computer vision applications. ArUco markers are square fiducial markers commonly used for camera calibration, pose estimation, and augmented reality.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/martinbibb-cmd/Aruco.git
cd Aruco
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Generate a Single Marker

Generate a single ArUco marker with default settings (ID 0, DICT_4X4_50, 200x200 pixels):
```bash
python generate_aruco.py --id 0
```

Generate a marker with custom settings:
```bash
python generate_aruco.py --id 5 --dict DICT_6X6_250 --size 300 --output my_marker.png
```

### Generate Multiple Markers

Generate 10 markers starting from ID 0:
```bash
python generate_aruco.py --multiple 10
```

Generate multiple markers with custom settings:
```bash
python generate_aruco.py --id 20 --multiple 5 --dict DICT_5X5_100 --size 250 --output-dir my_markers
```

## Command-Line Options

- `--id`: Marker ID to generate (default: 0)
- `--dict`: ArUco dictionary to use (default: DICT_4X4_50)
  - Available dictionaries: DICT_4X4_50, DICT_4X4_100, DICT_4X4_250, DICT_4X4_1000, DICT_5X5_50, DICT_5X5_100, DICT_5X5_250, DICT_5X5_1000, DICT_6X6_50, DICT_6X6_100, DICT_6X6_250, DICT_6X6_1000, DICT_7X7_50, DICT_7X7_100, DICT_7X7_250, DICT_7X7_1000
- `--size`: Marker size in pixels (default: 200)
- `--output`: Output file path for a single marker
- `--multiple`: Generate multiple markers starting from the specified ID
- `--output-dir`: Output directory for multiple markers (default: aruco_markers)

## ArUco Dictionary Types

The number in the dictionary name (e.g., 4X4, 5X5) indicates the grid size of the marker, and the last number indicates the total number of markers in that dictionary:
- **4X4**: 4x4 bit markers (smaller, faster detection)
- **5X5**: 5x5 bit markers (good balance)
- **6X6**: 6x6 bit markers (more robust)
- **7X7**: 7x7 bit markers (most robust, slower detection)

Choose based on your needs:
- Use smaller dictionaries (4X4) for faster detection
- Use larger dictionaries (6X6, 7X7) for better error correction and robustness

## Examples

1. **Basic usage**: Generate marker ID 0
   ```bash
   python generate_aruco.py --id 0
   ```

2. **Custom size**: Generate a larger marker (400x400 pixels)
   ```bash
   python generate_aruco.py --id 1 --size 400
   ```

3. **Different dictionary**: Use a 6x6 dictionary with 250 markers
   ```bash
   python generate_aruco.py --id 10 --dict DICT_6X6_250
   ```

4. **Batch generation**: Create markers 0-9 for a project
   ```bash
   python generate_aruco.py --multiple 10 --output-dir project_markers
   ```

## Output

Generated markers are saved as PNG images with black markers on a white background, ready for printing or digital use.

## Requirements

- Python 3.6+
- OpenCV (opencv-contrib-python)
- NumPy

## License

This project is open source and available for use in computer vision applications.
