#!/usr/bin/env python3
"""Independently check multilabel metrics, online updates, OOB, CDF, SE and VIF."""
import itertools
import json
import math
from fractions import Fraction as F
import numpy as np


def verify():
    truth=np.array([[1,0,1,0],[0,1,0,0],[1,1,0,0]])
    prediction=np.array([[1,0,0,0],[0,1,0,1],[1,1,0,0]])
    error=truth!=prediction
    assert error.sum()==2 and F(int(error.sum()),error.size)==F(1,6)
    assert F(int(np.all(~error,axis=1).sum()),3)==F(1,3)
    tp=((truth==1)&(prediction==1)).sum(axis=0)
    fp=((truth==0)&(prediction==1)).sum(axis=0)
    fn=((truth==1)&(prediction==0)).sum(axis=0)
    f1=lambda t,p,n:F(2*int(t),2*int(t)+int(p)+int(n))
    macro=sum(f1(t,p,n) for t,p,n in zip(tp,fp,fn))/4
    micro=f1(tp.sum(),fp.sum(),fn.sum())
    samples=sum(f1(((y==1)&(p==1)).sum(),((y==0)&(p==1)).sum(),((y==1)&(p==0)).sum()) for y,p in zip(truth,prediction))/3
    assert tuple(map(int,[tp.sum(),fp.sum(),fn.sum()]))==(4,1,1)
    assert (macro,micro,samples)==(F(1,2),F(4,5),F(7,9))
    rare=np.eye(100,dtype=int)
    assert np.mean(rare!=0)==.01 and np.all(rare==0,axis=1).sum()==0
    assert np.linalg.matrix_rank(np.array([[1,2],[0,0]]))==1
    assert np.linalg.matrix_rank(np.eye(2))==2
    # Online order and every final signed margin, including the bias update.
    X=np.array([[2,1],[1,-1],[-1,2],[-2,-1]])
    y=np.array([1,-1,1,-1]);w=np.zeros(2,dtype=int);b=0;updates=[]
    for x,label in zip(X,y):
        score=int(w@x+b)
        if label*score<=0:
            w+=label*x;b+=int(label);updates.append({'score_before':score,'w':w.tolist(),'b':b})
    assert updates==[{'score_before':0,'w':[2,1],'b':1},{'score_before':2,'w':[1,2],'b':0}]
    signed=y*(X@w+b)
    assert np.array_equal(signed,[4,1,3,4])
    # Enumerate all 5^5 bootstrap sequences, without relying on an asymptotic claim.
    sequences=list(itertools.product(range(5),repeat=5))
    omitted=sum(0 not in draw for draw in sequences)
    expected_missing=sum(5-len(set(draw)) for draw in sequences)
    assert F(omitted,len(sequences))==F(4,5)**5==F(1024,3125)
    assert F(expected_missing,len(sequences))==F(1024,625)
    draws=np.array([[1,1,2,4,4],[2,3,3,5,5],[1,2,2,3,5],[1,3,4,4,5]])
    counts=np.array([np.bincount(draw,minlength=6)[1:] for draw in draws])
    assert np.all(counts.sum(axis=1)==5)
    assert np.array_equal(counts,[[2,1,0,2,0],[0,1,2,0,2],[1,2,1,0,1],[1,0,1,2,1]])
    assert np.array_equal(np.where(counts[:,3]==0)[0],[1,2])
    assert (F(4,5)+F(3,5))/2==F(7,10)
    logits=np.zeros((2,3));targets=np.array([[1,0,1],[0,1,0]])
    bce=np.logaddexp(0,logits)-targets*logits
    assert np.isclose(bce.sum(),6*math.log(2))
    assert np.isclose(bce.mean(),math.log(2))
    assert np.isclose(bce.sum(axis=1).mean(),3*math.log(2))
    residual=np.array([1,2,3])-np.array([1,1,5])
    assert np.array_equal(residual,[0,1,-2]) and np.isclose((residual**2).mean(),5/3)
    masses={F(0):F(3,4),F(1):F(1,4)}
    cdf=lambda t:sum(p for x,p in masses.items() if x<=t)
    left=lambda t:sum(p for x,p in masses.items() if x<t)
    assert cdf(0)==F(3,4) and left(0)==0
    assert cdf(1)-cdf(0)==F(1,4) and cdf(1)-left(0)==1
    uniform_cdf=lambda t:max(F(0),min(F(1),2*t))
    assert uniform_cdf(F(2,5))-uniform_cdf(F(1,10))==F(3,5)
    # Exact distribution of means from a two-point population: same first two moments as N(4,4).
    mean_variances={};tail_bounds={}
    for n in [1,4,16]:
        values=[F(2)+F(4*k,n) for k in range(n+1)]
        probs=[F(math.comb(n,k),2**n) for k in range(n+1)]
        mean=sum(p*x for p,x in zip(probs,values))
        variance=sum(p*(x-mean)**2 for p,x in zip(probs,values))
        assert mean==4 and variance==F(4,n)
        tail=sum(p for p,x in zip(probs,values) if abs(x-4)>1)
        assert tail<=variance
        biased_mse=sum(p*(F(n,n+1)*x-4)**2 for p,x in zip(probs,values))
        assert biased_mse==F(4*(n+4),(n+1)**2)
        mean_variances[n]=float(variance);tail_bounds[n]=[float(tail),float(variance)]
    sample=np.array([2,4,4,6]);assert sample.mean()==4
    assert np.isclose(sample.var(ddof=1),8/3)
    assert np.isclose(sample.std(ddof=1)/math.sqrt(4),math.sqrt(2/3))
    x1=np.array([-1,-1,1,1]);x2=np.array([-1,0,0,1])
    design=np.column_stack([np.ones(4),x1,x2])
    inv=np.linalg.inv(design.T@design)
    auxiliary=np.column_stack([np.ones(4),x2])
    fit=auxiliary@np.linalg.lstsq(auxiliary,x1,rcond=None)[0]
    r2=1-np.sum((x1-fit)**2)/np.sum((x1-x1.mean())**2)
    assert np.isclose(r2,.5) and np.isclose(1/(1-r2),2) and np.isclose(inv[1,1],.5)
    rescaled=design.copy();rescaled[:,1]*=10
    assert np.isclose(np.linalg.inv(rescaled.T@rescaled)[1,1],inv[1,1]/100)
    # Explicit logit transformation of the two calibration groups.
    scores=np.array([-math.log(9),math.log(9)])
    calibrated=1/(1+np.exp(-.5*scores))
    assert np.allclose(calibrated,[.25,.75])
    outcomes=np.array([0,0,0,1,0,1,1,1]);s=np.repeat(scores,4)
    p=np.repeat(calibrated,4)
    grad=np.array([np.dot(p-outcomes,s),(p-outcomes).sum()])/8
    assert np.allclose(grad,0,atol=1e-14)
    design_cal=np.column_stack([s,np.ones(8)])
    hessian=design_cal.T@((p*(1-p))[:,None]*design_cal)/8
    assert np.linalg.eigvalsh(hessian).min()>0
    return {'status':'PASS','multilabel':{'hamming':'1/6','subset_accuracy':'1/3','macro_f1':str(macro),'micro_f1':str(micro),'samples_f1':str(samples)},
            'perceptron_updates':updates,'final_signed_margins':signed.tolist(),
            'bootstrap_sequences':len(sequences),'oob_probability':str(F(omitted,len(sequences))),
            'expected_oob_count':str(F(expected_missing,len(sequences))),
            'uniform_interval_probability':'3/5','mean_variances':mean_variances,
            'chebyshev_tail_and_bound':tail_bounds,'sample_sd':float(sample.std(ddof=1)),
            'estimated_mean_se':float(sample.std(ddof=1)/2),'auxiliary_r2':float(r2),'vif':2,
            'coefficient_variance_over_noise':float(inv[1,1]),'calibrated_probabilities':calibrated.tolist(),
            'calibration_gradient_max_error':float(abs(grad).max())}


if __name__=='__main__':
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
