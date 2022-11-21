#include <cstdlib>
#include <cmath>
#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <vector>

//int drf = 1;
//int dta = 1;

using namespace std;

class Tensor
{
public:
    /*
      Default constructor
    */
    Tensor();

    /*
      Constructor that uses a file to extract information about the tensor
      file includes length of each dimension, and data
    */
    Tensor(char* filename);

    /*
      Constructor where the dimensions of the tensor are known, but not the
      data. Leaves the data initilized but not assigned
    */
    Tensor(const vector<unsigned int>& Dims, const unsigned int NumDims);

    /*
      Copy constructor
    */
    Tensor(const Tensor& obj);

    /*
      Destructor
    */
    ~Tensor();

    /*
      computer the distance bewtween the tensor approximation and the tensor
    */
    double distance(const vector < vector < double > >& unew,
		    const vector < vector < double > >& vnew,
		    const vector < vector < double > >& wnew,
		    const double lambda);
    
    /*
      calculates the lambda value accross the entire tensor and component
      vectors.
      E UiVjWk * Xijk
    */
    double lambda(const vector < vector < double > >& unew,
		  const vector < vector < double > >& vnew,
		  const vector < vector < double > >& wnew);

    /*
      function to print the tensor
      ostream is for cerr or cout
    */
    void print(ostream & stream);
    
    /*
      Resizes the tensor to it's already set dimensions
    */
    void resize();

    /*
      Resizes the tensor to the given dimensions
    */
    void resize(const vector<unsigned int>& Dims);

    /*
      Adds two tensors
      This tensor is updated with the answers
    */
    void add(const Tensor& t1);

    /*
      Returns the value at the specified tensor co-ordinates
      Co-ordinates are passed in as vector<int>
    */
    double at(const unsigned int c[]) const;

    /*
      Sets the value at the specified tensor co-ordinates
      Co-ordinates are pass in as vector<int>
    */
    void set(const vector<unsigned int>& c, const double& val);

    /*
      Prints dimensions of the tensor
      Used for debugging
    */
    void printDims(ostream& o);
    
    /*
      scales the tensor by a scalar
    */
    void scalarMul(const double lambda);

    vector < vector < vector < double > > > t;
    vector<unsigned int> dims; // contains lengths of each dimension
    unsigned int numDims;
};
