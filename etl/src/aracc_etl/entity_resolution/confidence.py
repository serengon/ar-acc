def normalize_score(match_probability: float) -> float:
    """Clamp a match probability to [0, 1]."""
    return max(0.0, min(1.0, match_probability))


def classify_confidence(score: float) -> str:
    """Classify a normalized score into confidence tiers.

    Returns "high" (>=0.9), "medium" (>=0.7), or "low" (<0.7).
    """
    if score >= 0.9:
        return "high"
    if score >= 0.7:
        return "medium"
    return "low"
