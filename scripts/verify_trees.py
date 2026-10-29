#!/usr/bin/env python3
"""Independent finite calculations for tree, Bayes and ensemble examples."""
import json
import math
from fractions import Fraction as F
from itertools import product


def rss(values):
    mean=sum(values)/len(values)
    return sum((v-mean)**2 for v in values)


def gini(labels):
    p=F(sum(labels),len(labels));return 1-p*p-(1-p)**2


def verify():
    labels=[1,1,1,0,0,0,0,1]
    candidates=[(i-F(1,2),F(i,8)*gini(labels[:i])+F(8-i,8)*gini(labels[i:])) for i in range(1,8)]
    best=min(candidates,key=lambda p:p[1])
    assert best==(F(5,2),F(1,5)) and gini(labels)-best[1]==F(3,10)
    ys=list(map(F,[1,1,5,7]));splits=[rss(ys[:i])+rss(ys[i:]) for i in range(1,4)]
    assert rss(ys)==27 and splits.index(min(splits))==1 and min(splits)==2
    scores=[F(3,5)*F(4,5)*F(1,2),F(2,5)*F(1,5)*F(1,4)]
    posterior=scores[0]/sum(scores)
    assert posterior==F(12,13)
    # Exact integration of theta^2*(1-theta) and theta^3*(1-theta).
    normalizer=F(1,3)-F(1,4);first_moment=F(1,4)-F(1,5)
    assert first_moment/normalizer==F(3,5)
    probabilities=[F(49,100),F(49,100),F(99,100)]
    assert sum(p>=F(1,2) for p in probabilities)==1
    assert sum(probabilities)/3>F(1,2)
    variance=[]
    for count in [10,100]:variance.append(.2+.8/count)
    # Correlated predictions U+2*V_i: var=5, covariance=1; exact 16-case check for B=3.
    ensemble=[F(u)+F(2,3)*sum(vs) for u,*vs in product([-1,1],repeat=4)]
    enum_variance=sum(v*v for v in ensemble)/len(ensemble)
    assert math.isclose(float(enum_variance),5*(.2+.8/3))
    targets=list(map(F,[0,2,4]));before=[F(2)]*3;weak=[F(-2),F(1),F(1)]
    step=F(1,1000)
    def half_squared(y,p):return (p-y)**2/2
    negative_gradient=[-(half_squared(y,p+step)-half_squared(y,p-step))/(2*step) for y,p in zip(targets,before)]
    assert negative_gradient==list(map(F,[-2,0,2]))
    full_squared_gradient=[-((p+step-y)**2-(p-step-y)**2)/(2*step) for y,p in zip(targets,before)]
    assert full_squared_gradient==[2*g for g in negative_gradient]
    after=[p+F(1,2)*h for p,h in zip(before,weak)]
    mse_before=sum((p-y)**2 for p,y in zip(before,targets))/3
    mse_after=sum((p-y)**2 for p,y in zip(after,targets))/3
    assert after==list(map(F,[1,F(5,2),F(5,2)])) and mse_before==F(8,3) and mse_after==F(7,6)
    error=.25;alpha=.5*math.log((1-error)/error)
    labels=[-1,1,1,-1];preds=[-1,1,1,1]
    raw=[.25*math.exp(-alpha*y*h) for y,h in zip(labels,preds)]
    weights=[w/sum(raw) for w in raw]
    assert all(math.isclose(a,b) for a,b in zip(weights,[1/6,1/6,1/6,.5]))
    assert math.isclose(sum(weights),1) and math.isclose(sum(raw),math.sqrt(3)/2)
    return dict(status='PASS',classification_best_threshold=str(best[0]),weighted_gini=str(best[1]),
                gini_drop='3/10',regression_parent_rss='27',regression_split_rss=[str(v) for v in splits],
                naive_bayes_posterior=str(posterior),beta_posterior_mean=str(first_moment/normalizer),
                mean_probability=str(sum(probabilities)/3),ensemble_variance=variance,
                enumerated_correlated_variance=float(enum_variance),gradient_boosting_before=str(mse_before),
                half_squared_negative_gradient=[str(g) for g in negative_gradient],
                full_squared_negative_gradient=[str(g) for g in full_squared_gradient],
                gradient_boosting_after=str(mse_after),adaboost_alpha=alpha,adaboost_weights=weights)


if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
