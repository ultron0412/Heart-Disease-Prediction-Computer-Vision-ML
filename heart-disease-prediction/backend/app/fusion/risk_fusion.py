"""
Decision Fusion Logic
---------------------
Combines:
- Clinical ML probability
- ECG CNN probability

Outputs:
- Final risk score
- Risk category
"""

def fuse_risk(
    clinical_prob: float,
    ecg_prob: float
) -> dict:
    """
    Args:
        clinical_prob (float): Probability from clinical ML model (0–1)
        ecg_prob (float): Probability from ECG CNN (0–1)

    Returns:
        dict: fused risk result
    """

    # Weighted fusion (medical logic)
    final_risk = (0.65 * clinical_prob) + (0.35 * ecg_prob)

    # Risk categorization
    if final_risk < 0.30:
        category = "Low Risk"
    elif final_risk < 0.60:
        category = "Moderate Risk"
    else:
        category = "High Risk"

    return {
        "clinical_probability": round(clinical_prob, 3),
        "ecg_probability": round(ecg_prob, 3),
        "final_risk_score": round(final_risk, 3),
        "risk_category": category
    }
