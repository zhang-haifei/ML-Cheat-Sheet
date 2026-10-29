#!/usr/bin/env python3
"""Exact rational least squares, independent of the plot-generation routine."""
import csv
import json
import math
from fractions import Fraction as F
from itertools import product
from pathlib import Path


def solve(a, b):
    m = [row[:] + [rhs] for row, rhs in zip(a, b)]
    n = len(b)
    for k in range(n):
        pivot = next(i for i in range(k, n) if m[i][k])
        m[k], m[pivot] = m[pivot], m[k]
        scale = m[k][k]
        m[k] = [v / scale for v in m[k]]
        for i in range(n):
            if i != k:
                factor = m[i][k]
                m[i] = [x - factor * y for x, y in zip(m[i], m[k])]
    return [row[-1] for row in m]


def value(c, x):
    return sum(v * x ** i for i, v in enumerate(c))


def verify():
    root = Path(__file__).resolve().parents[1]
    xs = [F(i, 4) for i in range(-4, 5)]
    eps = [F(s) for s in ['.10','-.08','.05','-.12','.07','.05','-.05','.08','-.10']]
    ys = [x*x+e for x,e in zip(xs, eps)]
    models, results = {}, []
    grid = [F(i, 100) for i in range(-100, 101)]
    for degree in [0, 2, 8]:
        powers = range(degree + 1)
        gram = [[sum(x ** (i+j) for x in xs) for j in powers] for i in powers]
        rhs = [sum(y*x**i for x,y in zip(xs,ys)) for i in powers]
        coeff = solve(gram, rhs)
        models[degree] = coeff
        train = sum((value(coeff,x)-y)**2 for x,y in zip(xs,ys))/len(xs)
        signal = sum((value(coeff,x)-x*x)**2 for x in grid)/len(grid)
        if degree == 8:
            assert train == 0  # Exact interpolation, without floating-point tolerance.
        results.append(dict(degree=degree,training_mse=float(train),grid_signal_mse=float(signal)))
    assert results[1]['grid_signal_mse'] < results[2]['grid_signal_mse'] < results[0]['grid_signal_mse']
    with (root/'figures/foundations/fits.csv').open() as f:
        points=list(csv.DictReader(f))
    assert len(points)==201
    for row in points:
        x=F(row['x'])
        assert math.isclose(float(row['signal']),float(x*x),abs_tol=1e-9)
        for degree,c in models.items():
            assert math.isclose(float(row[f'degree{degree}']),float(value(c,x)),abs_tol=1e-9)
    predictions=[F(1),F(2),F(3)];truth=F(5,2);mean=sum(predictions)/3
    bias=mean-truth;variance=sum((p-mean)**2 for p in predictions)/3
    noises=[F(-1,2),F(1,2)];noise_variance=sum(e*e for e in noises)/2
    direct=sum((truth+e-p)**2 for p,e in product(predictions,noises))/6
    assert bias==F(-1,2) and variance==F(2,3)
    assert direct==bias*bias+variance+noise_variance==F(7,6)
    return dict(status='PASS',fits=results,plot_points_checked=len(points),
                bias=str(bias),bias_squared=str(bias*bias),variance=str(variance),
                noise_variance=str(noise_variance),direct_six_case_mse=str(direct))


if __name__=='__main__':
    print(json.dumps(verify(),ensure_ascii=False,indent=2))
