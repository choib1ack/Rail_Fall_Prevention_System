# https://076923.github.io/posts/Python-opencv-2/
import cv2
import numpy as np
import sys
from tkinter import *
from tkinter import messagebox
from functools import reduce
from multiprocessing import Process
import operator
import math

WIDTH = 640
HEIGHT = 480

pause = 0
check = 0
now_frame = None
ix, iy = -1, -1
pre_event = -1
pre_frame = []
pre_point = []
now_point = []
margin_point = []
corners = []
count = 0
value = 0


# 점과 점사이 직선의 윈도우 테두리 점 찾기
def find_point(p1, p2):
    # a -> 기울기
    # b -> 절편
    if p2[1] == p1[1]:
        c = round(p1[1])
        return 0, c, WIDTH, c
    if p2[0] == p1[0]:
        c = round(p1[0])
        return c, 0, c, HEIGHT

    a = (p2[0] - p1[0]) / (p2[1] - p1[1])
    b = (-1) * a * p1[1] + p1[0]

    x1, y1, x2, y2 = 0, 0, 0, 0
    if a >= 0:
        if 0 <= b <= WIDTH:
            # 상
            x1 = b
            y1 = 0
        elif 0 <= (-1) * b / a <= HEIGHT:
            # 좌
            x1 = 0
            y1 = (-1) * b / a

        if 0 <= (WIDTH - b) / a <= HEIGHT:
            # 우
            x2 = WIDTH
            y2 = (WIDTH - b) / a
        elif 0 <= a * HEIGHT + b <= WIDTH:
            # 하
            x2 = a * HEIGHT + b
            y2 = HEIGHT

    else:
        if 0 <= b <= WIDTH:
            # 상
            x1 = b
            y1 = 0
        elif 0 <= (WIDTH - b) / a <= HEIGHT:
            # 우
            x1 = WIDTH
            y1 = (WIDTH - b) / a

        if 0 <= a * HEIGHT + b <= WIDTH:
            # 하
            x2 = a * HEIGHT + b
            y2 = HEIGHT
        elif 0 <= (-1) * b / a <= HEIGHT:
            # 좌
            x2 = 0
            y2 = (-1) * b / a

    x1 = round(x1)
    x2 = round(x2)
    y1 = round(y1)
    y2 = round(y2)

    return x1, y1, x2, y2


# 마우스 콜백 함수
def mouse_callback(event, x, y, flags, param):
    global ix, iy, pre_event, count, now_frame

    pre_event = event

    # 프레임 고정
    if pause == 1:
        if event == cv2.EVENT_FLAG_LBUTTON:
            if now_frame is None:
                now_frame = frame.copy()

            if ix == x and iy == y:
                '''
                경고 메시지 UI
                '''
                warn_msg("같은 위치에 점을 찍을 수 없습니다!")
                # 팝업
                print('Error: 같은 위치에 점을 찍을 수 없습니다.')

            elif count < 4:
                count += 1
                tmp = now_frame.copy()
                pre_frame.append(tmp)

                # 점찍기
                cv2.circle(now_frame, (x, y), 1, (255, 0, 0), 2, cv2.FILLED)
                if ix == -1 and iy == -1:
                    pre_point.append((-1, -1))
                    ix, iy = x, y
                else:
                    # 라인그리기
                    x1, y1, x2, y2 = find_point((ix, iy), (x, y))
                    cv2.line(now_frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
                    pre_point.append((ix, iy))
                    now_point.append((ix, iy))
                    now_point.append((x, y))
                    ix, iy = -1, -1

                cv2.imshow("Video frame", now_frame)
            else:
                '''
                경고 메시지 UI
                '''
                warn_msg("더이상 점을 찍을 수 없습니다!")
                # 팝업
                print('Error: 더이상 점을 찍을 수 없습니다.')

        elif event == cv2.EVENT_MOUSEWHEEL:
            # 뒤로가기
            if len(pre_frame) > 0:
                now_frame = pre_frame.pop().copy()
                ix, iy = pre_point.pop()
                if count % 2 == 0:
                    now_point.pop()
                    now_point.pop()

                cv2.imshow("Video frame", now_frame)
                count -= 1
            else:
                '''
                경고 메시지 UI
                '''
                warn_msg("프레임이 없습니다!")
                # 팝업
                print('Error: 프레임이 없습니다.')


def make_roi():
    mask = np.zeros(frame.shape, dtype=np.uint8)
    roi_corners = np.array([corners], dtype=np.int32)

    # fill the ROI so it doesn't get wiped out when the mask is applied
    channel_count = frame.shape[2]
    ignore_mask_color = (255,) * channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)

    # apply the mask
    masked_frame = cv2.bitwise_and(frame, mask)

    # save the result
    cv2.imshow('Video frame', masked_frame)


def sorting_corners():
    global corners

    center = tuple(map(operator.truediv, reduce(lambda x, y: map(operator.add, x, y), corners), [len(corners)] * 2))
    corners = sorted(corners,
                     key=lambda coord: (-135 - math.degrees(
                         math.atan2(*tuple(map(operator.sub, coord, center))[::-1]))) % 360)


def check_intersection(x1, y1, x2, y2, x3, y3, x4, y4):
    if y1 == y2 and y3 == y4:
        return -1, -1
    if y1 == y2:
        cy = y1
        m2 = (x3 - x4) / (y3 - y4)
        cx = m2 * (cy - y3) + x3
    elif y3 == y4:
        cy = y3
        m1 = (x1 - x2) / (y1 - y2)
        cx = m1 * (cy - y1) + x1
    else:
        m1 = (x1 - x2) / (y1 - y2)
        m2 = (x3 - x4) / (y3 - y4)
        if m1 == m2:
            return -1, -1
        cy = (y1 * m1 - x1 - y3 * m2 + x3) / (m1 - m2)
        cx = m1 * (cy - y1) + x1

    if 0 <= cx <= WIDTH and 0 <= cy <= HEIGHT:
        return round(cx), round(cy)
    else:
        return -1, -1


def count_corners():
    global pause, pre_event, now_frame, ix, iy, count, check

    # 사용자가 찍은 점 4개의 좌표
    x = []
    y = []
    for point in margin_point:
        x.append(point[0])
        y.append(point[1])

    # 사용자가 찍은 4개의 점으로부터 만들어진 직선이 윈도우 테두리에 맞닿는 좌표
    fx1, fy1, fx2, fy2 = find_point((x[0], y[0]), (x[1], y[1]))
    fx3, fy3, fx4, fy4 = find_point((x[2], y[2]), (x[3], y[3]))

    # 두 직선의 교차점이 윈도우 내부에 있는지 확인
    # 윈도우 내부에 있다면 해당 좌표를 반환하고 외부에 있거나 존재하지 않으면 (-1, -1) 반환
    cx, cy = check_intersection(x[0], y[0], x[1], y[1], x[2], y[2], x[3], y[3])
    flag = 0
    # 교차점이 윈도우 내부에 있다면
    if cx != -1 and cy != -1:
        corners.append((cx, cy))

        # 교차점 기준 점 4개가 좌측에 있음
        if x[0] <= cx and x[1] <= cx and x[2] <= cx and x[3] <= cx:
            # 직각
            if fx1 == cx and fx2 == cx:
                if y[0] <= cy and y[1] <= cy:
                    if fy1 == 0:
                        corners.append((fx1, fy1))
                    elif fy2 == 0:
                        corners.append((fx2, fy2))
                elif y[0] >= cy and y[1] >= cy:
                    if fy1 == HEIGHT:
                        corners.append((fx1, fy1))
                    elif fy2 == HEIGHT:
                        corners.append((fx2, fy2))

            elif fx3 == cx and fx4 == cx:
                if y[2] <= cy and y[3] <= cy:
                    if fy3 == 0:
                        corners.append((fx3, fy3))
                    elif fy4 == 0:
                        corners.append((fx4, fy4))
                elif y[2] >= cy and y[3] >= cy:
                    if fy3 == HEIGHT:
                        corners.append((fx3, fy3))
                    elif fy4 == HEIGHT:
                        corners.append((fx4, fy4))
            if fx1 < cx:
                corners.append((fx1, fy1))
            elif fx2 < cx:
                corners.append((fx2, fy2))
            if fx3 < cx:
                corners.append((fx3, fy3))
            elif fx4 < cx:
                corners.append((fx4, fy4))

            flag = 1

        # 교차점 기준 점 4개가 우측에 있음
        elif x[0] >= cx and x[1] >= cx and x[2] >= cx and x[3] >= cx:
            # 직각
            if fx1 == cx and fx2 == cx:
                if y[0] <= cy and y[1] <= cy:
                    if fy1 == 0:
                        corners.append((fx1, fy1))
                    elif fy2 == 0:
                        corners.append((fx2, fy2))
                elif y[0] >= cy and y[1] >= cy:
                    if fy1 == HEIGHT:
                        corners.append((fx1, fy1))
                    elif fy2 == HEIGHT:
                        corners.append((fx2, fy2))

            elif fx3 == cx and fx4 == cx:
                if y[2] <= cy and y[3] <= cy:
                    if fy3 == 0:
                        corners.append((fx3, fy3))
                    elif fy4 == 0:
                        corners.append((fx4, fy4))
                elif y[2] >= cy and y[3] >= cy:
                    if fy3 == HEIGHT:
                        corners.append((fx3, fy3))
                    elif fy4 == HEIGHT:
                        corners.append((fx4, fy4))
            if fx1 > cx:
                corners.append((fx1, fy1))
            elif fx2 > cx:
                corners.append((fx2, fy2))
            if fx3 > cx:
                corners.append((fx3, fy3))
            elif fx4 > cx:
                corners.append((fx4, fy4))

            flag = 2

        # 교차점 기준 점 4개가 하단에 있음
        elif y[0] <= cy and y[1] <= cy and y[2] <= cy and y[3] <= cy:
            # 직각
            if fy1 == cy and fy2 == cy:
                if x[0] <= cx and x[1] <= cx:
                    if fx1 == 0:
                        corners.append((fx1, fy1))
                    elif fx2 == 0:
                        corners.append((fx2, fy2))
                elif x[0] >= cx and x[1] >= cx:
                    if fx1 == WIDTH:
                        corners.append((fx1, fy1))
                    elif fx2 == WIDTH:
                        corners.append((fx2, fy2))

            elif fy3 == cy and fy4 == cy:
                if x[2] <= cx and x[3] <= cx:
                    if fx3 == 0:
                        corners.append((fx3, fy3))
                    elif fx4 == 0:
                        corners.append((fx4, fy4))
                elif x[2] >= cx and x[3] >= cx:
                    if fx3 == WIDTH:
                        corners.append((fx3, fy3))
                    elif fx4 == WIDTH:
                        corners.append((fx4, fy4))
            if fy1 < cy:
                corners.append((fx1, fy1))
            elif fy2 < cy:
                corners.append((fx2, fy2))
            if fy3 < cy:
                corners.append((fx3, fy3))
            elif fy4 < cy:
                corners.append((fx4, fy4))

            flag = 3

        # 교차점 기준 점 4개가 상단에 있음
        elif y[0] >= cy and y[1] >= cy and y[2] >= cy and y[3] >= cy:
            # 직각
            if fy1 == cy and fy2 == cy:
                if x[0] <= cx and x[1] <= cx:
                    if fx1 == 0:
                        corners.append((fx1, fy1))
                    elif fx2 == 0:
                        corners.append((fx2, fy2))
                elif x[0] >= cx and x[1] >= cx:
                    if fx1 == WIDTH:
                        corners.append((fx1, fy1))
                    elif fx2 == WIDTH:
                        corners.append((fx2, fy2))

            elif fy3 == cy and fy4 == cy:
                if x[2] <= cx and x[3] <= cx:
                    if fx3 == 0:
                        corners.append((fx3, fy3))
                    elif fx4 == 0:
                        corners.append((fx4, fy4))
                elif x[2] >= cx and x[3] >= cx:
                    if fx3 == WIDTH:
                        corners.append((fx3, fy3))
                    elif fx4 == WIDTH:
                        corners.append((fx4, fy4))
            if fy1 > cy:
                corners.append((fx1, fy1))
            elif fy2 > cy:
                corners.append((fx2, fy2))
            if fy3 > cy:
                corners.append((fx3, fy3))
            elif fy4 > cy:
                corners.append((fx4, fy4))

            flag = 4

        # 좌표가 한방향으로 찍혀있지 않으면 잘못되었다고 판단
        else:
            '''
             경고 메시지 UI
             '''
            warn_msg("직선을 다시 그려주세요!")
            print('Error: 직선을 다시 그려주세요.')

            pause = 1
            pre_event = -1
            now_frame = None
            ix, iy = -1, -1
            del pre_point[:]
            del now_point[:]
            del corners[:]
            del margin_point[:]
            del pre_frame[:]
            count = 0
            check = 0

            return

    # 교차점이 외부에 있거나 존재하지 않으면
    else:
        corners.append((fx1, fy1))
        corners.append((fx2, fy2))
        corners.append((fx3, fy3))
        corners.append((fx4, fy4))

    # 윈도우 테두리와 두 직선의 교차점 개수
    intersections = [0, 0, 0, 0]

    # 상하좌우 테두리에 몇개의 직선이 지나가는지 확인
    # 0 -> 상 / 1 -> 우 / 2 -> 하 / 3 -> 좌
    for i in range(len(corners)):
        if corners[i][0] == 0:
            intersections[3] += 1
        elif corners[i][0] == WIDTH:
            intersections[1] += 1
        if corners[i][1] == 0:
            intersections[0] += 1
        elif corners[i][1] == HEIGHT:
            intersections[2] += 1

    # 교차점이 윈도우 내부에 존재
    if cx != -1:
        # 4개의 점이 교차점 기준 좌측에 존재
        if flag == 1:
            if intersections[3] == 1:
                if intersections[0] == 1:
                    corners.append((0, 0))
                elif intersections[2] == 1:
                    corners.append((0, HEIGHT))
            elif intersections[3] == 0 and intersections[0] == 1 and intersections[2] == 1:
                corners.append((0, 0))
                corners.append((0, HEIGHT))
        # 4개의 점이 교차점 기준 우측에 존재
        elif flag == 2:
            if intersections[1] == 1:
                if intersections[0] == 1:
                    corners.append((WIDTH, 0))
                elif intersections[2] == 1:
                    corners.append((WIDTH, HEIGHT))
            elif intersections[1] == 0 and intersections[0] == 1 and intersections[2] == 1:
                corners.append((WIDTH, 0))
                corners.append((WIDTH, HEIGHT))
        # 4개의 점이 교차점 기준 상단에 존재
        elif flag == 3:
            if intersections[0] == 1:
                if intersections[1] == 1:
                    corners.append((WIDTH, 0))
                elif intersections[3] == 1:
                    corners.append((0, 0))
            elif intersections[0] == 0:
                corners.append((WIDTH, 0))
                corners.append((0, 0))
        # 4개의 점이 교차점 기준 하단에 존재
        elif flag == 4:
            if intersections[2] == 1:
                if intersections[1] == 1:
                    corners.append((WIDTH, HEIGHT))
                elif intersections[3] == 1:
                    corners.append((0, HEIGHT))
            elif intersections[2] == 0:
                corners.append((WIDTH, HEIGHT))
                corners.append((0, HEIGHT))

    # 교차점이 없거나 윈도우 외부에 존재
    else:
        # 2개의 직선이 지나가는 면을 확인한다
        # 2개의 직선이 지나가는 면이 2개 -> 4개의 포인트로 진행
        # 2개의 직선이 지나가는 면이 1개 -> 모서리 포인트 추가
        # 2개의 직선이 지나가는 면이 0개 -> 양쪽 코너 추가
        cnt = intersections.count(2)
        if cnt:
            i = intersections.index(2)  # 지나가는 선분이 2개인 면 인덱스
            j = i  # 지나가는 선분이 2개인 면의 반대면 인덱스
            if i > 1:
                j -= 2
            else:
                j += 2

            if intersections[j] == 1:
                # 반대면이 1개의 직선이 지나가면 나머지 두 면 중 하나의 면에 직선이 지나감
                if j % 2 == 0:
                    if i > j:  # 2(하)가 직선 2개
                        if intersections[1] == 1:
                            corners.append((WIDTH, 0))
                        elif intersections[3] == 1:
                            corners.append((0, 0))
                    else:  # 0(상)이 직선 2개
                        if intersections[1] == 1:
                            corners.append((WIDTH, HEIGHT))
                        elif intersections[3] == 1:
                            corners.append((0, HEIGHT))
                else:
                    if i > j:  # 3(좌)이 직선 2개
                        if intersections[0] == 1:
                            corners.append((WIDTH, 0))
                        elif intersections[2] == 1:
                            corners.append((WIDTH, HEIGHT))
                    else:  # 1(우)이 직선 2개
                        if intersections[0] == 1:
                            corners.append((0, 0))
                        elif intersections[2] == 1:
                            corners.append((0, HEIGHT))
            elif intersections[j] == 0:
                # 반대면에 맞닿는 직선이 없으면 좌우 or 상하에 직선이 하나씩 지나감
                if j == 0:
                    corners.append((0, 0))
                    corners.append((WIDTH, 0))
                elif j == 1:
                    corners.append((WIDTH, 0))
                    corners.append((WIDTH, HEIGHT))
                elif j == 2:
                    corners.append((0, HEIGHT))
                    corners.append((WIDTH, HEIGHT))
                elif j == 3:
                    corners.append((0, 0))
                    corners.append((0, HEIGHT))

        elif cnt == 0:
            # 4개의 면에 하나씩 선분이 지나가는 경우 -> 두 직선의 기울기가 같은 부호임
            a = (x[0] - x[1]) / (y[0] - y[1])
            if a > 0:
                corners.append((0, 0))
                corners.append((WIDTH, HEIGHT))
            elif a < 0:
                corners.append((WIDTH, 0))
                corners.append((0, HEIGHT))


# 점 p3 가 직선(p1-p2)의 왼쪽 공간에 있다면 음수, 오른쪽 공간에 있다면 양수, 직선과 겹친다면 0
def check_direction(p1, p2, p3):
    return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p3[0] - p1[0]) * (p2[1] - p1[1])


def draw_margin_line():
    # 사용자가 찍은 점 4개의 좌표
    x = []
    y = []
    for point in now_point:
        x.append(point[0])

    # x축과 맞물리는 각도를 구한다
    theta = []
    slope = []
    for i in range(0, 3, 2):
        if x[i] == x[i + 1]:
            theta.append(90)
            slope.append(0)
        elif y[i] == y[i + 1]:
            theta.append(0)
            slope.append(sys.maxsize)
        else:
            dx = abs(x[i + 1] - x[i])
            dy = abs(y[i + 1] - y[i])
            theta.append(math.atan(dy / dx))
            slope.append((y[i + 1] - y[i]) / (x[i + 1] - x[i]))

    # 방향성을 아래 -> 위 or 왼 -> 오 바꿈
    if y[0] < y[1]:
        x[0], x[1] = x[1], x[0]
        y[0], y[1] = y[1], y[0]
    elif y[0] == y[1] and x[0] > x[1]:
        x[0], x[1] = x[1], x[0]
        y[0], y[1] = y[1], y[0]

    direction = check_direction((x[0], y[0]), (x[1], y[1]), (x[2], y[2]))
    vx1 = value * math.sin(theta[0])
    vy1 = value * math.cos(theta[0])
    vx2 = value * math.sin(theta[1])
    vy2 = value * math.cos(theta[1])

    mp11, mp12 = (-1, -1), (-1, -1)
    mp21, mp22 = (-1, -1), (-1, -1)

    cx, cy = check_intersection(x[0], y[0], x[1], y[1], x[2], y[2], x[3], y[3])

    if direction > 0:
        if slope[0] == 0:
            mp11 = (x[0] - value, y[0])
            mp12 = (x[1] - value, y[1])

            # 0 - 0
            if slope[1] == 0:
                mp21 = (x[2] + value, y[2])
                mp22 = (x[3] + value, y[3])

            # 0 - 180
            elif slope[1] == sys.maxsize:
                if y[2] <= y[0] and y[2] <= y[1]:
                    mp21 = (x[2], y[2] - value)
                    mp22 = (x[3], y[3] - value)
                elif y[2] >= y[0] and y[2] >= y[1]:
                    mp21 = (x[2], y[2] + value)
                    mp22 = (x[3], y[3] + value)

            # 0 - +
            # 0 - -
            else:
                if slope[1] > 0:
                    if y[2] >= cy and y[3] >= cy and y[0] <= cy and y[1] <= cy:
                        mp21 = (x[2] - vx2, y[2] + vy2)
                        mp22 = (x[3] - vx2, y[3] + vy2)
                    else:
                        mp21 = (x[2] + vx2, y[2] - vy2)
                        mp22 = (x[3] + vx2, y[3] - vy2)

                elif slope[1] < 0:
                    if y[2] <= cy and y[3] <= cy and y[0] >= cy and y[1] >= cy:
                        mp21 = (x[2] - vx2, y[2] - vy2)
                        mp22 = (x[3] - vx2, y[3] - vy2)
                    else:
                        mp21 = (x[2] + vx2, y[2] + vy2)
                        mp22 = (x[3] + vx2, y[3] + vy2)

        elif slope[0] == sys.maxsize:
            mp11 = (x[0], y[0] - value)
            mp12 = (x[1], y[1] - value)

            # 180 - 180
            if slope[1] == sys.maxsize:
                mp21 = (x[2], y[2] + value)
                mp22 = (x[3], y[3] + value)

            # 180 - 0
            elif slope[1] == 0:
                mp21 = (x[2] + value, y[2])
                mp22 = (x[3] + value, y[3])

            # 180 - +
            # 180 - -
            else:
                if slope[1] > 0:
                    if x[2] >= cx and x[3] >= cx and x[0] <= cx and x[1] <= cx:
                        mp21 = (x[2] + vx2, y[2] - vy2)
                        mp22 = (x[3] + vx2, y[3] - vy2)
                    else:
                        mp21 = (x[2] - vx2, y[2] + vy2)
                        mp22 = (x[3] - vx2, y[3] + vy2)

                elif slope[1] < 0:
                    if x[2] <= cx and x[3] <= cx and x[0] >= cx and x[1] >= cx:
                        mp21 = (x[2] - vx2, y[2] - vy2)
                        mp22 = (x[3] - vx2, y[3] - vy2)
                    else:
                        mp21 = (x[2] + vx2, y[2] + vy2)
                        mp22 = (x[3] + vx2, y[3] + vy2)

        elif slope[0] > 0:
            mp11 = (x[0] - vx1, y[0] + vy1)
            mp12 = (x[1] - vx1, y[1] + vy1)

            # + - 0
            if slope[1] == 0:
                if x[2] <= x[0] and x[2] <= x[1]:
                    mp21 = (x[2] - value, y[2])
                    mp22 = (x[3] - value, y[3])
                elif x[2] >= x[0] and x[2] >= x[1]:
                    mp21 = (x[2] + value, y[2])
                    mp22 = (x[3] + value, y[3])

            # + - 180
            elif slope[1] == sys.maxsize:
                if y[2] <= y[0] and y[2] <= y[1]:
                    mp21 = (x[2], y[2] - value)
                    mp22 = (x[3], y[3] - value)
                elif y[2] >= y[0] and y[2] >= y[1]:
                    mp21 = (x[2], y[2] + value)
                    mp22 = (x[3], y[3] + value)

            # + - +
            elif slope[1] > 0:
                mp21 = (x[2] + vx2, y[2] - vy2)
                mp22 = (x[3] + vx2, y[3] - vy2)

            # + - -
            elif slope[1] < 0:
                if y[2] <= y[0] and y[2] <= y[1]:
                    mp21 = (x[2] - vx2, y[2] - vy2)
                    mp22 = (x[3] - vx2, y[3] - vy2)
                elif x[2] >= x[0] and x[2] >= x[1]:
                    mp21 = (x[2] + vx2, y[2] + vy2)
                    mp22 = (x[3] + vx2, y[3] + vy2)

        elif slope[0] < 0:
            mp11 = (x[0] - vx1, y[0] - vy1)
            mp12 = (x[1] - vx1, y[1] - vy1)

            # - - 0
            if slope[1] == 0:
                if x[2] <= x[0] and x[2] <= x[1]:
                    mp21 = (x[2] - value, y[2])
                    mp22 = (x[3] - value, y[3])
                elif x[2] >= x[0] and x[2] >= x[1]:
                    mp21 = (x[2] + value, y[2])
                    mp22 = (x[3] + value, y[3])

            # - - 180
            elif slope[1] == sys.maxsize:
                if y[2] <= y[0] and y[2] <= y[1]:
                    mp21 = (x[2], y[2] - value)
                    mp22 = (x[3], y[3] - value)
                elif y[2] >= y[0] and y[2] >= y[1]:
                    mp21 = (x[2], y[2] + value)
                    mp22 = (x[3], y[3] + value)

            # - - +
            elif slope[1] > 0:
                if y[2] >= y[0] and y[2] >= y[1]:
                    mp21 = (x[2] - vx2, y[2] + vy2)
                    mp22 = (x[3] - vx2, y[3] + vy2)
                elif x[2] >= x[0] and x[2] >= x[1]:
                    mp21 = (x[2] + vx2, y[2] - vy2)
                    mp22 = (x[3] + vx2, y[3] - vy2)

            # - - -
            elif slope[1] < 0:
                mp21 = (x[2] + vx2, y[2] + vy2)
                mp22 = (x[3] + vx2, y[3] + vy2)

    elif direction < 0:
        if slope[0] == 0:
            mp11 = (x[0] + value, y[0])
            mp12 = (x[1] + value, y[1])

            # 0 - 0
            if slope[1] == 0:
                if x[2] <= x[0] and x[2] <= x[1]:
                    mp21 = (x[2] - value, y[2])
                    mp22 = (x[3] - value, y[3])
                elif x[2] >= x[0] and x[2] >= x[1]:
                    mp21 = (x[2] + value, y[2])
                    mp22 = (x[3] + value, y[3])

            # 0 - 180
            elif slope[1] == sys.maxsize:
                if y[2] <= y[0] and y[2] <= y[1]:
                    mp21 = (x[2], y[2] - value)
                    mp22 = (x[3], y[3] - value)
                elif y[2] >= y[0] and y[2] >= y[1]:
                    mp21 = (x[2], y[2] + value)
                    mp22 = (x[3], y[3] + value)

            # 0 - +
            # 0 - -
            else:
                if slope[1] > 0:
                    if y[2] <= cy and y[3] <= cy and y[0] >= cy and y[1] >= cy:
                        mp21 = (x[2] + vx2, y[2] - vy2)
                        mp22 = (x[3] + vx2, y[3] - vy2)
                    else:
                        mp21 = (x[2] - vx2, y[2] + vy2)
                        mp22 = (x[3] - vx2, y[3] + vy2)

                elif slope[1] < 0:
                    if y[2] >= cy and y[3] >= cy and y[0] <= cy and y[1] <= cy:
                        mp21 = (x[2] + vx2, y[2] + vy2)
                        mp22 = (x[3] + vx2, y[3] + vy2)
                    else:
                        mp21 = (x[2] - vx2, y[2] - vy2)
                        mp22 = (x[3] - vx2, y[3] - vy2)

        elif slope[0] == sys.maxsize:
            mp11 = (x[0], y[0] + value)
            mp12 = (x[1], y[1] + value)

            # 180 - 180
            if slope[1] == sys.maxsize:
                mp21 = (x[2], y[2] - value)
                mp22 = (x[3], y[3] - value)

            # 180 - 0
            elif slope[1] == 0:
                if x[2] <= x[0] and x[2] <= x[1]:
                    mp21 = (x[2] - value, y[2])
                    mp22 = (x[3] - value, y[3])
                elif x[2] >= x[0] and x[2] >= x[1]:
                    mp21 = (x[2] + value, y[2])
                    mp22 = (x[3] + value, y[3])

            # 180 - +
            # 180 - -
            else:
                if slope[1] > 0:
                    if x[2] <= cx and x[3] <= cx and x[0] >= cx and x[1] >= cx:
                        mp21 = (x[2] - vx2, y[2] + vy2)
                        mp22 = (x[3] - vx2, y[3] + vy2)
                    else:
                        mp21 = (x[2] + vx2, y[2] - vy2)
                        mp22 = (x[3] + vx2, y[3] - vy2)

                elif slope[1] < 0:
                    if x[2] >= cx and x[3] >= cx and x[0] <= cx and x[1] <= cx:
                        mp21 = (x[2] + vx2, y[2] + vy2)
                        mp22 = (x[3] + vx2, y[3] + vy2)
                    else:
                        mp21 = (x[2] - vx2, y[2] - vy2)
                        mp22 = (x[3] - vx2, y[3] - vy2)

        elif slope[0] > 0:
            mp11 = (x[0] + vx1, y[0] - vy1)
            mp12 = (x[1] + vx1, y[1] - vy1)

            # + - 0
            if slope[1] == 0:
                if x[2] <= x[0] and x[2] <= x[1]:
                    mp21 = (x[2] - value, y[2])
                    mp22 = (x[3] - value, y[3])
                elif x[2] >= x[0] and x[2] >= x[1]:
                    mp21 = (x[2] + value, y[2])
                    mp22 = (x[3] + value, y[3])

            # + - 180
            elif slope[1] == sys.maxsize:
                if y[2] <= y[0] and y[2] <= y[1]:
                    mp21 = (x[2], y[2] - value)
                    mp22 = (x[3], y[3] - value)
                elif y[2] >= y[0] and y[2] >= y[1]:
                    mp21 = (x[2], y[2] + value)
                    mp22 = (x[3], y[3] + value)

            # + - +
            elif slope[1] > 0:
                mp21 = (x[2] - vx2, y[2] + vy2)
                mp22 = (x[3] - vx2, y[3] + vy2)

            # + - -
            elif slope[1] < 0:
                if y[2] >= y[0] and y[2] >= y[1]:
                    mp21 = (x[2] + vx2, y[2] + vy2)
                    mp22 = (x[3] + vx2, y[3] + vy2)
                elif x[2] <= x[0] and x[2] <= x[1]:
                    mp21 = (x[2] - vx2, y[2] - vy2)
                    mp22 = (x[3] - vx2, y[3] - vy2)

        elif slope[0] < 0:
            mp11 = (x[0] + vx1, y[0] + vy1)
            mp12 = (x[1] + vx1, y[1] + vy1)

            # - - 0
            if slope[1] == 0:
                if x[2] <= x[0] and x[2] <= x[1]:
                    mp21 = (x[2] - value, y[2])
                    mp22 = (x[3] - value, y[3])
                elif x[2] >= x[0] and x[2] >= x[1]:
                    mp21 = (x[2] + value, y[2])
                    mp22 = (x[3] + value, y[3])

            # - - 180
            elif slope[1] == sys.maxsize:
                if y[2] <= y[0] and y[2] <= y[1]:
                    mp21 = (x[2], y[2] - value)
                    mp22 = (x[3], y[3] - value)
                elif y[2] >= y[0] and y[2] >= y[1]:
                    mp21 = (x[2], y[2] + value)
                    mp22 = (x[3], y[3] + value)

            # - - +
            elif slope[1] > 0:
                mp21 = (x[2] - vx2, y[2] + vy2)
                mp22 = (x[3] - vx2, y[3] + vy2)
                if y[2] <= y[0] and y[2] <= y[1]:
                    mp21 = (x[2] + vx2, y[2] - vy2)
                    mp22 = (x[3] + vx2, y[3] - vy2)
                elif x[2] <= x[0] and x[2] <= x[1]:
                    mp21 = (x[2] - vx2, y[2] + vy2)
                    mp22 = (x[3] - vx2, y[3] + vy2)

            # - - -
            elif slope[1] < 0:
                mp21 = (x[2] - vx2, y[2] - vy2)
                mp22 = (x[3] - vx2, y[3] - vy2)

    margin_point.append((round(mp11[0]), round(mp11[1])))
    margin_point.append((round(mp12[0]), round(mp12[1])))
    margin_point.append((round(mp21[0]), round(mp21[1])))
    margin_point.append((round(mp22[0]), round(mp22[1])))

    # elif direction == 0:
    '''이거랑 직각'''


def popup_destroy():
    root.destroy()


def start_destroy():
    start.destroy()

def system_destroy():
    sys.exit()


def save_value(event):
    global value
    value = int(txt.get())


# UI창을 가운데 놓기 (ui, 창의 가로크기, 창의 세로크기)
def center_window(ui, width, height):
    # get screen width and height
    screen_width = ui.winfo_screenwidth()
    screen_height = ui.winfo_screenheight()
    # 창을 놓을 수 있는 위치를 계산
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)

    ui.geometry('%dx%d+%d+%d' % (width, height, x, y))


def warn_msg(msg):
    messagebox.showerror("Error", msg)


'''
시작 UI
작동방법 설명
'''
start = Tk()
start.title("프로그램")
center_window(start, 900, 400)
start.resizable(0, 0)

topFrame = Frame(start, relief="solid")
topFrame.pack(side="top")

bottomFrame = Frame(start, relief="solid", height="100")
bottomFrame.pack(side="bottom", expand=True)

img = PhotoImage(master=topFrame, file="explanation2.png")
imgLbl = Label(topFrame, image=img)
imgLbl.pack()

confirmBtn = Button(bottomFrame, text='설정시작', width=6, height=1, command=start_destroy)
confirmBtn.grid(row=0, column=0)
closeBtn = Button(bottomFrame, text='종료', width=3, height=1, command=system_destroy)
closeBtn.grid(row=0, column=1)

start.mainloop()

# n은 카메라의 장치 번호를 의미합니다. 노트북을 이용할 경우, 내장 카메라가 존재하므로 카메라의 장치 번호는 0이 됩니다.
# 카메라를 추가적으로 연결하여 외장 카메라를 사용하는 경우, 장치 번호가 1~n까지 변화합니다.

# capture.set(option, n)을 이용하여 카메라의 속성을 설정할 수 있습니다.
# option은 프레임의 너비와 높이 등의 속성을 설정할 수 있습니다.
# n의 경우 해당 너비와 높이의 값을 의미합니다.

# 멀티 스레드 구현부분 (제어 part와 카메라 part를 나눈다)
# '''
# 제어 UI
# '''
# def win_control():
#     control = Tk()
#     control.title("Control cam")
#     center_window(control, 300, 400)
#     control.resizable(False, False)

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

cv2.namedWindow('Video frame')

# 변경방법 1: 키보드 waitkey변경 (종료: ESC, 영상정지: space bar, 다시재생: Enter -- 한번씩만 눌러도 잘됨)
while True:
    cv2.setMouseCallback('Video frame', mouse_callback)

    # 연속 프레임
    if pause == 0:
        ret, frame = capture.read()
        k = cv2.waitKey(1)
        if check == 0:
            cv2.imshow("Video frame", frame)
        elif check == 1:
            fx1, fy1, fx2, fy2 = find_point((now_point[0][0], now_point[0][1]), (now_point[1][0], now_point[1][1]))
            fx3, fy3, fx4, fy4 = find_point((now_point[2][0], now_point[2][1]), (now_point[3][0], now_point[3][1]))
            cv2.line(frame, (fx1, fy1), (fx2, fy2), (0, 0, 255), 1)
            cv2.line(frame, (fx3, fy3), (fx4, fy4), (0, 0, 255), 1)

            make_roi()

        # 종료
        if k == 27: # ESC key
            '''
            알림(확인/취소) UI
            '''
            root = Tk()
            root.title("프로그램")
            center_window(root, 400, 250)
            root.resizable(0, 0)

            frame1 = Frame(root, relief="solid", height="100")
            frame1.pack(side="top")
            frame2 = Frame(root, relief="solid", height="100")
            frame2.pack(side="bottom", expand=True)

            text = '종료하시겠습니까?'
            lbl = Label(frame1, text=text, font="NanumGothic 10")
            lbl.pack()

            confirmBtn = Button(frame2, text='확인', width=3, height=1, command=system_destroy)
            confirmBtn.grid(row=0, column=0)
            cancelBtn = Button(frame2, text='취소', width=3, height=1, command=popup_destroy)
            cancelBtn.grid(row=0, column=1)

            root.mainloop()
        # 프레임 고정
        elif k == 32: # spacebar key
            ret, frame = capture.read()
            pause = 1
            pre_event = -1
            now_frame = None
            ix, iy = -1, -1
            del pre_point[:]
            del now_point[:]
            del corners[:]
            del pre_frame[:]
            del margin_point[:]
            count = 0
            check = 0

    # 고정 프레임
    elif pause == 1:
        if count == 0:
            cv2.imshow("Video frame", frame)
        cv2.waitKey(1)

        # 연속 프레임
        if cv2.waitKey(1) == 13: # Enter key
            pause = 0
            pre_event = -1
            check = 0
        # 마진 설정
        elif pre_event == cv2.EVENT_FLAG_RBUTTON:
            if count == 4:
                value = 0
                # 반드시 직선 2개가 있어야 마진을 설정할 수 있음
                margin = Tk()
                margin.title("Set margin")
                center_window(margin, 400, 250)
                margin.resizable(0, 0)

                margin_frame1 = Frame(margin, height=100)
                margin_frame1.pack(side="top")
                margin_frame2 = Frame(margin, height=100)
                margin_frame2.pack(expand=True)

                margin_text = '< 마진을 설정해주세요 >\n(마진값 저장-> Enter key)\n\n'
                margin_lbl1 = Label(margin_frame1, text=margin_text, font="NanumGothic 10")
                margin_lbl1.grid(row=0, column=0, columnspan=2)

                text = '마진값:  '
                margin_lbl2 = Label(margin_frame1, text=text, font="NanumGothic 10")
                margin_lbl2.grid(row=1, column=0)
                # value = StringVar()
                txt = Entry(margin_frame1)
                txt.bind("<Return>", save_value)
                txt.grid(row=1, column=1)

                confirmBtn = Button(margin_frame2, text='확인', width=3, height=1, command=margin.destroy)
                confirmBtn.grid(row=2, column=0)
                backBtn = Button(margin_frame2, text='뒤로 가기', height=1, command=margin.destroy)
                backBtn.grid(row=2, column=1)

                margin.mainloop()

                draw_margin_line()

                count_corners()
                if count != 0:
                    sorting_corners()

                    check = 1
                    pause = 0

            elif count < 4:
                '''
                오류 메시지 UI
                '''
                warn_msg("직선 두개를 그려주세요")

# ---------------------------------------------------------------------------------------

capture.release()
cv2.destroyAllWindows()