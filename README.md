# NaturalSortNoPadding: Video Generation Without Zero-Padding

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## The Problem This Solves

When creating videos from image sequences, a critical issue often arises: **frame ordering without zero padding**.

Consider a sequence of frames named:
```
frame1.png, frame2.png, ..., frame9.png, frame10.png, frame11.png, ...
```

Standard alphabetical sorting orders these incorrectly as:
```
frame1.png, frame10.png, frame11.png, ..., frame2.png, ...
```

This results in jumbled videos where frames appear out of sequence, making the output unusable.

This problem is pervasive in computer vision, machine learning pipelines, and video processing workflows where:
- **Files lack zero-padding** (e.g., using `frame1.png` instead of `frame01.png`, `frame001.png`)
- Files are renamed during processing, losing any original zero-padding
- Different naming conventions are used across datasets
- Files come from multiple sources with different naming patterns

## The Solution

This tool implements **alphanumeric sorting without zero-padding requirements** (a form of natural sorting) to address this issue. The algorithm specifically identifies numeric segments in strings and treats them as numbers rather than characters, ensuring proper sequence even without zero-padding:

```
frame1.png < frame2.png < ... < frame9.png < frame10.png < frame11.png
```

The script:
1. Automatically detects and sorts image frames in the correct numeric order even without zero padding
2. Creates properly sequenced videos using FFmpeg
3. Works with various image formats (.png, .jpg, .jpeg)
4. Can process individual directories or entire directory structures recursively

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

#### Using the provided sample data:
```bash
# Process frames_sample1 directory
python frame_to_video.py -i /Users/ameerkhan/Downloads/NaturalSortNoPadding/example_data/frames_sample1 -o ./output_videos

# Process frames_sample2 directory
python frame_to_video.py -i /Users/ameerkhan/Downloads/NaturalSortNoPadding/example_data/frames_sample2 -o ./output_videos

# Process both sample directories at once
python frame_to_video.py -i /Users/ameerkhan/Downloads/NaturalSortNoPadding/example_data -o ./output_videos --recursive
```

#### Custom naming:
```bash
python frame_to_video.py -i ./example_data/frames_sample1 -o ./project/videos -n "my_video"
```

#### Custom resolution and frame rate:
```bash
python frame_to_video.py -i ./example_data/frames_sample2 -o ./videos -r 640x480 -f 30
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
example_data/frames_sample1/
├── frame_000.png
├── frame_001.png
├── ...
└── frame_100.png
```
Use: `python frame_to_video.py -i /Users/ameerkhan/Downloads/NaturalSortNoPadding/example_data/frames_sample1 -o output_directory`

Result: One video file created in the output directory

### Mode 2: Recursive Mode (Multiple Sequences)
```
example_data/
├── frames_sample1/
│   ├── frame_000.png
│   ├── frame_001.png
│   └── ...
└── frames_sample2/
    ├── frame_000.png
    ├── frame_001.png
    └── ...
```
Use: `python frame_to_video.py -i parent_directory -o output_directory --recursive`

Result: Multiple video files created in the output directory, one for each sequence folder

## License

MIT License - see the [LICENSE](LICENSE) file for details.