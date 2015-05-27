from numpy import *
from os import listdir
import operator


def createDataSet():
    group = array([[1.0,1.1],[1.0,1.0],[0,2],[0,0.1]])
    labels = ['A','A','B','B']
    return group, labels
'''
group
labels
'''
def classify0(inX,dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    diffMat = tile(inX, (dataSetSize,1)) - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    sortedDistIndicies = distances.argsort()
    classCount={}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel,0) + 1
    sortedClassCount = sorted(classCount.iteritems(),
                              key=operator.itemgetter(1),reverse=True)
    return sortedClassCount[0][0]
'''
import kNN
group, labels = kNN.createDataSet()
kNN.classify0([0,0], group, labels, 3)
'''
# 2-2
def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())         #get the number of lines in the file
    returnMat = zeros((numberOfLines,3))        #prepare matrix to return
    classLabelVector = []                       #prepare labels return   
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index,:] = listFromLine[0:3]
        classLabelVector.append(int(listFromLine[-1]))
        index += 1
    return returnMat,classLabelVector
    
'''


excute:

reload(kNN)
datingDataMat,datingLabels = kNN.file2matrix('datingTestSet.txt')

and 

import matplotlib
import matplotlib.pyplot as plt
fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(datingDataMat[:,1],datingDataMat[:,2])
plt.show()

and

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(datingDataMat[:,1],datingDataMat[:,2],15.0*array(datingLabels),15.0*array(datingLabels))
plt.show()

'''
# 2-3

def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros(shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - tile(minVals,(m,1))
    normDataSet = normDataSet/tile(ranges,(m,1))
    return normDataSet, ranges,minVals

'''
excute:

reload(kNN)
normMat,ranges,minVals = kNN.autoNorm(datingDataMat)
normMat


'''
# 2-4 test
def datingClassTest():
   hoRatio = 0.10
   datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
   normMat,ranges,minVals = autoNorm(datingDataMat)
   m = normMat.shape[0]
   numTestVecs = int(m*hoRatio)
   errorCount = 0.0
   for i in range(numTestVecs):
       classifierResult = classify0(normMat[i,:],normMat[numTestVecs:m,:],datingLabels[numTestVecs:m],3)
       print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, datingLabels[i])
       if(classifierResult != datingLabels[i]): errorCount += 1.0
   print "the total error rate is: %f" % (errorCount/float(numTestVecs))
   print "error count: %d" % errorCount
'''
reload(kNN)
kNN.datingClassTest()
'''
# 2-5

def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(raw_input(\
        "percenttage of time spent playing video games?"))
    ffMiles = float(raw_input("frequent filer miles earned per year?"))
    iceCream = float(raw_input("liters of ice create consumed per year?"))
    datingDataMat,datingLabels = file2matrix('datingTestSet2.txt')
    normMat, ranges,minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles, percentTats, iceCream])
    classifierResult = classify0((inArr-minVals)/ranges,normMat,datingLabels,3)
    print "You will brobably like this person: ",resultList[classifierResult - 1]
    
def img2vector(filename):
    returnVect = zeros((1,1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0,32*i+j] = int(lineStr[j])
    return returnVect

'''
2-6
 Hand writing identify test
'''
def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('trainingDigits')
    m = len(trainingFileList)
    trainingMat = zeros((m,1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        if(fileNameStr == ".DS_Store"):continue  # ignore .DS_Store file
        # print "fileNameStr="+fileNameStr
        fileStr = fileNameStr.split('.')[0]
        # print "fileStr="+fileStr
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i,:] = img2vector('trainingDigits/%s' % fileNameStr)
    testFileList = listdir('testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        if(fileNameStr == ".DS_Store"):continue  # ignore .DS_Store file
        # print "fileNameStr="+fileNameStr
        fileStr = fileNameStr.split('.')[0]
        # print "fileStr="+fileStr
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('testDigits/%s' % fileNameStr)
        classifierResult = classify0(vectorUnderTest, trainingMat,hwLabels,3)
        print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)
        if(classifierResult != classNumStr): errorCount += 1.0
    print "\nthe total number of errors is: %d" % errorCount
    print "\nthe total error rate is: %f" % (errorCount/float(mTest))

    