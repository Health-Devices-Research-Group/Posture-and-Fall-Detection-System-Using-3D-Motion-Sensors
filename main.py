import tensorflow as tf
import numpy as np
import os
from time import sleep
from common import common as cm
import queue
import threading
import time
from keras.models import load_model

UBUNTU = True  # False
CLASSIFICATION_OUTPUT_TO_STR = {0: "STANDING", 1: "SITTING", 2: "LYING DOWN", 3: "BENDING"}
fallNum = 0

lowest_y_point = 1000

# Threshold of how many meters from the lowest point in the room is acceptable to approve the person is lying down on the ground
M_FROM_FLOOR = 0.25

objects_per_room = {}   

comm = cm()

def importFloorData(roomNumber):
    filepath = "data/floorplans/" + str(roomNumber) + ".txt"
    if (os.path.isfile(filepath)):
        file = open(filepath, 'r')
        objects_per_room[str(roomNumber)] = []  # This room has a list of objects
        objects = file.read().splitlines()
        num_objects = int(len(objects) / 4)  # Each file has 4 coords
        for i in range(num_objects):
            objects_per_room[str(roomNumber)].append(
                objects[(i * 4):(i * 4) + 4])  # Append the object to the list of objects for that particular room
    print("FLOOR OBJECT DATA IMPORTED FOR ROOM #" + str(roomNumber) + "... !")
    return

# deprecated but still usable, isLayingOnTheFloor() is the new implementation
def isWithinGroundRange(x, z, roomNumber):
    objects = objects_per_room[str(roomNumber)]  # Impoted floor data for that room
    for object in objects:
        if (x > float(object[0]) and x < float(object[1]) and z > float(object[2]) and z < float(object[3])):  # If person is on that object
            return False
    return True


def getLSTMClassification(inputVals):
    if (inputVals[0][0] < 0.3):
        return "LYING DOWN"
    classification_output = model.predict(np.array([tuple(inputVals)]).reshape(1,7,1))
    return CLASSIFICATION_OUTPUT_TO_STR[np.argmax(classification_output,1)[0]]

def isLayingOnTheFloor(footRightPosY, footLeftPosY):
    if ((footRightPosY < (lowest_y_point + M_FROM_FLOOR)) and (footLeftPosY < (lowest_y_point + M_FROM_FLOOR))):
        return True
    return False

if __name__ == "__main__":
    print("Loading model..")
    model = load_model('postureDetection_LSTM.h5')

    # LAUNCH TKINTER UI IF USING WINDOWS
    root = ""
    labelText = ""
    if (not UBUNTU):
        from tkinter import Tk, StringVar, Label

        root = Tk()
        root.title("POSTURE DETECTION")
        root.geometry("400x100")
        labelText = StringVar()
        labelText.set('Starting...!')
        button = Label(root, textvariable=labelText, font=("Helvetica", 40))
        button.pack()
        root.update()

    roomNumber = 0  # Room number 0
    importFloorData(roomNumber)

    #file = open('data/real_time_joints_data.txt', 'w+')
    file = open('real_time_joints_data.txt', 'w+')
    index = 0

    # Initialization step
    # Extract data from sensor and take the lowest point of foot left & right
    while (index < 300):  # 3 sec * 10numbers/frame 10frames/sec
        lines = file.read().splitlines()
        file.seek(0)
        if (len(lines) >= index + 10):  # if there is new data
            index += 10
            inp = lines[index - 10:index]  # get data for next frame
            # Which Y-position is lower?
            if (float(inp[7]) < float(inp[8])):  # Then use inp[5] because it's the smallest Y-point
                if (lowest_y_point > float(inp[7])):
                    lowest_y_point = float(inp[7])
            else:
                if (lowest_y_point > float(inp[8])):
                    lowest_y_point = float(inp[8])

    print("LOWEST_Y_POINT === " + str(lowest_y_point))

    # End of initialization step
    #file = open('data/real_time_joints_data.txt', 'w+')
    file = open('real_time_joints_data.txt', 'w+')
    index = 0

    # Start system
    while True:
        global posture
        lines = file.read().splitlines()
        file.seek(0)  # move cursor to beggining of file for next loop
        if (len(lines) >= index + 10):  # if there is new data
            index += 10
            inp = lines[index - 10:index]  # get data for next frame
            # index += 20 #10 FPS
            inp = [float(i) for i in inp]
            inputVals = np.random.rand(1, 7)
            inputVals[0] = inp[:7]  # Only the first 7 values. The other two values will be used to check the floor plan
            posture = getLSTMClassification(inputVals)
            if (not UBUNTU):
                labelText.set(posture)
                root.update()
            print(posture)
            if (posture == "LYING DOWN"):
                if (isLayingOnTheFloor(float(inp[7]), float(inp[8]))):
                    # timestamps = []
                    # timestamps.append(inp[9])
                    timestamp = inp[9]
                    fall = True
                    allowed = 2  # at least 95% of the time detected as LYING DOWN.
                    allowed_not_on_floor = 5
                    for i in range(20):  # check LYING DOWN for 2 seconds (10fps*2s = 20 frames)
                        while (len(lines) < index + 10):
                            lines = file.read().splitlines()
                            file.seek(0)  # move cursor to beggining of file for next loop
                        index += 10
                        inp = lines[index - 10:index]  # get data for next frame
                        # index += 20 #10 FPS
                        inp = [float(i) for i in inp]
                        inputVals = np.random.rand(1, 7)
                        inputVals[0] = inp[:7]
                        # timestamps.append(inp[9])
                        posture = getLSTMClassification(inputVals)
                        print(posture)
                        if (not UBUNTU):
                            labelText.set(posture)
                            root.update()
                        if (posture == "LYING DOWN"):  # Is the person LYING DOWN on the floor?
                            print('LYING DOWN')
                            if (isLayingOnTheFloor(float(inp[7]), float(inp[8])) == False):
                                if (allowed_not_on_floor == 0):
                                    print("PERSON IS NOT LAYING ON THE FLOOR! No fall..!")
                                    fall = False
                                    break
                                else:
                                    allowed_not_on_floor -= 1
                        else:  # 10% allowed to not be LYING DOWN (2/20)
                            if (allowed == 0):
                                print("PERSON HAS NOT BEEN LAYING ON THE FLOOR FOR MORE THAN 2 SECONDS! No fall..!")
                                fall = False
                                break
                            else:
                                allowed -= 1
                    if (fall):
                        if (not UBUNTU):
                            labelText.set("FALLEN!")
                            root.update()
                        print("--FALLEN!--")

                        # You can now reset index=0 and delete the file to restart the While loop from current data.
                        while posture=="LYING DOWN":  # Fallen until detected in another posture
                            while (len(lines) < index + 10):
                                lines = file.read().splitlines()
                                file.seek(0)  # move cursor to beggining of file for next loop
                            index += 10
                            inp = lines[index - 9:index]  # get data for next frame
                            inp = [float(i) for i in inp]
                            inputVals = np.random.rand(1, 7)
                            inputVals[0] = inp[:7]
                            posture = getLSTMClassification(inputVals)
                            print(posture)
                            if posture != "LYING DOWN":
                                if (not UBUNTU):
                                    labelText.set(posture)
                                    root.update()
                                file = open('real_time_joints_data.txt', 'w+')
                                index = 0
        if (index > 2500):
            # index = 300
            file = open('real_time_joints_data.txt', 'w+')
            index = 0


