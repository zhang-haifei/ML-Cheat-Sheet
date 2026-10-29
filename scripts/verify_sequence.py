#!/usr/bin/env python3
"""Independently verify text, shared recurrence and masked attention examples."""
import json
import math
import numpy as np


def softmax(x):
    e = np.exp(x - np.max(x, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def verify():
    counts = np.array([[2., 0, 1, 0], [0, 1, 1, 0], [1, 0, 0, 1]])
    df = (counts > 0).sum(axis=0)
    assert np.array_equal(df, [2, 1, 2, 1])
    idf = np.log(4 / (1 + df)) + 1
    tfidf = counts * idf
    normalized = tfidf / np.linalg.norm(tfidf, axis=1, keepdims=True)
    assert np.allclose(normalized[0], [2/math.sqrt(5), 0, 1/math.sqrt(5), 0])
    embedding = np.arange(12).reshape(4, 3)
    assert np.array_equal(embedding[[1, 2, 3]], [[3, 4, 5], [6, 7, 8], [9, 10, 11]])

    # Differentiate through the shared recurrent parameter, including every use.
    inputs = [1., 0., -1.]
    def recurrence(w):
        state = 0.; derivative = 0.; states = []
        for x in inputs:
            new_state = math.tanh(x + w*state)
            derivative = (1-new_state**2)*(state + w*derivative)
            state = new_state; states.append(state)
        return states, state*derivative
    states, gradient = recurrence(.5)
    eps = 1e-6
    difference = (.5*recurrence(.5+eps)[0][-1]**2 -
                  .5*recurrence(.5-eps)[0][-1]**2)/(2*eps)
    assert abs(difference-gradient) < 1e-9
    cell = .9*2 + .2*(-.5)
    hidden = .8*math.tanh(cell)
    assert abs(cell-1.7) < 1e-14 and round(hidden, 3) == .748

    q = np.array([[math.log(3)]])
    k = np.array([[0.], [1.]])
    v = np.array([[2., 0], [0, 4.]])
    weights = softmax(q @ k.T)
    output = weights @ v
    assert np.allclose(weights, [[.25, .75]])
    assert np.allclose(output, [[.5, 3.]])
    # Q gradient through softmax and aggregation, checked against finite difference.
    dweight = output @ v.T
    dscore = weights*(dweight - (dweight*weights).sum(axis=-1, keepdims=True))
    dq = dscore @ k
    def attention_loss(query):
        result = softmax(query @ k.T) @ v
        return .5*np.sum(result**2)
    numerical = (attention_loss(q+eps)-attention_loss(q-eps))/(2*eps)
    assert abs(float(dq[0, 0])-numerical) < 1e-8

    mask = np.where(np.tril(np.ones((3, 3), dtype=bool)), 0., -np.inf)
    causal = softmax(np.zeros((3, 3)) + mask)
    assert np.allclose(causal, [[1, 0, 0], [.5, .5, 0], [1/3, 1/3, 1/3]])
    values = np.array([[1., 2.], [3., 4.], [5., 6.]])
    perturbed = values.copy(); perturbed[2] += 1000
    assert np.array_equal((causal@values)[:2], (causal@perturbed)[:2])
    assert not np.allclose(softmax(np.zeros((3, 3)))*np.tril(np.ones((3, 3))), causal)
    # Permuting tokens permutes unmasked self-attention output; positions break this symmetry.
    x = np.array([[1., 2.], [-1., 3.], [2., 0.]])
    perm = [2, 0, 1]
    result = softmax(x @ x.T/math.sqrt(2)) @ x
    xp = x[perm]
    assert np.allclose(softmax(xp @ xp.T/math.sqrt(2)) @ xp, result[perm])
    # LayerNorm reduces the feature axis separately at each token.
    ln = lambda z: (z-z.mean(axis=-1, keepdims=True))/np.sqrt(z.var(axis=-1, keepdims=True)+1e-5)
    assert np.allclose(ln(x+np.array([[10.], [-7.], [2.]])), ln(x))
    heads = [np.zeros((3, 2)), np.ones((3, 2))]
    assert np.concatenate(heads, axis=-1).shape == (3, 4)
    assert 4*4**2 == 64
    memory = {str(t): 2*4*t*t*4/2**20 for t in (128, 256)}
    assert memory == {'128': .5, '256': 2.}
    return dict(status='PASS', document_frequencies=df.tolist(), idf=idf.tolist(),
                normalized_first_document=normalized[0].tolist(), rnn_states=states,
                shared_recurrence_gradient=gradient, recurrence_difference=abs(gradient-difference),
                lstm_cell=cell, lstm_hidden=hidden, attention_weights=weights.tolist(),
                attention_output=output.tolist(), attention_q_gradient=float(dq[0, 0]),
                attention_gradient_difference=abs(float(dq[0, 0])-numerical),
                causal_weights=causal.tolist(), memory_MiB=memory,
                permutation_equivariance='PASS', future_value_invariance='PASS')


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
