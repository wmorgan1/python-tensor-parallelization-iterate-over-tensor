import random
import sys
import math
import numpy as np

d = True
dn = True
dls = True

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
        print("v1 = ", v1)
        print("v2 = ", v2)
        print("v3 = ", v3)
    
    for i in range(len(v1)):
        top = 0

        '''
        what happens if v1/v2/v3 are of different lengths??
        '''

        # summation from j, k to n
        for j in range(len(v2)):
            for k in range(len(v3)):
                '''if dls:
                print("top = ", top)
                print("j = ", j, " k = ", k)
                print("tensorIJK = ", tensor[i][j][k])'''
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
                        print("bottom = ", bottom)'''
                    bottom += v2[j]**2 * v3[k]**2

        if dls and i == 0:
            print("top = ", top, " bottom = ", bottom)



        v1[i] = top / bottom

    return


'''
v1 is u/v/wold and v2 is u/v/wnew
the components of v1 and v2 are summed
these sums are then subtracted and squared
the result is returned
'''
def normalize(v1):
    x = 0

    for i in v1:
        x += (i**2)

    x = math.sqrt(x)

    for i in range(len(v1)):
        v1[i] = v1[i] / x
        
    return x


def distance(v1, v2):

    assert( len(v1) == len(v2) )

    sum = 0
    for i in range(len(v1)):
        sum += (v1[i] - v2[i])**2
    return sum
    
def main():
    norm = False
    sigma = 1
    
    if len(sys.argv) > 2:
        if sys.argv[2] == 'norm':
            norm = True
    sigma = float(sys.argv[1])

    print("Sigma =", sigma)

    # test tensor 
#     tensor = [
#         [[2,2,2],[2,2,2],[2,2,2]],
#         [[1,1,1],[1,1,1],[1,1,1]],
#         [[1,1,1],[1,1,1],[1,1,1]]]

    r1tst = np.outer(np.outer([20,1,1], [1,1,1]), [1,1,1])
    delta = np.outer(np.outer([1,1,1], [18, 1, 1]), [1, 1, 1])

# One compontent test tensor

#     tensor = [[list(r1tst[0]), list(r1tst[1]), list(r1tst[2])], 
#              [list(r1tst[3]), list(r1tst[4]), list(r1tst[5])], 
#              [list(r1tst[6]), list(r1tst[7]), list(r1tst[8])]]

# Two component test tensor

    tensor = [[list(r1tst[0]+delta[0]), list(r1tst[1]+delta[1]), list(r1tst[2]+delta[2])], 
             [list(r1tst[3]+delta[3]), list(r1tst[4]+delta[4]), list(r1tst[5]+delta[5])], 
             [list(r1tst[6]+delta[6]), list(r1tst[7]+delta[7]), list(r1tst[8]+delta[8])]]

    print tensor

    # Initial "random" start vectors
    unew = uold = np.float_([1, 1, 1])
    vnew = vold = np.float_([1, 1, 1])
    wnew = wold = np.float_([1, 1, 1])

    # Normalize random starts
    lambdaU = normalize(unew)
    lambdaV = normalize(vnew)
    lambdaW = normalize(wnew)
    
    while True:

        # Step 1: The 'new' approximations become old
        np.copyto(uold, unew)
        np.copyto(vold, vnew)
        np.copyto(wold, wnew)

        # Step 2: Find new approximations
        LS(unew, vold, wold, tensor, 1)
        LS(vnew, uold, wold, tensor, 2)
        LS(wnew, uold, vold, tensor, 3)

        # Step 3: Normalize vectors    
        lambdaU = normalize(unew)
        lambdaV = normalize(vnew)
        lambdaW = normalize(wnew)

        if  ((distance(uold, unew) + distance(vold, vnew) + distance(wold, wnew))  < sigma):
            break

    print "unew: ", unew
    print "vnew: ", vnew
    print "wnew: ", wnew

    print "One component approximation:"
    print(np.outer(np.outer(lambdaU * unew, lambdaV * vnew), lambdaW * wnew))

main()
