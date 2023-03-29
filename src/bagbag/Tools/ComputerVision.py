from __future__ import annotations

import numpy as np
import cv2
import types
import typing
import time
import os

objectClasses = ["background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant", "sheep",
    "sofa", "train", "tvmonitor"]

here = os.path.dirname(os.path.abspath(__file__))

net = None 

# net = cv2.dnn.readNetFromCaffe(
#     os.path.join(here, "resources", "MobileNetSSD_deploy.prototxt.txt"), 
#     os.path.join(here, "resources", "MobileNetSSD_deploy.caffemodel"),
# )

class cvStreamFrameObjectDetectionResult():
    def __init__(self, detections) -> None:
        self.detections = detections

    def Draw(self, frame:cvStreamFrame, filterAbove:int=0, filterName:list=[]) -> cvStreamFrame:
        """
        > Draws a rectangle around each object detected by the SSD model, and displays the object's name
        and confidence level
        
        :param frame: the frame to draw on
        :type frame: cvStreamFrame
        :param filterAbove: Filter out detections with confidence below this value, defaults to 0. 百分比, 100为完全匹配.
        :type filterAbove: int (optional)
        :param filterName: list of strings, names of objects to filter out
        :type filterName: list
        :return: A frame with the detections drawn on it.
        """
        (H, W) = frame.frame.shape[:2]

        for i in np.arange(0, self.detections.shape[2]):
            # extract the confidence (i.e., probability) associated
            # with the prediction
            confidence = self.detections[0, 0, i, 2]
            # filter out weak detections by ensuring the `confidence`
            # is greater than the minimum confidence
            if confidence > filterAbove / 100:
                # extract the index of the class label from the
                # detections list
                idx = int(self.detections[0, 0, i, 1])
                name = objectClasses[idx]
                if name in filterName:
                    continue 
                # if the class label is not a car, ignore it
                # if objectClasses[idx] != "car":
                #     continue
                # compute the (x, y)-coordinates of the bounding box
                # for the object
                box = self.detections[0, 0, i, 3:7] * np.array([W, H, W, H])
                (startX, startY, endX, endY) = box.astype("int")
                
                cv2.rectangle(
                    frame.frame, 
                    (startX, startY), 
                    (endX, endY), 
                    (0, 255, 0), 1)

                cv2.putText(frame.frame, '%s: %.2f%%' % (name, confidence*100),
                        (startX+25, startY+30),
                        cv2.FONT_HERSHEY_DUPLEX,
                        1, (0, 255, 0), 1) 
        
        return frame

    def Objects(self) -> dict:
        resp = {}

        for i in np.arange(0, self.detections.shape[2]):
            confidence = self.detections[0, 0, i, 2]
            idx = int(self.detections[0, 0, i, 1])
            name = objectClasses[idx]
            resp[name] = confidence
        
        return resp

class cvStreamFrameDifference():
    def __init__(self, cnts) -> None:
        self.cnts = cnts

    def Draw(self, frame:cvStreamFrame, minAreaSize:int=250) -> cvStreamFrame:
        for c in self.cnts:
            if cv2.contourArea(c) > minAreaSize:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame.frame, (x, y), (x + w, y + h), (0, 255, 0), 1)
        
        return frame

    def HasDifference(self) -> bool:
        return len(self.cnts) != 0

class cvStreamFrame():
    def __init__(self, frame) -> None:
        self.frame = frame
        self.grayFrame = None 

    def __grayFrame(self):
        # print(type(self.grayFrame))
        if type(self.grayFrame) == types.NoneType:
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            self.grayFrame = cv2.GaussianBlur(gray, (21, 21), 0)
        
        return self.grayFrame
    
    def Objects(self) -> cvStreamFrameObjectDetectionResult:
        global net 
        if type(net) == types.NoneType:
            net = cv2.dnn.readNetFromCaffe(
                os.path.join(here, "resources", "MobileNetSSD_deploy.prototxt.txt"), 
                os.path.join(here, "resources", "MobileNetSSD_deploy.caffemodel"),
            )

        # convert the frame to a blob and pass the blob through the
        # network and obtain the detections
        blob = cv2.dnn.blobFromImage(self.frame, size=(300, 300), ddepth=cv2.CV_8U)
        net.setInput(blob, scalefactor=1.0/127.5, mean=[127.5, 127.5, 127.5])
        detections = net.forward()

        return cvStreamFrameObjectDetectionResult(detections)

    def Compare(self, frame:cvStreamFrame) -> cvStreamFrameDifference:
        # Compare the difference between current frame and the background frame 
        frameDelta = cv2.absdiff(self.__grayFrame(), frame.__grayFrame())
        thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

        # Expand the threshold image to fill the hole, and then find the contour on the threshold image
        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        
        return cvStreamFrameDifference(cnts)

    def Show(self, title:str=""):
        cv2.imshow(title, self.frame) 

    def Resize(self, precent:float) -> cvStreamFrame:
        """
        转换图片/帧的大小, precent为百分比. 大于100为放大, 小于100为缩小. 
        
        :param precent: The percentage of the original size you want to resize the image to
        :type precent: int
        :return: A cvStreamFrame object
        """
        precent = precent / 100
        frame = cv2.resize(self.frame, (0, 0), fx=precent, fy=precent)
        return cvStreamFrame(frame)

    def Bright(self, times:int) -> cvStreamFrame:
        """
        > It takes an image and a number, and returns a brighter version of the image
        
        :param times: How many times to brighter
        :type times: int
        :return: A cvStreamFrame object.
        """
        if times == 1:
            return self
        
        img2 = cv2.add(self.frame, self.frame)
        if times == 2:
            return cvStreamFrame(img2) 
        else:
            for _ in range(2, times):
                img2 = cv2.add(img2, self.frame)
        
            return cvStreamFrame(img2)

    def Rotate(self, side:int) -> cvStreamFrame:
        """
        旋转或者镜像

        :param side: 0, 1, -1分别为逆时针旋转90度, 180度, 左右镜像
        :type side: int
        :return: A cvStreamFrame object
        """
        frame = cv2.flip(cv2.transpose(self.frame), side)
        return cvStreamFrame(frame)

    def Text(self, text:str, x:int=None, y:int=None) -> cvStreamFrame:
        x = 10 if x == None else x 
        y = self.frame.shape[0] - 10 if y == None else y
        cv2.putText(self.frame, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 2)
        return self
    
    def Size(self) -> typing.Tuple[int, int]:
        return self.frame.shape[0], self.frame.shape[1]

class Stream():
    def __init__(self, source:int|str) -> None:
        """
        source可以是数字, 0, 1, 2, 表示摄像头的编号. 可以是本地视频文件的路径. 可以是远程摄像头的http地址.
        
        :param source: The source of the video. 
        :type source: int|str
        """
        self.source = source
        self.stream = cv2.VideoCapture(source)
    
    def FPS(self) -> int:
        # Number of frames to capture
        num_frames = 120
        # Start time
        start = time.time()

        # Grab a few frames
        for i in range(0, num_frames) :
            ret, _ = self.stream.read()
            if not ret:
                return None 

        # End time
        end = time.time()
        # Time elapsed
        seconds = end - start
        # print ("Time taken : {0} seconds".format(seconds))

        # Calculate frames per second
        fps  = int(num_frames / seconds)
        # print("Estimated frames per second : {0}".format(fps))
        # 
        return fps 

    def Close(self):
        self.stream.release()
        cv2.destroyAllWindows()
    
    def Get(self) -> cvStreamFrame:
        (grabbed, frame) = self.stream.read()

        if not grabbed:
            return 
        
        return cvStreamFrame(frame)

    def __iter__(self) -> typing.Iterator[cvStreamFrame]:
        while True:
            (grabbed, frame) = self.stream.read()

            if not grabbed:
                return 

            key = cv2.waitKey(1) & 0xFF
            if key == ord("q"):
                break

            yield cvStreamFrame(frame)
            
    def __enter__(self):
        return self 
    
    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.Close()
        except:
            pass

class VideoWriter():
    def __init__(self, path:str, fps:int, width:int, height:int) -> None:
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.writer = cv2.VideoWriter(path, fourcc, fps, (height, width))
        self.closed = False

    def Write(self, frame:cvStreamFrame):
        if self.closed == True:
            self.writer.write(frame.frame) 

    def Close(self):
        if self.closed == False:
            self.closed = True 
            self.writer.release() 

if __name__ == "__main__":
    import os
    import datetime 
    
    # web camera
    # stream = Stream("http://10.129.129.207:8080/video")

    # usb camera
    stream = Stream(0)

    # print(stream.FPS())

    # Video file
    stream = Stream(os.getenv("HOME") + "/Desktop/1080p/2022-12-04.19.37.08.mp4")

    # bg = stream.Get()
    # for frame in stream:
    #     frame.Compare(bg).Draw(frame).Text(datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")).Show("test")

    # bg = stream.Get().Bright(5).Rotate(0)
    # for frame in stream:
    #     frame = frame.Bright(5).Rotate(0)
    #     frame.Compare(bg).Draw(frame).Text(datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p")).Show("test")

    # for frame in stream:
    #     frame.Objects().Draw(frame, filterAbove=70).Show("")

    frame = stream.Get()
    w, h = frame.Size()
    print(w,h )
    writer = VideoWriter("video.mp4", 25, w, h)

    for _ in range(0, 250):
        writer.Write(stream.Get())
    
    writer.Close()