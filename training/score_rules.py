def compute_quality_score(listing: dict) -> dict:
    score = 100
    issues = []

    if listing.get("photo_count", 0) < 3:
        score -= 20
        issues.append("Too few photos")

    if listing.get("description_length", 0) < 100:
        score -= 15
        issues.append("Short description")

    if listing.get("price", 0) / listing.get("surface", 1) > 15000:
        score -= 10
        issues.append("Suspicious price/surface ratio")

    if not listing.get("rooms"):
        score -= 10
        issues.append("No room information")

    if listing.get("location_precision") == "city":
        score -= 10
        issues.append("Location too vague")

    tier = "HIGH" if score >= 75 else "MEDIUM" if score >= 50 else "LOW"
    return {"quality_score": score, "tier": tier, "issues": issues}