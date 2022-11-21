import sys
import random

def main():

    if len(sys.argv) < 3:
        print("python testMake.py <output filename> <size> <standard deviation>")
        sys.exit()

    size = int(sys.argv[2])
    filename = sys.argv[1]
    fileobj = open(filename, "w")
    fileobj.write("sptensor\n3\n" + str(size) + " " + str(size) + " " + str(size) + "\n" + str(size**3) + "\n")
    sd = float(sys.argv[3])

    for i in range(size):
        for j in range(size):
            for k in range(size):
                fileobj.write(str(i) + " " + str(j) + " " + str(k) + " " + 
                              str(((i+1) * (j+1) * (k+1)) + random.normalvariate(0, sd)) + "\n")

main()
