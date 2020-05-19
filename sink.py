import sys
import time
import zmq


class Skin:
    def __init__(self):
        self.context = zmq.Context()
        self.fan = self.context.socket(zmq.PULL)
        self.fan.bind("tcp://*:5558")
        self.sendFan = self.context.socket(zmq.PUSH)
        self.sendFan.connect('tcp://localhost:5559')

    def runSkin(self):
        recvIniticalTask = self.fan.recv_json()
        print(recvIniticalTask['numberTask'])

        for task in range(recvIniticalTask['numberTask']):
            s = self.fan.recv_json()
            print(s['clusters'])
            self.sendFan.send_json(s)

if __name__ == '__main__':
    skin = Skin()
    skin.runSkin()
