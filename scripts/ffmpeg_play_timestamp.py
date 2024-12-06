import os
import subprocess
import re
import pandas as pd
from datetime import datetime
import time
import pygetwindow as gw

# Paths
video_path = "C:\\Users\\hxiong\\Desktop\\Haolin_research\\Digital_self\\stimulus\\emotion_videos\\disgust_pinkflamingos.mp4"  # Replace with your video file
output_dir = "C:\\Users\\hxiong\\Desktop\\Haolin_research\\Digital_self\\stimulus_outputs"
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

# Extract frame timestamps from the log file and save to CSV using pandas
def extract_timestamps_to_csv(log_file, timestamps_csv, start_timestamp = 0.0):
    pattern = r'n:\s*(\d+)\s*pts:\s*(\d+)\s*pts_time:(\d+\.\d+)' #regex to find the data in log
    data = []
    # Parse the log file
    with open(log_file, "r") as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                frame_number = int(match.group(1))
                # timestamp = float(match.group(2))
                pts_time = float(match.group(3))
                data.append({"Frame": frame_number, "Time_Delta(s)": pts_time})
    # Save to CSV using pandas
    df = pd.DataFrame(data)
    df["Unix Time"] = start_timestamp + df["Time_Delta(s)"]
    # print(df["Unix Time"][-1])
    df.to_csv(timestamps_csv, index=False)
    print(f"Timestamps saved to {timestamps_csv}")

# Main function to run the steps
def main(video_path):
    start_time = datetime.now()
    print(f"Starting video playback at {start_time.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}")

    # Record timestamps
    record_timestamps(video_path, log_file)

    # Play video in fullscreen
    start_time, end_time = play_video_fullscreen(video_path)

    # Extract timestamps to CSV
    extract_timestamps_to_csv(log_file, timestamps_csv, start_timestamp = start_time)

    print("Process complete!")

if __name__ == "__main__":
    main(video_path)