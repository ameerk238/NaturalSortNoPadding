#!/bin/bash

# Basic example - single directory
python frame_to_video.py -i ./example_data/frames_sample1 -o ./output_videos

# Custom name
python frame_to_video.py -i ./example_data/frames_sample1 -o ./output_videos -n "sample1_video"

# Process multiple frame directories at once
python frame_to_video.py -i ./example_data -o ./output_videos --recursive

# Process specific examples from the provided sample data
python frame_to_video.py -i /Users/ameerkhan/Downloads/NaturalSortNoPadding/example_data/frames_sample1 -o ./output_videos

# Process both sample directories in the download location
python frame_to_video.py -i /Users/ameerkhan/Downloads/NaturalSortNoPadding/example_data -o ./output_videos --recursive

# Custom resolution and frame rate for sample2
python frame_to_video.py -i ./example_data/frames_sample2 -o ./output_videos -r 640x480 -f 30