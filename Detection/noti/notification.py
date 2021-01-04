"""notification.py
"""


noti = False


# 점 p3 가 직선(p1-p2)의 왼쪽 공간에 있다면 음수, 오른쪽 공간에 있다면 양수, 직선과 겹친다면 0
def check_direction(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])

    
def first_notification(point, cp):
    # TODO: 직선 범위 지정
    # 1. 사용자가 찍은 점으로 직선을 만든다
    # 2. box의 하단 중간 좌표가 직선에 맞닿는지 확인한다
    # 3. 맞닿았다면 1차로 스피커로 경고음을 낸다

    area1 = abs(check_direction(cp, point[0], point[1]))
    AB1 = ((point[0][0] - point[1][0]) ** 2 + (point[0][1] - point[1][1]) ** 2) ** 0.5
    area2 = abs(check_direction(cp, point[2], point[3]))
    AB2 = ((point[2][0] - point[3][0]) ** 2 + (point[2][1] - point[3][1]) ** 2) ** 0.5

    if area1 / AB1 < 20:
        noti = True
    else:
        noti = False
    
    if area2 / AB2 < 20:
        noti = True
    else:
        noti = False

    return noti


def second_notification(point, center_point):
    # 두 직선에 대한 ccw를 구해 곱해서 -1이면 return true
    ccw1 = check_direction(point[0], point[1], center_point)
    ccw2 = check_direction(point[2], point[3], center_point)

    if ccw1 * ccw2 < 0:
        return True
    else:
        return False


def danger_sound():
    from playsound import playsound

    playsound("./noti/noti.wav")
