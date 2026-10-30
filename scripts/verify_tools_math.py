#!/usr/bin/env python3
"""Enumerate finite probability spaces and recompute tools/math examples."""
import json
import math
from fractions import Fraction as F
from itertools import product


def mm(a,b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]


def verify():
    observations=[2,4,8,10]
    means=[sum(sample)/4 for sample in product(observations,repeat=4)]
    bootstrap_mean=sum(means)/len(means)
    bootstrap_variance=sum((x-bootstrap_mean)**2 for x in means)/len(means)
    assert bootstrap_mean==6 and bootstrap_variance==2.5
    assert sum(observations[i-1] for i in [1,1,3,4])/4==5.5
    omission=sum(2 not in sample for sample in product(observations,repeat=4))/256
    assert omission==(1-1/4)**4
    aic_bic=[dict(k=k,log_likelihood=ell,aic=2*k-2*ell,bic=k*math.log(100)-2*ell)
             for k,ell in [(3,-120),(5,-117)]]
    assert aic_bic[1]['aic']<aic_bic[0]['aic'] and aic_bic[0]['bic']<aic_bic[1]['bic']
    result=mm([[1,2,0],[0,1,3]],[[2,1],[1,2],[3,0]])
    assert result==[[4,5],[10,2]]
    assert 2*2-1*0==4 and math.hypot(3,-4)==5
    x=[[1,2],[3,4]];w=[.5,-.25];y=[1,0]
    def objective(weights):
        prediction_error=[sum(a*b for a,b in zip(row,weights))-yi for row,yi in zip(x,y)]
        return sum(e*e for e in prediction_error)/4
    gradient=[.25,0];eps=1e-5
    predictions=[sum(a*b for a,b in zip(row,w)) for row in x]
    residuals=[yi-p for yi,p in zip(y,predictions)]
    assert predictions==[0,.5] and residuals==[1,-.5]
    assert [-sum(row[j]*e for row,e in zip(x,residuals))/len(x) for j in range(2)]==gradient
    numerical=[]
    for i in range(2):
        plus=w[:];minus=w[:];plus[i]+=eps;minus[i]-=eps
        numerical.append((objective(plus)-objective(minus))/(2*eps))
    assert objective(w)==.3125
    assert max(abs(a-b) for a,b in zip(gradient,numerical))<1e-9
    fair=[sum(toss) for toss in product([0,1],repeat=2)]
    fair_mean=F(sum(fair),len(fair));fair_var=sum((v-fair_mean)**2 for v in fair)/4
    assert fair_mean==1 and fair_var==F(1,2)
    xs=[F(-1),F(0),F(1)];ys=[v*v for v in xs]
    cov=sum(a*b for a,b in zip(xs,ys))/3-sum(xs)/3*sum(ys)/3
    assert cov==0 and len(set(ys))>1
    posterior=F(9,10)*F(1,100)/(F(9,10)*F(1,100)+F(5,100)*F(99,100))
    assert posterior==F(2,13)
    pmf=[F(math.comb(4,k))*F(1,4)**k*F(3,4)**(4-k) for k in range(5)]
    assert sum(pmf)==1 and sum(k*p for k,p in enumerate(pmf))==1
    assert sum((k-1)**2*p for k,p in enumerate(pmf))==F(3,4)
    loss_errors=[0,-1,2]
    assert sum(abs(e) for e in loss_errors)/3==1
    assert F(sum(e*e for e in loss_errors),3)==F(5,3)
    chords=0
    for a,b,t in product(range(-3,4),range(-3,4),[F(0),F(1,4),F(1,2),F(3,4),F(1)]):
        assert (t*a+(1-t)*b)**2<=t*a*a+(1-t)*b*b
        chords+=1
    assert [4*t*(t*t-1) for t in [-1,0,1]]==[0,0,0]
    assert [12*t*t-4 for t in [-1,0,1]]==[8,-4,8]
    return dict(status='PASS',bootstrap_cases=len(means),bootstrap_mean=bootstrap_mean,
                bootstrap_variance=bootstrap_variance,omission_n4=omission,aic_bic=aic_bic,
                dimension_cells=[5**d for d in [1,2,5,10]],matrix_product=result,
                gradient=gradient,finite_difference_gradient=numerical,
                residuals=residuals,prediction_errors=[-e for e in residuals],
                two_coin_mean=str(fair_mean),two_coin_variance=str(fair_var),
                zero_covariance_dependent_example=str(cov),bayes_posterior=str(posterior),
                cross_entropy=[-math.log(.8),-math.log(.2)],convex_chords_checked=chords,
                bayes_error=.5*.1+.5*.4)


if __name__=='__main__':
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
