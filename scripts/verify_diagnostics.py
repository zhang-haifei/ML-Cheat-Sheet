#!/usr/bin/env python3
"""Check probability quality, decision cost, interval and clustering examples."""
import itertools
import json
import math
from fractions import Fraction as F
import numpy as np


def wilson(k, n, z=1.96):
    p=k/n;den=1+z*z/n
    center=(p+z*z/(2*n))/den
    radius=z*math.sqrt(p*(1-p)/n+z*z/(4*n*n))/den
    return center-radius, center+radius


def verify():
    y=np.array([0,0,0,1,0,1,1,1])
    pa=np.array([.1]*4+[.9]*4);pb=np.array([.25]*4+[.75]*4)
    results={}
    for name,p in [('A',pa),('B',pb)]:
        pos=p[y==1];neg=p[y==0]
        auc=sum((a>b)+.5*(a==b) for a in pos for b in neg)/16
        results[name]=dict(brier=float(np.mean((p-y)**2)),
                           logloss=float(-np.mean(y*np.log(p)+(1-y)*np.log(1-p))),
                           accuracy=float(np.mean((p>=.5)==y)),auc=float(auc))
        assert results[name]['accuracy']==.75 and auc==.75
    assert abs(results['A']['brier']-.21)<1e-14
    assert abs(results['B']['brier']-.1875)<1e-14
    # Exact expected loss: a non-extreme probability is optimal for random labels.
    q=F(1,4)
    for p in map(lambda k:F(k,20),range(21)):
        expected=q*(p-1)**2+(1-q)*p*p
        assert expected==(p-q)**2+q*(1-q)
    cfp,cfn=F(1),F(4);threshold=cfp/(cfp+cfn)
    for p in map(lambda k:F(k,100),range(101)):
        assert (cfp*(1-p)<=cfn*p)==(p>=threshold)
    tp,fn,fp,tn=18,12,7,63
    mcc=(tp*tn-fp*fn)/math.sqrt((tp+fp)*(tp+fn)*(tn+fp)*(tn+fn))
    actual=[1]*tp+[1]*fn+[0]*fp+[0]*tn
    predicted=[1]*tp+[0]*fn+[1]*fp+[0]*tn
    assert abs(mcc-np.corrcoef(actual,predicted)[0,1])<1e-14
    interval=wilson(81,100)
    assert np.allclose(interval,[.7222,.8749],atol=5e-5)
    # All possible success counts: intervals remain in [0,1] and have ordered endpoints.
    for n in [1,2,10,100]:
        for k in range(n+1):
            low,high=wilson(k,n)
            assert -1e-14<=low<=high<=1+1e-14
    coverages={}
    for p in [.01,.1,.5,.81,.99]:
        coverages[str(p)]=sum(math.comb(100,k)*p**k*(1-p)**(100-k)
                            for k in range(101) if wilson(k,100)[0]<=p<=wilson(k,100)[1])
    # Fraction arithmetic makes the epsilon-neighborhood convention unambiguous.
    points=list(map(F,['0','.1','.2','.3','.55','1.5','2.5','2.6','2.7','2.8']))
    epsilon=F('0.26');m=4
    neighborhoods=[{j for j,q in enumerate(points) if abs(p-q)<=epsilon} for p in points]
    core={i for i,neighbors in enumerate(neighborhoods) if len(neighbors)>=m}
    border={i for i in range(len(points)) if i not in core and neighborhoods[i]&core}
    noise=set(range(len(points)))-core-border
    assert core=={1,2,3,7,8} and border=={0,4,6,9} and noise=={5}
    assert neighborhoods[3]=={1,2,3,4}
    groups=[];unseen=core.copy()
    while unseen:
        group={unseen.pop()};frontier=group.copy()
        while frontier:
            i=frontier.pop();new=neighborhoods[i]&unseen
            group|=new;frontier|=new;unseen-=new
        groups.append(group|{i for i in border if neighborhoods[i]&group})
    assert {frozenset(g) for g in groups}=={frozenset(range(5)),frozenset(range(6,10))}
    pair_distances=[abs(a-b) for a,b in itertools.product([0,1],[4,6])]
    assert min(pair_distances)==3 and max(pair_distances)==6 and sum(pair_distances)/4==4.5
    return dict(status='PASS',probabilities=results,brier_properness='21 exact Fraction checks',
                cost_threshold=float(threshold),mcc=mcc,wilson_interval=interval,
                exact_binomial_coverage_of_approximate_intervals=coverages,
                dbscan_neighbor_counts=list(map(len,neighborhoods)),core_indices=sorted(core),
                border_indices=sorted(border),noise_indices=sorted(noise),
                cluster_indices=[sorted(g) for g in groups],
                linkage=dict(single=3,complete=6,average=4.5),
                search_fits=dict(grid_cv=3*4*5,grid_with_refit=61,nested=5*(3*8+1)))


if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
