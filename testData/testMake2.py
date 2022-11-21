import sys
import random
import math

def normalize(vec):
    x = 0
    for i in range(len(vec)):
        x += vec[i] * vec[i]

    x = math.sqrt(x)

    for i in range(len(vec)):
        vec[i] = vec[i] / x

    return vec

def main():

    if len(sys.argv) < 3:
        print("python testMake2.py <output filename> <size> <standard deviation> <lambda1> <lambda2> ...")
        sys.exit()

    size = int(sys.argv[2])
    filename = sys.argv[1]
    fileobj = open(filename, "w")
    distFileObj = open("dist" + filename, "w")
    fileobj.write("sptensor\n3\n" + str(size) + " " + str(size) + " " + str(size) + "\n" + str(size**3) + "\n")
    sd = float(sys.argv[3])
    distance = 0

    lambdaList = []
    for i in range(4, len(sys.argv)):
        lambdaList.append(float(sys.argv[i]))


    u = []
    v = []
    w = []
    for i in range(len(lambdaList)):
        u.append([])
        v.append([])
        w.append([])
    


    for i in range(len(lambdaList)):
        for j in range(size):
            u[i].append(random.normalvariate(0,sd))
            v[i].append(random.normalvariate(0,sd))
            w[i].append(random.normalvariate(0,sd))
        normalize(u[i])
        normalize(v[i])
        normalize(w[i])

    for i in range(size):
        for j in range(size):
            for k in range(size):
                temp = 0 # for output
                temp2 = 0 # for distance
                # running total of decomp rank component addition
                for c in range(len(lambdaList)):
                    temp += lambdaList[c] * u[c][i] * v[c][j] * w[c][k]
                fileobj.write(str(i) + " " + str(j) + " " + str(k) + " " + 
                              str(temp) + "\n")
                temp2 = (lambdaList[0] * u[0][i] * v[0][j] * w[0][k]) - temp;
                distance += temp2 * temp2

    distance = distance / size**3
    distFileObj.write("{0:.9e}".format(distance))
    print("Distance = ", distance)
main()
