import matplotlib.pyplot as p
import numpy as np
import kagglehub
import pandas


df=pandas.read_csv("diag_surg_complic.csv")
samples=dict(zip(df["time_diag_surg"], df["bleeding"]))

def sigma(array):
    value=0
    for i in array:
        value+=i
    return value

def logitExponent(coord):
    indepValues=list(coord.keys())
    depValues=list(coord.values())

    mean=[0,0]
    for index in range(0,len(indepValues)):
        mean[0]+=indepValues[index]
        mean[1]+=depValues[index]
    mean[0]=mean[0]/len(indepValues)
    mean[1]=mean[1]/len(depValues)

    numerator=[]
    denominator=[]
    for index in range(0,len(indepValues)):
        residualX=indepValues[index]-mean[0]
        residualY=depValues[index]-mean[1]
        numerator.append(residualX*residualY)
        denominator.append(residualX**2)
    Coefficient=sigma(numerator)/sigma(denominator)
    Intersection=mean[1]-(mean[0]*Coefficient)
    return((Coefficient, Intersection))


Func=logitExponent(samples)
indexes=np.arange(0, 300, 0.5)
Values=1/(1+np.exp(-indexes*Func[0]+ Func[1]))
p.plot(indexes, Values)
p.show()
