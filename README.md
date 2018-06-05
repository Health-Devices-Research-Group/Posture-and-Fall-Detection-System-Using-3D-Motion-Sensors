# Posture and Fall Detection System Using 3D Motion Sensors
This work presents a supervised learning approach for training a posture detection classifier, and implementing a fall detection system using the posture classification results as inputs with a Microsoft Kinect v2 sensor. The Kinect v2 skeleton tracking provides 3D depth coordinates for 25 body parts. We use these depth coordinates to extract seven features consisting of the height of the subject and six angles between certain body parts. These features are then fed into a fully connected neural network that outputs one of three considered postures for the subject: standing, sitting, or lying down. An average classification rate of over 99.30% for all three postures was achieved on test data consisting of multiple subjects where the subjects were not even facing the Kinect depth camera most of the time and were located in different locations. These results show the feasibility to classify human postures with the proposed setup independently of the location of the subject in the room and orientation to the 3D sensor.

**SYSTEM DEMO**  
Please watch the *Posture_fall_detection_demo.mp4* video to get a sense of the posture and fall detection system.

**RUN INSTRUCTIONS: (WINDOWS)**  
1- Download the Kinect SDK 2.0 as per the official website https://www.microsoft.com/en-ca/download/details.aspx?id=44561  
2- Download Visual studio 2015 and open the solution *skeletonTracking/skeletonTracking.sln* then run the code.  
3- Run main.py with Python3.  
  
**EXPLANATION OF TRAINING/TESTING DATA**  
The figure below illustrates six of the seven training/testing features for all three postures (standing, sitting, and lying down), named as follows: Left hip angle (1), right hip angle (2), left knee angle (3), right knee angle (4), chest angle(5), and chest-knee angle (6).  The seventh feature is the height of the person computed by taking the Y-position of the head and subtracting the lower Y-position value of the right and left foot from it.
![Alt text](images/kinectSkeletonFeatures.png?raw=true "Visualization of six of the seven features that will be used for posture classification in the Kinect Skeleton.")
  
**EXPERIMENTAL SETUP**  
Six people of different heights and shapes were asked to participate in the data collection phase, which consisted of four one-minute rounds, where in each round, the subject was allowed to either move or stay in a fixed posture: that is standing for one minutes, sitting for one minutes, and lying down for one minutes. The Kinect V2 sensor has a frame rate of 30 frames per second, thus 1800 frames for each one-minute round per subject per posture were collected which led to about 9000 training frames per posture in total.
  
**LINK TO PAPER**  
The paper can be read from the *Paper_Posture-and-Fall-Detection-System-Using-3D-Motion-Sensors.pdf* file.
  
**LINKS TO OUR LABS**  
- http://health-devices.eecs.uottawa.ca/  
- http://carg.site.uottawa.ca/  

**LINKS TO SIMILAR WORKS**  
- https://pdfs.semanticscholar.org/b8ac/6f5f1a3362f83aef7c75b0b75ab09e17a3c1.pdf  
- http://journals.sagepub.com/doi/full/10.5772/62163  
- https://ieeexplore.ieee.org/document/4373773/?reload=true  
- http://download.atlantis-press.com/php/download_paper.php?id=25866362  
