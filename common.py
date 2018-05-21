import sqlite3
import numpy as np

class common(object):
    
    def connect(self):
        conn = sqlite3.connect("data/fallDetection.db", isolation_level=None, check_same_thread=False)
        c = conn.cursor()
        return c, conn
    
    def disconnect(self, c, conn):
        c.close()
        conn.close()
        return
    
    # Copies training and testing data from the files to the database
    def setUpTrainingTestingDatabase(self):
        c, conn = common.connect(self)
        c.execute('CREATE TABLE IF NOT EXISTS standing_training(height real, leftHipAngle real, rightHipAngle real, leftKneeAngle real, RightKneeAngle real, chestAngle real, chestKneeAngle real);')
        print('0')
        file = open('data/files/joints_training_data_standing.txt','r')#joints_testing_data_standing.txt','r')
        inp = file.read().splitlines()
        inp = [float(i) for i in inp]
        for i in range(int(len(inp)/7)):
            data = inp[(i*7):(i*7)+7]
            c.execute("INSERT INTO standing_training VALUES(?,?,?,?,?,?,?);",(data[0],data[1],data[2],data[3],data[4],data[5],data[6]))
        c.execute('CREATE TABLE IF NOT EXISTS standing_testing(height real, leftHipAngle real, rightHipAngle real, leftKneeAngle real, RightKneeAngle real, chestAngle real, chestKneeAngle real);')
        print('1')
        file = open('data/files/joints_data_standing_testing.txt','r')#joints_testing_data_standing.txt','r')
        inp = file.read().splitlines()
        inp = [float(i) for i in inp]
        for i in range(int(len(inp)/7)):
            data = inp[(i*7):(i*7)+7]
            c.execute("INSERT INTO standing_testing VALUES(?,?,?,?,?,?,?);",(data[0],data[1],data[2],data[3],data[4],data[5],data[6]))
        c.execute('CREATE TABLE IF NOT EXISTS sitting_training(height real, leftHipAngle real, rightHipAngle real, leftKneeAngle real, RightKneeAngle real, chestAngle real, chestKneeAngle real);')
        print('2')
        file = open('data/files/joints_training_data_sitting.txt','r')
        inp = file.read().splitlines()
        inp = [float(i) for i in inp]
        for i in range(int(len(inp)/7)):
            data = inp[(i*7):(i*7)+7]
            c.execute("INSERT INTO sitting_training VALUES(?,?,?,?,?,?,?);",(data[0],data[1],data[2],data[3],data[4],data[5],data[6]))
        c.execute('CREATE TABLE IF NOT EXISTS sitting_testing(height real, leftHipAngle real, rightHipAngle real, leftKneeAngle real, RightKneeAngle real, chestAngle real, chestKneeAngle real);')
        print('3')
        file = open('data/files/joints_testing_data_sitting.txt','r')
        inp = file.read().splitlines()
        inp = [float(i) for i in inp]
        for i in range(int(len(inp)/7)):
            data = inp[(i*7):(i*7)+7]
            c.execute("INSERT INTO sitting_testing VALUES(?,?,?,?,?,?,?);",(data[0],data[1],data[2],data[3],data[4],data[5],data[6]))
        c.execute('CREATE TABLE IF NOT EXISTS laying_training(height real, leftHipAngle real, rightHipAngle real, leftKneeAngle real, RightKneeAngle real, chestAngle real, chestKneeAngle real);')
        print('4')
        file = open('data/files/joints_training_data_laying_down.txt','r')
        inp = file.read().splitlines()
        inp = [float(i) for i in inp]
        for i in range(int(len(inp)/7)):
            data = inp[(i*7):(i*7)+7]
            c.execute("INSERT INTO laying_training VALUES(?,?,?,?,?,?,?);",(data[0],data[1],data[2],data[3],data[4],data[5],data[6]))
        c.execute('CREATE TABLE IF NOT EXISTS laying_testing(height real, leftHipAngle real, rightHipAngle real, leftKneeAngle real, RightKneeAngle real, chestAngle real, chestKneeAngle real);')
        print('5')
        file = open('data/files/joints_testing_data_laying_down.txt','r')
        inp = file.read().splitlines()
        inp = [float(i) for i in inp]
        for i in range(int(len(inp)/7)):
            data = inp[(i*7):(i*7)+7]
            c.execute("INSERT INTO laying_testing VALUES(?,?,?,?,?,?,?);",(data[0],data[1],data[2],data[3],data[4],data[5],data[6]))
        c.execute('CREATE TABLE IF NOT EXISTS bending_training(height real, leftHipAngle real, rightHipAngle real, leftKneeAngle real, RightKneeAngle real, chestAngle real, chestKneeAngle real);')
        print('6')
        file = open('data/files/joints_training_data_bending.txt','r')
        inp = file.read().splitlines()
        inp = [float(i) for i in inp]
        for i in range(int(len(inp)/7)):
            data = inp[(i*7):(i*7)+7]
            c.execute("INSERT INTO bending_training VALUES(?,?,?,?,?,?,?);",(data[0],data[1],data[2],data[3],data[4],data[5],data[6]))
        c.execute('CREATE TABLE IF NOT EXISTS bending_testing(height real, leftHipAngle real, rightHipAngle real, leftKneeAngle real, RightKneeAngle real, chestAngle real, chestKneeAngle real);')
        print('7')
        file = open('data/files/joints_testing_data_bending.txt','r')
        inp = file.read().splitlines()
        inp = [float(i) for i in inp]
        for i in range(int(len(inp)/7)):
            data = inp[(i*7):(i*7)+7]
            c.execute("INSERT INTO bending_testing VALUES(?,?,?,?,?,?,?);",(data[0],data[1],data[2],data[3],data[4],data[5],data[6]))
        c.execute('CREATE TABLE IF NOT EXISTS realTimeData(height real, leftHipAngle real, rightHipAngle real, leftKneeAngle real, RightKneeAngle real, chestAngle real, chestKneeAngle real, xfoot real, zfoot real);')
        print('end..')
        c.execute('DELETE FROM realTimeData;')
        common.disconnect(self, c, conn)
        return
    
    def getTrainingData(self):
        c, conn = common.connect(self)
        x_train = []
        y_train = []
        inp = c.execute('SELECT * from standing_training;').fetchall()
        for row in inp:
            x_temp = np.random.rand(1,7)
            y_temp = np.random.rand(1, 4)
            x_temp[0] = list(row)
            y_temp[0] = [1,0,0,0]
            x_train.append(x_temp)
            y_train.append(y_temp)
        inp = c.execute('SELECT * from sitting_training;').fetchall()
        for row in inp:
            x_temp = np.random.rand(1,7)
            y_temp = np.random.rand(1, 4)
            x_temp[0] = list(row)
            y_temp[0] = [0,1,0,0]
            x_train.append(x_temp)
            y_train.append(y_temp)
        inp = c.execute('SELECT * from laying_training;').fetchall()
        for row in inp:
            x_temp = np.random.rand(1,7)
            y_temp = np.random.rand(1, 4)
            x_temp[0] = list(row)
            y_temp[0] = [0,0,1,0]
            x_train.append(x_temp)
            y_train.append(y_temp)
#         inp = c.execute('SELECT * from bending_training;').fetchall()
#         for row in inp:
#             x_temp = np.random.rand(1,7)
#             y_temp = np.random.rand(1, 4)
#             x_temp[0] = list(row)
#             y_temp[0] = [0,0,0,1]
#             x_train.append(x_temp)
#             y_train.append(y_temp)
        common.disconnect(self, c, conn)
        return x_train, y_train
        return
    
    def getTestingData(self):
        c, conn = common.connect(self)
        x_test = []
        y_test = []
        inp = c.execute('SELECT * from standing_testing;').fetchall()
        for row in inp:
            x_temp = np.random.rand(1,7)
            y_temp = np.random.rand(1, 4)
            x_temp[0] = list(row)
            y_temp[0] = [1,0,0,0]
            x_test.append(x_temp)
            y_test.append(y_temp)
        inp = c.execute('SELECT * from sitting_testing;').fetchall()
        for row in inp:
            x_temp = np.random.rand(1,7)
            y_temp = np.random.rand(1, 4)
            x_temp[0] = list(row)
            y_temp[0] = [0,1,0,0]
            x_test.append(x_temp)
            y_test.append(y_temp)
        inp = c.execute('SELECT * from laying_testing;').fetchall()
        for row in inp:
            x_temp = np.random.rand(1,7)
            y_temp = np.random.rand(1, 4)
            x_temp[0] = list(row)
            y_temp[0] = [0,0,1,0]
            x_test.append(x_temp)
            y_test.append(y_temp)
#         inp = c.execute('SELECT * from bending_testing;').fetchall()
#         for row in inp:
#             x_temp = np.random.rand(1,7)
#             y_temp = np.random.rand(1, 4)
#             x_temp[0] = list(row)
#             y_temp[0] = [0,0,0,1]
#             x_test.append(x_temp)
#             y_test.append(y_temp)
        common.disconnect(self, c, conn)
        return x_test, y_test
    
# def getTestingData():
#     x_train = []
#     y_train = []
#     file = open('data/joints_data_standing_testing.txt','r')#joints_testing_data_standing.txt','r')
#     inp = file.read().splitlines()
#     inp = [float(i) for i in inp]
#     for i in range(int(len(inp)/7)):
#         x_temp = np.random.rand(1,7)
#         y_temp = np.random.rand(1, 4)
#         x_temp[0] = inp[(i*7):(i*7)+7]
#         y_temp[0] = [1,0,0,0]
#         x_train.append(x_temp)
#         y_train.append(y_temp)
#     file.close()
#     file = open('data/joints_testing_data_sitting.txt','r')
#     inp = file.read().splitlines()
#     inp = [float(i) for i in inp]
#     for i in range(int(len(inp)/7)):
#         x_temp = np.random.rand(1,7)
#         y_temp = np.random.rand(1, 4)
#         x_temp[0] = inp[(i*7):(i*7)+7]
#         y_temp[0] = [0,1,0,0]
#         x_train.append(x_temp)
#         y_train.append(y_temp)
#     file.close()
#     file = open('data/joints_testing_data_laying_down.txt','r')
#     inp = file.read().splitlines()
#     inp = [float(i) for i in inp]
#     for i in range(int(len(inp)/7)):
#         x_temp = np.random.rand(1,7)
#         y_temp = np.random.rand(1, 4)
#         x_temp[0] = inp[(i*7):(i*7)+7]
#         y_temp[0] = [0,0,1,0]
#         x_train.append(x_temp)
#         y_train.append(y_temp)
#     file.close()
# #     file = open('data/joints_testing_data_bending.txt','r')
# #     inp = file.read().splitlines()
# #     inp = [float(i) for i in inp]
# #     for i in range(int(len(inp)/7)):
# #         x_temp = np.random.rand(1,7)
# #         y_temp = np.random.rand(1, 4)
# #         x_temp[0] = inp[(i*7):(i*7)+7]
# #         y_temp[0] = [0,0,0,1]
# #         x_train.append(x_temp)
# #         y_train.append(y_temp)
# #     file.close()
#     return x_train, y_train

#normalize data
#take origin point in data
#look at paper. box strategy 
#normalize data again to make the x, y, and z the same height at different depths.
# def getTrainingData():
#     x_train = []
#     y_train = []
#     file = open('data/joints_training_data_standing.txt','r')
#     inp = file.read().splitlines()
#     inp = [float(i) for i in inp]
#     for i in range(int(len(inp)/7)):
#         x_temp = np.random.rand(1,7)
#         y_temp = np.random.rand(1, 4)
#         x_temp[0] = inp[(i*7):(i*7)+7]
#         y_temp[0] = [1,0,0,0]
#         x_train.append(x_temp)
#         y_train.append(y_temp)
#     file.close()
#     file = open('data/joints_training_data_sitting.txt','r')
#     inp = file.read().splitlines()
#     inp = [float(i) for i in inp]
#     for i in range(int(len(inp)/7)):
#         x_temp = np.random.rand(1,7)
#         y_temp = np.random.rand(1, 4)
#         x_temp[0] = inp[(i*7):(i*7)+7]
#         y_temp[0] = [0,1,0,0]
#         x_train.append(x_temp)
#         y_train.append(y_temp)
#     file.close()
#     file = open('data/joints_training_data_laying_down.txt','r')
#     inp = file.read().splitlines()
#     inp = [float(i) for i in inp]
#     for i in range(int(len(inp)/7)):
#         x_temp = np.random.rand(1,7)
#         y_temp = np.random.rand(1, 4)
#         x_temp[0] = inp[(i*7):(i*7)+7]
#         y_temp[0] = [0,0,1,0]
#         x_train.append(x_temp)
#         y_train.append(y_temp)
#     file.close()
#     file = open('data/joints_training_data_bending.txt','r') #bending
#     inp = file.read().splitlines()
#     inp = [float(i) for i in inp]
#     for i in range(int(len(inp)/7)):
#         x_temp = np.random.rand(1,7)
#         y_temp = np.random.rand(1, 4)
#         x_temp[0] = inp[(i*7):(i*7)+7]
#         y_temp[0] = [0,0,0,1]
#         x_train.append(x_temp)
#         y_train.append(y_temp)
#     return x_train, y_train
# 
# def getTestingData():
#     x_train = []
#     y_train = []
#     file = open('data/joints_testing_standing_data.txt','r')
#     inp = file.read().splitlines()
#     inp = [float(i) for i in inp]
#     for i in range(int(len(inp)/45)):
#         x_temp = np.random.rand(1,45)
#         y_temp = np.random.rand(1, 4)
#         x_temp[0] = inp[(i*45):(i*45)+45]
#         y_temp[0] = [1,0,0,0]
#         x_train.append(x_temp)
#         y_train.append(y_temp)
#     file.close()
#     file = open('data/joints_testing_sitting_data.txt','r')
#     inp = file.read().splitlines()
#     inp = [float(i) for i in inp]
#     for i in range(int(len(inp)/45)):
#         x_temp = np.random.rand(1,45)
#         y_temp = np.random.rand(1, 4)
#         x_temp[0] = inp[(i*45):(i*45)+45]
#         y_temp[0] = [0,1,0,0]
#         x_train.append(x_temp)
#         y_train.append(y_temp)
#     file.close()
# #     file = open('data/joints_testing_laying_data.txt','r')
# #     inp = file.read().splitlines()
# #     inp = [float(i) for i in inp]
# #     for i in range(int(len(inp)/45)):
# #         x_temp = np.random.rand(1,45)
# #         y_temp = np.random.rand(1, 4)
# #         x_temp[0] = inp[(i*45):(i*45)+45]
# #         y_temp[0] = [0,0,1,0]
# #         x_train.append(x_temp)
# #         y_train.append(y_temp)
# #     file.close()
#     file = open('data/joints_testing_others_data.txt','r')
#     inp = file.read().splitlines()
#     inp = [float(i) for i in inp]
#     for i in range(int(len(inp)/7)):
#         x_temp = np.random.rand(1,7)
#         y_temp = np.random.rand(1, 4)
#         x_temp[0] = inp[(i*7):(i*7)+7]
#         y_temp[0] = [0,0,0,1]
#         x_train.append(x_temp)
#         y_train.append(y_temp)
#     file.close()
#     return x_train, y_train
