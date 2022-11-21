#include "tensor.h"

int drf = 0;
int dta = 0;

Tensor::Tensor()
{
    return;
}

Tensor::Tensor(char* filename)
{
    ifstream file;
    unsigned int it = 0; //x = 0, y = 0, z = 0, it = 0, i, j, k;
    double val;
    string line;
    unsigned int * loc;

    unsigned int drf = 0;
    if (drf) cout << "Tensor::Tensor(file)" << endl;
    file.open(filename, ios::in);

    if (file.is_open())
    {
	// read in data
	while(getline(file, line))
	{
	    if (drf) cout << line << endl;


	    char* split = new char[line.size() + 1];
	    copy(line.begin(), line.end(), split);
	    split[line.size()] = '\0';

	    // line that contains numDims
	    if (it == 1)
	    {
		numDims = atoi(strtok(split, " "));
		//dims = new unsigned int[numDims];
		dims.resize(numDims);
		loc = new unsigned int[numDims];
	    }
	    // line that contains tensor dimensions
	    else if (it == 2)
	    {
		// line format: x y z etc
		dims[0] = atoi(strtok(split, " "));
		if (drf) cerr << "\t0 dim = " << dims[0] << endl;
		
		for (unsigned int i = 1; i < numDims; i++)
		{
		    dims[i] = atoi(strtok(NULL, " "));
		    if (drf) cerr << "\t" << i << " dim = " << dims[i] << endl;
		}
		resize();
		/*x = atoi(strtok(split, " "));
		y = atoi(strtok(NULL, " "));
		z = atoi(strtok(NULL, " "));
		if (drf)
		{
		    cerr << "\tx = " << x << endl;
		    cerr << "\ty = " << y << endl;
		    cerr << "\tz = " << z << endl;
		}
		resizeT(tensor, x, y, z);*/
		//printT(tensor, x, y, z, cerr);
	    }
	    // lines that contain tensor values
	    else if (it > 3)
	    {
		// line format: i j k val
		loc[0] = atoi(strtok(split, " "));
		if (drf) cerr << "\tt0 = " << loc[0] << endl;
		for (unsigned int i = 1; i < numDims; i++)
		{
		    loc[i] = atoi(strtok(NULL, " "));
		    if (drf) cerr << "\tt" << i << " = " << loc[i] << endl;
		}
		val = atof(strtok(NULL, " "));
		if (drf) cerr << "\tval = " << val << endl;
		/*
		  i = atoi(strtok(split, " "));
		  j = atoi(strtok(NULL, " "));
		  k = atoi(strtok(NULL, " "));
		  val = atof(strtok(NULL, " "));
		  if (drf)
		  {
		  cout << "\ti = " << i << endl;
		  cout << "\tj = " << j << endl;
		  cout << "\tk = " << k << endl;
		  cout << "\tval = " << val << endl;
		  }
		*/
		t[loc[0]][loc[1]][loc[2]] = val;
	    }
	    delete [] split;
	    it++;
	}	
	delete [] loc;	
    }
    else
    {
	// error opening file
	cerr << "Error opening input file. Program exit." << endl;
	exit(1);
    }
}

Tensor::Tensor(const vector<unsigned int>& Dims, const unsigned int NumDims)
{
    dims = Dims;
    numDims = NumDims;
    resize();
}

Tensor::Tensor(const Tensor& obj)
{
    t = obj.t;
    dims = obj.dims;
    numDims = obj.numDims;
}

Tensor::~Tensor()
{
}

double Tensor::distance(const vector < vector < double > >& unew,
			const vector < vector < double > >& vnew,
			const vector < vector < double > >& wnew,
			const double lambda)
{
    int A = unew.size(); // number of approximations
    unsigned int c[3] = {};
    double retVal = 0, temp = 0;
    for (int a = 0; a < A; a++)
    {
// parallelized just because i can
#pragma omp parallel for private(c, temp) reduction(+:retVal)
	for (unsigned int i = 0; i < dims[0]; i++)
	{
	    c[0] = i;
	    for (unsigned int j = 0; j < dims[1]; j++)
	    {
		c[1] = j;
		for (unsigned int k = 0; k < dims[2]; k++)
		{
		    c[2] = k;
		    temp =  (lambda * unew[a][i] * vnew[a][j] * wnew[a][k]) - at(c);
		    retVal += temp * temp;
		}
	    }
	}
    }
    return (retVal / (dims[0] * dims[1] * dims[2]));
    //return retVal;
}

double Tensor::lambda(const vector < vector < double > >& unew,
	      const vector < vector < double > >& vnew,
	      const vector < vector < double > >& wnew)
{
    double lambda = 0;
    unsigned int c[3] = {};
    int I = dims[0], J = dims[1], K = dims[2];
#pragma omp parallel for private(c) reduction(+:lambda)
    for (unsigned int i = 0; i < I; i++)
    {
	c[0] = i;
	for (unsigned int j = 0; j < J; j++)
	{
	    c[1] = j;
	    for (unsigned int k = 0; k < K; k++)
	    {
		c[2] = k;
		lambda += unew[0][i] * vnew[0][j] * wnew[0][k] * at(c);
	    }
	}
    }
    return lambda;
}  
		
void Tensor::print(ostream& stream)
{
    stream << "tensor: " << endl;
    for (unsigned int i = 0; i < dims[0]; i++)
    {
	stream << "\t[";
	for (unsigned int j = 0; j < dims[1]; j++)
	{
	    stream << "[";
	    for (unsigned int k = 0; k < dims[2]; k++)
	    {
		if (k == 0)
		{
		    stream << t[i][j][k];
		}
		else
		{
		    stream << ", " << t[i][j][k];
		}
	    }
	    if (j == dims[1] - 1)
	    {
		stream << "]";
	    }
	    else
	    {
		stream << "], ";
	    }
	}
	stream << "]" << endl;
    }    
}

void Tensor::resize()
{
    t.resize(dims[0]);
    for (unsigned int i = 0; i < dims[0]; i++)
    {
	t[i].resize(dims[1]);
	for ( unsigned int j = 0; j < dims[1]; j++)
	{
	    t[i][j].resize(dims[2]);
	}
    }
}

void Tensor::resize(const vector<unsigned int>& Dims)
{
    t.resize(Dims[0]);
    for (unsigned int i = 0; i < Dims[0]; i++)
    {
	t[i].resize(Dims[1]);
	for ( unsigned int j = 0; j < Dims[1]; j++)
	{
	    t[i][j].resize(Dims[2]);
	}
    }
}

void Tensor::add(const Tensor& t1)
{
    if (dta) cout << "Tensor::add" << endl;
    if (numDims != t1.numDims)
    {
	cerr << "Error in Tensor::add :: tensors have different number of"
	     << "dimensions." << endl;
	return;
    }
    for (unsigned int i = 0; i < numDims; i++)
    {
	if (dims[i] != t1.dims[i])
	{
	    cerr << "Err in Tensor::add :: tensors dimension " << i
		 << " are not equal." << endl;
	    return;
	}
    }
    for (unsigned int i = 0; i < dims[0]; i++)
    {
	for (unsigned int j = 0; j < dims[1]; j++)
	{
	    for (unsigned int k = 0; k < dims[2]; k++)
	    {
		t[i][j][k] += t1.t[i][j][k];
	    }
	}
    }
}

double Tensor::at(const unsigned int c[]) const
{
    return t[c[0]][c[1]][c[2]];
}

void Tensor::set(const vector<unsigned int>& c, const double& val)
{
    t[c[0]][c[1]][c[2]] = val;
}

void Tensor::printDims(ostream & o)
{
    for (size_t i = 0; i < numDims; i++)
    {
	o << "\t" << i << " dim = " << dims[i] << endl;
    }
}

void Tensor::scalarMul(const double lambda)
{
    int I = dims[0], J = dims[1], K = dims[2];
#pragma omp parallel for
    for (int i = 0; i < I; i++)
    {
	for (int j = 0; j < J; j++)
	{
	    for (int k = 0; k < K; k++)
	    {
		t[i][j][k] *= lambda;
	    }
	}
    }
}
