import random
import sys
import math
import numpy as np

d = False
dn = False
dls = False

'''
experiment in coding Least Squares on a tensor
this code will only work on 3 dimensional cubes

This code is not currently generalized, and was made for the test case
of a 3x3x3 tensor
Generalizing this would be fairly simple
'''

# dimensions of the tensor
x = 3
y = 3
z = 3

'''
Least Squares method
v1 is the u/v/w vector to be approximated
v2/v3 are the other two vectors
tensor is the tensor
dim is the dimension being held constant
python list are passed by reference, so changes to v1 apply in all scopes 
v1 exists in
'''

'''
change fn to take in a list of vectors
[u, v, w]
and an index to hold steady (tensorijk is wrong)
'''

def LS(v1, v2, v3, tensor, dim):
    top = 0
    bottom = 0

    if dls:
        print("LS")
        print("\tv1 = ", v1)
        print("\tv2 = ", v2)
        print("\tv3 = ", v3)
    
    for i in range(len(v1)):
        top = 0

        # summation from j, k to n
        for j in range(len(v2)):
            for k in range(len(v3)):
                '''if dls:
                print("\ttop = ", top)
                print("\tj = ", j, " k = ", k)
                print("\ttensorIJK = ", tensor[i][j][k])'''
                # Vj * Wk * Xijk
                if dim == 1:
                    top += v2[j] * v3[k] * tensor[i][j][k]
                elif dim == 2:
                    top += v2[j] * v3[k] * tensor[j][i][k]
                elif dim == 3:
                    top += v2[j] * v3[k] * tensor[j][k][i]


        # bottom only needs to happen once
        if (i == 0):
            # summation from j, k to n
            # currently, n is just the length of v2 and v3, both equal to 3
            for j in range(len(v2)):
                for k in range(len(v3)):
                    '''if dls:
                        print("\tbottom = ", bottom)'''
                    bottom += v2[j]**2 * v3[k]**2

        if dls:
            print("\ttop = ", top, " bottom = ", bottom)



        v1[i] = top / bottom

    return


'''
v1 is u/v/wold and v2 is u/v/wnew
the components of v1 and v2 are summed
these sums are then subtracted and squared
the result is returned
'''
def normalize(v1):
    if dn:
        print("normalize ", v1)
    
    x = 0

    # x = (Eu**2)**(1/2)
    for i in v1:
        x += (i**2)
    if dn:
        print("\tx summed =", x)
    x = math.sqrt(x)
    if dn:
        print("\tsqrt(x) =", x)

    for i in range(len(v1)):
        v1[i] = v1[i] / x
        
    return x


'''
v1 is u/v/wold and v2 is u/v/wnew
result is returned
'''
def distance(v1, v2):
    assert (len(v1) == len(v2))
    sum = 0
    for i in range(len(v1)):
        sum += (v1[i] - v2[i])**2
    return sum
    
def main():
    norm = False
    sigma = 1
    componentModel = 0
    it = 0
    global d
    global dn
    global dls


    # no command line parameters
    if (len(sys.argv) == 1):
        print("Format: python3 leastSquares.py -s <sigma>  <other paramters>")
        sigstr = "\t-s <numeric value> :: distance between approximation " + \
        "vectors required to stop the algorithm"
        print(sigstr)
        normstr = "\t-n :: if you want the vectors to be normalized on every iteration"
        print(normstr)
        print("\t-c <1/2> :: 1 or 2 component approximation")
        debugstr = "\t-d <all/d/dn/dls> :: all debug statements OR main OR " + \
                   "normalize OR LS. They can be several -d IE -d d -d dn"
        print(debugstr)
        sys.exit(1)
    else:
        for i in range(1, len(sys.argv)):
            if sys.argv[i] == "-s":
                sigma = float(sys.argv[i + 1])
            elif sys.argv[i] == "-n":
                norm = True
            elif sys.argv[i] == "-c":
                componentModel = int(sys.argv[i + 1])
            elif sys.argv[i] == "-d":
                if sys.argv[i + 1] == "all":
                    d = True
                    dn = True
                    dls = True
                elif sys.argv[i + 1] == "d":
                    d = True
                elif sys.argv[i + 1] == "dn":
                    dn = True
                elif sys.argv[i + 1] == "dls":
                    dls = True
                else:
                    print("Error parsing -d flag. Program exit.")
                    sys.exit(1)

    if d:
        print("sigma =", sigma)
        print("norm =", norm)
        print("model =", componentModel)
        print("d =", d)
        print("dn =", dn)
        print("dls =", dls)
        
    tensor = [
        [[2,2],[1,1],[1,1]],
        [[2,2],[1,1],[1,1]],
        [[2,2],[1,1],[1,1]],
        [[2,2],[1,1],[1,1]]]
    '''
    r1tst = np.outer(np.outer([20,1,1], [1,1,1]), [1,1,1])
    delta = np.outer(np.outer([1,1,1], [18, 1, 1]), [1, 1, 1])

    if componentModel == 1:
        # One compontent test tensor

        tensor = [[list(r1tst[0]), list(r1tst[1]), list(r1tst[2])], 
                  [list(r1tst[3]), list(r1tst[4]), list(r1tst[5])], 
                  [list(r1tst[6]), list(r1tst[7]), list(r1tst[8])]]
    elif componentModel == 2:
        # Two component test tensor
        
        tensor = [[list(r1tst[0]+delta[0]), list(r1tst[1]+delta[1]), list(r1tst[2]+delta[2])], 
                  [list(r1tst[3]+delta[3]), list(r1tst[4]+delta[4]), list(r1tst[5]+delta[5])], 
                  [list(r1tst[6]+delta[6]), list(r1tst[7]+delta[7]), list(r1tst[8]+delta[8])]]
    '''
    if d:
        print(tensor)
        
    

    # vector approximations
    unew = uold = np.float_([1, 1, 1, 1])
    vnew = vold = np.float_([1, 1, 1])
    wnew = wold = np.float_([1, 1])

    lamdaU = normalize(unew)
    lamdaV = normalize(vnew)
    lamdaW = normalize(wnew)
    if d:
        print("unew =", unew)
        print("vnew =", vnew)
        print("wnew =", wnew)
    

    while True:
        # Step 1: Perform comparison, abovew
        it += 1
        
        if d:
            print("main: in while loop")

        # Step 2: The 'new' approximations become old
        np.copyto(uold, unew)
        np.copyto(vold, vnew)
        np.copyto(wold, wnew)


        # Step 3: Find new approximations
        LS(unew, vold, wold, tensor, 1)
        LS(vnew, uold, wold, tensor, 2)
        LS(wnew, uold, vold, tensor, 3)
        

        if d:
            print("main: back from LS")
            print("unew =", unew)
            print("vnew =", vnew)
            print("wnew =", wnew)

        # Step 4: normalize the vectors, if applicable
        if norm:
            lamdaU = normalize(unew)
            lamdaV = normalize(vnew)
            lamdaW = normalize(wnew)
            if d:
                print("\tlamdaU =", lamdaU)
                print("\tlamdaV =", lamdaV)
                print("\tlamdaW =", lamdaW)

        if d and norm:
            print("\tu norm = ", unew)
            print("\tv norm = ", vnew)
            print("\tw norm = ", wnew)

        if d:
            print("\tu dist = ", distance(uold, unew))        
            print("\tv dist = ", distance(vold, vnew))
            print("\tw dist = ", distance(wold, wnew))
            print("\tdistance =", (distance(uold, unew) +
                   distance(vold, vnew) +
                   distance(wold, wnew)))
        print("ITERATION = ", it)

        if  ((distance(uold, unew) + distance(vold, vnew) + \
              distance(wold, wnew)) < sigma):
            break        
    print("END unew = ", unew)
    print("END vnew = ", vnew)
    print("END wnew = ", wnew)

    if componentModel == 1:
        if norm:
            print("Normalized 1 component approximation:")
            print(np.outer(np.outer(lamdaU * unew, lamdaV * vnew), lamdaW * wnew))
        else:
            print("1 component approximation")
            print(np.outer(np.outer(unew,vnew),wnew))
    if componentModel == 2:
        if norm:
            print("Normalized 2 component approximation:")
            print(np.outer(np.outer(lamdaU * unew, lamdaV * vnew), lamdaW * wnew))
        else:
            print("2 component approximation")
            print(np.outer(np.outer(unew,vnew),wnew))
    #print(np.outer(unew,vnew))


main()
