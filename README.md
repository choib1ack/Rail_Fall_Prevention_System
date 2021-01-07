Rail Fall Prevention System
=============================
The Rail Fall Prevention System is designed to prevent rail crashes by determining whether a person fall on a rail.

[Introduction Videos](https://github.com/JunHeon-Ch/Rail_Fall_Prevention_System/wiki/Videos)
---------------------------
Click on the following picture to watch the *Proposal video*.

[![Proposal 영상을 시청하려면 다음 사진을 클릭해주세요.](https://img.youtube.com/vi/II5gYJ-4010/0.jpg)](https://www.youtube.com/watch?v=II5gYJ-4010)

Click on the following picture to watch the *Final video*.

[![Final 영상을 시청하려면 다음 사진을 클릭해주세요.](https://img.youtube.com/vi/kym3mti6I8A/0.jpg)](https://www.youtube.com/watch?v=kym3mti6I8A&feature=youtu.be)

DEMO video
---------------------------
[![Demo video](https://img.youtube.com/vi/E-d7NiPAkk8/0.jpg)](https://www.youtube.com/watch?v=E-d7NiPAkk8)

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
현재 대부분의 승강장에는 스크린도어가 설치되어 있지만 KTX나 무궁화호 열차가 정차하는 승강장에서는 열차 문마다 크기, 높이, 위치가 달라 *정지 위치 유지*에 어려움을 겪고 있다.
스크린 도어 설치에 대한 예산 문제로 인해 일부 지역의 *스크린 도어 설치율이 매우 낮습니다*.
- **GIDS**   
GIDS는 적외선센서를 이용해 접근거리를 인식하는 기술을 이용하여 비용도 절감할 수 있어 다양한 플랫폼에 적용할 수 있지만 *센서 제한 때문에 정확도가 낮습니다*.

**기존의 스크린 도어와 GIDS의 단점을 보완하기 위해 영상을 활용하여 추락을 판단할 수 있는 *'영상 인식 기반' 선로 추락 방지 시스템을 고안했다.***



Brief Description
---------------------------
- 엣지 컴퓨팅기법을 통해 좀 더 빠르게 선로추락사고에 대한 대처를 할 수 있도록 하는 시스템입니다.
- 영상인식 기술을 통해 사람이 선로에 떨어지는지에 대한 여부를 판단합니다.
- 사고가 났을때 경고음을 울려주고, 앱을 통해 사고에 대한 정보를 빠르게 알 수 있습니다.

*이 시스템은 다음과 같은 사항을 중점적으로 고려하여 만들어졌습니다.*

1. **`신속성`** : 선로추락사고가 발생하였을때 빠르게 경고 알림을 울리게 하거나 사고에 대한 정보를 전달받기 위해 신속성을 높이기위한 방법을 사용합니다.

2. **`정확성`** : 추락사고의 여부를 판단하는 데 있어서 정확한 판단히 매우 중요하기 때문에 정확성을 높이기위한 방법을 사용합니다.

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
    
Technology
---------------------------
> ### Edge Computing

- 이 시스템이 추구하는 점인 '신속성'을 높이기 위해서 ***엣지 노드***에서 일을 처리하도록 하는 ***엣지 컴퓨팅***을 사용하였습니다.

> ### Jetson Nano

- 엣지 컴퓨팅을 위해 ***엔비디아의 젯슨 나노***를 사용하였습니다.

> ### Open CV

- 웹캠에서 얻어지는 동영상에서 ***ROI지정***을 위해 Open CV를 사용하였습니다. 

> ### YOLO

- CNN, SSD같은 다른 영상인식 툴보다 월등히 빠른속도를 가진 ***YOLO***를 채택하여 보다 신속하게 처리할 수 있도록 하였습니다.

> ### TensorRT

- 이 시스템에서 쓰이고 있는 YOLOv4에 TensorRT를 추가하여 이미지탐색 최적화 모델의 ***속도를 약 4.2배 증가***시켰습니다.

> ### Auto Line Detection

- 화면상에서의 직선을 자동검출하기 위해서 ***허프변환 알고리즘***을 이용해 구현하였습니다.

> ### Android apps

- 엣지 컴퓨터에서 보내준 사고 정보들을 전달받고 알려주는 ***2차 경고를 위한 메세지 앱***을 제작하였습니다.

> ### Speaker

- ***스피커 모듈***을 장착하여 1차 경고로 경고음을 주변에 내도록 하였습니다.

Team Members
---------------------------
||최준헌|양희림|최한빈|전수환|
|:---:|:---:|:---:|:---:|:---:|
|E-mail   |chjh12100@gmail.com|yanghl1998@gmail.com|wkghskak@naver.com|jsuhwan34@gmail.com|
|역할   |Line Detection & Object detection & Set TensorRt|Notification (Speaker, App), Connect app and server|Setting preferences & Person detection(YOLO) & Auto line detection & Implement TCP Socket|Notification & GUI|



