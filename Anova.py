import math
"""
Observations=[[82,93,61,74,69,70,53],
            [71,71,62,94,85,78,66],
            [56,64,73,87,91,78,87]]
"""
Observations=[[75,70,50,65,80,65],
            [75,70,55,60,65,65],
            [90,70,75,85,80,65]]
#"""


def sigma(samples):
    value=0
    for i in samples:
        value+=i
    return value

def Anova(samples):
    SST,SSB,SSC,numOBS=SScalc(samples)

    print("SST:{}       SSB:{}      SSC:{}\n".format(SST, SSB+(SST-(SSB+SSC)), SSC))

    df=[numOBS-len(samples), len(samples)-1]
    MSB, MSC=SSB/df[0], SSC/df[1]
    print("MSB:{}       MSC:{}\n".format(MSB, MSC))

    f=MSC/MSB
    print("F-RATIO:{}".format(f))

def SScalc(samples):
    means=[]
    columnOBS=len(samples[0])
    deviations=[[],[],[],[]]
    SS=[]
    block=[]

    for index in range(0, len(samples)):
        means.append(sigma(samples[index])/columnOBS)

        for item in samples[index]:
            deviations[0].append(item)
            deviations[1].append((item-means[index])**2)

    means.append(sigma(means)/len(means))

    block.append([])
    for rows in range(0, columnOBS):
        block.append([])
        for index in range(0, len(samples)):
            block[rows].append(samples[index][rows])
        block[rows]=sigma(block[rows])/len(block[rows])
        deviations[-1].append(((block[rows]-means[-1])**2)*len(samples))

    for index in range(0,len(deviations[0])):
        deviations[0][index]=(deviations[0][index]-means[-1])**2

    SS.append(sigma(deviations[0]))
    SS.append(sigma(deviations[1]))

    for index in range(0, len(samples)):
        deviations[2].append(((means[index]-means[-1])**2)*columnOBS)
    SS.append(sigma(deviations[2]))

    for index in range(0, len(SS)):
        SS[index]=round(SS[index], 4)

    return SS[0], SS[-1], SS[2], len(deviations[0])


Anova(Observations)
