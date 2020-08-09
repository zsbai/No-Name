import math
import time

import cv2
import numpy as numpy
from PIL import Image,ImageGrab
import win32gui,win32api,win32con

###########
# 变量定义
 
DEBUGE_MODE = False

#窗口的最小宽度和高度 （win10默认设置）

PW = 32
PH = 30

# 生成图像的区域
if DEBUGE_MODE:
    SCREEN_W = 32
    SCREEN_H = 30


    VIDEO_OFFSET_X = 0
    VIDEO_OFFSET_Y = 0

else:
    ## SCREEN_W = 1024
    ## SCREEN_H = 720
    ##
    ##VIDEO_OFFSET_X = 448
    ##VIDEO_OFFSET_Y = 180
    SCREEN_W = 1200
    SCREEN_H = 900

    VIDEO_OFFSET_X = 320
    VIDEO_OFFSET_Y = 60

# 生成图片的分辨率
ResX = math.floor(SCREEN_W/PW)
ResY = math.floor(SCREEN_H/PH)


#窗口句柄矩阵
hWndArray = [[0]*ResX for row range(ResY)]
#窗口可见性矩阵（缓存，提高效率用）
# 1为可见，0为不可见
visibleArray = [[1]*ResX for row in range(ResY)]

#########
#函数定义

#根据img中每个点的像素值，显示或隐藏对应位置下的窗口
#   为提高效率使用了visible[][]来记录每个窗口的可见行
def showingByNotepad(img):
    img = img.convert("L")
    pixels = img.load()


    for w in range(img.width):
        for h in range(img.height):
            if pixels[w,h] > 100:
                #认为是白色，显示对应的窗口
                if visibleArray[h][w] == 0:
                    win32gui.ShowWindow(hWndArray[h][w],win32con.SW_SHOW)
                    visibleArray[h][w] = 1
            else:
                #认为是黑色，要把对应的窗口隐藏
                if visibleArray[h][w] == 1:
                    win32gui.ShowWindow(hWndArray[h][w],win32con.SW_HIDE)
                    visibleArray[h][w] = 0

# x，y为用户坐标，和矩阵系数不相同，但有对应关系
# show就是隐藏对应的窗口，把桌面背景show出来
def showPixel(x,y):
    win32gui.ShowWindow(hWndArray[y][x],win32con.SW_HIDE)


#批量创建进程，并将进程主窗口句柄放在hWndArray[][]中
def createWindows():
    global hWndArray

    for x in range(ResX):
        for y in range(ResY):
            hWnd = createNotepad(x * ResX + y)
            hWndArray[y][x] = hWnd
            resizeAndMove(hWnd,x,y)#y


#调整窗口大小和位置，让它们排队站好
def resizeAndMove(hWnd,x,y):
    win32gui.MoveWindow(hWnd,x*PW - 8 + VIDEO_OFFSET_X,y*PH + VIDEO_OFFSET_Y,PW,PH,win32con.TRUE)#-8位置


#创建单个进程
def createNotepad(index):
    #创建单个进程
    hlnstance = win32api.ShellExecute(0,'open',' F:\\路径.exe',",",1)
#创建速度不能太快，否则系统响应不及，就出错了
    if index<1000:
        win32api.Sleep(50)
    else:
        win32api.Sleep(100)

    hWnd = win32gui.GetForegroundWinodw()
    return hWnd


#截图
#参数是左上角和右下角坐标点的屏幕坐标
#返回彩色cv2格式的图片，其实用灰度会比彩色快一些
def takeScreenshot(left,top,right,bottom):
    img = ImageGrab.grab(bbow=(left,top,right,bottom))
    img = cv2.cvtColor(np.asarry(img),cv2.COLOR_RGB2BGR)
    return img

#由bmp图像对窗口进行排列
def bmp2notepad():
    count = 6450
    while(count<=6502):
        #加载opencv处理后的图片
        img = Image.open("./frames-40x30/ba-" + str(count).zfill(4) + "jpg")
        #根据图片内容控制窗口矩阵的显示和隐藏
        showImgByNotepad(img)
        #把窗口组成的图像截图存储
        capImage = takeScreenshot(0,0,1920,1080)
        cv2.imwrite("./outcome-40x30/ba-" + str(count).zfill(4) + "jpg", capImage)

        #log
        print(time.asctime(time.localtime(time.time())),’\t\tcount:‘,count)
        count += 1


#######
#程序入口
if __name__=="__main__":
    # 创建多个窗口并初始化
    createWindows()