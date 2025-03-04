#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
NaturalSortNoPadding: Video Generation Without Zero-Padding

This script solves the critical problem of generating videos from image sequences
where frame filenames don't have consistent zero-padding (e.g., frame1.png vs frame01.png).
Standard alphabetical sorting would order frames incorrectly (e.g., frame1.png, frame10.png, frame2.png).
This implementation ensures correct numeric ordering without requiring zero-padding.
"""

import os
import re
import argparse
import subprocess
from typing import List


def natural_sort(file_list: List[str]) -> List[str]:
    """
    Sort a list of strings using alphanumeric sorting without requiring zero-padding.
    
    This ensures that values like "frame10.png" come after "frame9.png" instead of
    between "frame1.png" and "frame2.png" as would happen with standard sorting,
    even when filenames lack zero-padding (e.g., frame01.png, frame001.png).
    
    Args:
        file_list: List of filenames to sort
        
    Returns:
        Alphanumerically sorted list of filenames (numeric parts sorted as integers)
    """
    def convert(text):
        return int(text) if text.isdigit() else text.lower()
    
    def alphanum_key(key):
        return [convert(c) for c in re.split('([0-9]+)', key)]
    
    return sorted(file_list, key=alphanum_key)


def create_video_from_frames(
    frames_path: str,
    output_path: str,
    output_filename: str = None,
    fps: int = 20,
    resolution: str = "256x256",
    recursive: bool = False
) -> None:
    """
    Create a video from a sequence of image frames using natural sorting.
    
    Args:
        frames_path: Directory containing the image frames
        output_path: Directory where the output video will be saved
        output_filename: Name of the output video file (without extension)
        fps: Frames per second for the output video
        resolution: Resolution of the output video (WIDTHxHEIGHT)
        recursive: Whether to process subdirectories recursively
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    
    # Process the directory or directories
    if recursive:
        folders = [f for f in os.listdir(frames_path) if os.path.isdir(os.path.join(frames_path, f))]
        if not folders:
            # If no subdirectories found but recursive was requested, process the main directory
            process_single_directory(frames_path, output_path, None, fps, resolution)
        else:
            for folder in folders:
                try:
                    folder_frames_path = os.path.join(frames_path, folder)
                    process_single_directory(folder_frames_path, output_path, folder, fps, resolution)
                except Exception as e:
                    print(f"Error processing folder {folder}: {str(e)}")
    else:
        # Process just the single directory
        process_single_directory(frames_path, output_path, output_filename, fps, resolution)
    
    print("All videos have been processed!")


def process_single_directory(
    frames_path: str,
    output_path: str,
    output_filename: str = None,
    fps: int = 20,
    resolution: str = "256x256"
) -> None:
    """
    Process a single directory of frames to create a video.
    
    Args:
        frames_path: Directory containing the image frames
        output_path: Directory where the output video will be saved
        output_filename: Name of the output video file (without extension)
        fps: Frames per second for the output video
        resolution: Resolution of the output video (WIDTHxHEIGHT)
    """
    # Determine output filename if not provided
    if not output_filename:
        output_filename = os.path.basename(frames_path.rstrip("/\\"))
    
    # Remove .mp4 extension if it exists in the folder name
    base_name = output_filename.replace('.mp4', '')
    
    # Construct output video path
    output_video_path = os.path.join(output_path, f"{base_name}.mp4")
    
    print(f"Processing {frames_path} -> {output_video_path}")
    
    # Get and sort frame files
    frame_files = [f for f in os.listdir(frames_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    if not frame_files:
        print(f"No image files found in {frames_path}")
        return
    
    sorted_frames = natural_sort(frame_files)
    
    # Create a temporary file listing frames in correct order
    list_file_path = os.path.join(output_path, f'{base_name}_frames.txt')
    frame_duration = 1.0 / fps
    
    with open(list_file_path, 'w') as f:
        for frame in sorted_frames:
            # Write full path to each frame
            f.write(f"file '{os.path.join(frames_path, frame)}'\n")
            f.write(f"duration {frame_duration}\n")
    
    # FFmpeg command
    ffmpeg_command = [
        'ffmpeg', '-y',
        '-f', 'concat',
        '-safe', '0',
        '-i', list_file_path,
        '-s', resolution,
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-r', str(fps),
        output_video_path
    ]
    
    # Execute ffmpeg command
    process = subprocess.run(
        ffmpeg_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Clean up the temporary file
    os.remove(list_file_path)
    
    if process.returncode == 0:
        print(f"✓ Successfully created video: {output_video_path}")
    else:
        print(f"✗ Error creating video for {frames_path}")
        print(f"FFmpeg error: {process.stderr.decode()}")


def main():
    """Parse arguments and run the video generation process."""
    parser = argparse.ArgumentParser(
        description='Create videos from image frames without requiring zero-padding in filenames.'
    )
    
    parser.add_argument(
        '-i', '--input',
        required=True,
        help='Input directory containing frames or subdirectories of frames'
    )
    
    parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output directory for videos'
    )
    
    parser.add_argument(
        '-n', '--name',
        help='Output filename (without extension, only used in non-recursive mode)'
    )
    
    parser.add_argument(
        '-r', '--resolution',
        default='256x256',
        help='Output video resolution (WIDTHxHEIGHT, default: 256x256)'
    )
    
    parser.add_argument(
        '-f', '--fps',
        type=int,
        default=20,
        help='Frames per second (default: 20)'
    )
    
    parser.add_argument(
        '--recursive',
        action='store_true',
        help='Process subdirectories recursively'
    )
    
    args = parser.parse_args()
    
    create_video_from_frames(
        args.input,
        args.output,
        args.name,
        args.fps,
        args.resolution,
        args.recursive
    )


if __name__ == "__main__":
    main()