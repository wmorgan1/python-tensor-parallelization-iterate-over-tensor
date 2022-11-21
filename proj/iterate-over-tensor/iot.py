


d = 0
dn = 0
dls = 0
totalThreads = 0

# Prints a list
# stream is a string to indicate printing to cout or cerr
def printL(text, list_obj, stream):


    if stream == "cout": stream = sys.stdout
    elif stream == "cerr": stream = sys.stderr
        
    print(f"{text} {list_obj}", file=stream)

    return


# Print a matrix
# stream is a string to indicate printing to cout or cerr
def printM(text, matrix, stream):

    if stream == "cout": stream = sys.stdout
    elif stream == "cerr": stream = sys.stderr

    for x in range(len(matrix)):
        print(f"{text}\n\t{matrix[x]}", file=stream)

    return


# Take 2 vectors and perform dot/cross product
# v1: left vector
# v2: right vector
# m: product matrix, INITIALIZED ONLY
# lambda{1,2}: lambda values of each vector
##### May be faster with Numpy ??? #####
def VtoVmul(v1, v2, m, lambda1 = 1, lambda2 = 1):

    lv1 = len(v1)
    lv2 = len(v2)
    
    # assuming pre-allocation is faster, but testing should be done
    m = [ None for x in range(lv1) ]

    for x in range(lv1):
        m[x] = [ None for y in range(lv2) ]

        for y in range(lv2):
            m[x][y] = lambda1 * v1[x] * lambda2 * v2[y]
    return


# Take a matrix and a vector and return tensor product
# m: matrix
# v: vector
# t: tensor to return
# lambda1: lambda value of the vector, default to 1
##### May be faster with Numpy ??? #####
def MtoVmul(m, v, t, lambda1 = 1):
    x = len(m)
    y = len(m[0])
    z = len(v)

    print(f"numDims = {t.GetnumDims()}")

    c = [ 0 for i in range(t.GetnumDims()) ]

    for x in range(c[0], c[0] < x, c[0] = c[0] + 1):
        for y in range(c[1], c[1] < y, c[1] += 1):
            for z in range(c[2], c[2] < z, c[2] += 1):
                t.setIndex(c, m[c[0]][c[1]] * v[c[2]] * lambda)

    return


# Helper method for LS() , ie Least Squares
# Calculates E UliVliWli where l != a
# uold, vold, wold: matrixes to calculate over, only a single vector for each is used
# i: index of uold, i.e. which vector of uold to use
# j: index of vold, ""
# k: index of wold, ""
# a: component in question of u,v,w
# A: the total number of components
# returns a double
#### This function is NOT parallelized, as all available processes should be busy in LS() ####
def helper(uold, vold, wold, i, j, k, a, A):
    result = 0

    for it in range(A):
        if (it != a): result += uold[it][i] * vold[it][j] * wold[it][k]

    return result


# Calculate Least Squares
            
    
