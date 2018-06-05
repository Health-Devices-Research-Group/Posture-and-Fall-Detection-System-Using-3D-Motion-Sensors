# Posture and Fall Detection System Using 3D Motion Sensors
This work presents a supervised learning approach for training a posture detection classifier, and implementing a fall detection system using the posture classification results as inputs with a Microsoft Kinect v2 sensor. The Kinect v2 skeleton tracking provides 3D depth coordinates for 25 body parts. We use these depth coordinates to extract seven features consisting of the height of the subject and six angles between certain body parts. These features are then fed into a fully connected neural network that outputs one of three considered postures for the subject: standing, sitting, or lying down. An average classification rate of over 99.30% for all three postures was achieved on test data consisting of multiple subjects where the subjects were not even facing the Kinect depth camera most of the time and were located in different locations. These results show the feasibility to classify human postures with the proposed setup independently of the location of the subject in the room and orientation to the 3D sensor.

**RUN INSTRUCTIONS: (WINDOWS)**  
1- Download the Kinect SDK 2.0 as per the official website https://www.microsoft.com/en-ca/download/details.aspx?id=44561  
2- Download Visual studio 2015 and open the solution skeletonTracking/skeletonTracking.sln then run the code.  
3- Run main.py with Python3.  
  
**EXPLANATION OF TRAINING/TESTING DATA**  
![Alt text](images/kinectSkeletonFeatures.png?raw=true "Visualization of six of the seven features that will be used for posture classification in the Kinect Skeleton.")

  
**LINK TO PAPER**  
http://carg.site.uottawa.ca/  
  

**LINK TO OUR LABS**
- http://health-devices.eecs.uottawa.ca/  
- http://carg.site.uottawa.ca/  
