#!/usr/bin/env python3
"""Recompute margins, clustering distances, covariance and projection examples."""
import json
import math
from fractions import Fraction as F
import numpy as np


def verify():
    positions=[(-2,1,-1),(-1,0,-1),(1,0,1),(2,1,1)]
    assert all(label*x>=1 for x,_,label in positions)
    scores=[F(6,5),F(2,5),F(0),F(-2,5)]
    slack=[max(F(0),1-s) for s in scores]
    assert slack==[F(0),F(3,5),F(1),F(7,5)]
    rbf=math.exp(-.5*(1**2+1**2));assert math.isclose(rbf,math.exp(-1))
    points=[F(0),F(1),F(4),F(5)];old=[F(0),F(5)]
    groups=[[x for x in points if min(range(2),key=lambda j:(x-old[j])**2)==i] for i in range(2)]
    centers=[sum(g)/len(g) for g in groups]
    initial=sum(min((x-c)**2 for c in old) for x in points)
    final=sum(min((x-c)**2 for c in centers) for x in points)
    assert centers==[F(1,2),F(9,2)] and initial==2 and final==1
    silhouette=[]
    for group in groups:
        other=next(g for g in groups if g is not group)
        for x in group:
            a=sum(abs(x-z) for z in group if z!=x)/(len(group)-1)
            b=sum(abs(x-z) for z in other)/len(other)
            silhouette.append((b-a)/max(a,b))
    average=sum(silhouette)/4
    assert silhouette==[F(7,9),F(5,7),F(5,7),F(7,9)] and average==F(47,63)
    data=np.array([[2,1],[1,2],[-1,-2],[-2,-1]],dtype=float)
    covariance=data.T@data/3
    assert np.allclose(covariance,[[10/3,8/3],[8/3,10/3]])
    eigenvalues,vectors=np.linalg.eigh(covariance)
    assert np.allclose(eigenvalues,[2/3,6])
    direction=np.array([1,1])/math.sqrt(2)
    assert np.allclose(covariance@direction,6*direction)
    projected=data@direction
    reconstructed=np.outer(projected,direction)
    squared=np.sum((data-reconstructed)**2,axis=1)
    assert np.allclose(squared,[.5]*4) and math.isclose(squared.sum(),2)
    ratios=eigenvalues[::-1]/eigenvalues.sum()
    assert np.allclose(ratios,[.9,.1])
    h=np.eye(4)-np.ones((4,4))/4
    assert np.allclose(h@h,h) and np.allclose(h@np.ones(4),0)
    kernel=np.exp(-.5*np.sum((data[:,None,:]-data[None,:,:])**2,axis=2))
    centered=h@kernel@h
    assert np.allclose(centered.sum(axis=0),0) and np.min(np.linalg.eigvalsh(kernel))>=-1e-12
    return dict(status='PASS',hard_margin_width=2,slack=[str(v) for v in slack],rbf=rbf,
                kmeans_centers=[str(c) for c in centers],kmeans_initial_sse=str(initial),kmeans_final_sse=str(final),
                silhouettes=[str(v) for v in silhouette],silhouette_mean=str(average),
                pca_covariance=covariance.tolist(),pca_eigenvalues=eigenvalues[::-1].tolist(),
                pca_explained_ratio=ratios.tolist(),first_point_projection=float(projected[0]),
                first_point_reconstruction=reconstructed[0].tolist(),reconstruction_sse=float(squared.sum()),
                centered_kernel_max_row_sum=float(abs(centered.sum(axis=0)).max()))


if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
