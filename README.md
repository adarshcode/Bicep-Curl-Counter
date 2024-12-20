# Bicep-Curl-Counter

It's a GUI based bicep curl counter application which takes real time feed from the webcam and counts the no. of reps and sets done by the user. 
It uses Mediapipe which provides a model to detects positions for your shoulder (A), elbow (B) and wrist (C). 
Mediapipe is an open-source framework which helps in pose estimation and provides us with co-ordinates for these positions. 

Logic:-
- Let's say the positions are A, B and C in the same order for the body parts mentioned. Once the co-ordinates are obtained, we can use some Math to find the angle ABC the angle between elbow to shoulders (BA) and elbow to wrist (BC). 
- Now the angle decreases and increases during the concentric and eccentric motion of the curl respectively. 
- Thus, we can have a threshold for both concentric and eccentric points. So, if the angle is less than the eccentric threshold, we mark it as UP stage and count the rep and when its greater than concentric we mark it as DOWN stage. 
- And the count increases whenever the UP stage is hit.
- The angle can be calculated by using cross product between vectors BA and BC. NumPy has arctan2 function which helps in this.

For future, I can store all the stats and integrate a CNN or media-based DL model to analyze the form of the workout using the frames as image from the video.

#### [LinkedIn Post](https://www.linkedin.com/posts/adarsh-gupta-1086351a0_hi-linkedin-this-is-a-project-on-which-activity-7195153710056943616-Dntd?utm_source=share&utm_medium=member_desktop) with demo video
