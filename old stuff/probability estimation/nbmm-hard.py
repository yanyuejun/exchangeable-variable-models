import numpy as np
from operator import mul
import operator
import scipy
from collections import Counter
from scipy.cluster.hierarchy import linkage, fcluster
from scipy.spatial.distance import squareform

# class representing one NB mixture component
class NBComponent:

	ms = array([])

	# part is the partition in form of an array [0, 0, 1, 0, 1, 2, 3, 1] indicating column membership on (here: 4) partitions
	def __init__(self, data, weights):
		
		# dimensions of data
		m,n = data.shape

		self.ms = zeros(n, dtype=float)
		for i in arange(n):
			self.ms[i] = (float(sum(weights[data[:,i]==1])) + 1.0) / (float(sum(weights[data[:,i]<=1])) + 2.0)

		#print self.ms

	# returns the probability of one particular configuration (here: conditional probability)
	def prob(self, data_point):

		currProb = 1.0
		for i in arange(len(data_point)):
			currProb = currProb * ((1.0-data_point[i])*(1.0-self.ms[i])+data_point[i]*self.ms[i])
		return currProb

	# returns the probability of one particular configuration (here: conditional probability)
	def probLog(self, data_point):

		currProb = 0.0
		for i in arange(len(data_point)):
			currProb = currProb + log(((1.0-data_point[i])*(1.0-self.ms[i])+data_point[i]*self.ms[i]))
		return currProb


# the name of the data set	
dataSetName = "webkb"

# load the training data
data = numpy.loadtxt(open(dataSetName+".ts.data","rb"),dtype=int,delimiter=",")

# get the dimensions of the trainging data matrix
m,n = data.shape

# compute the priors from the training data: prob(x=1)
ms = zeros(n,dtype=float)
for i in arange(n):
	ms[i] = mean(data[:,i])

# the number of mixture components (latent variable values)
numComponents = 5

initData = np.random.randint(2, size=(m, n))
initData = array_split(initData, numComponents)

# comp are the mixture components
comp = array([])
# initialization of the components
for j in arange(numComponents):
	# create a mixture component for the ith row having value '0'
	compTemp = NBComponent(initData[j], ones(m, dtype=float))
	#savetxt(dataSetName+str(j)+".shuffle.data", data, fmt='%c', delimiter=',')   # X is an array
	comp = append(comp, compTemp)

# class probabilities initialized to uniform probabilities
latentProb = ones(numComponents, dtype=float)
latentProb = latentProb/sum(latentProb)

print latentProb

for c in arange(10):
	print "EM iteration: ",c
	# iterate over the training samples (all of them) an compute probability
	compPr = zeros(numComponents, dtype=float)
	weights = zeros((numComponents, m), dtype=float)
	# the E step
	for i in arange(m):
		probSum = 0.0
		pr = zeros(numComponents, dtype=float)
		for j in arange(numComponents):
			# probability (unnormalized) of the data point i for the component j
			pr[j] = log(latentProb[j]) + comp[j].probLog(data[i])
		
		#print " "
		#print weights
		#print probSum
		maxProb = argmax(pr)

		for j in arange(numComponents):

			# normalize the probabilities
			if maxProb == j:
				weights[j][i] = 1.0
			else:
				weights[j][i] = 0.0
			# aggregate the normalized probabilities
			compPr[j] += weights[j][i]
			#print weights[j][i],

		#print " ---- "

	# the M step
	# update the class priors
	latentProb = compPr/sum(compPr)

	# update the parameters of the mixture components
	# comp are the mixture components
	comp = array([])
	# run inference in the components and compute the new probabilities
	for j in arange(numComponents):
		# this indicates that we are using the fully exchangeable model
		#assign = zeros(n,dtype=int)
		# create a mixture component for the ith row having value '0'
		compTemp = NBComponent(data, weights[j])
		comp = append(comp, compTemp)
		#print weights[j]

	print latentProb
	#print "---"




# load test data
data_test = numpy.loadtxt(open(dataSetName+".test.data","rb"),dtype=int,delimiter=",")

# dimensions of test data
mt,nt = data_test.shape

# compute the log-likelihood of the test data for the partial exchangeable model
testCounter = 0
sumn = 0.0
for x in data_test:
	testCounter += 1
	prob = 0.0
	for j in arange(numComponents):
		if latentProb[j] > 0.0:
			prob = prob + latentProb[j] * comp[j].prob(x)
	sumn = sumn + log(prob)

print testCounter
print "Latent variable Naive Bayes: ",sumn / len(data_test)

