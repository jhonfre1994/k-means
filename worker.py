import sys
import time
import zmq



class Worker:
    def __init__(self):
        self.context = zmq.Context()
        self.work = self.context.socket(zmq.PULL)
        self.work.connect('tcp://localhost:5557')
        self.sink = self.context.socket(zmq.PUSH)
        self.sink.connect('tcp://localhost:5558')

    def runWorker(self):
        while True:
            s = self.work.recv_json()
            print(s['clusters'])
            self.sink.send_json(s)

if __name__ == '__main__':
    worker = Worker()
    worker.runWorker()