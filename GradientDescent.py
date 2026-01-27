import matplotlib.pyplot as plt
import statistics as stats

points={0.5:1.4, 2.3:1.9, 2.9:3.2}#{89:7,66:5.4,78:6.6,111:7.4,44:4.8,77:6.4,80:7,66:5.6,109:7.3,76:6.4}

def GradientDescent(dataset, learningRate=.01, descents=100,):
    intercept=0
    slope=1
    interStep=-1
    slopeStep=-1
    samplesNum=len(dataset.items())
    plt.scatter(dataset.keys(), dataset.values())
    #while abs(interStep)>0.001 and abs(slopeStep)>0.001:
            #print(intercept, slope)
    for i in range(descents):
            derivInt=0
            derivSlope=0
            for x,y in dataset.items():
                derivInt+=-2*(y-(intercept+slope*x))
                derivSlope+=-2*x*(y-(intercept+slope*x))
            interStep=derivInt*learningRate
            slopeStep=derivSlope*learningRate
            intercept-=interStep
            slope-=slopeStep
    regrSlope, regrInter=stats.linear_regression(dataset.keys(), dataset.values())
    plt.plot((0, max(dataset.keys())+5), (intercept,((max(dataset.keys())+5)*slope)+intercept))
    plt.plot((0, max(dataset.keys())+5), (regrInter,((max(dataset.keys())+5)*regrSlope)+regrInter), linewidth=5)
    plt.show()
    return(slope, intercept)

print(GradientDescent(points, 0.01))
