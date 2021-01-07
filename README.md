Rail Fall Prevention System
=============================
Rail Fall Prevention System은 사람이 선로에 떨어지는지에 대한 여부를 판단하여 선로추락사고를 방지하기 위한 시스템입니다.   

[Introduction Videos](https://github.com/JunHeon-Ch/Rail_Fall_Prevention_System/wiki/Videos)
---------------------------
Proposal 영상을 시청하려면 다음 사진을 클릭해주세요.

[![Proposal 영상을 시청하려면 다음 사진을 클릭해주세요.](https://img.youtube.com/vi/II5gYJ-4010/0.jpg)](https://www.youtube.com/watch?v=II5gYJ-4010)

Final 영상을 시청하려면 다음 사진을 클릭해주세요.

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
GIDS can be cost-saving and applicable to a variety of platforms using infrared sensors to recognize access, but *its accuracy is low due to sensor limitations*.

**To compensate for the shortcomings of existing screen doors and GIDS, *we came up with a 'image recognition-based' rail fall prevention system that can be used to determine the rail fall*


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
1. 카메라를 실행시킵니다.
2. 카메라로부터 얻어진 이미지를 토대로, 자동 직선검출을 이용해 구역이 지정됩니다.
3. 검출된 직선구역으로 부족할 경우, 직선의 탐색 범위를 더 넓히고, 마진을 두어 ROI를 설정합니다.
4. 지정된 ROI에서 탐색된 바운더리 박스 밑변의 중앙 점의 좌표를 추출합니다. 
5. 추출한 좌표를 이용하여 추락을 판단합니다.


6. 추락했다고 판단했을 경우 다음 두가지 방법으로 알림을 줍니다.
    - 좌표가 경계에 **걸쳤을경우** : 엣지 디바이스에 장착된 스피커에서 1차 경고로 **경고음**을 줍니다.
    - 좌표가 경계를 **넘어갔을 경우** : 추락으로 판단하여 엣지 디바이스와 연동된 앱으로 2차 **경고 알림 메세지**를 사고 정보와 함께 줍니다.


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



