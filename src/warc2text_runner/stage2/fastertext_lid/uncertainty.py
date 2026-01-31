"""Module for calculating language identification uncertainty."""

from __future__ import annotations

from typing import Dict, List, Union

import fasttext
import numpy as np
from scipy.stats import entropy
from scipy.special import softmax
from scipy.spatial import distance


def calculate_uncertainty(
    probabilities: List[float],
    model: fasttext.FastText._FastText,
    text: str,
    predicted_label: str,
) -> Dict[str, Union[str, None]]:
    """
    Calculates uncertainty metrics based on prediction probabilities.
    The input list of probabilities is expected to be sorted in descending order.

    Args:
        probabilities: A list of probabilities from the language identification model.
        model: The fasttext model object.
        text: The preprocessed text.
        predicted_label: The top predicted label.

    Returns:
        A dictionary containing uncertainty metrics, with float values formatted as strings
        in exponential notation with 5 digits after the decimal point.
    """
    metrics: Dict[str, Union[str, None]] = {}

    # 1. Predicted probability of the most probable class
    metrics["prob"] = f"{probabilities[0]:.5e}"

    # 2. Top-two difference
    metrics["top2diff"] = f"{probabilities[0] - probabilities[1] :.5e}"
    metrics["top2logratio"] = f"{np.log(probabilities[0]) - np.log(probabilities[1]) :.5e}"

    # 3. Entropy of the full distribution
    metrics["entropy"] = f"{float(entropy(probabilities)):.5e}"

    # 4. Embedding-based scores
    text_embedding = model.get_sentence_vector(text)
    label_id = model.get_label_id(predicted_label)
    label_embedding = model.get_output_matrix()[label_id]

    metrics["dot"] = f"{float(np.dot(text_embedding, label_embedding)):.5e}"

    for metric_name in ["cosine", "euclidean", "cityblock", "canberra"]:
        dist_func = getattr(distance, metric_name)

        for norm in (None, 1, 2):
            v1, v2 = (v / np.linalg.norm(v, ord=norm) if norm else v
                      for v in (text_embedding, label_embedding))
            dist_val = dist_func(v1, v2)
            name = f"-norm{norm}_d{metric_name}" if norm else f"-d{metric_name}"
            metrics[name] = f"{float(-dist_val):.5e}"

    # Sanity check: recalculate probabilities and compare
    output_matrix = model.get_output_matrix()
    logits = np.dot(text_embedding, output_matrix.T)
    softmax_probs = softmax(logits)

    max_prob_index = np.argmax(softmax_probs)
    recalculated_prob = softmax_probs[max_prob_index]
    recalculated_label = model.get_labels()[max_prob_index]

    try:
        assert recalculated_label == predicted_label, f"Recalculated label '{recalculated_label}' does not match predicted label '{predicted_label}'."
        assert np.isclose(recalculated_prob, probabilities[0], rtol=1e-4), f"Recalculated probability {recalculated_prob} does not match input probability {probabilities[0]}."
    except AssertionError as e:
        print(f"Assertion failed: {e}")

    return metrics
