# This script plays a stimulus video and record timestamp

import cv2
import time
import numpy as np
import os
import pandas as pd
from datetime import datetime

# Path to the video file
video_path = "C:\\Users\\27270\\docker_env\\Digital_self\\stimulus\\pinkflamingos_extract.mp4"
output_path = "C:\\Users\\27270\\docker_env\\Digital_self\\stimulus_output\\"
video_name = os.path.basename(video_path)


output_dir = os.path.join(output_path,video_name.split('.')[0])
frame_dir = os.path.join(output_dir,'frames')
os.makedirs(frame_dir,exist_ok=True)

cap = cv2.VideoCapture(video_path)
fps  = cap.get(cv2.CAP_PROP_FPS)
fps_scaling = 1.0 # Try increasing this number if effective FPS is lower than target FPS, vice versa 

if not cap.isOpened():
    print("Error: Cannot open video.")
    exit()


# Get video resolution
video_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
video_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
print(f"Video Resolution: {video_width}x{video_height}")

# Get screen resolution (modify for your screen dimensions)
# screen_width = 1920
# screen_height = 1080
screen_width = 2560
screen_height = 1440



# Calculate scaling factor to maintain aspect ratio
scale_width = screen_width / video_width
scale_height = screen_height / video_height
scaling_factor = min(scale_width, scale_height)



# Calculate new dimensions
new_width = int(video_width * scaling_factor * 0.9)
new_height = int(video_height * scaling_factor * 0.9)

timestamps = list()
frames = list()
resized_frames = list()

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frames.append(frame)
cap.release()

# Resize the frame to fit the screen
for frame in frames: 
    resized_frame = cv2.resize(frame, (new_width, new_height))
    black_frame = np.zeros((screen_height, screen_width, 3), dtype=np.uint8)
    x_offset = (screen_width - new_width) // 2
    y_offset = (screen_height - new_height) // 2
    black_frame[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = resized_frame
    resized_frames.append(black_frame)



for frame in resized_frames:
    cv2.imshow("Full-Screen Video", frame)
    timestamps.append(time.time())
    # Break the loop on pressing 'q'
    if cv2.waitKey(round(1000/(fps*fps_scaling))) == ord('q'):
        break

cv2.destroyAllWindows()

formatted_times = [datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S.%f')[:-3] for ts in timestamps]
timestamp_df = pd.DataFrame(data={"Unix":timestamps, "Formatted":formatted_times})
timestamp_df.to_csv(os.path.join(output_dir,'timestamp.csv'))

elapsed_time = timestamps[-1] - timestamps[0]
effective_fps = len(frames)/ elapsed_time
print(f"Number of frames: {len(frames)}")
print(f"Elapsed Time: {elapsed_time:.2f} seconds")
print(f"Target FPS: {fps:.2f}")
print(f"Effective FPS: {effective_fps:.2f}")

for idx, frame in enumerate(resized_frames):
    cv2.imwrite(os.path.join(frame_dir,f'{idx}.png'), frame)