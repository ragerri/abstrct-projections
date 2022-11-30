# coding=utf-8
# Copyright 2018 The Google AI Language Team Authors and The HuggingFace Inc. team.
# Copyright (c) 2018, NVIDIA CORPORATION.  All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

try:
    from scipy.stats import pearsonr, spearmanr
    from sklearn.metrics import matthews_corrcoef, f1_score, confusion_matrix, classification_report

    _has_sklearn = True
except (AttributeError, ImportError):
    _has_sklearn = False


def is_sklearn_available():
    return _has_sklearn


if _has_sklearn:

    def simple_accuracy(preds, labels):
        return (preds == labels).mean()

    def acc_and_f1(preds, labels):
        #acc = simple_accuracy(preds, labels)
        #f1 = f1_score(y_true=labels, y_pred=preds)
        f1_micro = f1_score(labels, preds, labels=[1, 2, 3, 4, 5], average='micro')
        f1_macro = f1_score(labels, preds, average='macro')
        f1_claim = f1_score(labels, preds, labels=[1,2], average='micro')
        f1_evidence = f1_score(labels, preds, labels=[3,4], average='micro')

        return {
            #"acc": acc,
            #"f1": f1,
            'eval_f1_micro': f1_micro,
            'eval_f1_macro': f1_macro,
            'f1_claim':f1_claim,
            'f1_evidence':f1_evidence,
            #"acc_and_f1": (acc + f1) / 2,
        }

    def f1_scores(y_pred, y_true, labelfilter=None):

        f1_micro_filtered = f1_score(y_true, y_pred, labels=labelfilter, average='micro')
        f1_macro_filtered = f1_score(y_true, y_pred, labels=labelfilter, average='macro')
        f1_micro = f1_score(y_true, y_pred, average='micro')
        f1_macro = f1_score(y_true, y_pred, average='macro')

        clf_report = classification_report(y_true, y_pred)

        return {
            "eval_f1_micro_filtered": f1_micro_filtered,
            "eval_f1_macro_filtered": f1_macro_filtered,
            'eval_f1_micro': f1_micro,
            'eval_f1_macro': f1_macro,
            'clf_report': clf_report
        }


    def pearson_and_spearman(preds, labels):
        pearson_corr = pearsonr(preds, labels)[0]
        spearman_corr = spearmanr(preds, labels)[0]
        return {
            "pearson": pearson_corr,
            "spearmanr": spearman_corr,
            "corr": (pearson_corr + spearman_corr) / 2,
        }

    def compute_confusion_matrix(task_name, y_pred, y_true):

        assert len(y_pred) == len(y_true)
        if task_name == "multichoice" or task_name == "relclass":
            return confusion_matrix(y_true, y_pred)
        else:
            raise KeyError(task_name)

    def compute_metrics(task_name, y_pred, y_true):
        assert len(y_pred) == len(y_true)
        if task_name == "seqtag":
            return acc_and_f1(y_pred, y_true)
        elif task_name == "relclass":
            return f1_scores(y_pred, y_true, [0, 1])
        elif task_name == "outcomeclf":
            return f1_scores(y_pred, y_true)
        elif task_name == "multichoice":
            return f1_scores(y_pred, y_true, [0, 1])
        else:
            raise KeyError(task_name)

