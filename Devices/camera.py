from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import sys
from time import sleep

print("Initializing Camera ...")

sleep(0.1)

def discard_outlier(dimA, dimB) -> bool:
    if dimA > 60 or dimB > 60:
        return True
    if abs(dimA - dimB) >= 0.8 * max(dimA, dimB):
        return True
    return False


def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


def capture_image():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error opening camera ...")
        sys.exit(1)
    ret, frame = cap.read()
    if not ret:
        print("Error capturing image...")
        sys.exit(1)
    return frame


def get_object_size(image, distance_bet_cam_obj, height_of_camera, pixel_per_metric):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (7, 7), 0)
    edged = cv2.Canny(gray, 50, 100)
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1)
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    (cnts, _) = contours.sort_contours(cnts)

    d0 = height_of_camera
    d1 = distance_bet_cam_obj

    max_dim_A = float('-inf')
    max_dim_B = float('-inf')

    for c in cnts:
        if cv2.contourArea(c) < 100:
            continue

        orig = image.copy()
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        box = perspective.order_points(box)

        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)

        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

        pixelsPerMetric = round(pixel_per_metric, 4)

        dimA = (dA * d1) / (pixelsPerMetric * d0)
        dimB = (dB * d1) / (pixelsPerMetric * d0)

        if check_outlier(dimA, dimB):
            continue

        max_dim_A = max(max_dim_A, dimA)
        max_dim_B = max(max_dim_B, dimB)

    return {"length": max(max_dim_A, max_dim_B), "breadth": min(max_dim_A, max_dim_B)}


def get_length_width(image, height):

    height_of_camera = 57.7
    object_to_camera = height_of_camera - height
    pixel_per_metric = 45
    object_size = get_object_size(image,
                                  object_to_camera, height_of_camera, pixel_per_metric)
    return object_size["length"], object_size["breadth"]
