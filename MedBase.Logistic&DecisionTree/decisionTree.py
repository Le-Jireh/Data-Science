import matplotlib.pyplot as plot
import pandas as pd
import numpy as np


# Download latest version
"""
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score
import kagglehub

path = kagglehub.dataset_download("itachi9604/disease-symptom-description-dataset")
df=pd.read_csv(file)
df.head()
df.dtypes()
X_train, X_test, Y_train, Y_test=train_test_split(x_encoded, y, random_state=42)
clf_dt=DecisionTreeClassifier(random_state=42)
AlphaPath=clf_dt.cost_complexity_pruning_path(X_train, Y_train)
ccp_alphas=AlphaPath.ccp_alphas
ccp_alphas=ccp_alphas[:-1]
AlphaLoopValues=[]
for ccp_alpha in ccp_alphas:
    clf_dt = DecisionTreeClassifier(random_state=0, ccp_alpha=ccp_alpha)
    scores=cross_val_score(clf_dt, X_train, Y_train, cv=5)
    AlphaLoopValues.append([ccp_alpha, np.mean(scores), np.std(scores)])
alphaResults=pd.DataFrame(AlphaLoopValues, columns=["alpha", "mean", "std"])
best_ccp=alphaResults[(alphaResults["alpha"] > ...) & (alphaResults["alpha"] < ...)]
best_ccp=float(best_ccp)
clf_dt_pruned=DecisionTreeClassifier(random_state=42, ccp_alpha=best_ccp)
clf_dt_pruned=clf_dt_pruned.fit(X_train, Y_train)
#plot confusion matrix sklearn
#accuracy
"""
#did the operation last more than 1 hour
DataFrame=pd.read_csv("diag_surg_complic.csv")
FormatedData=DataFrame["time_diag_surg"].apply(lambda x: 1 if x>60 else 0)
DataFrame["time_diag_surg"]=FormatedData

def entropy(data, OUTCOMES=0):
    outcomes=[list(data).count(1), list(data).count(0)] if (OUTCOMES==0) else [OUTCOMES[0],OUTCOMES[1]]
    positiveEnt=(-outcomes[0]/len(list(data)))*np.log2(outcomes[0]/len(list(data))) if outcomes[0]!=0 else 0
    negativeEnt=(-outcomes[1]/len(list(data)))*np.log2(outcomes[1]/len(list(data))) if outcomes[1]!=0 else 0
    return negativeEnt+positiveEnt

testingdt=[[0,0,0,1,0,1,1,1,1,0],[0,0,0,0,1,1,1,1,1,1] ]
def DecisionTree():
    df=[]
    for column in DataFrame.columns:
        TempList=DataFrame[column].tolist()
        df.append(TempList)
    del df[0]

    totalEntropy=entropy(df[0])
    infoGain=[]
    for column in df[0:]:
        posIndexRow=[index for (index, item) in enumerate(column) if item==1]
        negIndexRow=[index for (index, item) in enumerate(column) if item==0]
        outcomeControl=[]
        colEntropy=0
        for array in list([posIndexRow,negIndexRow]):
            _outControl=[0,0]
            for value in array:
                if df[0][value]==1:
                    _outControl[0]+=1
                else:
                    _outControl[1]+=1
            outcomeControl=_outControl
            colEntropy+=(len(array)/len(column))*entropy(array, outcomeControl)
        infoGain.append(totalEntropy-colEntropy)
    #totalEntropy=entropy(infoGain[index(max(infoGain))])
    print(max(infoGain))
DecisionTree()

#print(DataFrame.loc[0])
