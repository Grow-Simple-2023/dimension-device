from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2
import sys
from time import sleep
import subprocess
from random import randint
import os

print("Initializing Camera ...")
if not os.path.exists("temp_images"):
    os.mkdir("temp_images")


sleep(0.1)


def discard_outlier(dimA, dimB) -> bool:
    if dimA > 60 or dimB > 60:
        return True
    if abs(dimA - dimB) >= 0.8 * max(dimA, dimB):
        return True
    return False


def midpoint(ptA, ptB):
    return ((ptA[0] + ptB[0]) * 0.5, (ptA[1] + ptB[1]) * 0.5)


def capture_image(contrast, brightness):
    img_path = f"./temp_images/{randint(0, 100000)}.jpg"
    subprocess.run(["raspistill", "-t", "1000ms", "-sh",
                   str(contrast), "-br", str(brightness), "-o", img_path])
    return img_path


def get_object_size(image_path, distance_bet_cam_obj, height_of_camera, pixel_per_metric):
    image = cv2.imread(image_path)
    a, b = [10, 40]
    a, b = int(a*pixel_per_metric), int(b*pixel_per_metric)
    image = image[:, a:b]
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

    height, weight = gray.shape[:2]

    print("No. of Objects Detected: ", len(cnts))
    maximum_cnt, max_area = None, float('-inf')
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        if w/pixel_per_metric > 35 or h/pixel_per_metric > 35:
            continue
        if max_area < w*h:
            max_area = w*h
            maximum_cnt = c

    cnts = [maximum_cnt]
    print("Filtered contour", len(cnts))
    
    for c in cnts:
        x, y, w, h = cv2.boundingRect(c)
        # print(w, h)
        orig = image.copy()
        box = cv2.minAreaRect(c)
        box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
        box = np.array(box, dtype="int")

        box = perspective.order_points(box)
        cv2.drawContours(orig, [box.astype("int")], -1, (0, 255, 0), 2)

        for (x, y) in box:
            cv2.circle(orig, (int(x), int(y)), 5, (0, 0, 255), -1)

        (tl, tr, br, bl) = box
        (tltrX, tltrY) = midpoint(tl, tr)
        (blbrX, blbrY) = midpoint(bl, br)

        (tlblX, tlblY) = midpoint(tl, bl)
        (trbrX, trbrY) = midpoint(tr, br)

        cv2.circle(orig, (int(tltrX), int(tltrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(blbrX), int(blbrY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(tlblX), int(tlblY)), 5, (255, 0, 0), -1)
        cv2.circle(orig, (int(trbrX), int(trbrY)), 5, (255, 0, 0), -1)

        cv2.line(orig, (int(tltrX), int(tltrY)), (int(blbrX), int(blbrY)),
                 (255, 0, 255), 2)
        cv2.line(orig, (int(tlblX), int(tlblY)), (int(trbrX), int(trbrY)),
                 (255, 0, 255), 2)

        dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
        dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

        pixelsPerMetric = round(pixel_per_metric, 4)

        dimA = (dA * d1) / (pixelsPerMetric * d0)
        dimB = (dB * d1) / (pixelsPerMetric * d0)

        cv2.putText(orig, "{:.3f}cm".format(dimA),
                    (int(tltrX - 15), int(tltrY - 10)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (255, 255, 255), 2)
        cv2.putText(orig, "{:.3f}cm".format(dimB),
                    (int(trbrX + 10), int(trbrY)), cv2.FONT_HERSHEY_SIMPLEX,
                    0.65, (255, 255, 255), 2)

        cv2.imwrite(f"./temp_images/{randint(0, 100000)}.jpg", orig)
        # cv2.imshow("Image", orig)
        # cv2.waitKey(0)

        max_dim_A = max(max_dim_A, dimA)
        max_dim_B = max(max_dim_B, dimB)

    return {"length": max(max_dim_A, max_dim_B), "breadth": min(max_dim_A, max_dim_B)}
    # for c in cnts:
    #     if cv2.contourArea(c) < 100:
    #         continue

    #     orig = image.copy()
    #     box = cv2.minAreaRect(c)
    #     box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
    #     box = np.array(box, dtype="int")

    #     box = perspective.order_points(box)

    #     (tl, tr, br, bl) = box
    #     (tltrX, tltrY) = midpoint(tl, tr)
    #     (blbrX, blbrY) = midpoint(bl, br)

    #     (tlblX, tlblY) = midpoint(tl, bl)
    #     (trbrX, trbrY) = midpoint(tr, br)

    #     dA = dist.euclidean((tltrX, tltrY), (blbrX, blbrY))
    #     dB = dist.euclidean((tlblX, tlblY), (trbrX, trbrY))

    #     pixelsPerMetric = round(pixel_per_metric, 4)

    #     dimA = (dA * d1) / (pixelsPerMetric * d0)
    #     dimB = (dB * d1) / (pixelsPerMetric * d0)

    #     if discard_outlier(dimA, dimB):
    #         print("Discarding outlier", dimA, dimB)
    #         continue
    #     print("Dimensions", dimA, dimB)
    #     max_dim_A = max(max_dim_A, dimA)
    #     max_dim_B = max(max_dim_B, dimB)

    # return {"length": max(max_dim_A, max_dim_B), "breadth": min(max_dim_A, max_dim_B)}


def get_length_width(image_path, height):

    height_of_camera = 57.7
    object_to_camera = height_of_camera - height
    pixel_per_metric = 45.7
    object_size = get_object_size(image_path,
                                  object_to_camera, height_of_camera, pixel_per_metric)
    return object_size["length"], object_size["breadth"]


image_path = capture_image(contrast=50, brightness=60)
print(get_length_width(image_path, 2))
