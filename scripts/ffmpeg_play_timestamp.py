import os
import subprocess
import re
import pandas as pd
from datetime import datetime
import time
import pygetwindow as gw

# Paths
video_path = "/home/hxiong/Desktop/Research/Digital_self/stimulus/emotion_videos/disgust_pinkflamingos.mp4"  # Replace with your video file
output_dir = "/home/hxiong/Desktop/Research/Digital_self/stimulus_outputs/"
os.makedirs(output_dir, exist_ok=True)

# Output file paths
log_file = os.path.join(output_dir, "frame_timestamps.log")
timestamps_csv = os.path.join(output_dir, "timestamps.csv")

# Record frame timestamps using ffmpeg
def record_timestamps(video_path, log_file):
    command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", "showinfo",  # Video filter to log frame information
        "-f", "null", "-"   # Process video but don't output it
    ]
    with open(log_file, "w") as log:
        subprocess.run(command, stderr=log, stdout=subprocess.DEVNULL, check=True)
    print(f"Frame timestamps logged to {log_file}")


def play_video_fullscreen(video_path):
    start_time = time.time()
    command = [
        "ffplay",
        "-fs",  # Fullscreen mode
        "-i", video_path  # Input video
        
    ]
    subprocess.run(command)
    end_time = time.time()
    return start_time, end_time


def play_on_monitor(video_path, monitor_index=0):
    # Monitor configurations (example for two 1920x1080 monitors)
    monitors = [
        {"resolution": (2560, 1600), "offset": (1, 1)},     # Primary monitor
        {"resolution": (3840, 2160), "offset": (2560, 1)},  # Secondary monitor
    ]

    # Get the monitor's offset
    if monitor_index >= len(monitors):
        print(f"Monitor index {monitor_index} is out of range!")
        return

    monitor = monitors[monitor_index]
    width, height = monitor["resolution"]
    x_offset, y_offset = monitor["offset"]

    # Run ffplay command
    time_start = time.time()
    command = [
        "ffplay",
        "-fs",  # Fullscreen mode
        "-x", str(x_offset),
        "-y", str(y_offset),
        "-vf", f"scale={width}:-1",  # Scale to fit monitor width while maintaining aspect ratio
        "-i", video_path,
    ]

    subprocess.run(command)
    end_time = time.time()
    return time_start, end_time







def play_video_and_move(video_path, target_monitor):
    # Launch ffplay in a subprocess
    process = subprocess.Popen(["ffplay", "-noborder", "-i", video_path])

    # Wait briefly to allow the window to appear
    time.sleep(2)

    # Locate the ffplay window
    windows = gw.getWindowsWithTitle("ffplay")
    if not windows:
        print("ffplay window not found!")
        process.terminate()
        return

    # Get the target monitor's geometry
    monitors = gw.getAllScreens()
    if target_monitor >= len(monitors):
        print(f"Monitor index {target_monitor} is out of range!")
        process.terminate()
        return

    monitor = monitors[target_monitor]
    ffplay_window = windows[0]

    # Move the ffplay window to the target monitor
    ffplay_window.moveTo(monitor.left, monitor.top)
    ffplay_window.resizeTo(monitor.width, monitor.height)

    # Wait for the subprocess to finish
    process.wait()




































# Extract frame timestamps from the log file and save to CSV using pandas
def extract_timestamps_to_csv(log_file, timestamps_csv):
    pattern = r"n:(\d+) pts_time:([\d\.]+)"  # Regex to extract frame index and timestamp
    data = []

    # Parse the log file
    with open(log_file, "r") as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                frame_number = int(match.group(1))
                timestamp = float(match.group(2))
                data.append({"Frame": frame_number, "Timestamp (s)": timestamp})

    # Save to CSV using pandas
    df = pd.DataFrame(data)
    df.to_csv(timestamps_csv, index=False)
    print(f"Timestamps saved to {timestamps_csv}")

# Main function to run the steps
def main(video_path):
    start_time = datetime.now()
    print(f"Starting video playback at {start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")

    # Record timestamps
    record_timestamps(video_path, log_file)

    # Play video in fullscreen
    # play_video_fullscreen(video_path)
    play_on_monitor(video_path, monitor_index=1)
    # play_video_and_move(video_path, 1)

    # Extract timestamps to CSV
    # extract_timestamps_to_csv(log_file, timestamps_csv)

    print("Process complete!")

if __name__ == "__main__":
    main(video_path)