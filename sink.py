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

        self.averages = {}
        for i in range(recvIniticalTask['numerCluster']):
            self.averages[i] = []

        for task in range(int(recvIniticalTask['numberTask'])):
            s = self.fan.recv_json()
            for i in range(len(s['data'])):
                self.averages[s['data'][i]['cluster']].append(s['data'][i]['average'])
            if len(self.averages[0]) == 15:
                self.recomputeCentroids(self.averages, s)

    def recomputeCentroids(self,puntos,s):
        print(puntos)
        self.sendFan.send_json(s)
        for i in range(3):
            self.averages[i] = []



if __name__ == '__main__':
    skin = Skin()
    skin.runSkin()
