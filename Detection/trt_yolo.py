"""trt_yolo.py

This script demonstrates how to do real-time object detection with
TensorRT optimized YOLO engine.
"""
import os
import time
import argparse

import cv2
import pycuda.autoinit  # This is needed for initializing CUDA driver

import numpy as np
import sys
from tkinter import *
from tkinter import messagebox
from functools import reduce
import operator
import math

from utils.yolo_classes import get_cls_dict
from utils.camera import add_camera_args, Camera
from utils.display import open_window, set_display, show_fps
from utils.visualization import BBoxVisualization
from utils.yolo_with_plugins import TrtYOLO


WINDOW_NAME = 'TrtYOLODemo'

x1_points = []
y1_points = []
x2_points = []
y2_points = []

cross_check=0

WIDTH = 0
HEIGHT = 0

pause = 0
check = 0
now_frame = None
ix, iy, ix2, iy2 = -1, -1, -1, -1
pre_event = -1
pre_frame = []
pre_point = []
now_point = []
margin_point = []
corners = []
count = 0
value = 0
param_val = 200
frame = None
root = None
txt = None


def point_dist(x1,y1,x2,y2):
    a = abs(x1-x2)
    b = abs(y1-y2)
    d=math.sqrt((a*a)+(b*b))
    return d


# 수정 -  두 직선이 교차하는지
def is_cross_pt(x11,y11, x12,y12, x21,y21, x22,y22):
    b1 = is_divide_pt(x11,y11, x12,y12, x21,y21, x22,y22)
    b2 = is_divide_pt(x21,y21, x22,y22, x11,y11, x12,y12)
    if b1 and b2:
        return True
    return False


# 수정 - 두 직선의 교점 찾기
def get_crosspt(x1,y1, x2,y2, x3,y3, x4,y4):
    cx = ((((x1 * y2) - (y1 * x2)) * (x3 - x4)) - (x1 - x2) * ((x3 * y4) - (y3 * x4))) / (((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4)))
    cy = ((((x1 * y2) - (y1 * x2)) * (y3 - y4)) - (y1 - y2) * ((x3 * y4) - (y3 * x4))) / (((x1 - x2) * (y3 - y4)) - ((y1 - y2) * (x3 - x4)))
    return cx, cy

# 수정 - 클릭한 위치와 직선의 거리 구하기
def dist(x0,y0, x1,y1, x2,y2):
    area = abs ( (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0) )
    AB = ( (x1 - x2) ** 2 + (y1 - y2) ** 2 ) ** 0.5
    return ( area / AB )


# 수정 - 교차할 경우 점 찾는 함수
def get_newpt():
    cross_p = get_crosspt(now_point[0][0], now_point[0][1], now_point[1][0], now_point[1][1],
                          now_point[2][0], now_point[2][1], now_point[3][0], now_point[3][1])
    nx1, ny1, nx2, ny2, nx3, ny3, nx4, ny4 = -1, -1, -1, -1, -1, -1, -1, -1
    c1, c2 = -1, -1
    m1,n1,m2,n2 = -1,-1,-1,-1

    # 직선이 x축의 수직
    if now_point[1][0] == now_point[0][0]:
        c1 = 0
    # 직선이 x축의 평행
    elif now_point[1][1] == now_point[0][1]:
        c1 = 1
    # 직선의 기울기, y절편
    else:
        m1 = (now_point[1][1] - now_point[0][1]) / (now_point[1][0] - now_point[0][0])
        n1 = now_point[0][1]-(m1 * now_point[0][0])
        c1 = 2

    # 직선이 x축 수직
    if now_point[3][0] == now_point[2][0]:
        c2 = 0
    # 직선이 x축 평행
    elif now_point[3][1] == now_point[2][1]:
        c2 = 1
    # 직선의 기울기, y절편
    else:
        m2 = (now_point[3][1] - now_point[2][1]) / (now_point[3][0] - now_point[2][0])
        n2 = now_point[2][1] - (m2 * now_point[2][0])
        c2 = 2

    # 첫번째 직선
    # 첫번째 점 거리가 더 길어 첫번째 점으로 점 생성
    if point_dist(now_point[0][0], now_point[0][1], cross_p[0], cross_p[1]) > point_dist(now_point[1][0], now_point[1][1], cross_p[0],cross_p[1]):
        if c1 == 0:
            # 1/3지점과 2/3지점
            nx1 = now_point[0][0]
            ny1 = (now_point[0][1] + (2 * cross_p[1])) / 3
            nx2 = now_point[0][0]
            ny2 = ((2 * now_point[0][1]) + cross_p[1]) / 3

        elif c1 == 1:
            nx1 = (now_point[0][0] + (2 * cross_p[0])) / 3
            ny1 = now_point[0][1]
            nx2 = ((2 * now_point[0][0]) + cross_p[0]) / 3
            ny2 = now_point[0][1]

        else:
            # 직선 내 1/3, 2/3 지점 새로운 점
            nx1 = (now_point[0][0] + (2 * cross_p[0])) / 3
            ny1 = m1 * nx1 + n1
            nx2 = ((2 * now_point[0][0]) + cross_p[0]) / 3
            ny2 = m1 * nx2 + n1

        # 두번째 직선
        if point_dist(now_point[2][0], now_point[2][1], cross_p[0], cross_p[1]) > point_dist(now_point[3][0],now_point[3][1],cross_p[0], cross_p[1]):
            if c2 == 0:
                # 1/3지점과 2/3지점
                nx3 = now_point[2][0]
                ny3 = (now_point[2][1] + (2 * cross_p[1])) / 3
                nx4 = now_point[2][0]
                ny4 = ((2 * now_point[2][1]) + cross_p[1]) / 3

            elif c2 == 1:
                nx3 = (now_point[2][0] + (2 * cross_p[0])) / 3
                ny3 = now_point[2][1]
                nx4 = ((2 * now_point[2][0]) + cross_p[0]) / 3
                ny4 = now_point[2][1]

            else:
                nx3 = (now_point[2][0] + (2 * cross_p[0])) / 3
                ny3 = m2 * nx3 + n2
                nx4 = ((2 * now_point[2][0]) + cross_p[0]) / 3
                ny4 = m2 * nx4 + n2

        else:
            if c2 == 0:
                nx3 = now_point[3][0]
                ny3 = (now_point[3][1] + (2 * cross_p[1])) / 3
                nx4 = now_point[3][0]
                ny4 = ((2 * now_point[3][1]) + cross_p[1]) / 3

            elif c2 == 1:
                nx3 = (now_point[3][0] + (2 * cross_p[0])) / 3
                ny3 = now_point[3][1]
                nx4 = ((2 * now_point[3][0]) + cross_p[0]) / 3
                ny4 = now_point[3][1]
            else:
                nx3 = (now_point[3][0] + (2 * cross_p[0])) / 3
                ny3 = m2 * nx3 + n2
                nx4 = ((2 * now_point[3][0]) + cross_p[0]) / 3
                ny4 = m2 * nx4 + n2

    else:
        # 두번째 점을 기준으로 점 생성
        if c1 == 0:
            nx1 = now_point[1][0]
            ny1 = (now_point[1][1] + (2 * cross_p[1])) / 3
            nx2 = now_point[1][0]
            ny2 = ((2 * now_point[1][1]) + cross_p[1]) / 3

        elif c1 == 1:
            nx1 = (now_point[1][0] + (2 * cross_p[0])) / 3
            ny1 = now_point[1][1]
            nx2 = ((2 * now_point[1][0]) + cross_p[0]) / 3
            ny2 = now_point[1][1]
        else:
            # 직선 내 1/3, 2/3 지점 새로운 점
            nx1 = (now_point[1][0] + (2 * cross_p[0])) / 3
            ny1 = m1 * nx1 + n1
            nx2 = ((2 * now_point[1][0]) + cross_p[0]) / 3
            ny2 = m1 * nx2 + n1

        if point_dist(now_point[2][0], now_point[2][1], cross_p[0], cross_p[1]) > point_dist(now_point[3][0], now_point[3][1], cross_p[0], cross_p[1]):
            if c2 == 0:
                # 1/3지점과 2/3지점
                nx3 = now_point[2][0]
                ny3 = (now_point[2][1] + (2 * cross_p[1])) / 3
                nx4 = now_point[2][0]
                ny4 = ((2 * now_point[2][1]) + cross_p[1]) / 3

            elif c2 == 1:
                nx3 = (now_point[2][0] + (2 * cross_p[0])) / 3
                ny3 = now_point[2][1]
                nx4 = ((2 * now_point[2][0]) + cross_p[0]) / 3
                ny4 = now_point[2][1]

            else:
                nx3 = (now_point[2][0] + (2 * cross_p[0])) / 3
                ny3 = m2 * nx3 + n2
                nx4 = ((2 * now_point[2][0]) + cross_p[0]) / 3
                ny4 = m2 * nx4 + n2

        else:
            if c2 == 0:
                nx3 = now_point[3][0]
                ny3 = (now_point[3][1] + (2 * cross_p[1])) / 3
                nx4 = now_point[3][0]
                ny4 = ((2 * now_point[3][1]) + cross_p[1]) / 3

            elif c2 == 1:
                nx3 = (now_point[3][0] + (2 * cross_p[0])) / 3
                ny3 = now_point[3][1]
                nx4 = ((2 * now_point[3][0]) + cross_p[0]) / 3
                ny4 = now_point[3][1]
            else:
                nx3 = (now_point[3][0] + (2 * cross_p[0])) / 3
                ny3 = m2 * nx3 + n2
                nx4 = ((2 * now_point[3][0]) + cross_p[0]) / 3
                ny4 = m2 * nx4 + n2

    return nx1, ny1, nx2, ny2, nx3, ny3, nx4, ny4


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


# 수정 - 클릭한 위치와 직선의 거리 구하기
def dist(x0,y0, x1,y1, x2,y2):
    area = abs ( (x1 - x0) * (y2 - y0) - (y1 - y0) * (x2 - x0) )
    AB = ( (x1 - x2) ** 2 + (y1 - y2) ** 2 ) ** 0.5
    return ( area / AB )


def is_divide_pt(x11,y11, x12,y12, x21,y21, x22,y22):

    '''input: 4 points
    output: True/False
    '''
    #  // line1 extension이 line2의 두 점을 양분하는지 검사..
    # 직선의 양분 판단
    f1= (x12-x11)*(y21-y11) - (y12-y11)*(x21-x11)
    f2= (x12-x11)*(y22-y11) - (y12-y11)*(x22-x11)
    if f1*f2 < 0 :
      return True
    else:
      return False


# 수정 -  두 직선이 교차하는지
def is_cross_pt(x11,y11, x12,y12, x21,y21, x22,y22):
    b1 = is_divide_pt(x11,y11, x12,y12, x21,y21, x22,y22)
    b2 = is_divide_pt(x21,y21, x22,y22, x11,y11, x12,y12)
    if b1 and b2:
        return True
    return False


# 수정 - 두 직선의 교점 찾기
def get_crosspt(x11,y11, x12,y12, x21,y21, x22,y22):
    if x12==x11 or x22==x21:
        return None
    m1 = (y12 - y11) / (x12 - x11)
    m2 = (y22 - y21) / (x22 - x21)
    if m1==m2:
        return None
    cx = (x11 * m1 - y11 - x21 * m2 + y21) / (m1 - m2)
    cy = m1 * (cx - x11) + y11

    return cx, cy


# 마우스 콜백 함수
def mouse_callback(event, x, y, flags, param):
    global ix, iy, ix2, iy2, pre_event, count, now_frame, cross_check, now_point

    pre_event = event

    # 프레임 고정
    if pause == 1:
        if event == cv2.EVENT_FLAG_LBUTTON:
            if now_frame is None:
                now_frame = frame.copy()

            # 수정 - 카운트를 2로 줄임 -> 직선 개수는 총 2개
            if count < 2:
                count += 1
                distance = 5555555
                index = -1
                for i in range(len(x1_points)):
                    # 클릭한 좌표에서 직선들 사이 거리 최소인 직선
                    if (distance > dist(x, y, x1_points[i], y1_points[i], x2_points[i], y2_points[i])):
                        distance = dist(x, y, x1_points[i], y1_points[i], x2_points[i], y2_points[i])
                        index = i

                if index >= 0:
                    # 가장 최소인 직선의 좌표
                    line_x1, line_y1, line_x2, line_y2 = x1_points[index], y1_points[index], x2_points[index], y2_points[index]

                    # 같은 위치 직선일 경우
                    if ix == line_x1 and iy == line_y1 and ix2 == line_x2 and iy2 == line_y2:
                        '''
                        경고 메시지 UI
                        '''
                        warn_msg("같은 위치에 점을 찍을 수 없습니다!")
                        # 팝업
                        count -= 1

                    # 수정 - 직선 그리기
                    else:
                        tmp = now_frame.copy()
                        pre_frame.append(tmp)
                        pre_point.append((-1, -1, -1, -1))
                        ix, iy = line_x1, line_y1
                        # 라인그리기
                        ix2, iy2 = line_x2, line_y2
                        x1, y1, x2, y2 = find_point((ix, iy), (ix2, iy2))

                        cv2.line(now_frame, (x1, y1), (x2, y2), (0, 255, 255), 2)

                        pre_point.append((x1, y1))
                        pre_point.append((x2, y2))
                        now_point.append((x1, y1))
                        now_point.append((x2, y2))

                        # 수정
                        if len(now_point) > 3:
                            # 교차할 경우 교점 구하기
                            if is_cross_pt(now_point[0][0],now_point[0][1],now_point[1][0],now_point[1][1],
                                    now_point[2][0],now_point[2][1],now_point[3][0],now_point[3][1]):

                                # 교점과 점 사이 새로운 점 2개
                                nx1, ny1, nx2, ny2, nx3, ny3, nx4, ny4 = get_newpt()
                                now_point.clear()
                                now_point.append((round(nx1), round(ny1)))
                                now_point.append((round(nx2), round(ny2)))
                                now_point.append((round(nx3), round(ny3)))
                                now_point.append((round(nx4), round(ny4)))
                    print(now_point)
                    cv2.imshow("Video frame", now_frame)
                else:
                    warn_msg("검출된 직선이 없습니다!")
                    ix = -1
                    iy = -1
                    ix2 = -1
                    iy2 = -1
                    pre_event = -1
                    count = 0
                    now_frame = None
                    cross_check = 0
                    del now_point[:]
            else:
                '''
                경고 메시지 UI
                '''
                warn_msg("더이상 점을 찍을 수 없습니다!")
                
                ix = -1
                iy = -1
                ix2 = -1
                iy2 = -1
                pre_event = -1
                count = 0
                now_frame = None
                cross_check = 0
                del now_point[:]

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

                ix = -1
                iy = -1
                ix2 = -1
                iy2 = -1
                pre_event = -1
                count = 0
                now_frame = None
                cross_check = 0
                del now_point[:]


def make_roi(img):
    mask = np.zeros(img.shape, dtype=np.uint8)
    roi_corners = np.array([corners], dtype=np.int32)

    # fill the ROI so it doesn't get wiped out when the mask is applied
    channel_count = img.shape[2]
    ignore_mask_color = (255,) * channel_count
    cv2.fillPoly(mask, roi_corners, ignore_mask_color)

    # apply the mask
    masked_img = cv2.bitwise_and(img, mask)

    return masked_img


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
        y.append(point[1])

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

    direction1 = check_direction((x[0], y[0]), (x[1], y[1]), (x[2], y[2]))
    direction2 = check_direction((x[0], y[0]), (x[1], y[1]), (x[3], y[3]))
    vx1 = value * math.sin(theta[0])
    vy1 = value * math.cos(theta[0])
    vx2 = value * math.sin(theta[1])
    vy2 = value * math.cos(theta[1])

    mp11, mp12 = (-1, -1), (-1, -1)
    mp21, mp22 = (-1, -1), (-1, -1)

    cx, cy = check_intersection(x[0], y[0], x[1], y[1], x[2], y[2], x[3], y[3])

    if direction1 > 0:
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

    elif direction1 < 0:
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

    # TODO: 한직선 위에 다른 점이 있다.
    # 한 점만 직선 위에 있다면?
    # 두 점 모두 직선 위에 있다면?
    # elif direction1 == 0 or direction2 == 0:


def popup_destroy():
    global root
    root.destroy()


def start_destroy():
    global root
    root.destroy()


def system_destroy():
    sys.exit()


def save_value(event):
    global value, txt
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
    msgBox = Tk()
    msgBox.title("Warning!")
    center_window(msgBox, 250, 50)
    msgBox.resizable(False, False)

    warnLbl = Label(msgBox, text=msg)
    warnLbl.pack()

    warnBtn = Button(msgBox, text="확인", command=msgBox.destroy)
    warnBtn.pack()

    msgBox.mainloop()
''''''


def parse_args():
    """Parse input arguments."""
    desc = ('Capture and display live camera video, while doing '
            'real-time object detection with TensorRT optimized '
            'YOLO model on Jetson')
    parser = argparse.ArgumentParser(description=desc)
    parser = add_camera_args(parser)
    parser.add_argument(
        '-c', '--category_num', type=int, default=80,
        help='number of object categories [80]')
    parser.add_argument(
        '-m', '--model', type=str, required=True,
        help=('[yolov3|yolov3-tiny|yolov3-spp|yolov4|yolov4-tiny]-'
              '[{dimension}], where dimension could be a single '
              'number (e.g. 288, 416, 608) or WxH (e.g. 416x256)'))
    args = parser.parse_args()
    return args


def loop_and_detect(cam, trt_yolo, cls_dict, conf_th, vis):
    """Continuously capture images from camera and do object detection.

    # Arguments
      cam: the camera instance (video source).
      trt_yolo: the TRT YOLO object detector instance.
      conf_th: confidence/score threshold for object detection.
      vis: for visualization.
    """
    from threading import Thread
    import pandas as pd
    from server.networking import Server
    from server.data_upload import Upload


    fb = Upload()
    fb.firebase_init()

    server = Server()
    server_th = Thread(target=server.runServer)
    server_th.start()

    # 열차 들어오는 시간을 csv 파일로 받은 후에 해당 시간에는 detection을 멈춘다.
    stop_data = pd.read_csv('stop_detection.csv')
    index = 0
    for i in range(len(stop_data)):
        now = int(time.strftime('%H%M%S'))
        if now < stop_data['start'][i]:
            index = i
            break

    full_scrn = False
    fps = 0.0
    tic = time.time()
    init_time = time.time()
    time_list = list()
    det_list = list()

    stop_dtct = False

    while True:
        if cv2.getWindowProperty(WINDOW_NAME, 0) < 0:
            break
        img = cam.read()
        if img is None:
            break

        fx1, fy1, fx2, fy2 = find_point((now_point[0][0], now_point[0][1]), (now_point[1][0], now_point[1][1]))
        fx3, fy3, fx4, fy4 = find_point((now_point[2][0], now_point[2][1]), (now_point[3][0], now_point[3][1]))
        cv2.line(img, (fx1, fy1), (fx2, fy2), (0, 0, 255), 2)
        cv2.line(img, (fx3, fy3), (fx4, fy4), (0, 0, 255), 2)

        img = make_roi(img)
        
        # 열차 들어오는 시간을 csv 파일로 받은 후에 해당 시간에는 detection을 멈춘다.
        now = int(time.strftime('%H%M%S'))
        if index < len(stop_data):
            if stop_data['start'][index] <= now <= stop_data['end'][index]:
                stop_dtct = True
            elif now > stop_data['end'][index]:
                stop_dtct = False
                index += 1
        
        if not stop_dtct:
            boxes, confs, clss = trt_yolo.detect(img, conf_th)

            img, det_cnt = vis.draw_bboxes(img, boxes, confs, clss, now_point, server, fb)
            det_list.append(det_cnt)

        img = show_fps(img, fps)
        cv2.imshow(WINDOW_NAME, img)
        toc = time.time()
        curr_fps = 1.0 / (toc - tic)
        time_list.append(toc - tic)
        # calculate an exponentially decaying average of fps number
        fps = curr_fps if fps == 0.0 else (fps*0.95 + curr_fps*0.05)
        tic = toc

        key = cv2.waitKey(1)
        if key == 27:  # ESC key: quit program
            break
        elif key == ord('F') or key == ord('f'):  # Toggle fullscreen
            full_scrn = not full_scrn
            set_display(WINDOW_NAME, full_scrn)
    
    pcss_time = time.time() - init_time

    return pcss_time, time_list, det_list


def line_detection(cam):
    global root, txt, WIDTH, HEIGHT
    global pause, pre_event, now_frame, ix, iy, count, check, frame, param_val

    WIDTH = cam.img_width
    HEIGHT = cam.img_height
    '''
    시작 UI
    작동방법 설명
    '''
    root = Tk()
    root.title("프로그램")
    center_window(root, 900, 400)
    root.resizable(0, 0)

    topFrame = Frame(root, relief="solid")
    topFrame.pack(side="top")

    bottomFrame = Frame(root, relief="solid", height="100")
    bottomFrame.pack(side="bottom", expand=True)

    img = PhotoImage(master=topFrame, file="setting.png")
    imgLbl = Label(topFrame, image=img)
    imgLbl.pack()

    confirmBtn = Button(bottomFrame, text='설정시작', width=6, height=1, command=start_destroy)
    confirmBtn.grid(row=0, column=0)
    closeBtn = Button(bottomFrame, text='종료', width=3, height=1, command=system_destroy)
    closeBtn.grid(row=0, column=1)

    root.mainloop()

    cv2.namedWindow('Video frame')

    while True:
        cv2.setMouseCallback('Video frame', mouse_callback)

        # 연속 프레임
        if pause == 0:
            frame = cam.read()
            k = cv2.waitKey(1)
            cv2.imshow("Video frame", frame)

            # 종료
            if k == 27:
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
            elif k == 32:
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
            k = cv2.waitKey(1)
            if count == 0:
                cv2.imshow("Video frame", frame)
            # 수정 - 자동 직선 검출
            if k == 8:
                # 1. 그레이 변환
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                # 2 . 엣지 찾기
                if param_val >= 30:
                    canny = cv2.Canny(gray, param_val, param_val * 3)
                    # 3. 찾은 엣지로 직선 검출
                    lines = cv2.HoughLines(canny, 1, np.pi / 180, 150)
                else:
                    warn_msg("더이상 적합한 직선을 찾을 수 없습니다!")
                    param_val = 200

                    pause = 0
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

                if lines is None:
                    pass
                else:
                    c = 0
                    for i in lines:
                        rho, theta = i[0][0], i[0][1]
                        a, b = np.cos(theta), np.sin(theta)
                        x0, y0 = a * rho, b * rho
                        scale = frame.shape[0] + frame.shape[1]
                        x1_points.append(int(x0 + scale * -b))
                        y1_points.append(int(y0 + scale * a))
                        x2_points.append(int(x0 - scale * -b))
                        y2_points.append(int(y0 - scale * a))
                        cv2.line(frame, (x1_points[c], y1_points[c]), (x2_points[c], y2_points[c]), (0, 0, 255), 2)
                        cv2.imshow("Video frame", frame)
                        c += 1
                param_val -= 10

            # 연속 프레임
            if k == 13:
                pause = 0
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
            # 마진 설정
            elif pre_event == cv2.EVENT_FLAG_RBUTTON:
                if count == 2:
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
                        break

                elif count < 4:
                    '''
                    오류 메시지 UI
                    '''
                    warn_msg("직선 두개를 그려주세요")

    cv2.destroyAllWindows()


def main():
    args = parse_args()
    if args.category_num <= 0:
        raise SystemExit('ERROR: bad category_num (%d)!' % args.category_num)
    if not os.path.isfile('yolo/%s.trt' % args.model):
        raise SystemExit('ERROR: file (yolo/%s.trt) not found!' % args.model)

    cam = Camera(args)
    if not cam.isOpened():
        raise SystemExit('ERROR: failed to open camera!')

    cls_dict = get_cls_dict(args.category_num)
    yolo_dim = args.model.split('-')[-1]
    if 'x' in yolo_dim:
        dim_split = yolo_dim.split('x')
        if len(dim_split) != 2:
            raise SystemExit('ERROR: bad yolo_dim (%s)!' % yolo_dim)
        w, h = int(dim_split[0]), int(dim_split[1])
    else:
        h = w = int(yolo_dim)
    if h % 32 != 0 or w % 32 != 0:
        raise SystemExit('ERROR: bad yolo_dim (%s)!' % yolo_dim)

    trt_yolo = TrtYOLO(args.model, (h, w), args.category_num)

    line_detection(cam)
      
    open_window(
        WINDOW_NAME, 'Camera TensorRT YOLO Demo',
        cam.img_width, cam.img_height)
    vis = BBoxVisualization(cls_dict)
    pcss_time, t_list, d_list = loop_and_detect(cam, trt_yolo, cls_dict, conf_th=0.3, vis=vis)

    print(pcss_time)
    print(t_list)
    print(d_list)
    
    cam.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
