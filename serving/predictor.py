from training.score_rules import compute_quality_score


def predict_one(data: dict) -> dict:
    result = compute_quality_score(data)
    return {
        "quality_score": result["quality_score"],
        "tier": result["tier"],
        "issues": result["issues"],
    }
