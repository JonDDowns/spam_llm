"""
File: ./spam_llm/compute_metrics.py
Author: Jon Downs
Date: 5/24/2024
Description: Model evaluation function for validation step. Direct copy of examples in HuggingFace documentation for sequence classification.
"""

import evaluate
import numpy as np

accuracy = evaluate.load("accuracy")
def compute_metrics(eval_pred):
    predictions, labels = eval_pred
    predictions = np.argmax(predictions, axis=1)
    return accuracy.compute(predictions=predictions, references=labels)


