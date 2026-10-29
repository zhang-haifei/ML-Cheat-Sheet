#!/usr/bin/env python3
"""Recompute linear model, shrinkage, probability and neighbor examples."""
import json
import math
from fractions import Fraction as F


def verify():
    xs=[F(0),F(1),F(2)];ys=[F(1),F(2),F(2)]
    mx=sum(xs)/3;my=sum(ys)/3
    slope=sum((x-mx)*(y-my) for x,y in zip(xs,ys))/sum((x-mx)**2 for x in xs)
    intercept=my-slope*mx
    preds=[intercept+slope*x for x in xs];errors=[p-y for p,y in zip(preds,ys)]
    rss=sum(e*e for e in errors)
    assert slope==F(1,2) and intercept==F(7,6) and rss==F(1,6)
    assert sum(errors)==0 and sum(x*e for x,e in zip(xs,errors))==0
    assert [1+F(3,2)*x-F(1,2)*x*x for x in xs]==ys
    lam=F(1,2)
    shrink=[]
    for z in [F(0),F(3,10),F(2),F(-2)]:
        ridge=z/(1+lam)
        lasso=(1 if z>=0 else -1)*max(abs(z)-lam,0)
        # Derivative/subgradient optimality checks, independent of plots.
        assert ridge-z+lam*ridge==0
        if lasso:
            assert lasso-z+lam*(1 if lasso>0 else -1)==0
        else:
            assert abs(z)<=lam
        shrink.append(dict(z=str(z),ridge=str(ridge),lasso=str(lasso)))
    score=math.log(3);prob=1/(1+math.exp(-score))
    assert math.isclose(prob,.75) and prob>=.5 and prob<.8
    scores=[0,math.log(2),math.log(3)];exps=[math.exp(s) for s in scores]
    softmax=[e/sum(exps) for e in exps]
    assert all(math.isclose(a,b) for a,b in zip(softmax,[1/6,1/3,1/2]))
    # Logistic derivative by central difference at a nonzero score.
    def loss(s):return math.log1p(math.exp(s))-s
    eps=1e-5
    derivative=(loss(score+eps)-loss(score-eps))/(2*eps)
    assert abs(derivative-(prob-1))<1e-9
    query=F(9,5);train=[(F(0),0),(F(1),0),(F(3),1),(F(5),1)]
    nearest=sorted(train,key=lambda row:abs(row[0]-query))[:3]
    assert [int(x) for x,_ in nearest]==[1,3,0]
    assert sum(y for _,y in nearest)==1
    # Minkowski example exposes the old y_1-for-every-component indexing error.
    a=[1,4];b=[3,1];diff=[abs(x-y) for x,y in zip(a,b)]
    assert sum(diff)==5 and sum(d*d for d in diff)==13 and max(diff)==3
    return dict(status='PASS',ols_slope=str(slope),ols_intercept=str(intercept),
                ols_predictions=[str(p) for p in preds],residuals=[str(e) for e in errors],
                rss=str(rss),training_mse=str(rss/3),scalar_shrinkage=shrink,
                logistic_probability=prob,logistic_derivative=derivative,softmax=softmax,
                nearest_positions=[int(x) for x,_ in nearest],knn_prediction=0,
                minkowski=dict(l1=5,l2=math.sqrt(13),linf=3))


if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
