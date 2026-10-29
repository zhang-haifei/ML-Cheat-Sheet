#!/usr/bin/env python3
"""Independently check the published examples and backpropagation derivatives."""
import json
import math

def sigmoid(value):
    return 1 / (1 + math.exp(-value))

def softmax(values):
    largest = max(values)
    weights = [math.exp(value - largest) for value in values]
    return [weight / sum(weights) for weight in weights]

def loss(parameters):
    w1, b1, w2, b2 = parameters
    score = w2 * max(0, w1 * 2 + b1) + b2
    # For y=1: stable BCE from logits, without reusing backprop formulas.
    return max(0, -score) + math.log1p(math.exp(-abs(score)))

def main():
    parameters = [.5, 0., 1., 0.]
    p = sigmoid(1)
    analytical = [(p - 1) * 2, p - 1, p - 1, p - 1]
    numerical = []
    for index in range(4):
        positive, negative = parameters.copy(), parameters.copy()
        positive[index] += 1e-6
        negative[index] -= 1e-6
        numerical.append((loss(positive) - loss(negative)) / 2e-6)
    max_error = max(abs(a-b) for a, b in zip(analytical, numerical))
    assert max_error < 1e-8, (analytical, numerical)
    updated = [value - .1 * gradient for value, gradient in zip(parameters, analytical)]
    new_score = updated[2] * max(0, updated[0] * 2 + updated[1]) + updated[3]
    assert round(loss(parameters), 6) == .313262
    assert round(loss(updated), 3) == .265
    assert round(sigmoid(new_score), 3) == .767
    assert loss(updated) < loss(parameters)
    assert abs(sigmoid(.2) - .549833997312478) < 1e-14
    probs = softmax([2, 1, 0])
    assert [round(value, 3) for value in probs] == [.665, .245, .090]
    assert abs(-math.log(probs[0]) - .4076059644443803) < 1e-12
    assert max(abs(a-b) for a,b in zip(probs,softmax([1002,1001,1000]))) < 1e-14
    assert softmax([0, 0, 0]) == [1/3]*3
    assert (3*4+4)+(4*3+3)+(3*1+1) == 35
    assert (5*4+4)+(4*2+2) == 34
    for eta in [.1, .5, 2.]:
        value = 2.
        for step in range(11):
            assert abs(value - 2*(1-eta)**step) < 1e-12
            value -= eta * value
    print(json.dumps({'checks':'PASS', 'finite_difference_max_error':max_error,
                      'old_loss':loss(parameters), 'new_loss':loss(updated),
                      'new_probability':sigmoid(new_score), 'updated_parameters':updated,
                      'softmax':probs}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    main()
