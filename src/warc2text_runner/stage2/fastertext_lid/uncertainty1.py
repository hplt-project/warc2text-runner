"""Uncertainty score calculations for the FastText language identification model."""

from __future__ import annotations

import numpy
from scipy.spatial import distance
from scipy.stats import entropy


def calculate_uncertainty_scores(
    model, processed_text: str, labels: list[str], probs: list[float]
) -> dict:
    """
    Calculates entropy, logit, and distance-based uncertainty scores.

    Args:
        model: The loaded fasttext model object.
        processed_text: The preprocessed input text.
        labels: The full list of predicted labels from fasttext.
        probs: The full list of predicted probabilities from fasttext.

    Returns:
        A dictionary containing the calculated uncertainty scores.
    """
    # 1. Entropy
    entropy_score = entropy(probs, base=2)

    # 2. Logit of the top predicted class
    # Use the probability from the full distribution for the top class
    top_prob = probs[0] if probs else 0.0
    logit_score = None
    if 0 < top_prob < 1:
        logit_score = numpy.log(top_prob / (1 - top_prob))

    # 3. Distances
    text_vector = model.get_sentence_vector(processed_text)
    top_label_raw = labels[0]
    label_id = model.get_label_id(top_label_raw)
    distances = None
    if label_id != -1:
        output_matrix = model.get_output_matrix()
        label_vector = output_matrix[label_id]

        cosine_dist = distance.cosine(text_vector, label_vector)
        euclidean_dist = distance.euclidean(text_vector, label_vector)
        manhattan_dist = distance.cityblock(text_vector, label_vector)
        distances = {
            "cosine": numpy.round(cosine_dist, 4).item(),
            "euclidean": numpy.round(euclidean_dist, 4).item(),
            "manhattan": numpy.round(manhattan_dist, 4).item(),
        }

    return {
        "entropy": numpy.round(entropy_score, 4).item(),
        "logit": (
            numpy.round(logit_score, 4).item() if logit_score is not None else None
        ),
        "distance": distances,
    }
