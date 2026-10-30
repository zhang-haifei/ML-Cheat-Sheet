#!/usr/bin/env python3
"""High-precision and finite-difference checks for numerical training details."""
import itertools
import json
import math
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import numpy as np


def softplus(z):return max(z,0)+math.log1p(math.exp(-abs(z)))


def verify():
    xor=[]
    for x1,x2 in itertools.product([0,1], repeat=2):
        h1=max(0,x1-x2);h2=max(0,x2-x1)
        assert (h1+h2>.5)==bool(x1!=x2)
        xor.append(dict(input=[x1,x2],hidden=[h1,h2],target=int(x1!=x2)))
    assert np.array_equal(np.mean([[1,0],[0,1]],axis=0),np.mean([[0,0],[1,1]],axis=0))
    eps=1e-6;gradient_errors=[]
    for z in [-4.,-1.,.2,2.,4.]:
        sigmoid=1/(1+math.exp(-z))
        gradient_errors.append(abs((softplus(z+eps)-softplus(z-eps))/(2*eps)-sigmoid))
        gradient_errors.append(abs((math.tanh(z+eps)-math.tanh(z-eps))/(2*eps)-(1-math.tanh(z)**2)))
    assert max(gradient_errors)<1e-8
    assert softplus(1000)==1000 and math.isfinite(softplus(-1000))
    # Read the margin plot at its two annotated reference positions.
    margin_losses = []
    for margin, expected_logistic in [(0, .693), (1, .313)]:
        hinge = max(0, 1-margin)
        logistic = softplus(-margin)
        assert hinge == 1-margin and round(logistic, 3) == expected_logistic
        margin_losses.append(dict(margin=margin, hinge=hinge, logistic=logistic))
    with localcontext() as context:
        context.prec=60
        lse=D(1001)+(D(1)+D(-1).exp()+D(-2).exp()).ln()
        ce=lse-D(1000)
        v=D(0);w=D(1);trajectory=[]
        for g in [D(2),D(-1)]:
            v=D('.9')*v+D('.1')*g*g
            w-=D('.1')*g/v.sqrt()
            trajectory.append(dict(v=str(v),w=str(w)))
    z=np.array([1000.,1001.,999.])
    def ce_loss(scores):
        a=scores.max()
        return a+np.log(np.exp(scores-a).sum())-scores[0]
    stable=ce_loss(z)
    assert abs(stable-float(ce))<1e-12
    probs=np.exp(z-z.max());probs/=probs.sum()
    analytic=probs-np.array([1,0,0])
    numerical=[]
    for i in range(3):
        offset=np.zeros(3);offset[i]=1e-4
        numerical.append((ce_loss(z+offset)-ce_loss(z-offset))/(2e-4))
    assert np.max(abs(analytic-numerical))<1e-8
    for logit,y in itertools.product([-1000.,-1.,0.,1.,1000.],[0,1]):
        bce=softplus(logit)-y*logit
        assert math.isfinite(bce) and bce>=0
    assert softplus(1000)-0*1000==1000
    weights=[F(1),F(2)];g=[F(1,5)]*2;scale=[F(1),F(1,10)]
    eta=penalty=F(1,10)
    coupled=[w-eta*d*(grad+penalty*w) for w,grad,d in zip(weights,g,scale)]
    decoupled=[(1-eta*penalty)*w-eta*d*grad for w,grad,d in zip(weights,g,scale)]
    assert coupled==[F('0.970'),F('1.996')] and decoupled==[F('.970'),F('1.978')]
    grad=np.array([3.,4.]);clipped=grad*2/np.linalg.norm(grad)
    assert np.allclose(clipped,[1.2,1.6]) and abs(np.linalg.norm(clipped)-2)<1e-14
    assert np.allclose(clipped/np.linalg.norm(clipped),grad/np.linalg.norm(grad))
    assert abs(np.linalg.norm(np.clip(grad,-2,2))-2*math.sqrt(2))<1e-14
    masked_outputs=[max(0,2*m1-2*m2) for m1,m2 in itertools.product([0,1],repeat=2)]
    assert sum(masked_outputs)/4==.5 and max(0,1-1)==0
    return dict(status='PASS',xor=xor,margin_losses=margin_losses,activation_derivative_max_error=max(gradient_errors),
                categorical_ce_decimal=str(ce),categorical_ce_stable=stable,
                categorical_gradient=analytic.tolist(),categorical_gradient_max_error=float(np.max(abs(analytic-numerical))),
                extreme_logits_BCE='finite at -1000 and 1000 for either target',rmsprop=trajectory,
                coupled_l2=list(map(float,coupled)),decoupled_decay=list(map(float,decoupled)),
                clipped_gradient=clipped.tolist(),dropout_mean=.5,deterministic_relu=0,
                transfer_head_parameters=16*3+3)


if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
