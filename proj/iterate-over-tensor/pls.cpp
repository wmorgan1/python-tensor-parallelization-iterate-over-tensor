#include <cstdlib>
#include <cmath>
#include <iostream>
#include <fstream>
#include <string>
#include <cstring>
#include <vector>
#include <ctype.h>
#include <cstdio>
#include <unistd.h>
#include <omp.h>
#include <chrono>
#include <algorithm>
#include "tensor.h"



using namespace std;
using namespace std::chrono;

int d = 0;
int dn = 0;
int dls = 0;
//int drf = 0;
unsigned int totalThreads = 0;

/*
  function to print a vector
  ostream is for cerr or cout
*/
void printV(string v, const vector < double >& v1, ostream& stream)
{
    stream << v;
    int v1s = v1.size();

    for (int i = 0; i < v1s; i++)
    {
	stream << " " << v1[i];
    }
    stream << endl;
}

/*
  function to print a matrix, in the case of n component models
  ostream is for cerr or cout
*/
void printM(string v, const vector < vector < double > >& v1, ostream& stream)
{
    int x = v1.size(), y = v1[0].size();
    stream << v << endl;
    for (int i = 0; i < x; i++)
    {
	stream << "\t[";
	for (int j = 0; j < y; j++)
	{
	    if (j == 0)
	    {
		stream << v1[i][j];
	    }
	    else
	    {
		stream << ", " << v1[i][j];
	    }
	}
	stream << "]" << endl;
    }
}

/*
  takes two vectors and performs the dot/cross product
  v1 is the left vector, v2 is the right vector
  m is the matrix to 'return'
  lamda1/2 are the lamda values of v1 and v2, set as default value of 1 in case
  norms aren't applied in program run
*/
void VtoVmul(const vector < double >& v1, const vector < double >& v2,
	     vector < vector < double > >& m, const double& lamda1 = 1,
	     const double& lamda2 = 1)
{
    int v1s = v1.size(), v2s = v2.size();
    
    // size the matrix appropriately
    m.resize(v1s);
    for (int i = 0; i < v1s; i++)
    {
	m[i].resize(v2s);
    }

    for (int i = 0; i < v1s; i++)
    {
	for (int j = 0; j < v2s; j++)
	{
	    m[i][j] = lamda1 * v1[i] * lamda2 * v2[j];
	}
    }
}

/*
  tensor product of a matrix and a vector, returns the tensor approximation
  m is the matrix
  v is the vector
  t is the tensor to 'return'
  lamda is the lamda value of the vector, set as default value of 1 in case
  norms aren't applied in program run
*/
void MtoVmul(const vector < vector < double > >& m, const vector < double >& v,
	     Tensor& t,
	     const double& lamda = 1)
{
    unsigned int x = m.size(), y = m[0].size(), z = v.size();
    cout << "numDims = " << t.numDims << endl;
    vector <unsigned int> c (t.numDims, 0);

    //for (int i = 0; i < x; i++)
    for (c[0] = 0; c[0] < x; c[0] = c[0] + 1)
    {
	//for (int j = 0; j < y; j++)
	for (c[1] = 0; c[1] < y; c[1]++)
	{
	    //for (int k = 0; k < z; k++)
	    for (c[2] = 0; c[2] < z; c[2]++)
	    {
		// t[i][[j][k] = m[i][j] * v[k] * lamda
		t.set(c, m[c[0]][c[1]] * v[c[2]] * lamda);
	    }
	}
    }
}

/*
  helper method for LS
  Calculates E UliVliWli where l != a
  uold, vold, wold are self explanatory
  i is the index of u in question
  j is the index of v in question
  w is the index of w in question
  a is the component in question of u,v,w
  A is the total number of components
  returns a double

  This function is NOT parallelized, as all available threads should be busy in
  LS.
*/
double helper(const vector < vector < double > >& uold,
	    const vector < vector < double > >& vold,
	    const vector < vector < double > >& wold,
	    const int i, const int j, const int k, const int a,
	    const int A)
{
    double result = 0;

    for (int it = 0; it < A; it++)
    {
	if (it != a)
	{
	    result += uold[it][i] * vold[it][j] * wold[it][k];
	}
    }
    return result;
}
	    
/*
  Least Squares method
  u/v/wnew are the new component matrices to be filled
  
  tensor is the tensor
  dim is the dimension being help constant
*/
void LS(vector < vector < double > >& unew,
	vector < vector < double > >& vnew,
	vector < vector < double > >& wnew,
	const vector < vector < double > >& uold,
	const vector < vector < double > >& vold,
	const vector < vector < double > >& wold,
	const Tensor& tensor)
{
    double tensorAt = 0;    // tensor.at(c) - helper
    double top[3] = {};
    unsigned int approximations = uold.size(); // component vectors per component
    unsigned int uSize = uold[0].size(), vSize = vold[0].size(), wSize = wold[0].size();
    unsigned int c[3] = {};
    //high_resolution_clock::time_point l1, l2;    
    vector < vector < vector < double > > > ucopy;
    vector < vector < vector < double > > > vcopy;
    vector < vector < vector < double > > > wcopy;

    /*if (dls)
    {
	cout << "LS" << endl;
	printM("\tunew:", unew, cerr);
	printM("\tuold:", uold, cerr);
	printM("\tvnew:", vold, cerr);
	printM("\tvold:", vnew, cerr);
	printM("\twnew:", wnew, cerr);
	printM("\twold:", wold, cerr);
    }*/

    // set up copy vectors for each thread
#pragma omp parallel num_threads(3)
    {
	int thread = omp_get_thread_num();
	if (thread == 0)
	{
	    ucopy.resize(totalThreads);
	    for (int i = 0; i < totalThreads; i++)
	    {
		ucopy[i].resize(approximations);
		for (int j = 0; j < approximations; j++)
		{
		    ucopy[i][j].resize(uSize, 0);
		}
	    }
	}
	else if (thread == 1)
	{
	    vcopy.resize(totalThreads);
	    for (int i = 0; i < totalThreads; i++)
	    {
		vcopy[i].resize(approximations);
		for (int j = 0; j < approximations; j++)
		{
		    vcopy[i][j].resize(vSize, 0);
		}
	    }
	}
	else if (thread == 2)
	{
	    wcopy.resize(totalThreads);
	    for (int i = 0; i < totalThreads; i++)
	    {
		wcopy[i].resize(approximations);
		for (int j = 0; j < approximations; j++)
		{
		    wcopy[i][j].resize(wSize, 0);
		}
	    }
	}
    }

    // set all entries in unew, vnew, wnew to 0
    // these vectors are used as in-place accumlators
#pragma omp parallel num_threads(3)
    {
	int thread = omp_get_thread_num();
	if (thread == 0)
	{
	    for (unsigned int a = 0; a < approximations; a++)
	    {
		fill(unew[a].begin(), unew[a].end(), 0);
	    }
	}
	else if (thread == 1)
	{
	    for (unsigned int a = 0; a < approximations; a++)
	    {
		fill(vnew[a].begin(), vnew[a].end(), 0);
	    }
	}
	else if (thread == 2)
	{
	    for (unsigned int a = 0; a < approximations; a++)
	    {
		fill(wnew[a].begin(), wnew[a].end(), 0);
	    }
	}
    }

    //l1 =  high_resolution_clock::now();
    // go thru each component vector
    for (unsigned int a = 0; a < approximations; a++)
    {
	
	//
	//
	// calculate the top values
	//
	//
#pragma omp parallel for private(c, top, tensorAt)
	for (unsigned int i = 0; i < tensor.dims[0]; i++)
	{
	    int thread = omp_get_thread_num();
	    for (unsigned int j = 0; j < tensor.dims[1]; j++)
	    {
		for (unsigned int k = 0; k < tensor.dims[2]; k++)
		{
		    // tensor index
		    c[0] = i; c[1] = j; c[2] = k;

		    // tensor.at(c) - UliVljWlk, to take into account all components
		    /*tensorAt = tensor.at(c) - 
		      helper(uold, vold, wold, i, j, k, a, approximations);*/
		    
		    /*if (dls)
		    {
#pragma omp critical
			{
			    cout << "tensor.at(c) = " << tensor.at(c) << endl;
			    cout << "helper = " 
				 << helper(uold, vold, wold, i, j, k, a, approximations)
				 << endl;
			    cout << "tensorAt = " << tensorAt << endl << endl;
			}
			}*/
		    // calculations over u
		    top[0] = vold[a][j] * wold[a][k] * tensor.at(c);
		    ucopy[thread][a][i] += top[0];
		    /*top[0] = vold[a][j] * wold[a][k] * tensor.at(c);
		    #pragma omp atomic
		      unew[a][i] += top[0];*/

		    // calculations over v
		    top[1] = uold[a][i] * wold[a][k] * tensor.at(c);
		    vcopy[thread][a][j] += top[1];
		    /*top[1] = uold[a][i] * wold[a][k] * tensor.at(c);
                    #pragma omp atomic
		      vnew[a][j] += top[1];*/

		    // calculations over w
		    top[2]= uold[a][i] * vold[a][j] * tensor.at(c);
		    wcopy[thread][a][k] += top[2];
                    /*top[2] = uold[a][i] * vold[a][j] * tensor.at(c);
		    #pragma omp atomic
		    wnew[a][k] += top[2];*/
		}
	    }
	}
    }
    /*l2 =  high_resolution_clock::now();
    auto lduration = duration_cast<microseconds>( l2 - l1).count();
    if (dls) 
    {
	cout << "LS loop time = " << lduration << endl;
	}*/
    
    // copy results into component vectors
#pragma omp parallel num_threads(3)
    {
	int thread = omp_get_thread_num();
	if (thread == 0)
	{
	    for (int a = 0; a < approximations; a++)
	    {
		for (int i = 0; i < uSize; i++)
		{
		    for (int j = 0; j < totalThreads; j++)
		    {
			unew[a][i] += ucopy[j][a][i];
		    }
		}
	    }
	}
	else if (thread == 1)
	{
	    for (int a = 0; a < approximations; a++)
	    {
		for (int i = 0; i < vSize; i++)
		{
		    for (int j = 0; j < totalThreads; j++)
		    {
			vnew[a][i] += vcopy[j][a][i];
		    }
		}
	    }

	}
	else if (thread == 2)
	{
	    for (int a = 0; a < approximations; a++)
	    {
		for (int i = 0; i < wSize; i++)
		{
		    for (int j = 0; j < totalThreads; j++)
		    {
			wnew[a][i] += wcopy[j][a][i];
		    }
		}
	    }

	}
    }
}


/*
  This function normalizes a matrix of vector approximation
  each approximation is a row in the matrix, for better cacheing
  results are returned in a vector
*/
void normalize(vector < vector < double > >& v1)
{
    if (dn)
    {
	cout << "normalize " << endl;
	printM("", v1, cerr);
    }

    int numApproximations = v1.size();
    int approximationSize = v1[0].size();
    double temp = 0, x = 0;;

    // i for the rows, j to iterate thru each row
#pragma omp parallel for private(x)
    for (int i = 0; i < numApproximations; i++)
    {
	// x = (E u^2)^(1/2)
	x = 0;
	for (int j = 0; j < approximationSize; j++)
	{
	    /*
	     * removing pow from use saved about 10k microseconds in a 50x50x50
	     * tensor, pow is thread-safe, so this makes sense
	     */
	    x += v1[i][j] * v1[i][j];
	    //temp += pow(v1[i][j], 2);
	    //x[i] += pow(v1[i][j], 2);
	}
	if (dn)
	{
	    cout << "\tx summed = " << x << endl;
	}
	x = sqrt(x);
	if (dn)
	{
	    cout << "\tsqrt(x) = " << x << endl;
	}
	for (int j = 0; j < approximationSize; j++)
	{
	    v1[i][j] = v1[i][j] / x;
	}
    }
    return;
}

/*
  This function finds the distance between two vectors
  v1 is u/v/wold and v2 is u/v/wnew
  v1s is the length of v1
  v2s is the length of v2
  result is returned
*/
double distance(const vector < double >& v1, const vector < double >& v2)
{
    double sum = 0;
    double temp = 0;
    int v1s = v1.size(), v2s = v2.size();
    
    if (v1s != v2s) throw 1;

//#pragma omp parallel for shared(v1,v2,temp) reduction(+:sum)
    for (int i = 0; i < v1s; i++)
    {
	//errno = 0;
	temp = v1[i] - v2[i];

	/*
	 * removing pow from use saved about 10k microseconds in a 50x50x50
	 * tensor, pow is thread-safe, so this makes sense
	 */
	sum += temp * temp;
	//sum += pow(temp, 2);
	//if (errno != 0) throw 2;
    }

    return sum;
}

int main(int argc, char* argv[])
{
    bool tensorPrint = false, vectorPrint = false;
    float sigma = 0;
    int it = 0, c = 1, parsedArg;
    int x = 0, y = 0, z = 0;
    totalThreads = max(atoi(getenv("OMP_NUM_THREADS")), 1);
    Tensor tensor;
    vector < vector < double > > unew, uold, vnew, vold, wnew, wold;
    high_resolution_clock::time_point t1, t2, l1, l2, v1, v2, d1, d2, i1, i2, la1, la2;
    double duration, lduration, vduration, dduration, iduration, laduration;
    double lambda = 1;

    //cout << "getenv: " << getenv("OMP_NUM_THREADS") << endl;
    //cout << "atoi(getenv): " << atoi(getenv("OMP_NUM_THREADS")) << endl;

#pragma omp parallel
    {
	printf("Hello from thread %03d of %03d\n",omp_get_thread_num(), totalThreads);
    }

    // no cli args
    if (argc == 1)
    {
	cout << "Format: ./als -s <sigma> -f <input file path>"
	     << " <other parameters>" << endl;
	cout << "\t-s <float value> :: distance between approximation vectors "
	     << "required to stop the algorithm" << endl;
	cout << "\t-n :: if you want the vectors to be normalized on every "
	     << "iteration. Defaults to False." << endl;
	cout << "\t-c <1..n> :: the number of components you want in the "
	     << "approximation. Defaults to 1." << endl;
	cout << "\t-d <all/d/dn/dls/drf> :: all debug statements OR main OR "
	     << "normalize OR LS OR readFile. There can be several -d IE"
	     << " -d d -d dn. Defaults to none." << endl;
	cout << "\t-f <filename> :: the path to the input file" << endl;
	cout << "\t-t :: if you want to print out the tensor made from the"
	     << "approximation vectors." << endl;
	cout << "\t-v :: if you want to print out the appoximation vectors."
	     << endl;
	exit(1);
    }
    else
    {
	/*
	  The following adapted from 
	  https://www.gnu.org/software/libc/manual/html_node/Example-of-Getopt.html
	*/
	while ((parsedArg = getopt (argc, argv, "s:nc:d:f:tv")) != -1)
	{
	    switch (parsedArg)
	    {
	    case 's':
		sigma = atof(optarg);
		break;
	    case 'n':
		break;
	    case 'c':
		c = atoi(optarg);
		break;
	    case 'd':
		if (!strcmp("all", optarg))
		{
		    d = true;
		    dn = true;
		    dls = true;
		    //drf = true;
		}
		else if (!strcmp("d", optarg))
		{
		    d = true;
		}
		else if (!strcmp("dn", optarg))
		{
		    dn = true;
		}
		else if (!strcmp("dls", optarg))
		{
		    dls = true;
		}
		else if (!strcmp("drf", optarg))
		{
		    //drf = true;
		}
		else
		{
		    cout << "Error parsing -d flag. Program exit." << endl;
		    exit(1);
		}
		break;
	    case 'f':
	    {
		//string temp(optarg);
		tensor = Tensor(optarg);
		x = tensor.dims[0];
		y = tensor.dims[1];
		z = tensor.dims[2];
		break;
	    }
	    case 't':
	    {
		tensorPrint = true;
		break;
	    }
	    case 'v':
	    {
		vectorPrint = true;
		break;
	    }
	    case '?':
		if (optopt == 'c' || optopt == 's' || optopt == 'd' || optopt == 'f')
		    fprintf (stderr, "Option -%c requires an argument.\n", optopt);
		else if (isprint (optopt))
		    fprintf (stderr, "Unknown option `-%c'.\n", optopt);
		else
		    fprintf (stderr,
			     "Unknown option character `\\x%x'.\n",
			     optopt);
		exit(1);
	    default:
		abort ();
	    }
	}
	if (sigma == 0)
	{
	    cout << "A sigma value is required. Program Exit." << endl;
	    exit(1);
	}
	else if (x == 0)
	{
	    cout << "An input fie was not given and is required. Program Exit."
		 << endl;
	    exit(1);
	}
    }

    if (d)
    {
	cerr << "sigma = " << sigma << endl;
	cerr << "components = " << c << endl;
	cerr << "d = " << d << endl;
	cerr << "dn = " << dn << endl;
	cerr << "dls = " << dls << endl;
	cerr << "tensor dim[0] = " << tensor.dims[0] << endl;
	cerr << "tensor dim[1] = " << tensor.dims[1] << endl;
	cerr << "tensor dim[2] = " << tensor.dims[2] << endl;
    }


    if (d)
    {
	//printT(tensor, x, y, z, cerr);
	//tensor.print(cerr);
    }
    

    /*
      size the vector approximations and put in the data
      treat vectors as rows of a matrix
      [0] = aprox 1
      [1] = aprox 2
      [n] = aprox n
    */
    // each row is 1 component, size vectors for proper number of components
    unew.resize(c);
    uold.resize(c);
    vnew.resize(c);
    vold.resize(c);
    wnew.resize(c);
    wold.resize(c);
    // size each row for proper dimensions
    for (int i = 0; i < c; i++)
    {
	unew[i].resize(x,1);
	uold[i].resize(x,1);
	vnew[i].resize(y,1);
	vold[i].resize(y,1);
	wnew[i].resize(z,1);
	wold[i].resize(z,1);
    }

    // perform first normalization of approximation vectors
    /*try
    {
	lamdaU = normalize(unew);
	lamdaV = normalize(vnew);
	lamdaW = normalize(wnew);
    }
    catch (int e)
    {
	if (e == 2)
	{
	    cout << "Error in normalize : error in pow" << endl;
	    exit(1);
	}
	else if (e == 3)
	{
	    cout << "Error in normalize : error in sqrt" << endl;
	    exit(1);
	}
	}*/
    normalize(unew);
    normalize(vnew);
    normalize(wnew);

    if (d)
    {
	printM("unew: ", unew, cerr);
	printM("vnew: ", vnew, cerr);
	printM("wnew: ", wnew, cerr);
    }


    /*
     *
     * BEGIN TIMING HERE
     *
     */
    cout << "Timing has begun" << endl;
    t1 = high_resolution_clock::now();


    while (true)
    {
	i1 = high_resolution_clock::now();
	it += 1;

	if (d)
	{
	    cout << "main: in while loop" << endl;
	}

	// Step 1: The 'new' approximations become old
	v1 = high_resolution_clock::now();
	uold = unew;
	vold = vnew;
	wold = wnew;
	v2 = high_resolution_clock::now();
	vduration = duration_cast<microseconds>( v2 - v1).count();
	if (it < 10) cout << "VC time = " << vduration << endl;

	// Step 2: Find new approximations, iterate over tensor once
	/*
	 * iterating over tensor once cut down run time by about 68%
	 * see LS for more detail
	 */
	l1 = high_resolution_clock::now();
	LS(unew, vnew, wnew, uold, vold, wold, tensor);
	normalize(unew);
	normalize(vnew);
	normalize(wnew);
	l2 = high_resolution_clock::now();
	lduration = duration_cast<microseconds>( l2 - l1).count();
	if (it < 10) cout << "LS time = " << lduration << endl;

	if (d)
	{
	    cout << "main: back from LS" << endl;
	    printM("unew: ", unew, cerr);
	    printM("vnew: ", vnew, cerr);
	    printM("wnew: ", wnew, cerr);
	}

	try
	{
	    if (d)
	    {
		cout << "\tu dist = " << distance(uold[0], unew[0]) << endl;
		cout << "\tv dist = " << distance(vold[0], vnew[0]) << endl;
		cout << "\tw dist = " << distance(wold[0], wnew[0]) << endl;
		cout << "\tdistance = " << distance(uold[0], unew[0]) +
		    distance(vold[0], vnew[0]) +
		    distance(wold[0], wnew[0]) << endl;
		cout << "ITERATION = " << it << endl;
	    }

	    
	    // Step 4: compute the distance of the vectors and compare to the
	    // sigma value. Break the loop, if applicable
	    d1 = high_resolution_clock::now();
	    int breakCount = 0;
#pragma omp parallel for shared(breakCount)
	    for (int i = 0; i < c; i++)
	    {
		if ((distance(uold[i], unew[i]) + distance(vold[i], vnew[i]) +
		     distance(wold[i], wnew[i])) < sigma)
		{
		    #pragma omp atomic
		    breakCount++;
		}
	    }
	    if (breakCount == c) break;
	    d2 = high_resolution_clock::now();
	    dduration = duration_cast<microseconds>(d2 - d1).count();
	    if (it < 10) cout << "dist time = " << dduration << endl;
	}
	catch (int e)
	{
	    if (e == 1)
	    {
		cout << "Error in distance :: vector sizes do not match"
		     << endl;
		exit(1);
	    }
	    else if (e == 2)
	    {
		cout << "Error in distance :: pow fn error" << endl;
		exit(1);
	    }
	}
	i2 = high_resolution_clock::now();
	iduration = duration_cast<microseconds>( i2 - i1).count();
	if (it < 10) cout << "it time = " << iduration << endl;
    }

    /*
     *
     * END TIMING HERE
     *
     */
    t2 = high_resolution_clock::now();
    cout << "Timing has ended" << endl;
    duration = double(duration_cast<microseconds>( t2 - t1).count() / 1000000.0);
    cout << "Time elapsed: " << duration << endl;
    cout << "ITERATIONS = " << it << endl;

    // calculate distance between tensor and approximation
    lambda = tensor.lambda(unew,vnew,wnew);
    cout.precision(9);
    cout << "Lambda = " << lambda << endl;
    cout << "Distance = " << tensor.distance(unew, vnew, wnew, 
					     tensor.lambda(unew, vnew, wnew)) << endl;


    if (vectorPrint)
    {
	printM("END unew: ", unew, cout);
	printM("END vnew: ", vnew, cout);
	printM("END wnew: ", wnew, cout);
    }

    if (tensorPrint)
    {
	vector < vector < double > > m;
	Tensor temp(tensor.dims, tensor.numDims), finalT(tensor.dims, tensor.numDims);
	// Calculate each uvw tensor and add them all together
	for (int i = 0; i < c; i++)
	{
	    VtoVmul(unew[i], vnew[i], m);
	    MtoVmul(m, wnew[i], temp);
	    finalT.add(temp);
	}
	finalT.scalarMul(lambda);
	finalT.print(cout);
    }
    return 0;
}
