import matplotlib.pyplot as p
import math

points={89:7,66:5.4,78:6.6,111:7.4,44:4.8,77:6.4,80:7,66:5.6,109:7.3,76:6.4}
#points={8:4, 1:2, 36:1, 12:30}
#points={5:6 , 7:8, 13:12 , 12:14}
#points={1:4,3:2,4:1,5:0,8:0}

means=[0,0]
residuals=[[],[]]
SSR=[[],[]]
SSE=0
func=[]

#--Sommation function
def sigma(array):
    value=0
    for i in array:
        value+=i
    return value

#--Setting all the variables needed for the formulas
def getValues(coord):
    arrayX=list(coord.keys())
    arrayY=list(coord.values())

    #Getting the means
    for index in range(0,len(arrayX)):
        means[0]+=arrayX[index]
        means[1]+=arrayY[index]
    means[0]=means[0]/len(arrayX)
    means[1]=means[1]/len(arrayY)

    #Getting the residuals and SSR for X
    for item in arrayX:
        residuals[0].append(item-means[0])
        SSR[0].append((item-means[0])**2)
    #Getting the residuals and SSR for Y
    for item in arrayY:
        residuals[1].append(item-means[1])
        SSR[1].append((item-means[1])**2)


#--Pearson Coefficient
def eRatio(coord):
    numerator=[]

    for index in range(0, len(list(coord.keys()))):
        numerator.append(residuals[0][index]*residuals[1][index])
    denominator=sigma(SSR[0])*sigma(SSR[1])
    return sigma(numerator)/(math.sqrt(denominator))

#--Linear Line Function
def linearEquation(coord):
    arrayX=list(coord.keys())
    arrayX.sort()
    numeratorSlope=[]
    result=[]

    #-Finding Numerator=Deviation Product and Denominator
    for index in range(0, len(list(coord.keys()))):
        numeratorSlope.append(residuals[0][index]*residuals[1][index])
    denominatorSlope=sigma(SSR[0])

    slope=sigma(numeratorSlope)/denominatorSlope
    intersection=means[1]-m*means[0]
    result=[intersection, slope]
    X=[arrayX[0], arrayX[-1]]
    y=[result[0]+result[1]*X[0], result[0]+result[1]*X[1]]

    p.plot(x,y)
    return(result)

def modelError(coord, intersection ,slope ):
    arrayX=list(coord.keys())
    arrayY=list(coord.values())
    for index in range(0, len(arrayY)):
        SSE+=((intersection+slope*arrayX[index])-(arrayY[index]))**2
    SSE=SSE/len(arrayX)

for X, Y in points.items():
    p.scatter(X, Y)
getValues(points)
pearson=eRatio(points)

if abs(pearson)>0.35:
    func=linearEquation(points)
    equation="y={}{}{}x".format(func[0], "+" if func[1]>0 else "",func[1])
    modelError(points, func[0], func[1])
    if pearson>0:
        p.title(equation+"\npositive linear relationship: "+str((pearson*100))+"%"+str(SSE[1]))
    elif pearson<0:
        p.title(equation+"\n negative linear relationship: "+str(int(pearson*100))+"%")
else:
    p.title("The is not high positive correlation (greater than 35%)\n"+str(int(abs(pearson*100)))+"%")
p.show()
