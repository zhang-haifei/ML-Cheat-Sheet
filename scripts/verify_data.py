#!/usr/bin/env python3
"""Independently recompute the data-preparation chapter's worked examples."""
import json
import math
from statistics import median


def verify():
    observed = [10, 20, 30]
    fill = median(observed)
    assert fill == 20
    filled = [10, fill, 20, 30]
    indicator = [0, 1, 0, 0]
    assert filled == [10, 20, 20, 30] and sum(indicator) == 1
    records = [(1, 10), (2, 12), (8, 80), (9, 90)]
    query = 2.1
    distances = [abs(a - query) for a, _ in records]
    nearest = sorted(records, key=lambda row: abs(row[0] - query))[:2]
    knn_fill = sum(b for _, b in nearest) / len(nearest)
    assert knn_fill == 11 and median([b for _, b in records]) == 46
    mean = sum(observed) / len(observed)
    variance = sum((x - mean) ** 2 for x in observed) / len(observed)
    sd = math.sqrt(variance)
    scaled = [(x - mean) / sd for x in observed]
    assert math.isclose(sum(scaled), 0, abs_tol=1e-14)
    assert math.isclose(sum(z * z for z in scaled) / len(scaled), 1)
    new_minmax = (40 - min(observed)) / (max(observed) - min(observed))
    new_standard = (40 - mean) / sd
    assert new_minmax == 1.5 and math.isclose(new_standard, math.sqrt(6))
    onehot = [[int(i == j) for j in range(3)] for i in range(3)]
    assert all(sum(row) == 1 for row in onehot)
    # Including an intercept gives a column equal to the sum of all dummy columns.
    assert all(sum(row) == intercept for row, intercept in zip(onehot, [1] * 3))
    xi, xj, fraction = (1, 2), (3, 4), 0.25
    synthetic = [a + fraction * (b - a) for a, b in zip(xi, xj)]
    assert synthetic == [1.5, 2.5]
    for lam in [0, 0.25, 0.5, 1]:
        assert all(min(a, b) <= a + lam * (b - a) <= max(a, b)
                   for a, b in zip(xi, xj))
    return dict(status="PASS", median_fill=fill, missing_indicator=indicator,
                knn_distances=distances, knn_fill=knn_fill, global_median=46,
                mean=mean, population_sd=sd, standardized=scaled,
                new_minmax=new_minmax, new_standardized=new_standard,
                sampling_counts=dict(original=[90, 10], undersampled=[20, 10],
                                     oversampled=[90, 45]), smote=synthetic)


if __name__ == "__main__":
    print(json.dumps(verify(), ensure_ascii=False, indent=2))
