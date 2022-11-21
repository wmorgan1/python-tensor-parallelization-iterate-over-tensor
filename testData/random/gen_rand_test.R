# R script to generate random tensor test cases
#
# Usage:
#
#    Rscript dim1 dim2 ... dimn filename
#
# Generates tensor of dimensions (dim1, dim2, ..., dimn) and writes
# the tensor to the specified filename.  One-component decomposition is
# written to stdout.
#
# Example:
#
#    Rscript 4 5 6 t_4-5-6.dat
#
# Creates a random tensor of dimension (4, 5, 6), writes the tensor 
# to the file "t_4-5-6.dat" and writes the one-component decomposition
# to stdout.

#
# step(): step through the vector of indices; indices are treated
#    like an odomoter, with first elmenet stepping fastest.
# 
# Example: Suppose indx = (2, 4, 1, 1) and dims = (4, 4, ,4 ,4);
#   indx <- step(indx, dims) updates indx to (3, 4, 1, 1)
#   indx <- step(indx, dims) updates indx to (4, 4, 1, 1)
#   indx <- step(indx, dims) updates indx to (1, 1, 2, 1)

step <- function(indx, dims) {
  n <- length(dims)
  for (i in 1:n) {
    if (indx[i] == dims[i]) {
      indx[i] <- 1
      next
    } else {
      indx[i] <- indx[i] + 1
      break
    }
  }
  return(indx)
}

#
# write_tensor(): write the tensor in SNL-format to a specified file.
#

write_tensor <- function(t, filename) {
  dims <- dim(t)
  n <- length(dims)
  tv <- vec(t)
  indx <- rep(1, n)   # indx initialized to (1, 1, ..., 1)

  # Write SNL-format header 
  write("sptensor", file=filename)
  write(n, file=filename, append=TRUE)
  write(dims, file=filename, append=TRUE)
  write(length(tv), file=filename, append=TRUE)

  # Write the data
  for (x in tv) {
    pindx <- indx
    for (i in 1:length(pindx)) {
      pindx[i] <- pindx[i] - 1
    }
    cat(format(pindx), x, "\n",  file=filename, append=TRUE)
    indx <- step(indx, dims)
  }
}

#
# gen_rand_test(): generate a random test case of specified size;
#   write tensor to specified output file.  One-component tensor
#   decomposition is written to stdout.
#   

gen_rand_test <- function(dims, filename) {
  t <- rand_tensor(dims)
  write_tensor(t, filename)
  ddims <- rep(1, length(dims))
  td <- tucker(t, ddims)
  return(td$U)
}


#
# script begins here
#

# requires rTensor library
library(rTensor)

# command line argument processing
args <- commandArgs(TRUE)
nargs <- length(args)
dims <- as.integer(args[1])
for (i in 2:(nargs-1)) {
  dims <- c(dims, as.integer(args[i]))
}
fname <- args[nargs]

# call test generation function
gen_rand_test(dims, fname)