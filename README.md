Rail Fall Prevention System 
=============================
[English](https://github.com/JunHeon-Ch/Rail_Fall_Prevention_System/wiki/Description-English) [Korean](https://github.com/JunHeon-Ch/Rail_Fall_Prevention_System/wiki/Description-Korean)

The Rail Fall Prevention System is designed to prevent rail crashes by determining whether a person fall on a rail.

[Introduction Videos](https://github.com/JunHeon-Ch/Rail_Fall_Prevention_System/wiki/Videos)
---------------------------
Click on the following picture to watch the *Proposal video*.

[![Proposal 영상을 시청하려면 다음 사진을 클릭해주세요.](https://img.youtube.com/vi/II5gYJ-4010/0.jpg)](https://www.youtube.com/watch?v=II5gYJ-4010)

Click on the following picture to watch the *Final video*.

[![Final 영상을 시청하려면 다음 사진을 클릭해주세요.](https://img.youtube.com/vi/kym3mti6I8A/0.jpg)](https://www.youtube.com/watch?v=kym3mti6I8A&feature=youtu.be)

---------------------------

DEMO video
---------------------------
[![Demo video](https://img.youtube.com/vi/E-d7NiPAkk8/0.jpg)](https://www.youtube.com/watch?v=E-d7NiPAkk8)

---------------------------

Brief Description
---------------------------
- A system that uses edge computing techniques to help you deal with track crashes more quickly.
- Use image recognition technology to determine if a person falls onto the track.
- Sound an alarm when an accident occurs, and the application allows employees and station employees to quickly know about the accident.

*The system was built with the following focus:*

1. **'Quickness'** : To raise the alert notification and to receive information about an accident when a track crash occurs, use the method to increase the speed.
2. **'Correctness'**: Because it is very important to determine whether a fall occurred or not, use the method the method to increase the accuracy.
---------------------------

Motivation
---------------------------
- **Accident occurrence**   
On trains that are frequently used by people, *large and small accidents occur* every year, and they often accidentally fall or jump onto tracks without a screen door or safety barrier.
- **Difficulty installing Platform Screen door(PSD)**   
Currently, most platforms are equipped with screen doors, but some platforms where KTX or Mugunghwa trains stop *have difficulty keeping the stationary position* due to the varying size, height, and location of each train door.   
Due to the budget problem for installing screen doors, *the installation rate of screen doors* in some areas is *quite low*.
- **GIDS**   
GIDS can be applied to a variety of platforms because it can be used to reduce costs by using infrared sensors to recognize access distances, *but its accuracy is low due to sensor limitations*.

**To compensate for the shortcomings of traditional screen doors and GIDS, we have devised a *imaging recognition-based" track crash prevention system that can be used to determine falls using images.***
---------------------------

Process
---------------------------
1. Run the program.
2. Area is specified using automatic straight line detection from images obtained from the camera.
3. The user selects the appropriate track boundary from the detected straight line and enters the margin value.
4. If there is no suitable line among the detected lines, expand the scope of the search for the straight line to detect the appropriate line.
5. Add margins from the selected straight line and set the zone to Region Of Interest (ROI).
6. Only the person objects within the ROI will be detailed to determine in real time if there is a person who has fallen on the track.
7. At this point, the coordinates of the center point at the bottom of the investegated bounder box are considered to be the coordinates of the human foot.
8. Use the foot coordinates to determine the fall.
- If the system determines that a person has fallen, it notifies in two ways:
    - If coordinates **are reached at the boundary**: The speakers installed on the edge device will give **a warning sound** as the primary warning.
    - If coordinates **are crossed the boundary**: Application linked to edge devices will be used with secondary **warning notification message** along with incident information. 
    - If the train comes in, the detection will be temporarily stopped during the train's entry, as it can also be determined that boarding the train has crashed onto the tracks.
---------------------------

Problem statement
---------------------------
1. The disadvantages of cloud computing in traditional image recognition systems
![Architecture](https://github.com/JunHeon-Ch/Rail_Fall_Prevention_System/blob/master/wiki_image/architecture.png)
- As is..
    - Assuming that this system is used on a real-world platform, it sends a huge amount of frames from numerous cameras to the server.
    - This process **consumes significant bandwidth** and at the same time is a **constant and significant burden on the Internet infrastructure**. This may also **lead to delays**.
    - In our system, where **'real-time'** is important, we judged that the structure was inappropriate.
- To be..
    - The use of edge computing structures complements the disadvantages of cloud computing, **enabling data stream acceleration, including real-time data processing without latency**.
    - Taking these advantages of edge computing, we designed our system structure, which is important for real-time.
2. Processing optimization   
- Edge systems show weakness over cloud-based systems in terms of **computational performance**.
- To compensate for the weakness of processing performance in edge computing, we have devised three ways to **reduce the size of the computations** that need to be handled.
    - **Minimize the range of detection** by only the area inside and near the track, not the entire image, of the area that detects the accident.
    - Increase accuracy and speed by **limiting objects to be detected to people only**.
    - **Optimization of YOLO model** increases inference performance and speed.
---------------------------

Technology
---------------------------
> ### Auto Line Detection
- To automatically detect the boundary of the track, we used a grayscale, canny edge detection, and hough transformation from opencv.
- How to automatically detect lines
    - Reducing the three-dimensional operation of the rgb value to one-dimensional using Grayscale, and detecting the edges required for hough transformation using Canny algorithm.
    - At this time, track boundaries are often difficult to see in clear straight lines and may not be easily detected, depending on the quality of the camera and the thickness of the line. So we can adjust the parameters of the Canny function so that users can find the right straight line.
    - Afterwards, we received the desired margin value from the user and set the ROI to detail the person.   
    *We were able to find about 32 cases in the process of setting up ROIs, and we implemented our own algorithm that considered all of these cases.*

> ### Optimization yolo model using tensorRT
- TensorRT is a model optimization engine that can help improve deep learning services by automatically applying network compression, network optimization, and GPU optimization technologies to deep learning models for optimal inference performance on NVIDIA platforms.
- TensorRT optimizes models through technologies such as Quantization, Precision Calibration, and Graph Optimization.
- How to optimize model
    - Reduce the size of data and the number of bits of weights to reduce precision for fast and efficient operations.
    - Reducing precision affects model accuracy, so additional calibration is performed to minimize loss of information.
    - Graph optimization simplifies model graphs to reduce the number of layers in the model.
**Using the optimized yolo model using tensorRT showed approximately 4.2 times faster inference speed than using the traditional darknet yolo model.**

> ### Networking
- We used tcp socket communication to quickly communicate risk detection to stakeholders without going through the cloud server.

> ### Mobile Application
- Risk detection information can be sent to the stakeholders via socket and stored in the Firebase database to check the accident history with the app.
- Multiple clients can be managed with multi-threading.
---------------------------

Result
---------------------------
![Result](https://github.com/JunHeon-Ch/Rail_Fall_Prevention_System/blob/master/wiki_image/result1.png)
![Result](https://github.com/JunHeon-Ch/Rail_Fall_Prevention_System/blob/master/wiki_image/result2.png)
As a result of minimizing of process, we significantly reduced the number of object detection, and the results of checking processing time per frame have been reduced by approximately 12 seconds in vedio that takes 1 minute and 17 seconds, resulting in a **performance improvement of 1.84%** over just using the model.
---------------------------

Team Members
---------------------------
||최준헌|양희림|최한빈|전수환|
|:---:|:---:|:---:|:---:|:---:|
|E-mail   |chjh12100@gmail.com|yanghl1998@gmail.com|wkghskak@naver.com|jsuhwan34@gmail.com|
|Role   |Line Detection & Object detection & Set TensorRt|Notification (Speaker, App), Connect app and server|Setting preferences & Person detection(YOLO) & Auto line detection & Implement TCP Socket|Notification & GUI|



