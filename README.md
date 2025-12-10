# ArUco Marker Generator

Generate ArUco markers for computer vision applications. ArUco markers are square fiducial markers commonly used for camera calibration, pose estimation, and augmented reality.

This tool supports generating individual markers as well as print-ready layouts for credit cards, A4, and A5 paper formats.

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

### Generate Print Layouts

Create print-ready layouts optimized for different paper formats:

#### Credit Card Format (85.60mm × 53.98mm)
Generate a single marker layout for credit card printing:
```bash
python generate_aruco.py --print-layout creditcard --id 0
```

#### A4 Paper Format (210mm × 297mm)
Generate a 3×3 grid of 9 markers on A4 paper:
```bash
python generate_aruco.py --print-layout a4 --id 0 --count 9
```

#### A5 Paper Format (148mm × 210mm)
Generate a 2×2 grid of 4 markers on A5 paper:
```bash
python generate_aruco.py --print-layout a5 --id 0 --count 4
```

Custom print layout options:
```bash
# High resolution (600 DPI) A4 layout with custom margins
python generate_aruco.py --print-layout a4 --id 10 --count 6 --dpi 600 --margin 15

# A5 layout with different dictionary
python generate_aruco.py --print-layout a5 --id 0 --count 4 --dict DICT_6X6_250
```

## Command-Line Options

### Basic Options
- `--id`: Marker ID to generate (default: 0)
- `--dict`: ArUco dictionary to use (default: DICT_4X4_50)
  - Available dictionaries: DICT_4X4_50, DICT_4X4_100, DICT_4X4_250, DICT_4X4_1000, DICT_5X5_50, DICT_5X5_100, DICT_5X5_250, DICT_5X5_1000, DICT_6X6_50, DICT_6X6_100, DICT_6X6_250, DICT_6X6_1000, DICT_7X7_50, DICT_7X7_100, DICT_7X7_250, DICT_7X7_1000
- `--size`: Marker size in pixels (default: 200)
- `--output`: Output file path for a single marker

### Multiple Markers Options
- `--multiple`: Generate multiple markers starting from the specified ID
- `--output-dir`: Output directory for multiple markers (default: aruco_markers)

### Print Layout Options
- `--print-layout`: Generate a print layout for specific paper format
  - `creditcard`: Credit card format (85.60mm × 53.98mm) - 1 marker
  - `a4`: A4 paper (210mm × 297mm) - up to 9 markers in 3×3 grid
  - `a5`: A5 paper (148mm × 210mm) - up to 4 markers in 2×2 grid
- `--count`: Number of markers to include in print layout (default: auto based on format)
- `--dpi`: DPI resolution for print layout (default: 300, recommended: 300-600 for printing)
- `--margin`: Margin in millimeters for print layout (default: 10mm)

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

5. **Print layout for credit card**: Create a printable credit card sized marker
   ```bash
   python generate_aruco.py --print-layout creditcard --id 0
   ```

6. **Print layout for A4 paper**: Create 9 markers on a single A4 sheet
   ```bash
   python generate_aruco.py --print-layout a4 --id 0 --count 9
   ```

7. **Print layout for A5 paper**: Create 4 markers on a single A5 sheet
   ```bash
   python generate_aruco.py --print-layout a5 --id 0 --count 4
   ```

8. **High-quality print layout**: Generate A4 layout at 600 DPI
   ```bash
   python generate_aruco.py --print-layout a4 --id 0 --dpi 600
   ```

## Output

Generated markers are saved as PNG images with black markers on a white background, ready for printing or digital use.

### Print Layout Features
- **High-resolution output**: 300 DPI by default (customizable up to 600 DPI or higher)
- **Precise sizing**: Markers are sized according to the actual paper dimensions
- **ID labels**: Each marker is labeled with its ID number for easy identification
- **Centered layout**: Markers are automatically centered on the page with consistent spacing
- **Print guides**: Light gray border indicates the paper edge for accurate cutting

Print layouts can be sent directly to a printer or saved as high-resolution PNG files for professional printing services.

## Requirements

- Python 3.6+
- OpenCV (opencv-contrib-python)
- NumPy
- Pillow (for print layout generation)

## License

This project is open source and available for use in computer vision applications.
