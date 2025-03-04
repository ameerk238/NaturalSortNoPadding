# NaturalSortNoPadding: Video Generation Without Zero-Padding

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

NaturalSortNoPadding solves the critical issue of creating videos from image frames with inconsistent naming. When standard sorting fails with filenames like frame1.png, frame10.png, frame2.png, this tool correctly orders frames numerically, ensuring properly sequenced videos without requiring manual filename adjustments.

## The Problem This Solves

When creating videos from image sequences, a critical issue often arises: **frame ordering without zero padding**.

Consider these two common examples:

**Example 1: No padding**
```
frame1.png, frame2.png, ..., frame9.png, frame10.png, ..., frame100.png
```

**Example 2: Inconsistent padding**
```
frame001.png, frame002.png, ..., frame0010.png, ..., frame00100.png
```

Standard alphabetical sorting orders these incorrectly as:

**Example 1 (wrong order):**
```
frame1.png, frame10.png, frame100.png, ..., frame2.png, ...
```

**Example 2 (wrong order):**
```
frame001.png, frame0010.png, frame00100.png, ..., frame002.png, ...
```

This results in jumbled videos where frames appear out of sequence, making the output unusable.

## The Solution

This tool implements **alphanumeric sorting without zero-padding requirements** to address this issue. The algorithm specifically identifies numeric segments in strings and treats them as numbers rather than characters, ensuring proper sequence even without zero-padding:

**Example 1 (correct order):**
```
frame1.png < frame2.png < ... < frame9.png < frame10.png < ... < frame100.png
```

**Example 2 (correct order):**
```
frame001.png < frame002.png < ... < frame0010.png < ... < frame00100.png
```

## Requirements

- Python 3.6+
- FFmpeg (must be installed and available in your system PATH)

## Installation

```bash
# Clone the repository
git clone https://github.com/ameerk238/NaturalSortNoPadding.git
cd NaturalSortNoPadding

# Install dependencies (optional: create a virtual environment first)
pip install -r requirements.txt
```

## Usage

### Basic Usage

```bash
python frame_to_video.py -i /path/to/frames -o /path/to/output
```

### Command Line Arguments

```
usage: frame_to_video.py [-h] -i INPUT -o OUTPUT [-n NAME] [-r RESOLUTION] [-f FPS] [--recursive]

Create videos from image frames without requiring zero-padding in filenames.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        Input directory containing frames or subdirectories of frames
  -o OUTPUT, --output OUTPUT
                        Output directory for videos
  -n NAME, --name NAME  Output filename (without extension, only used in non-recursive mode)
  -r RESOLUTION, --resolution RESOLUTION
                        Output video resolution (WIDTHxHEIGHT, default: 256x256)
  -f FPS, --fps FPS     Frames per second (default: 20)
  --recursive           Process subdirectories recursively
```

### Examples

#### Example 1: Basic usage with non-padded filenames
```bash
# For a directory with frame1.png, frame2.png, ..., frame10.png, etc.
python frame_to_video.py -i ./frames_no_padding -o ./output_videos
```

#### Example 2: Processing inconsistently padded filenames
```bash
# For a directory with frame001.png, frame002.png, ..., frame0010.png, etc.
python frame_to_video.py -i ./frames_inconsistent_padding -o ./output_videos
```

#### Processing multiple frame directories at once
```bash
python frame_to_video.py -i ./all_frame_folders -o ./output_videos --recursive
```

#### Custom output name, resolution and frame rate
```bash
python frame_to_video.py -i ./frames -o ./videos -n "my_sequence" -r 640x480 -f 30
```

## How It Works

1. **Natural Sorting Without Zero-Padding**: Splits filenames into text and numeric parts, then sorts them in proper numeric order regardless of padding
2. **Frame Listing**: Creates a temporary file with properly sorted frame references for video generation
3. **FFmpeg Integration**: Uses the FFmpeg concat demuxer for frame-accurate video creation
4. **Multi-Format Support**: Works with PNG, JPEG, and other image formats

## Directory Structure Handling

The script can work with two types of directory structures:

### Mode 1: Single Directory Mode
```
frames_directory/
├── frame1.png (or frame001.png)
├── frame2.png (or frame002.png)
├── ...
└── frame100.png (or frame00100.png)
```

### Mode 2: Recursive Mode (Multiple Sequences)
```
parent_directory/
├── sequence1/
│   ├── frame1.png
│   ├── frame2.png
│   └── ...
└── sequence2/
    ├── frame001.png
    ├── frame002.png
    └── ...
```

## License

MIT License - see the [LICENSE](LICENSE) file for details.
