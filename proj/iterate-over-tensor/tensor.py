


class Tensor:


    # Multiple ways of contructing the basic tensor
    # 1) manually pass in dimensions e.g. Tensor(x = x, y = y, z = y)
    # 2) pass in an input file e.g. Tensor(inputFile = "filepath")
    def __init__(self, *, x = None, y = None, z = None, filepath = None):

        # The following attributes will be created
        # self.t : the tensor
        # self.numDims : int, the number of dimensions
        # self.dims : list[int], the size of each dimension
        # self.x : int, size of x dimension
        # self.y : int, size of y dimension
        # self.z : int, size of z dimension        
        if (!filepath and x and y and z):
            # dimensions manually passed in
            # TENSOR NOT FILLED WITH DATA
            self.__contruct_from_dims(x, y, z)
            
        elif (!x and !y and !z and filepath):
            # input file passed in
            # TENSOR FILLED WITH DATA FROM FILE
            self.__construct_from_file(filepath)
            
        else:
            sys.exit("Invalid data passed to class initialization. Program exit")

            

    def __contruct_from_dims(self, x, y, z):
        self.t = []
        self.x = x
        self.y = y
        self.z = z

        self.numDims = 3
        self.dims = [x, y, z]

        self.resize()
        return

    

    def __construct_from_file(self, filepath):

        self.t = []
        with open(filepath, "r")as inputFile:
            i = 0
            for line in inputFile.readline():
                
                # first line not currently used, but would be used to specify sparse/dense tensor
                if i == 0:
                    i+= 1
                
                # second line is the number of dimensions for the tensor. Currently, only 3 dimensions can be handled
                # this is really in here in case I ever do a custom datastructure for a tensor
                elif i == 1:
                    i += 1
                    self.numDims = int(line)
                    
                # third line is the size of each dimension, x y z
                elif i == 2:
                    i += 1
                    self.dims = [int(i) for i in line.split()]
                    self.x = self.dims[0]
                    self.y = self.dims[1]
                    self.z = self.dims[2]
                    
                    self.resize()
                
                # fourth line is total number of data in tensor
                # not used, but can be used to indicate sparse/dense
                elif i == 3:
                    i += 1

                # all other lines are the contexts of each cell
                # x y z int_data
                elif i > 3:
                    d = line.split()

                    self.t[int(d[0])][int(d[1])][int(d[2])] = d[3]
        return



    # Getter got numDims
    def GetnumDims(self):
        return self.numDims


    # resize the tensor based upon (assumed) updated self.x/y/z
    # this will clear the data in the tensor
    def resize(self):
        self.t = [ [ [ None for z in self.z ] for y in self.y ] for x in self.x ]

        return



    # Sets value at specified index
    # c: list containing index, e.g. c[0] = x, c[1] = y, c[2] = z
    # val: value to set
    def setIndex(self, c, val):
        self.t[c[0]][c[1]][c[2]] = val
        return
