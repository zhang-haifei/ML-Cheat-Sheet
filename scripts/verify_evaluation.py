#!/usr/bin/env python3
"""Verify classification examples and AUC by two independent definitions."""
import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def pair_auc(positive, negative):
    return sum((p > n) + .5*(p == n) for p in positive for n in negative)/(len(positive)*len(negative))

def roc_points(positive, negative):
    points = [(0., 0., math.inf)]
    for threshold in sorted(set(positive+negative), reverse=True):
        points.append((sum(s >= threshold for s in negative)/len(negative),
                       sum(s >= threshold for s in positive)/len(positive), threshold))
    return points

def main():
    tp, fn, fp, tn = 18, 12, 7, 63
    accuracy = (tp+tn)/(tp+fn+fp+tn)
    precision, recall = tp/(tp+fp), tp/(tp+fn)
    f1 = 2*tp/(2*tp+fp+fn)
    assert (accuracy,precision,recall) == (.81,.72,.6)
    assert math.isclose(f1,2*precision*recall/(precision+recall))
    assert math.isclose(f1,36/55)
    assert tn/(tn+fp)==.9 and fp/(fp+tn)==.1
    positive, negative = [.9,.8,.5,.4], [.8,.6,.4,.1]
    points = roc_points(positive,negative)
    area = sum((x2-x1)*(y1+y2)/2 for (x1,y1,_),(x2,y2,_) in zip(points,points[1:]))
    assert area == pair_auc(positive,negative) == .6875
    assert pair_auc([.8,.4],[.8,.2]) == .625
    assert pair_auc([.5],[.5]) == .5
    assert pair_auc([1,2],[0,-1]) == 1
    assert pair_auc([0,-1],[1,2]) == 0
    assert pair_auc([math.exp(x) for x in positive],[math.exp(x) for x in negative]) == area
    with (ROOT/'figures/evaluation/roc.csv').open() as stream:
        rows=list(csv.DictReader(stream))
    assert len(rows)==len(points)
    for row,(fpr,tpr,threshold) in zip(rows,points):
        assert float(row['fpr'])==fpr and float(row['tpr'])==tpr
        assert float(row['threshold'])==threshold
    # A complete single-label multiclass example: micro P/R/F1 equals accuracy.
    confusion=[[8,2,0],[1,5,0],[0,1,3]]
    total=sum(map(sum,confusion));correct=sum(confusion[i][i] for i in range(3))
    false_positive=sum(sum(confusion[r][c] for r in range(3) if r!=c) for c in range(3))
    false_negative=sum(sum(confusion[r][c] for c in range(3) if c!=r) for r in range(3))
    assert correct/(correct+false_positive)==correct/(correct+false_negative)==correct/total==.8
    ppv=lambda prior: prior*.8/(prior*.8+(1-prior)*.1)
    assert round(ppv(.5),3)==.889 and round(ppv(.01),3)==.075
    target=[1,2,3];prediction=[1,2,4];mean_target=2
    rss=sum((a-b)**2 for a,b in zip(target,prediction))
    tss=sum((a-mean_target)**2 for a in target)
    ess=sum((b-mean_target)**2 for b in prediction)
    cross=2*sum((a-b)*(b-mean_target) for a,b in zip(target,prediction))
    assert (rss,tss,ess,cross)==(1,2,5,-4)
    assert tss==rss+ess+cross and tss!=rss+ess
    assert 1-rss/tss==.5
    assert 1-sum((a-4)**2 for a in target)/tss==-6
    pred_mean=sum(prediction)/3
    corr_squared=(sum((a-mean_target)*(b-pred_mean) for a,b in zip(target,prediction))**2
                  /(tss*sum((b-pred_mean)**2 for b in prediction)))
    assert math.isclose(corr_squared,27/28) and not math.isclose(corr_squared,.5)
    assert 1-15/10==-.5
    print(json.dumps({'checks':'PASS','classification':{'accuracy':accuracy,'precision':precision,
        'recall':recall,'f1':f1},'auc_pair_and_area':area,'roc_points_checked':len(points),
        'precision_at_prior_half':ppv(.5),'precision_at_prior_1percent':ppv(.01),
        'regression':{'tss':tss,'rss':rss,'ess':ess,'cross_term':cross,'r2':.5,
                      'negative_r2_example':-6,'squared_correlation':corr_squared}},ensure_ascii=False,indent=2))

if __name__=='__main__':
    main()
