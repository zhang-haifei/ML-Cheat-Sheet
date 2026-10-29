#!/usr/bin/env python3
"""Verify selection bias, robust summaries, contingency tables and Tomek links."""
import itertools
import json
from fractions import Fraction as F
import numpy as np


def verify():
    totals=[50,50];values=[20,80];rates=[F(4,5),F(1,5)]
    retained=[n*p for n,p in zip(totals,rates)]
    population=F(sum(n*x for n,x in zip(totals,values)),sum(totals))
    complete=sum(n*x for n,x in zip(retained,values))/sum(retained)
    adjusted=sum(F(n,sum(totals))*x for n,x in zip(totals,values))
    assert retained==[40,10] and population==50 and complete==32 and adjusted==50
    sample=np.array([1,2,2,3,100])
    q1,q3=np.quantile(sample,[.25,.75],method='linear')
    assert q1==2 and q3==3
    fences=[q1-1.5*(q3-q1),q3+1.5*(q3-q1)]
    assert fences==[.5,4.5]
    assert sample.mean()==21.6 and np.median(sample)==2 and np.clip(sample,None,5).mean()==2.6
    variances=[]
    for n1 in [50,10,1]:
        binary=np.array([1]*n1+[0]*(100-n1));p=F(n1,100)
        assert abs(binary.var()-float(p*(1-p)))<1e-14
        variances.append(float(p*(1-p)))
    observed=[[12,8],[4,16]]
    expected=[[F(sum(row)*sum(observed[k][j] for k in range(2)),40) for j in range(2)] for row in observed]
    chi2=sum((F(observed[i][j])-expected[i][j])**2/expected[i][j] for i,j in itertools.product(range(2),repeat=2))
    assert expected==[[8,12],[8,12]] and chi2==F(20,3)
    xor_tables=[]
    for feature in [0,1]:
        table=np.zeros((2,2),dtype=int)
        for x1,x2 in itertools.product([0,1],repeat=2):
            table[[x1,x2][feature],x1^x2]+=1
        assert np.array_equal(table,np.ones((2,2)))
        xor_tables.append(table.tolist())
    points=list(map(F,['0','1','1.1','3','3.2']));labels=['A','A','B','B','B']
    nearest=[]
    for i,x in enumerate(points):
        neighbors=sorted((abs(x-z),j) for j,z in enumerate(points) if i!=j)
        assert neighbors[0][0]<neighbors[1][0]
        nearest.append(neighbors[0][1])
    links=[(i,j) for i,j in enumerate(nearest) if i<j and nearest[j]==i and labels[i]!=labels[j]]
    assert nearest==[1,2,1,4,3] and links==[(1,2)]
    remaining=[label for i,label in enumerate(labels) if i!=2]
    assert remaining.count('A')==remaining.count('B')==2
    # Distinguish three formulas misnamed in source cards.
    tp,fn,fp=18,12,7
    assert F(tp,tp+fn)==F(3,5) and F(tp,tp+fp)==F(18,25)
    logits=np.zeros(3);independent_sigmoid=1/(1+np.exp(-logits));softmax=np.exp(logits)/np.exp(logits).sum()
    assert independent_sigmoid.sum()==1.5 and np.isclose(softmax.sum(),1)
    return dict(status='PASS',population_mean=float(population),complete_case_mean=float(complete),
                adjusted_mean=float(adjusted),quartiles=[float(q1),float(q3)],fences=fences,
                outlier_mean=float(sample.mean()),outlier_median=float(np.median(sample)),
                clipped_mean=float(np.clip(sample,None,5).mean()),binary_variances=variances,
                expected_counts=[[float(e) for e in row] for row in expected],chi2=str(chi2),
                xor_contingency_tables=xor_tables,nearest_indices=nearest,tomek_links=links,
                forward_candidate_sets=4+3,forward_fivefold_fits=35,
                TPR=float(F(tp,tp+fn)),precision=float(F(tp,tp+fp)),
                sigmoid_sum=float(independent_sigmoid.sum()),softmax_sum=float(softmax.sum()))


if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
