import numpy as np

dataSetName = "nltcs"
numQueryVariables = 8 

# load test data
data_test = numpy.loadtxt(open(dataSetName+".test.data","rb"),dtype=str,delimiter=",")

# compute 



# dimensions of test data
mt,nt = data_test.shape

#data_out = chararray((mt, nt))

for i in arange(mt):
	for j in arange(nt):
		if j < numQueryVariables:
			data_test[i][j] = '*'
		#else
			#data_test[i][j] = 

print data_test

savetxt(dataSetName+".libra.data", data_test, fmt='%c', delimiter=',')   # X is an array