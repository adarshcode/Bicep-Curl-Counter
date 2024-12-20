import cv2
import mediapipe as mp
import numpy as np 
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pyttsx3
        
# Function to calculate angle
def CalculateAngle(a, b, c):
    a = np.array(a) 
    b = np.array(b) 
    c = np.array(c) 
    
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians*180.0/np.pi)
    
    if angle >180.0:
        angle = 360-angle

    return angle


def update_stats():
    global sets, reps, stage, rangle, lshoulder, lelbow, lwrist, rshoulder, relbow, rwrist
    while feed.isOpened():
        ret, frame = feed.read()
        if ret:
            h, w, _ = frame.shape

            # Make detection and store all the landmarks 
            results = pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

            # Extract landmarks
            try:
                landmarks = results.pose_landmarks.landmark

                lshoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                lelbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                lwrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                rshoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                relbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                rwrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]

                if None not in (rshoulder, relbow, rwrist):

                    rangle = CalculateAngle(rshoulder, relbow, rwrist)
            
                    # Update GUI labels
                    sets_label.config(text=str(sets))
                    reps_label.config(text=str(reps))
                    stage_label.config(text=stage)
                    angle_label.config(text=f'{rangle:.2f}')

                    # Check for reps
                    if rangle > 150:
                        stage = "down"
    
                    if rangle < 50 and stage == "down":
                        stage = "up"
                        reps += 1
                        if reps % 3 == 0:
                                sets += 1
            except:
                pass
            
            
            # Render the results to the image back
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Display video feed
            img = cv2.resize(frame, (800, 530)) # Adjust size if necessary
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            img = cv2.flip(img, 1)
            imgtk = ImageTk.PhotoImage(image=Image.fromarray(img))
            video_label.imgtk = imgtk
            video_label.configure(image=imgtk)
            
            # Call update_stats after 100 milliseconds
            root.after(100, update_stats)
            break

# Initialize GUI
root = tk.Tk()
root.title("Bicep Curl Counter")

root.geometry("1200x800")

# Create video frame
video_frame = tk.Frame(root)
video_frame.pack(side=tk.RIGHT)

stats_frame = tk.Frame(root)
stats_frame.pack(side=tk.LEFT, padx=20)

# Video feed
feed = cv2.VideoCapture(0)

# Initialize stats
sets=0
reps = 0
stage = "down"
rangle = 0

# Initialize Mediapipe
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Video feed label
video_label = tk.Label(video_frame)
video_label.pack()

# Stats labels
sets_label = ttk.Label(stats_frame, text="0", font=('Helvetica', 20, 'bold'))
sets_label.grid(row=0, column=1, padx=10, pady=10, sticky="w")
reps_label = ttk.Label(stats_frame, text="0", font=('Helvetica', 20, 'bold'))
reps_label.grid(row=1, column=1, padx=10, pady=10, sticky="w")
stage_label = ttk.Label(stats_frame, text="down", font=('Helvetica', 20, 'bold'))
stage_label.grid(row=2, column=1, padx=10, pady=10, sticky="w")
angle_label = ttk.Label(stats_frame, text="0.00", font=('Helvetica', 20, 'bold'))
angle_label.grid(row=3, column=1, padx=10, pady=10, sticky="w")

# Labels descriptions
ttk.Label(stats_frame, text="Sets:", font=('Helvetica', 20, 'bold')).grid(row=0, column=0, padx=10, pady=10, sticky="e")
ttk.Label(stats_frame, text="Reps:", font=('Helvetica', 20, 'bold')).grid(row=1, column=0, padx=10, pady=10, sticky="e")
ttk.Label(stats_frame, text="Stage:", font=('Helvetica', 20, 'bold')).grid(row=2, column=0, padx=10, pady=10, sticky="e")
ttk.Label(stats_frame, text="Angle (Right):", font=('Helvetica', 20, 'bold')).grid(row=3, column=0, padx=10, pady=10, sticky="e")

# Function to reset stats
def reset_stats():
    global sets, reps, stage, rangle
    sets = 0
    reps = 0
    stage = "down"
    rangle = 0
    # Update GUI labels after resetting stats
    sets_label.config(text=str(sets))
    reps_label.config(text=str(reps))
    stage_label.config(text=stage)
    angle_label.config(text=f'{rangle:.2f}')

# Create a button to reset statistics
reset_button = ttk.Button(stats_frame, text="Reset Stats", style="Bold.TButton", command=reset_stats)
reset_button.grid(row=4, column=1, columnspan=2, padx=10, pady=10, sticky="ew")

# Run update_stats function
update_stats()

root.mainloop()
