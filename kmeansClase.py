import random
import math
import copy

class K_Means:
    def __init__(self, k, tolerance = 0.0001, max_iterations = 500):
        # Number of clusters to find
        self.k = k
        # When to stop
        self.tolerance = tolerance
        self.max_iterations = max_iterations

    def cluster(self, data):
        # Centroids initialization: choose the first k data points
        self.centroids = {}
        random.seed()
        for i in range(self.k):
            p = random.randint(0, len(data))
            print("Choosing point at {}".format(p))
            self.centroids[i] = data[p]

        print("Centroids: {}".format(self.centroids))
        # Main part of the algorithm: alternates phases 1 and 2:
        # Complexity O(I*(k*n+n)) = O(I*N*K)
        for i in range(self.max_iterations):
            print("Iteration {}".format(i))
            # Complexity: O(k)
            self.classes = {}
            for i in range(self.k):
                self.classes[i] = []

            # Find the nearest centroid to each point.
            # Complexity: O(n*k) n: numberof points to cluster
            for p in data:
                c = self.nearestCentroid(p)# Complexity O(k)
                self.classes[c].append(p)

            # for i in range(self.k):
                # print("cluster {} contains {} points".format(i,len(self.classes[i])))

            old = copy.deepcopy(self.centroids)
            # print(self.centroids)
            # print(self.classes[0])
            # Recompute coentroids
            # Complexity: O(n)
            for c in range(self.k):
                self.recomputeCentroid(c, self.classes[c])
            # print(self.centroids)
            delta = self.distanceOldNew(old, self.centroids)
            if delta < self.tolerance:
                print("delta")
                print(delta)
                break

    def distanceOldNew(self, old, new):
        d = 0.0
        for i in range(self.k):
            d += self.distance(old[i],new[i])
        return d
    def distance(self, p, q):
        s = 0
        for i in range(len(p)):
            s += (p[i] - q[i])**2
        return math.sqrt(s)
    
    def norm(self,p):
        s = 0.0
        for i  in range(len(p)):
            s += p[i]**2
        return math.sqrt(s)

    def angle(self, p, q):
        s = 0.0
        for i in range(len(p)):
            s += p[i]*q[i]
        f = s/(self.norm(p)*self.norm(q))
        f = round(f,5)
        return math.acos(f)

    def nearestCentroid(self, p):
        distindex = 0
        dist = math.inf
        for i in range(self.k):
            #d =self.distance(self.centroids[i],p)
            d = self.angle(self.centroids[i],p)
            if d < dist:
                dist = d
                distindex = i
        return distindex

    def recomputeCentroid(self, c, points):
        dimensions = len(points[0])
        for d in range(dimensions):
            sumd = 0
            for p in points:
                #print(p)
                sumd += p[d]
                #print(sumd)
            self.centroids[c][d] = sumd / len(points)

def readIris(filename):
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


def main():
    data = readIris("datos.csv")
    # print(data)
    m = K_Means(3, tolerance=0.000001)
    m.cluster(data)
    for i in range(m.k):
        print("cluster {} contains {} points".format(i,len(m.classes[i])))


if __name__ == "__main__":
    main()