import zmq
import random
import time


class K_Means:
    def __init__(self, k, tolerance=0.0001, max_iterations=500):
        self.k = k
        self.tolerance = tolerance
        self.max_iterations = max_iterations
        self.clusters = self.generateClusters()

        self.context = zmq.Context()
        self.sinkPush = self.context.socket(zmq.PUSH)
        self.workers = self.context.socket(zmq.PUSH)
        self.sinkPull = self.context.socket(zmq.PULL)
        self.sinkPull.bind('tcp://*:5559')
        self.sinkPush.connect('tcp://localhost:5558')
        self.workers.bind('tcp://*:5557')

    def generateClusters(self):
        data = self.readIris("datos.csv")
        clusters = []
        for i in range(self.k):
            p = random.randint(0, len(data))
            clusters.append(data[p])
        print("Choosing initical points at {}".format(clusters))
        return clusters

    def readIris(self, filename):
        data = []
        with open(filename, "r") as f:
            f.readline()
            while True:
                line = f.readline()
                if not line:
                    break
                parts = line.split(",")
                x, y, z, w, _ = parts
                data.append([float(x), float(y), float(z), float(w)])
            return data

    def cluster(self):
        dataSink = {
            'numberTask': 1000
        }
        self.sinkPush.send_json(dataSink)
        for i in range(self.max_iterations):
            print("Iteration {}".format(i))
            dataWorkes = {
                'clusters': self.clusters,
            }
            self.workers.send_json(dataWorkes)
        response = self.sinkPull.recv_json()
        print(response['clusters'])


def main():
    print("Press enter when workers are ready...")
    _ = input()
    print("sending tasks to workers")
    m = K_Means(3, tolerance=0.000001)
    m.cluster()


if __name__ == "__main__":
    main()
