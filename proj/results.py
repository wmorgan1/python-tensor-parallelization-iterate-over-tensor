import sys

def parse(outfile, filename):
    inFile = open(filename, "r")

    iterations = False
    avList = []
    distance = False

    outfile.write(filename[40:] + "\n")

    for line in inFile:
        splitLine = line.split()
        if splitLine[0] == "ITERATIONS" and iterations == False:
            outfile.write(splitLine[0] + " = " + splitLine[2] + "\n")
            iterations = True
        elif splitLine[0] == "Time" and splitLine[1] == "elapsed:":
            avList.append(splitLine[2])
            outfile.write(splitLine[2] + "\n")
        elif splitLine[0] == "Distance" and distance == False:
            outfile.write(splitLine[0] + " = " + splitLine[2] + "\n")
            distance = True


    average = 0
    for i in avList:
        average += float(i)

    average /= 5
    outfile.write("Average = " + str(average) + "\n")
    outfile.write("\n")



def main():
    out10 = ["/home/wmorgan1/cmarron_user/thesis/proj/als/10/10.out",
             "/home/wmorgan1/cmarron_user/thesis/proj/alternating-parallel-loops/10/10.out",
             "/home/wmorgan1/cmarron_user/thesis/proj/non-alternating-parallel-loops/10/10.out",
             "/home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/10/10.out",
             "/home/wmorgan1/cmarron_user/thesis/proj/shapes-over-tensor/10/10.out"]
    out50 = ["/home/wmorgan1/cmarron_user/thesis/proj/als/50/50.out",
             "/home/wmorgan1/cmarron_user/thesis/proj/alternating-parallel-loops/50/50.out",
             "/home/wmorgan1/cmarron_user/thesis/proj/non-alternating-parallel-loops/50/50.out",
             "/home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/50/50.out",
             "/home/wmorgan1/cmarron_user/thesis/proj/shapes-over-tensor/50/50.out"]
    out100 = ["/home/wmorgan1/cmarron_user/thesis/proj/als/100/100.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/alternating-parallel-loops/100/100.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/non-alternating-parallel-loops/100/100.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/100/100.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/shapes-over-tensor/100/100.out"]
    out150 = ["/home/wmorgan1/cmarron_user/thesis/proj/als/150/150.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/alternating-parallel-loops/150/150.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/non-alternating-parallel-loops/150/150.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/150/150.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/shapes-over-tensor/150/150.out"]
    out200 = ["/home/wmorgan1/cmarron_user/thesis/proj/als/200/200.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/alternating-parallel-loops/200/200.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/non-alternating-parallel-loops/200/200.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/200/200.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/shapes-over-tensor/200/200.out"]
    out300 = ["/home/wmorgan1/cmarron_user/thesis/proj/als/300/300.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/alternating-parallel-loops/300/300.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/non-alternating-parallel-loops/300/300.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/300/300.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/shapes-over-tensor/300/300.out"]
    out400 = ["/home/wmorgan1/cmarron_user/thesis/proj/als/400/400.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/alternating-parallel-loops/400/400.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/non-alternating-parallel-loops/400/400.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/400/400.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/shapes-over-tensor/400/400.out"]
    out500 = ["/home/wmorgan1/cmarron_user/thesis/proj/als/500/500.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/alternating-parallel-loops/500/500.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/non-alternating-parallel-loops/500/500.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/500/500.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/shapes-over-tensor/500/500.out"]
    outEnr = ["/home/wmorgan1/cmarron_user/thesis/proj/als/enron/to-from-time.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/alternating-parallel-loops/enron/to-from-time.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/non-alternating-parallel-loops/enron/to-from-time.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/enron/to-from-time.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/shapes-over-tensor/enron/to-from-time.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/als/enron/time-from-to.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/alternating-parallel-loops/enron/time-from-to.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/non-alternating-parallel-loops/enron/time-from-to.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/iterate-over-tensor/enron/time-from-to.out",
              "/home/wmorgan1/cmarron_user/thesis/proj/shapes-over-tensor/enron/time-from-to.out"]

    outFile = open("/home/wmorgan1/cmarron_user/thesis/testData/" + sys.argv[1] + "/results.txt", "w")

    for i in range(2, len(sys.argv)):
        cur = sys.argv[i]
        try:
            if cur == "10":
                for i in out10:
                    parse(outFile, i)
            elif cur == "50":
                for i in out50:
                    parse(outFile, i)
            elif cur == "100":
                for i in out100:
                    parse(outFile, i)
            elif cur == "150":
                for i in out150:
                    parse(outFile, i)
            elif cur == "200":
                for i in out200:
                    parse(outFile, i)
            elif cur == "300":
                for i in out300:
                    parse(outFile, i)
            elif cur == "400":
                for i in out400:
                    parse(outFile, i)
            elif cur == "500":
                for i in out500:
                    parse(outFile, i)
            elif cur == "enron":
                for i in outEnr:
                    parse(outFile, i)
        except IOError:
            print("Results do not exist for ", cur)
main()
