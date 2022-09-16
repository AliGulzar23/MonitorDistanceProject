import cv2
import Configuration
import os
import csv
import datetime

configuration = Configuration.Configuration()
calibration = False
currentArea = 0
status = 0


# 0 - too close 1 - correct distance 2 - too far

def configuration_Setup(configuration):
    if configuration.check_Config():
        configuration.load_From_Config()
        print("Using your previous settings. Press C to change them")
    else:
        print("No previous settings detected, transfering to setup")


def Main():
    print("Welcome, here is how to use the software: \nPress C to recalibrate your distance\nPress Q to quit ")
    print(
        "Please wait while we load the training data \nto get the best distance when calibrating\nmake sure your arm is fully extended when you press C\nRed square is too close, blue is too far. ")
    #f = open("Data.csv", 'a')
    previousTime = datetime.datetime.now()
    fileName = 'data/'+str(datetime.datetime.now().strftime("%Y%m%d-%H%M%S")) + '.csv'
    file = open(fileName, 'w')
    writer = csv.writer(file, lineterminator='\n')
    header = ['DateTime','Distance','Status']
    writer.writerow(header)
    trainedFaceData = cv2.CascadeClassifier(configuration.frontalFaceDataLocation)
    webcam = cv2.VideoCapture(0)
    configuration_Setup(configuration)
    timeKey = 1
    print('\nloading complete\n')
    while True:
        # find way to take the percentage of the monitor and place it into a csv
        # runs constantly unless stopped
        currentTime = datetime.datetime.now()
        difference = currentTime - previousTime
        if difference.seconds >= configuration.get_iteration():
            previousTime = datetime.datetime.now()

            # only want a specific type of step
            image_Detect(trainedFaceData, webcam)
            # data formad datetime,  area, status
            global currentArea
            row = [currentTime, currentArea, status]
            writer.writerow(row)
            key = cv2.waitKey(timeKey)
        if key == 67 or key == 99:  # the c keys
            print("entering calibration")
            configuration.save_To_Config(currentArea)  # saves new location to config File
            configuration.load_From_Config()  # reloads the file with the new values

        if key == 81 or key == 113:  # q key either capital or lower
            exit()


def image_Detect(trainedFaceData, webcam):
    faceCoordinates, frame = get_FaceCoordinates(trainedFaceData, webcam)
    try:
        color = determine_Color(faceCoordinates)
        draw_Rect_On_Face(faceCoordinates, frame, color)
    except:
        print("No face detected, PLEASE LOOK AT THE CAMERA")


def get_FaceCoordinates(trainedFaceData, webcam):
    successfulFrameRead, frame = webcam.read()
    # converts image to grayscale
    frameGrayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faceCoordinates = trainedFaceData.detectMultiScale(frameGrayscale)
    return faceCoordinates, frame


def determine_Color(faceCoordinates):
    global currentArea
    global status
    currentArea = get_CurrentArea(faceCoordinates)

    # calculates area from the width of the square
    currentDistance = configuration.get_Ratio() / currentArea
    if currentDistance < configuration.minThreshold:
        # too close
        color = (0, 0, 255)  # red
        status = 0
    elif currentDistance > configuration.maxThreshold:
        # too far
        color = (255, 0, 0)
        status = 1
    else:
        # perfect range of monitor
        color = (0, 255, 0)
        status = 2
    return color


def get_CurrentArea(faceCoordinates):
    global currentArea
    currentArea = faceCoordinates[0][3] ** 2
    return currentArea


def draw_Rect_On_Face(faceCoordinates, frame, color):
    for (x, y, w, h) in faceCoordinates:
        # gets the coordinates of the top left corner as well as the width and height
        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        # draws rectangle of the dimensions
    cv2.imshow('Monitor Measure', frame)


Main()
