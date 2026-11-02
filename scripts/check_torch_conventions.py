#!/usr/bin/env python3
"""Optional CPU checks of the handbook's PyTorch interface conventions.

The core verify_all.py checks remain independent of PyTorch. This script uses
small float64 examples and Python math / explicit values as reference results.
"""
import json
import math

try:
    import torch
except ModuleNotFoundError as error:
    if error.name != 'torch':
        raise
    raise SystemExit('Optional check: install PyTorch before running this script. '
                     'Core checks: python scripts/verify_all.py') from None
from torch import nn
from torch.nn import functional as F


def close(actual, expected):
    torch.testing.assert_close(actual, torch.tensor(expected, dtype=torch.float64),
                               rtol=1e-12, atol=1e-12)


def normalization():
    eps = 1e-5
    x = torch.tensor([[[[1., 3.]], [[10., 14.]]],
                      [[[5., 7.]], [[18., 22.]]]], dtype=torch.float64)
    expected_bn = [[[[-3/math.sqrt(5+eps), -1/math.sqrt(5+eps)]],
                    [[-6/math.sqrt(20+eps), -2/math.sqrt(20+eps)]]],
                   [[[1/math.sqrt(5+eps), 3/math.sqrt(5+eps)]],
                    [[2/math.sqrt(20+eps), 6/math.sqrt(20+eps)]]]]
    bn = nn.BatchNorm2d(2, affine=False, momentum=1., eps=eps, dtype=torch.float64)
    close(bn(x), expected_bn)
    close(bn.running_mean, [4., 16.])
    close(bn.running_var, [20/3, 80/3])
    bn.eval()
    expected_eval = [[[[(value+100-mean)/math.sqrt(variance+eps) for value in channel[0]]]
                      for channel, mean, variance in zip(sample, [4., 16.], [20/3, 80/3])]
                     for sample in x.tolist()]
    close(bn(x+100), expected_eval)
    close(bn.running_mean, [4., 16.])
    close(bn.running_var, [20/3, 80/3])

    batch_only = nn.BatchNorm2d(2, affine=False, track_running_stats=False,
                              eps=eps, dtype=torch.float64)
    original = batch_only(x)
    batch_only.eval()
    close(batch_only(x+100), original.tolist())
    assert batch_only.running_mean is None and batch_only.running_var is None
    changed = x.clone()
    changed[1] += 100
    assert not torch.allclose(batch_only(changed)[0], original[0])

    ln = nn.LayerNorm((2, 1, 2), elementwise_affine=False, eps=eps, dtype=torch.float64)
    expected_ln = [[[[-6/math.sqrt(27.5+eps), -4/math.sqrt(27.5+eps)]],
                    [[3/math.sqrt(27.5+eps), 7/math.sqrt(27.5+eps)]]],
                   [[[-8/math.sqrt(51.5+eps), -6/math.sqrt(51.5+eps)]],
                    [[5/math.sqrt(51.5+eps), 9/math.sqrt(51.5+eps)]]]]
    train_ln = ln(x)
    close(train_ln, expected_ln)
    ln.eval()
    close(ln(x), expected_ln)
    close(ln(changed)[0], train_ln[0].tolist())
    token_ln = nn.LayerNorm(2, elementwise_affine=False, eps=eps, dtype=torch.float64)
    close(token_ln(x.squeeze(2)),
          [[[-1/math.sqrt(1+eps), 1/math.sqrt(1+eps)],
            [-2/math.sqrt(4+eps), 2/math.sqrt(4+eps)]]]*2)
    return {'batch_mean': [4., 16.], 'batch_forward_variance': [5., 20.],
            'batch_running_variance': bn.running_var.tolist(),
            'layer_mean': [7., 13.], 'layer_variance': [27.5, 51.5],
            'eval_without_running_stats_uses_current_batch': True,
            'changing_other_sample_affects_bn_but_not_per_sample_ln': True,
            'layernorm_last_axis_and_full_sample_axes_checked': True}


def gru():
    cases = []
    for hidden_bias in [[0., 0.], [.2, -.4]]:
        cell = nn.GRUCell(1, 2, dtype=torch.float64)
        with torch.no_grad():
            for parameter in cell.parameters():
                parameter.zero_()
            # PyTorch packs reset, update, candidate gates in that order.
            cell.bias_ih[:2].copy_(torch.tensor([0., math.log(1/3)], dtype=torch.float64))
            cell.weight_hh[4:].copy_(torch.tensor([[1., 1.], [1., -1.]], dtype=torch.float64))
            cell.bias_hh[4:].copy_(torch.tensor(hidden_bias, dtype=torch.float64))
        x = torch.zeros((1, 1), dtype=torch.float64)
        h = torch.tensor([[.5, .5]], dtype=torch.float64)
        actual = cell(x, h)
        # Wh=(1,0), r=(.5,.25), z=(.5,.5); references use Python math.
        post = [.25+.5*math.tanh(.5*(1+hidden_bias[0])),
                .25+.5*math.tanh(.25*hidden_bias[1])]
        pre = [.25+.5*math.tanh(.375+hidden_bias[0]),
               .25+.5*math.tanh(.125+hidden_bias[1])]
        close(actual, [post])
        assert max(abs(a-b) for a, b in zip(post, pre)) > .01
        layer = nn.GRU(1, 2, dtype=torch.float64)
        with torch.no_grad():
            for name in ['weight_ih', 'weight_hh', 'bias_ih', 'bias_hh']:
                getattr(layer, name+'_l0').copy_(getattr(cell, name))
        output, state = layer(x.unsqueeze(0), h.unsqueeze(0))
        close(output[0], [post])
        close(state[0], [post])
        cases.append({'hidden_bias': hidden_bias, 'native_output': actual.detach().tolist()[0],
                      'reset_after_matrix_reference': post, 'reset_before_matrix_reference': pre})
    return {'gate_update_convention': 'z*h_previous + (1-z)*candidate',
            'gru_cell_and_sequence_layer_match_reset_after_matrix': True, 'cases': cases}


def convolution_and_pooling():
    image = torch.tensor([[[[1., 2., 0., 1.], [0., 1., 3., 2.],
                            [2., 0., 1., 1.], [1., 2., 1., 0.]]]], dtype=torch.float64)
    kernel = torch.tensor([[[[1., 0.], [0., -1.]]]], dtype=torch.float64)
    convolution = F.conv2d(image, kernel)
    close(convolution, [[[[0., -1., -2.], [0., 0., 2.], [0., -1., 1.]]]])
    pooling_image = torch.tensor([[[[1., 3., 2., 0.], [4., 6., 1., 5.],
                                    [2., 1., 8., 7.], [0., 3., 4., 9.]]]], dtype=torch.float64)
    maximum = F.max_pool2d(pooling_image, 2, stride=2)
    average = F.avg_pool2d(pooling_image, 2, stride=2)
    close(maximum, [[[[6., 5.], [3., 9.]]]])
    close(average, [[[[3.5, 2.], [1.5, 7.]]]])
    model = nn.Sequential(nn.Conv2d(3, 16, 3, padding=1, dtype=torch.float64),
                          nn.ReLU(), nn.MaxPool2d(2), nn.AdaptiveAvgPool2d(1),
                          nn.Flatten(1), nn.Linear(16, 10, dtype=torch.float64))
    parameters = sum(p.numel() for p in model.parameters())
    output = model(torch.zeros((8, 3, 32, 32), dtype=torch.float64))
    assert parameters == 618 and tuple(output.shape) == (8, 10)
    features = torch.arange(128, dtype=torch.float64).reshape(8, 16, 1, 1).expand(8, 16, 16, 16)
    close(F.adaptive_avg_pool2d(features, 1).flatten(1),
          [[float(b*16+c) for c in range(16)] for b in range(8)])
    return {'cross_correlation_output': convolution.tolist()[0][0],
            'max_pool_output': maximum.tolist()[0][0],
            'average_pool_output': average.tolist()[0][0],
            'toy_network_parameters': parameters, 'toy_network_output_shape': list(output.shape),
            'global_pooling_preserves_batch_and_channels': True}


def recurrent_states():
    layer = nn.RNN(1, 1, nonlinearity='tanh', dtype=torch.float64)
    with torch.no_grad():
        layer.weight_ih_l0.fill_(1.)
        layer.weight_hh_l0.fill_(.5)
        layer.bias_ih_l0.zero_()
        layer.bias_hh_l0.zero_()
    values = [1., 0., -1.]
    expected = []
    state = 0.
    for value in values:
        state = math.tanh(value+.5*state)
        expected.append(state)
    output, final = layer(torch.tensor(values, dtype=torch.float64).reshape(3, 1, 1),
                          torch.zeros((1, 1, 1), dtype=torch.float64))
    close(output.flatten(), expected)
    close(final.flatten(), [expected[-1]])
    cell = nn.LSTMCell(1, 1, dtype=torch.float64)
    with torch.no_grad():
        for parameter in cell.parameters():
            parameter.zero_()
        # LSTM packs input, forget, candidate, output gates.
        cell.bias_ih.copy_(torch.tensor([math.log(.2/.8), math.log(.9/.1),
                                        math.atanh(-.5), math.log(.8/.2)], dtype=torch.float64))
    hidden, memory = cell(torch.zeros((1, 1), dtype=torch.float64),
                          (torch.zeros((1, 1), dtype=torch.float64),
                           torch.tensor([[2.]], dtype=torch.float64)))
    close(memory, [[1.7]])
    close(hidden, [[.8*math.tanh(1.7)]])
    return {'rnn_states': output.detach().flatten().tolist(),
            'lstm_memory': memory.item(), 'lstm_hidden': hidden.item()}


def losses_and_update():
    logits = torch.tensor([[1000., 1001., 999.]], dtype=torch.float64)
    ce = nn.CrossEntropyLoss()(logits, torch.tensor([0]))
    expected_ce = 1+math.log(1+math.exp(-1)+math.exp(-2))
    close(ce, expected_ce)
    extreme = F.binary_cross_entropy_with_logits(
        torch.tensor([1000., -1000., 1000., -1000.], dtype=torch.float64),
        torch.tensor([0., 1., 1., 0.], dtype=torch.float64), reduction='none')
    close(extreme, [1000., 1000., 0., 0.])
    parameters = [torch.tensor(value, dtype=torch.float64, requires_grad=True)
                  for value in [.5, 0., 1., 0.]]
    w1, b1, w2, b2 = parameters
    score = w2*torch.relu(w1*2+b1)+b2
    loss = F.binary_cross_entropy_with_logits(score, torch.tensor(1., dtype=torch.float64))
    loss.backward()
    error = 1/(1+math.exp(-1))-1
    expected_gradients = [2*error, error, error, error]
    close(torch.stack([p.grad for p in parameters]), expected_gradients)
    optimizer = torch.optim.SGD(parameters, lr=.1)
    optimizer.step()
    expected_weights = [value-.1*gradient for value, gradient in
                        zip([.5, 0., 1., 0.], expected_gradients)]
    close(torch.stack(parameters), expected_weights)
    a, b, c, d = expected_weights
    expected_probability = 1/(1+math.exp(-(c*max(0, a*2+b)+d)))
    new_probability = torch.sigmoid(w2*torch.relu(w1*2+b1)+b2)
    close(new_probability, expected_probability)
    return {'categorical_cross_entropy': ce.item(), 'extreme_bce': extreme.tolist(),
            'single_step_gradients': expected_gradients,
            'single_step_parameters': [p.item() for p in parameters],
            'single_step_probability': new_probability.item()}


def verify():
    torch.set_num_threads(1)
    torch.manual_seed(0)
    return {'status': 'PASS', 'torch_version': torch.__version__, 'device': 'cpu',
            'dtype': 'float64', 'scope': 'Targeted interface checks on constructed examples; not a task-level training benchmark.',
            'normalization': normalization(), 'convolution_and_pooling': convolution_and_pooling(),
            'recurrent_states': recurrent_states(), 'gru': gru(),
            'losses_and_single_sgd_step': losses_and_update()}


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
