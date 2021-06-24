#Start by getting the camera from the computer
#Ideas:
#We can extract the exact contours (cnt) of each square per image and process its color.
#We can extract the cube first, locate all the shapes and then locate per square their color.


import cv2
import numpy as np

frameWidth = 640
frameHeight = 480

cap = cv2.VideoCapture(0) #Webcam
cap.set(3,frameWidth)
cap.set(4,frameHeight)


rubiks_colors = [
            [95,75,51,125,255,255], #Blue
            [26,104,33,96,255,69], #Green
            [0,107,95,4,255,164], #Red
            [0,156,143,37,255,172], #Orange
            [62,0,103,119,255,148], #White
            [10,114,108,82,255,217] #Yellow

]

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver


def preprocess(image):
    imgGray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) #returns a gray image
    imgBlur = cv2.GaussianBlur(imgGray, (7,7), 1) #returns a blurred image
    imgCanny = cv2.Canny(imgBlur, 50, 50)
    kernel = np.ones((5, 5))
    imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
    imgThres = cv2.erode(imgDial, kernel, iterations=1)
    return imgThres

def getContour(img): #An image of contours aka the canny edge detection image.
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, # Second param is retrieval method. There are several, we will use external method. It retrieves the extreme outer contours.
                                           cv2.CHAIN_APPROX_NONE)  # Method of approximation (request all of info or compressed value)
    # There are others that will detect all the details, but this one works great for outer corners

    for cnt in contours: #cnt is an array of basically the contour of what was detected.
        area = cv2.contourArea(cnt)
        if area > 400 and area < 7000:
            # cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 3)  # -1 = draw all contours.
            cv2.imshow("imgContoursDrawn",imgContour)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            x, y, w, h = cv2.boundingRect(approx)
            # if len(approx) == 4:
            cv2.drawContours(imgContour, cnt, -1, (255, 0, 255), 3)  # -1 = draw all contours.
            cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)

    return imgContour

def findColor(img):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    for color in rubiks_colors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        kernel = np.ones((5, 5))
        imgDial = cv2.dilate(mask, kernel, iterations=2)
        imgThres = cv2.erode(mask, kernel, iterations=1)
        getContour(imgThres)
    # return newPoints


while True:
    success, img = cap.read()
    imgContour = img.copy()

    imgCanny = preprocess(img)
    # imgContourDrawn = getContour(imgCanny)
    findColor(img)


    # stack_of_images = stackImages(0.6,([img, imgCanny, imgContourDrawn]))
    # cv2.imshow("Project Output", stack_of_images)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break




