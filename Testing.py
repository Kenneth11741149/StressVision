#Tests for the project
import cv2
import numpy as np


img = cv2.imread("TestImages/Orange.jpg")
path = ["TestImages/Green.jpg","TestImages/MixedCube.jpg","TestImages/Red.jpg","TestImages/Blue.jpg","TestImages/Yellow.jpg","TestImages/White.jpg","TestImages/Orange.jpg"]
width = 640
height = 480

def reorder(myPoints):
    myPoints = myPoints.reshape((4,2)) #4 by 2 por el problema de 4 by 1 by 2.
    myPointsNew = np.zeros((4,1,2),np.int32)
    add = myPoints.sum(1)
    # print("add",add)

    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    # print("NewPoints",myPointsNew)
    diff = np.diff(myPoints,axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    # print("NewPoints",myPointsNew)
    return myPointsNew

def getContour(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST,
                                           cv2.CHAIN_APPROX_NONE)  # Secon param is retrieval method. There are several, we will use external method. It retrieves the extreme outer contours.
    # There are others that will detect all the details, but this one works great for outer corners
    areas = []
    cnts = []
    approxs = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print("Area:")
        print(area)

        # If this is an image like this you dont have to. But you should give a threshold so you dont detect any noise.
        if area > 700:

            # Now we need to aproximate the edges.
            peri = cv2.arcLength(cnt, True)
            print(peri)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri,
                                      True)  # Play with epsilon if you are not getting good results. #True if closed.
            print("Approx")
            size = len(approx)

            print(approx)  # Returns corner points of each of the shapes.
            # We can then print the length of approx and we can find out the shape by finding out how many corners the image has.
            print(len(approx))  # Any length above 4 can most likely be a circle since we are not checking for more.
            objCor = len(approx)
            x, y, w, h = cv2.boundingRect(approx)
            # cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
            aspRatio = w / float(h)
            if aspRatio > 0.95 and aspRatio < 1.05:
                objectType = "Square"
            else:
                objectType = "Unrecog"
            if len(approx) == 4 and objectType == "Square":
                cnts.append(cnt)
                areas.append(area)
                approxs.append(size)
                cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # cv2.drawContours(imgContour, cnt, -1, (255, 255, 0), 3)  # -1 = draw all contours.
                # cv2.imshow("Lmao", imgContour)
                pass
    sum_areas = 0
    cont = 0
    for area in areas:
        sum_areas = sum_areas + area
        cont = cont + 1
    final_return = []
    if cont > 0:
        sum_areas = sum_areas/len(areas)
        upper_area_limit = sum_areas*1.1
        lower_area_limit = sum_areas*0.9
        cont = 0
        for area in areas:
            if area <= upper_area_limit and area >= lower_area_limit and approxs[cont] >= 4 and len(cnt) >= 8:
                print("help")
                final_return.append(approxs[cont].tolist())
                cv2.drawContours(imgContour, cnts[cont], -1, (255, 255, 0), 3)  # -1 = draw all contours.
                cv2.imshow("Lmao", imgContour)
            cont = cont + 1
    return final_return, imgContour
def empty(a):
    pass


def auto_canny(image, sigma=0.6):


    # compute the median of the single channel pixel intensities
    v = np.median(image)

    # apply automatic Canny edge detection using the computed median
    lower = int(max(0, (1.0 - sigma) * v))
    upper = int(min(255, (1.0 + sigma) * v))

    edged = cv2.Canny(image, lower, upper)
    # return the edged image
    return edged


cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640,240)
cv2.createTrackbar("Threshold Min","TrackBars",0, 255, empty) #Initial value, #Maximum value of hue #Hue has a maximum value of 360
cv2.createTrackbar("Threshold Max","TrackBars",0,255,empty)

cont = 0
cap = cv2.VideoCapture(0)  # Webcam
cap.set(3, width)
cap.set(4, height)
while True:
    # path = ["TestImages/Green.jpg", "TestImages/MixedCube.jpg", "TestImages/Red.jpg", "TestImages/Blue.jpg",
    #         "TestImages/Yellow.jpg", "TestImages/White.jpg", "TestImages/Orange.jpg"]
    # img = cv2.imread(path[cont])
    # img = cv2.resize(img, (width, height))

    success, img = cap.read()

    imgContour = img.copy()
    cont = cont + 1
    if cont >= 6:
        cont = 0




    imgContour = img.copy()
    thresh_min = cv2.getTrackbarPos("Threshold Min", "TrackBars")
    thresh_max = cv2.getTrackbarPos("Threshold Max", "TrackBars")


    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray,(3,3),0)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    gray = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
    gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)

    gray = cv2.adaptiveThreshold(gray, 20, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 5, 0)

    # imgCanny = cv2.Canny(imgBlur,thresh_min,thresh_max) #Threshold
    imgCanny = auto_canny(imgBlur)

    kernel = np.ones((5, 5), np.uint8)
    imgDilation = cv2.dilate(imgCanny, kernel, iterations=4)  # ImageCanny because we are talking about edges. Kernel is a matrix. We need numpy to make a matrix that in this case is all full of 1s.
    # Opposite of dilation is erosion.
    imgEroded = cv2.erode(imgDilation, kernel, iterations=1)

    approxs, imgContour = getContour(imgEroded)

    if len(approxs) >= 8:
        for approx in approxs:
            approx = reorder(approx)
        cv2.imshow("Face", imgContour)




    cv2.imshow("Original", img)
    cv2.imshow("Gray", gray)
    # cv2.imshow("Canny Edge", imgCanny)
    # cv2.imshow("Canny Edge2", imgEroded)
    cv2.waitKey(1)