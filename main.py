import cv2 as cv
import numpy as np

# Open the webcam (0 is the default camera)
cam = cv.VideoCapture(0)
cam.set(3, 740)  # Set frame width
cam.set(4, 580)  # Set frame height

# Create an empty array to store the class names
classNames = []

# Load the class names from 'coco.names' file
classFile = 'coco.names'
with open(classFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

# Load the pre-trained model
configPath = 'ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt'
weightsPath = 'frozen_inference_graph.pb'

net = cv.dnn_DetectionModel(weightsPath, configPath)
net.setInputSize(320, 230)
net.setInputScale(1.0 / 127.5)
net.setInputMean((127.5, 127.5, 127.5))
net.setInputSwapRB(True)

while True:
    isTrue, img = cam.read()  # Capture a frame from the webcam

    # Run the object detection on the captured frame
    classIds, confidences, boxes = net.detect(img, confThreshold=0.6)

    # If there are any detected objects
    if len(classIds) != 0:
        # Loop through each detected object and draw bounding boxes and labels
        for classId, confidence, box in zip(classIds.flatten(), confidences.flatten(), boxes):
            # Draw bounding box
            cv.rectangle(img, (box[0], box[1]), (box[0] + box[2], box[1] + box[3]), color=(0, 255, 0), thickness=3)

            # Put the class name text on the image
            cv.putText(img, classNames[classId - 1], (box[0] + 10, box[1] + 30), cv.FONT_HERSHEY_SIMPLEX, 1.5,
                       (0, 0, 0), 3)

    # Display the processed image with bounding boxes and labels
    cv.imshow('Camera', img)

    # Exit condition: Press 'q' to quit the loop and close the camera
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all OpenCV windows
cam.release()
cv.destroyAllWindows()
