import cv2 as cv

image = cv.imread("C:/Project/Document/20190522_130940.jpg", cv.IMREAD_UNCHANGED)
cv.imshow('yun', image)
cv.waitKey(0)
cv.destroyAllWindows()