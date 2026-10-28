#!/usr/bin/env python3
"""Recompute batch-two examples; use exhaustive masks and decimal Adam arithmetic."""
import csv
import itertools
import json
import math
from decimal import Decimal, localcontext
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def early_stopping(values, patience=2, delta=0):
    best, best_epoch, wait = math.inf, None, 0
    history = []
    for epoch, value in enumerate(values, 1):
        if value < best - delta:
            best, best_epoch, wait = value, epoch, 0
        else:
            wait += 1
        history.append((epoch, best_epoch, wait))
        if wait >= patience:
            return epoch, best_epoch, history
    return None, best_epoch, history

def main():
    assert math.ceil(10/4) == 3
    assert 5*math.ceil(103/32) == 20
    single = [0., -2., -4.]
    pairs = [sum(pair)/2 for pair in itertools.combinations(single, 2)]
    assert pairs == [-1., -2., -3.]
    mean = lambda values: sum(values)/len(values)
    variance = lambda values: mean([(x-mean(values))**2 for x in values])
    assert mean(single) == mean(pairs) == -2
    assert math.isclose(variance(single), 8/3)
    assert math.isclose(variance(pairs), 2/3)

    # Validate every plotted momentum point, not just the first/last value.
    with (ROOT/'figures/training/momentum-trajectory.csv').open() as stream:
        rows = list(csv.DictReader(stream))
    ordinary = momentum = 3.
    velocity = 0.
    for step, row in enumerate(rows):
        assert int(row['step']) == step
        assert math.isclose(float(row['sgd']), ordinary, abs_tol=1e-14)
        assert math.isclose(float(row['momentum']), momentum, abs_tol=1e-14)
        ordinary *= .9
        velocity = .8*velocity + momentum
        momentum -= .1*velocity
    assert math.isclose(float(rows[2]['momentum']), 2.19)
    assert min(float(row['momentum']) for row in rows) < 0

    # Compute the published Adam example using high-precision decimal arithmetic.
    with localcontext() as context:
        context.prec = 50
        beta1, beta2 = Decimal('.9'), Decimal('.999')
        rate, epsilon = Decimal('.1'), Decimal('1e-8')
        theta, m, v = Decimal(1), Decimal(0), Decimal(0)
        adam = []
        for step, gradient in enumerate([Decimal(2), Decimal(-1)], 1):
            m = beta1*m + (1-beta1)*gradient
            v = beta2*v + (1-beta2)*gradient**2
            corrected_m = m/(1-beta1**step)
            corrected_v = v/(1-beta2**step)
            theta -= rate*corrected_m/(corrected_v.sqrt()+epsilon)
            adam.append({'step':step, 'm':float(m), 'v':float(v),
                         'corrected_m':float(corrected_m),
                         'corrected_v':float(corrected_v), 'theta':float(theta)})
        assert round(float(theta), 6) == .873366
        assert m > 0  # The second input gradient is negative; history remains positive.
        assert adam[1]['theta'] < adam[0]['theta']
        for step in [1, 2, 10]:
            constant_m = (1-beta1**step)*3
            constant_v = (1-beta2**step)*9
            assert constant_m/(1-beta1**step) == 3
            assert constant_v/(1-beta2**step) == 9

    # Exhaust all 16 masks, with their exact probabilities, for two keep rates.
    activation = [2., 4., 6., 8.]
    for keep in [.5, .75]:
        expectations = [0.]*4
        second = [0.]*4
        mass = 0.
        for mask in itertools.product([0, 1], repeat=4):
            probability = keep**sum(mask)*(1-keep)**(4-sum(mask))
            mass += probability
            values = [m*a/keep for m, a in zip(mask, activation)]
            for j, value in enumerate(values):
                expectations[j] += probability*value
                second[j] += probability*value*value
        assert math.isclose(mass, 1)
        for j, value in enumerate(activation):
            assert math.isclose(expectations[j], value)
            assert math.isclose(second[j]-expectations[j]**2, (1-keep)/keep*value**2)
    assert [m*a/.5 for m,a in zip([1,0,1,0],activation)] == [4,0,12,0]
    assert 3/.75 == 4

    stop, best, history = early_stopping([.80,.60,.50,.52,.49,.51,.53])
    assert (stop, best) == (7, 5)
    assert history[3:] == [(4,3,1),(5,5,0),(6,5,1),(7,5,2)]
    assert early_stopping([.8,.6,.61,.59,.60,.62])[:2] == (6,4)
    assert early_stopping([.5,.5,.5])[:2] == (3,1)
    assert math.isclose(math.sqrt(6/(100+50)), .2)
    assert math.isclose(.2**2/3, 2/(100+50))
    assert round(math.sqrt(2/100), 6) == .141421
    assert round(.25**10, 9) == .000000954
    assert math.isclose((4*.2+4*.4+2*.8)/10, .4)
    print(json.dumps({'checks':'PASS', 'momentum_points_checked':len(rows),
        'single_gradient_variance':variance(single), 'pair_gradient_variance':variance(pairs),
        'adam':adam, 'dropout_masks_checked':32, 'early_stopping':{'stop':stop,'restore':best},
        'xavier_uniform_bound':.2, 'he_standard_deviation':math.sqrt(.02),
        'ten_sigmoid_like_factors':.25**10}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
