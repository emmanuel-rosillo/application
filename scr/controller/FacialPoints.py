import json
from flask import Flask
import cv2
import os
import mediapipe as mp
import numpy as np
from math import degrees, acos
import time
import imutils
from ..helpers import createPersonalPath
from ..models import FaceTool, Face
from  .ControllerUsers import registerVectors

mp_face_mesh = mp.solutions.face_mesh
mp_face_detection = mp.solutions.face_detection


def generate(name):
    if os.environ.get('WERKZEUG_RUN_MAIN') or Flask.debug is False:
        cap = cv2.VideoCapture(0)

    # personalPath##############
    personalPath = createPersonalPath(name)
    ############################

    timecount = 0
    start = 0
    end = 0
    counter = False
    listConstanEyes = []
    listConstanEars = []
    listConstanLips = []

    while True:
        ret, frame = cap.read()
        frame = cv2.flip(frame, 1)
        if not ret:
            print("not success camera")
        with mp_face_detection.FaceDetection(
                min_detection_confidence=0.7) as face_detection:
            height, width, _ = frame.shape
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = face_detection.process(frame_rgb)

            if results.detections is not None:
                for detection in results.detections:
                    # eye l
                    x1 = int(detection.location_data.relative_keypoints[0].x * width)
                    y1 = int(detection.location_data.relative_keypoints[0].y * height)

                    # eye r
                    x2 = int(detection.location_data.relative_keypoints[1].x * width)
                    y2 = int(detection.location_data.relative_keypoints[1].y * height)

                    # Mouth
                    mx = int(
                        mp_face_detection.get_key_point(detection,
                                                        mp_face_detection.FaceKeyPoint.MOUTH_CENTER).x * width)
                    my = int(
                        mp_face_detection.get_key_point(detection,
                                                        mp_face_detection.FaceKeyPoint.MOUTH_CENTER).y * height)

                    # Nose
                    elx = int(detection.location_data.relative_keypoints[2].x * width)
                    ely = int(detection.location_data.relative_keypoints[2].y * height)

                    # center
                    xC = int(width // 2)
                    yC = int(height // 2)

                    # points
                    p1 = np.array([x1, y1])
                    p2 = np.array([x2, y2])
                    p3 = np.array([x2, y1])
                    pn = np.array([elx, ely])
                    pc = np.array([xC, yC])

                    # distance between points
                    d_eyes = np.linalg.norm(p1 - p2)
                    l1 = np.linalg.norm(p1 - p3)
                    d_nc = np.linalg.norm(pn - pc)

                    # distance of face
                    W = 6.3  # weight lent of camera
                    f = 650  # Preset calculation of focal length
                    distance = int((W * f) // d_eyes)  # calculate the distance

                    # instance FaceTool object
                    toolEyes = FaceTool(distance)
                    dis = 40  # preselect adjust distance
                    disLarge = dis + 1
                    disShort = dis - 1

                    # Constant distance eyes
                    intEyes = int(d_eyes / 10)
                    constDistanceEyes = int((60 - toolEyes.distances) // 5)
                    distanceRealityEyes = int(intEyes - constDistanceEyes)

                    # transform the vector distance of point between nose a center
                    d_nc = int(d_nc / 10)

                    # check the distance focal is correct
                    if disLarge >= toolEyes.distances >= disShort:
                        cv2.putText(frame, "distancia correcta", (x1 - 50, y1 - 90), 1, 1.2, (0, 255, 0), 2)
                    elif toolEyes.distances > disLarge:
                        cv2.putText(frame, "acerquese un poco mas al lente", (x1 - 50, y1 - 90), 1, 1.2,
                                    (0, 0, 255), 2)
                    elif toolEyes.distances < disShort:
                        cv2.putText(frame, " alejese mas del lente", (x1 - 50, y1 - 90), 1, 1.2, (0, 0, 255), 2)

                    # check the distance "y" and "x" nose is correct

                    if 1 >= d_nc >= -1:
                        cv2.putText(frame, "alineado", (mx - 220, my + 110), 1, 1.2, (255, 0, 255), 2)
                    else:
                        if ely > yC:
                            cv2.putText(frame, "muy abajo, centre su nariz", (mx - 220, my + 110), 1, 1.2,
                                        (255, 0, 255), 2)
                        else:
                            cv2.putText(frame, "muy arriba, centre su nariz", (mx - 220, my + 110), 1, 1.2,
                                        (0, 128, 255), 2)
                        if elx > xC:
                            cv2.putText(frame, "demasiado a la derecha, centre su nariz",
                                        (mx - 220, my + 130), 1,
                                        1.2, (255, 0, 255), 2)
                        else:
                            cv2.putText(frame, "demasiado a la izquierda, centre su nariz",
                                        (mx - 220, my + 130),
                                        1, 1.2, (0, 128, 255), 2)
                        # put circle center
                        cv2.circle(frame, (xC, yC), 8, (255, 0, 255), 2)

                    # show user text put in area
                    if disLarge >= toolEyes.distances >= disShort and 1 >= d_nc >= -1:
                        cv2.putText(frame, "mantengase un momento", (xC - 130, 30), 1, 1.2, (0, 128, 255), 2)

                    # calculate angle from d_eyes and l1 to stabilizer frame
                    angle = degrees(acos(l1 / d_eyes))
                    if y1 < y2:
                        angle = - angle

                    # Aligned faces
                    M = cv2.getRotationMatrix2D((width // 2, height // 2), -angle, 1)
                    aligned_image = cv2.warpAffine(frame, M, (width, height))

                    # time register
                    if (disLarge >= toolEyes.distances >= disShort) and (1 >= d_nc >= -1):
                        if not counter:
                            start = time.time()
                        counter = True
                        end = time.time()
                        timer = int(end - start)
                        timecount += timer / 10
                    else:
                        timer = 0
                        counter = False

                    # aligned picture
                    results2 = face_detection.process(cv2.cvtColor(aligned_image, cv2.COLOR_BGR2RGB))
                    if results2.detections is not None:
                        for detection in results2.detections:
                            xmin = int(detection.location_data.relative_bounding_box.xmin * width)
                            ymin = int(detection.location_data.relative_bounding_box.ymin * height)
                            w = int(detection.location_data.relative_bounding_box.width * width)
                            h = int(detection.location_data.relative_bounding_box.height * height)
                            if xmin < 0 or ymin < 0:
                                continue
                            aligned_face = aligned_image[ymin: ymin + h, xmin: xmin + w]
            # encode stream webcam in front-end
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            if not flag:
                continue
            yield b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + bytearray(encodedImage) + b'\r\n'

            # red frame second with feshMesh
            with mp_face_mesh.FaceMesh(
                    max_num_faces=1,
                    refine_landmarks=True,
                    min_detection_confidence=0.5,
                    min_tracking_confidence=0.5) as face_mesh:

                height, width, _ = frame.shape
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = face_mesh.process(frame_rgb)

                if results.multi_face_landmarks:
                    for face_landmarks in results.multi_face_landmarks:

                        # ear left
                        elx = int(face_landmarks.landmark[127].x * width)
                        ely = int(face_landmarks.landmark[127].y * height)

                        # ear right
                        erx = int(face_landmarks.landmark[356].x * width)
                        ery = int(face_landmarks.landmark[356].y * height)

                        # lips right
                        lrx = int(face_landmarks.landmark[61].x * width)
                        lry = int(face_landmarks.landmark[61].y * height)

                        # lips left
                        llx = int(face_landmarks.landmark[291].x * width)
                        lly = int(face_landmarks.landmark[291].y * height)

                        # points
                        earLeft = np.array([elx, ely])
                        earRight = np.array([erx, ery])
                        lipsRight = np.array([lrx, lry])
                        lipsLeft = np.array([llx, lly])

                        # distance between points
                        dEars = np.linalg.norm(earLeft - earRight)
                        dLips = np.linalg.norm(lipsRight - lipsLeft)

                        W = 6.3
                        # distance relative dEars
                        distanceFocalEars = int((W * f) // dEars)
                        toolEars = FaceTool(distanceFocalEars)

                        # Constant distance Ears
                        intEars = int(dEars / 10)
                        constPointEars = int((60 - toolEars.distances) // 1)
                        distanceRealityEars = int(constPointEars - intEars)

                        # distance relative dLips
                        distanceFocalLips = int((W * f) // dLips)
                        toolLips = FaceTool(distanceFocalLips)

                        # Constant distance Lips
                        intLips = int(dLips / 10)
                        constPointLips = int((60 - toolLips.distances) // 5)
                        distanceRealityLips = int(intLips - constPointLips)

                        # add to list
                        if (disLarge >= toolEyes.distances >= disShort) and (1 >= d_nc >= -1) and (timecount < 20):
                            listConstanEyes.append(distanceRealityEyes)
                            listConstanEars.append(distanceRealityEars)
                            listConstanLips.append(distanceRealityLips)

            if timecount > 20:
                img = personalPath + '/face_{}.jpg'.format(name)
                image = imutils.resize(aligned_face, width=234)
                cv2.imwrite(img, image)
                v1 = (max(set(listConstanEyes), key=listConstanEyes.count))
                v2 = (max(set(listConstanEars), key=listConstanEars.count))
                v3 = (max(set(listConstanLips), key=listConstanLips.count))
                userVectors = Face(v1, v2, v3, name)
                registerVectors(userVectors)
                break
