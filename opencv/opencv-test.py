import cv2 as cv
import numpy as np

def demo():
    # 创建一个图像作为背景图，size:512*512，channel:3
    img = np.zeros((512, 512, 3), np.uint8)
    # 1.画蓝色对角线
    img = cv.line(img, (0, 0), (511, 511), (255, 0, 0), 5)
    # 显示并回收资源
    cv.imshow('draw',img)
    cv.waitKey(0)
    cv.destroyAllWindows()

def image_io_demo():
    image = cv.imread("E:/clib/data/test.jpg") # BGR
    h, w, c = image.shape
    print(h, w, c)

    cv.namedWindow("input", cv.WINDOW_AUTOSIZE)
    cv.imshow("input", image)
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    print(gray.shape)
    cv.imshow("gray", gray)
    cv.imwrite("E:/clib/data/test-gray.jpg", gray)
    cv.waitKey(0)
    cv.destroyAllWindows()


def video_io_demo():
    cap = cv.VideoCapture("E:/clib/data/test.mp4")
    while True:
        ret, frame = cap.read()
        if ret is not True:
            break
        cv.imshow("frame", frame)
        # TODO:
        # ......
        c = cv.waitKey(10)
        if c == 27:
            break
    cap.release()


def basic_ops_demo():
    image = cv.imread("E:/clib/data/test.jpg")  # BGR
    cv.imshow("input", image)
    h, w, c = image.shape
    print(h, w, c)
    mv = cv.split(image)
    blob = cv.resize(image, (300, 300))
    print(blob.shape) # HWC
    # NCHW
    image_blob = blob.transpose(2, 0, 1)
    print(image_blob.shape)
    image_blob = np.expand_dims(image_blob, 0)
    print(image_blob.shape)
    cv.imshow("blob", blob)
    cv.waitKey(0)
    cv.destroyAllWindows()

    a = np.array([1, 2,3, 4, 5, 6, 9, 88, 0, 12, 14, 5, 6])
    index = np.argmax(a)
    print(a[index])

    for row in range(h):
        for col in range(w):
            b, g, r = image[row, col]
            print(b, g, r)


if __name__ == "__main__":
    # demo()
    # image_io_demo()
    # video_io_demo()
    basic_ops_demo()