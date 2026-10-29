#!/usr/bin/env python3
"""Verify convolution, pooling, shape, sharing and normalization examples."""
import json
import math
import numpy as np


def verify():
    x=np.array([[1,2,0,1],[0,1,3,2],[2,0,1,1],[1,2,1,0]],dtype=float)
    kernel=np.array([[1,0],[0,-1]],dtype=float)
    windows=np.lib.stride_tricks.sliding_window_view(x,(2,2))
    out=np.einsum('ijuv,uv->ij',windows,kernel)
    expected=np.array([[0,-1,-2],[0,0,2],[0,-1,1]])
    assert np.array_equal(out,expected)
    # All nine positions contribute to each shared kernel gradient.
    analytic=np.einsum('ij,ijuv->uv',out,windows)
    numerical=np.zeros_like(kernel);eps=1e-5
    def loss(k):return .5*np.sum(np.einsum('ijuv,uv->ij',windows,k)**2)
    for index in np.ndindex(kernel.shape):
        plus=kernel.copy();minus=kernel.copy();plus[index]+=eps;minus[index]-=eps
        numerical[index]=(loss(plus)-loss(minus))/(2*eps)
    assert np.max(abs(analytic-numerical))<1e-8
    pool_input=np.array([[1,3,2,0],[4,6,1,5],[2,1,8,7],[0,3,4,9]],dtype=float)
    blocks=pool_input.reshape(2,2,2,2).transpose(0,2,1,3)
    maxima=blocks.max(axis=(2,3));averages=blocks.mean(axis=(2,3))
    assert np.array_equal(maxima,[[6,5],[3,9]])
    assert np.array_equal(averages,[[3.5,2],[1.5,7]])
    shape_cases=[(4,2,0,1,1,3),(32,3,1,1,1,32),(7,3,1,2,1,4),(7,3,0,1,2,3)]
    for length,k,p,s,d,expected in shape_cases:
        assert math.floor((length+2*p-d*(k-1)-1)/s)+1==expected
    r,j=1,1;fields=[]
    for k,s in [(3,1),(2,2),(3,1)]:
        r+=(k-1)*j;j*=s;fields.append([r,j])
    assert fields==[[3,1],[4,2],[8,2]]
    conv_params=16*(3*3*3+1);head_params=16*10+10
    assert conv_params==448 and head_params==170 and conv_params+head_params==618
    epsilon=1e-5;values=np.array([1.,3.]);normalized=(values-values.mean())/np.sqrt(values.var()+epsilon)
    assert np.allclose(normalized,np.array([-1,1])/math.sqrt(1+epsilon))
    # Global average preserves batch/channel axes, independently reducing space.
    activations=np.arange(8*16*16*16).reshape(8,16,16,16)
    gap=activations.mean(axis=(2,3));assert gap.shape==(8,16)
    assert gap[0,0]==np.arange(256).mean()
    # One NCHW tensor, two different reduction groups; neither reduces all axes.
    tensor=np.array([[[[1.,3.]],[[10.,14.]]],[[[5.,7.]],[[18.,22.]]]])
    bn_axes=(0,2,3);ln_axes=(1,2,3)
    bn_mean=tensor.mean(axis=bn_axes);bn_var=tensor.var(axis=bn_axes)
    ln_mean=tensor.mean(axis=ln_axes);ln_var=tensor.var(axis=ln_axes)
    assert np.array_equal(bn_mean,[4,16]) and np.array_equal(bn_var,[5,20])
    assert np.array_equal(ln_mean,[7,13]) and np.array_equal(ln_var,[27.5,51.5])
    def normalize(values,axes):
        return (values-values.mean(axis=axes,keepdims=True))/np.sqrt(values.var(axis=axes,keepdims=True)+epsilon)
    changed=tensor.copy();changed[1,0]+=100
    assert not np.allclose(normalize(tensor,bn_axes)[0],normalize(changed,bn_axes)[0])
    assert np.array_equal(normalize(tensor,ln_axes)[0],normalize(changed,ln_axes)[0])
    assert np.allclose(normalize(tensor+np.array([2.,-7.])[None,:,None,None],bn_axes),normalize(tensor,bn_axes))
    group_size=tensor.shape[0]*tensor.shape[2]*tensor.shape[3]
    unbiased=tensor.var(axis=bn_axes,ddof=1)
    assert np.allclose(unbiased,bn_var*group_size/(group_size-1))
    return dict(status='PASS',convolution=out.tolist(),shared_kernel_gradient=analytic.tolist(),
                max_gradient_difference=float(abs(analytic-numerical).max()),
                max_pool=maxima.tolist(),average_pool=averages.tolist(),shape_cases=shape_cases,
                receptive_fields=fields,parameters=dict(shared_small=5,unshared_small=45,dense_small=153,
                conv=conv_params,head=head_params,total=conv_params+head_params),
                tensor_elements=8*3*32*32,bn_example=normalized.tolist(),gap_shape=list(gap.shape),
                normalization_axes=dict(bn_mean=bn_mean.tolist(),bn_variance=bn_var.tolist(),
                ln_mean=ln_mean.tolist(),ln_variance=ln_var.tolist(),
                unbiased_batch_variance=unbiased.tolist(),other_sample_affects_bn_only='PASS'))


if __name__=='__main__':print(json.dumps(verify(),ensure_ascii=False,indent=2))
