#Tests for the project
import cv2
import numpy as np

img = cv2.imread("TestImages/Blue.jpg")

width = 640
height = 480

def getContour(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)  # Secon param is retrieval method. There are several, we will use external method. It retrieves the extreme outer contours.
    # There are others that will detect all the details, but this one works great for outer corners
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print("Area:")
        print(area)

        # If this is an image like this you dont have to. But you should give a threshold so you dont detect any noise.
        if area > 500:
            cv2.drawContours(imgContour, cnt, -1, (255, 255, 0), 3)  # -1 = draw all contours.
            cv2.imshow("Lmao", imgContour)
            # Now we need to aproximate the edges.
            peri = cv2.arcLength(cnt, True)
            print(peri)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri,
                                      True)  # Play with epsilon if you are not getting good results. #True if closed.
            print("Approx")
            print(approx)  # Returns corner points of each of the shapes.
            # We can then print the length of approx and we can find out the shape by finding out how many corners the image has.
            print(len(approx))  # Any length above 4 can most likely be a circle since we are not checking for more.
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)

def empty(a):
    pass

img = cv2.resize(img,(width,height))
imgContour = img.copy()
cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640,240)
cv2.createTrackbar("Threshold Min","TrackBars",0, 255, empty) #Initial value, #Maximum value of hue #Hue has a maximum value of 360
cv2.createTrackbar("Threshold Max","TrackBars",0,255,empty)

while True:
    imgContour = img.copy()
    thresh_min = cv2.getTrackbarPos("Threshold Min", "TrackBars")
    thresh_max = cv2.getTrackbarPos("Threshold Max", "TrackBars")


    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(7,7),0)

    imgCanny = cv2.Canny(imgBlur,thresh_min,thresh_max) #Threshold
    getContour(imgCanny)


    cv2.imshow("Original", img)
    cv2.imshow("Gray", imgGray)
    cv2.imshow("Canny Edge", imgCanny)
    cv2.waitKey(1)