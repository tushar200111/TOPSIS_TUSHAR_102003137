import numpy as np
import pandas as pd
import math as math
import operator
import sys

def main():
    if(len(sys.argv)!=5):
        print("Incorrect Number of Arguments")
        exit(0)
    
    dataset=pd.read_csv(sys.argv[1])
    weights=[float(w) for w in sys.argv[2].split(',')]
    impacts=[i for i in sys.argv[3].split(',')]

    if(len(weights)!=dataset.shape[1]-1):
        print("No of weights are not correct")
        exit(0)
    
    if(len(impacts)!=dataset.shape[1]-1):
        print("No of impacts are not correct")
        exit(0)

    #values will be copied one by one to new dataset
    dataset1 = dataset.iloc[:,1:].values

    try:
        weights=[w/sum(weights) for w in weights]
    except:
        print("Exception 1 raised")

    for i in range(dataset1.shape[1]):
        den=math.sqrt(sum(dataset1[:,i]**2))
        for j in range(dataset1.shape[0]):
            try:
                dataset1[j][i] = (dataset1[j][i])/den
            except:
                print("Exception 2 raised")
    
    for i in range(len(weights)):
        dataset1[:,i]=dataset1[:,i]*weights[i]

    ibv=[]
    iwv=[]
    for i in range(len(impacts)):
        if(impacts[i]=='+'):
            ibv.append(max(dataset1[:,i]))
            iwv.append(min(dataset1[:,i]))
        else:
            ibv.append(min(dataset1[:,i]))
            iwv.append(max(dataset1[:,i]))

    ebestd=[]
    eworstd=[]
    for i in range(dataset1.shape[0]):
        sum1=0
        sum2=0
        for j in range(dataset1.shape[1]):
            sum1=sum1+(dataset1[i,j] - ibv[j])**2
            sum1=math.sqrt(sum1)
            sum2=sum2+(dataset1[i,j] - iwv[j])**2
            sum2=math.sqrt(sum2)
        ebestd.append(sum1)
        eworstd.append(sum2)
    
    per=[]
    for i in range(len(ebestd)):
        try:
            per.append(eworstd[i]/(ebestd[i] + eworstd[i]))
        except:
            print("Exception 3 raised")
    
    matrix=[]
    for i in range(len(per)):
        matrix.append([i+1, dataset.iloc[i,0],per[i],0])
    
    matrix.sort(key=operator.itemgetter(2))

    for i in range(len(matrix)):
        matrix[i][3] = len(matrix)-i

    matrix.sort(key=operator.itemgetter(0))

    # dataset['S+']=ebestd
    # dataset['S-']=eworstd

    dataset['Performance']=per

    rank=[]
    for i in range(len(matrix)):
        rank.append(matrix[i][3])

    dataset['Rank']=rank
    of=sys.argv[4]
    dataset.to_csv(of) 
   # print("Finished")
                
if __name__=="__main__":
    main()







    
    
    







