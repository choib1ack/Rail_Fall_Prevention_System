Rail Fall Prevention System
=============================
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

- 엣지 컴퓨팅기법을 통해 좀 더 빠르게 선로추락사고에 대한 대처를 할 수 있도록 하는 시스템입니다.
- 영상인식 기술을 통해 사람이 선로에 떨어지는지에 대한 여부를 판단합니다.
- 사고가 났을때 경고음을 울려주고, 앱을 통해 사고에 대한 정보를 빠르게 알 수 있습니다.

*이 시스템은 다음과 같은 사항을 중점적으로 고려하여 만들어졌습니다.*

1. **`신속성`** : 선로추락사고가 발생하였을때 빠르게 경고 알림을 울리게 하거나 사고에 대한 정보를 전달받기 위해 신속성을 높이기위한 방법을 사용합니다.

2. **`정확성`** : 추락사고의 여부를 판단하는 데 있어서 정확한 판단히 매우 중요하기 때문에 정확성을 높이기위한 방법을 사용합니다.

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

- **사고 발생**   
사람들이 자주 이용하는 열차에서는 매년 *크고 작은 사고가 발생하며* 실수로 스크린도어나 안전장벽이 없는 선로에 떨어지거나 뛰어내리는 경우가 많습니다.
- **플랫폼 스크린 도어(PSD) 설치 어려움**   
현재 대부분의 승강장에는 스크린도어가 설치되어 있지만 KTX나 무궁화호 열차가 정차하는 승강장에서는 열차 문마다 크기, 높이, 위치가 달라 *정지 위치 유지*에 어려움을 겪고 있습니다.
스크린 도어 설치에 대한 예산 문제로 인해 일부 지역의 *스크린 도어 설치율이 매우 낮습니다*.
- **GIDS**   
GIDS는 적외선센서를 이용해 접근거리를 인식하는 기술을 이용하여 비용도 절감할 수 있어 다양한 플랫폼에 적용할 수 있지만 *센서 제한 때문에 정확도가 낮습니다*.

**기존의 스크린 도어와 GIDS의 단점을 보완하기 위해 영상을 활용하여 추락을 판단할 수 있는 *'영상 인식 기반' 선로 추락 방지 시스템을 고안하였습니다.***

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
    
1. 프로그램을 실행시킵니다.
2. 카메라로부터 얻어진 이미지에서 자동으로 직선을 검출합니다.
3. 사용자가 검출된 직선으로부터 적절한 선로 경계선을 선택하고 마진값을 입력합니다. 
4. 검출된 직선중 적합한 직선이 없을 경우, 직선의 탐색 범위를 더 넓혀 적합한 직선이 검출되도록 해줍니다.
5. 선택한 직선으로부터 마진을 추가하고 해당 구역을 Region Of Interest(ROI)로 설정합니다.
6. ROI 내의 사람 오브젝트만을 디텍션하여 실시간으로 선로에 추락한 사람이 있는지 판단하게 됩니다.
7. 이때, 탐색된 바운더리 박스 밑변의 중앙 점의 좌표를 사람 발의 좌표라고 판단합니다.
8. 발 좌표를 이용하여 추락을 판단합니다.
- 시스템이 사람이 추락했다고 판단했을 경우 다음 두가지 방법으로 알림을 줍니다.
    - 좌표가 경계선에 **걸쳤을 경우** : 엣지 디바이스에 설치된 스피커에서 1차 경고로 **경고음**을 줍니다.
    - 좌표가 경계선을 **넘어갔을 경우** : 추락으로 판단하여 엣지 디바이스와 연동된 앱으로 2차 **경고 알림 메세지**를 사고 정보와 함께 줍니다.  
    - 이때 만약 열차가 들어오게 된다면 열차에 탑승하는 것 또한 선로에 추락했다고 판단할 수 있기 때문에, 열차가 들어오는 시간에는 디텍션을 잠시 멈추게 됩니다.   
    
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

1. 기존 영상인식 시스템에서 사용되는 클라우드 컴퓨팅의 단점
![Architecture](https://github.com/JunHeon-Ch/Rail_Fall_Prevention_System/blob/master/wiki_image/architecture.png)
- As is..
    - 이 시스템을 실제 플랫폼에서 사용한다고 가정해보면, 수많은 카메라로부터 얻어지는 엄청난 양의 프레임을 서버로 전송하게 된다.
    - 이 과정에서 **상당한 대역폭이 소비되고** 이와 동시에 **인터넷 인프라에 지속적이고 상당한 부담이 됩니다**. 또한, 이로 인해 **지연이 발생**할 가능성이 있습니다. 
    - **'실시간성'** 이 중요한 저희 시스템에서는 해당 구조가 부적합하다고 판단하였습니다. 
- To be..
    - 엣지 컴퓨팅 구조를 사용하게 되면, 클라우드 컴퓨팅의 단점을 보완해 **대기 시간 없이 실시간 데이터 처리를 포함하여 데이터 스트림 가속화를 가능하게 해줍니다**. 
    - 이러한 엣지 컴퓨팅의 장점을 살려 실시간성이 중요한 저희 시스템 구조를 고안하였습니다.
2. 프로세싱 최적화   
- 엣지 시스템은 성능 면에서는 클라우드 기반 시스템보다 약점을 보입니다.
- 엣지 컴퓨팅 성능의 약점을 보완하고자 저희는 처리해야 할 연산의 크기를 줄이는 3가지 방법을 고안했다.
    - 사고 상황을 감지하는 지역을 영상 전체가 아닌 선로 내부와 근처 영역만으로 **디텍션 범위를 최소화**.
    - **디텍션 할 오브젝트를 사람으로만 한정**하여 정확도와 신속성을 높임.
    - **YOLO 모델의 최적화**를 통해 추론 성능과 속도를 높임.

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

> ### Auto Line Detection
- 자동으로 선로의 경계선을 검출하기 위해 opencv의 grayscale, canny edge 디텍션, 허프변환을 사용하였습니다.
- auto line detection의 방법
    - Grayscale을 통해 rgb값의 3차원 연산을 1차원으로 줄이고, canny 알고리즘으로 허프변환에 필요한 엣지를 검출합니다.
    - 이때, 선로 경계선은 명확한 직선으로 보기 어려운 경우가 많고 카메라의 화질과 선의 굵기에 따라 직선이 잘 검출되지 않을 수 있습니다. 따라서 저희는 Canny 함수의 파라미터를 조정하면서 사용자들에게 적합한 직선을 찾을 수 있도록 해줍니다.
    - 이후 사용자로부터 원하는 마진값을 입력 받아 사람을 디텍션 할 ROI를 설정하였습니다.   
    *ROI를 설정하는 과정에서 약 32가지의 경우의 수를 찾을 수 있었고 저희는 이러한 경우의 수를 모두 고려한 저희만의 알고리즘을 구현하여 ROI를 설정하였습니다.*

> ### Optimization YOLO using tensorRT
- TensorRT는 NVIDIA 플랫폼에서 최적의 추론 성능을 낼 수 있도록 Network compression, Network optimization, GPU 최적화 기술들을 딥러닝 모델에 자동 적용해 딥러닝 서비스를 개선하는데 도움을 줄 수 있는 모델 최적화 엔진입니다
- TensorRT는 Quantization, Precision Calibration, Graph Optimization 등의 기술을 통해 모델을 최적화해줍니다.
- 모델 최적화 방법
    - 빠르고 효율적인 연산을 위해 데이터의 크기 및 가중치들의 bit 수를 줄여 정밀도를 낮춥니다.
    - 정밀도를 낮추는 것은 모델 정확도에 영향을 주기 때문에 추가적으로 calibration 작업을 수행하여 정보의 손실을 최소화합니다.
    - 그래프 최적화를 통해 모델 그래프를 단순화시켜 모델의 layer 수를 감소시킵니다.
**tensorRT를 사용하여 최적화된 yolo 모델을 사용하는 것이 기존의 darknet yolo 모델을 사용하는 것 보다 약 4.2배의 향상된 추론 속도를 보였습니다.**

> ### Networking
- 저희는 클라우드를 거치지 않고 신속하게 위험 감지 내용을 관계자에게 전달하기 위해 tcp 소켓 통신을 이용했습니다.

> ### Mobile Application
- 위험 감지 정보는 소켓으로 관계자들에게 전송함과 동시에 파이어베이스 데이터베이스에 저장하여 앱으로 사고 내역 확인이 가능합니다.
- 멀티스레딩으로 여러 클라이언트를 관리할 수 있습니다.

---------------------------

Result
---------------------------
![Result](https://github.com/JunHeon-Ch/Rail_Fall_Prevention_System/blob/master/wiki_image/result1.png)
![Result](https://github.com/JunHeon-Ch/Rail_Fall_Prevention_System/blob/master/wiki_image/result2.png)
As a result of minimizing of process, we significantly reduced the number of object detection, and the results of checking processing time per frame have been reduced by approximately 12 seconds in vedio that takes 1 minute and 17 seconds, resulting in a **performance improvement of 1.84%** over just using the model.

![Result](https://github.com/JunHeon-Ch/Rail_Fall_Prevention_System/blob/master/wiki_image/result1.png)
![Result](https://github.com/JunHeon-Ch/Rail_Fall_Prevention_System/blob/master/wiki_image/result2.png)
이러한 모든 기술들을 사용하여 프로세싱을 최소화한 결과 detection 수를 크게 줄였고, frame당 processing 시간을 확인해본 결과 1분 17초의 영상에서 **약 12초의 processing 시간을 줄여 그냥 모델을 사용하는 것보다 약 1.84%의 성능 향상을 볼 수 있었습니다.**

---------------------------

Team Members
---------------------------
||최준헌|양희림|최한빈|전수환|
|:---:|:---:|:---:|:---:|:---:|
|E-mail   |chjh12100@gmail.com|yanghl1998@gmail.com|wkghskak@naver.com|jsuhwan34@gmail.com|
|역할   |Line Detection & Object detection & Set TensorRt|Notification (Speaker, App), Connect app and server|Setting preferences & Person detection(YOLO) & Auto line detection & Implement TCP Socket|Notification & GUI|



