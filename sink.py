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

        self.classes = {}
        for i in range(recvIniticalTask['numerCluster']):
            self.classes[i] = []

        for task in range(int(recvIniticalTask['numberTask'])):
            s = self.fan.recv_json()
            for p in range(recvIniticalTask['numerCluster']):
                if len(s['data'][str(p)])  != 0:
                    self.classes[p].append(s['data'][str(p)])
            print(self.classes)
                
                
        self.sendFan.send_json(s)

if __name__ == '__main__':
    skin = Skin()
    skin.runSkin()
