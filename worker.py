import sys
import time
import zmq
import itertools
import math
import pprint

class Worker:
    def __init__(self):
        self.context = zmq.Context()
        self.work = self.context.socket(zmq.PULL)
        self.work.connect('tcp://localhost:5557')
        self.sink = self.context.socket(zmq.PUSH)
        self.sink.connect('tcp://localhost:5558')
    def runWorker(self):
        while True:
            data = []
            s = self.work.recv_json()
            data = self.readFile(s['initLine'] - 1 , s['finalLine'])
            self.centroids = {}
            self.processInfo(data, s['clusters'])
            self.centroids = s['clusters']
            print("Procesando informacion, de la linea", str(s['initLine']), "hasta la linea", str(s['finalLine'])  )
            resSink = []
            for c in range(len(s['clusters'])):
                res = self.averagePoints(c, self.classes[c], len(data[0]))
                resSink.append(res)
            print(s['iteriator'])
            pprint.pprint(resSink)

            dataWorkers = {
                'data': resSink
            }
            self.sink.send_json(dataWorkers)

    def readFile(self, init, final):
        data = []
        with open("datos.csv", "r") as f:
            for line in itertools.islice(f, init, final):
                parts = line.split(",")
                x, y, z, w, _ = parts
                data.append([float(x), float(y), float(z), float(w)])
        return data

    def processInfo(self, data, clusters):
        self.classes = {}
        for i in range(len(clusters)):
            self.classes[i] = []

        for p in data:
            c = self.nearestCentroid(p, clusters)  # Complexity O(k)
            self.classes[c].append(p)

    def nearestCentroid(self, p, clusters):
        distindex = 0
        dist = math.inf
        for i in range(len(clusters)):
            d = self.angle(clusters[i], p)
            if d < dist:
                dist = d
                distindex = i
        return distindex

    def norm(self, p):
        s = 0.0
        for i in range(len(p)):
            s += p[i]**2
        return math.sqrt(s)

    def angle(self, p, q):
        s = 0.0
        for i in range(len(p)):
            s += p[i]*q[i]
        f = s/(self.norm(p)*self.norm(q))
        f = round(f, 5)
        return math.acos(f)

    def averagePoints(self, c, points, dim):
        dimensions = dim
        for d in range(dimensions):
            sumd = 0
            for p in points:
                sumd += p[d]
            self.centroids[c][d] = sumd
            json = {
                'average': self.centroids[c],
                'cluster': c,
                'sizePoints': len(points)
            }
        return json


if __name__ == '__main__':
    worker = Worker()
    worker.runWorker()
