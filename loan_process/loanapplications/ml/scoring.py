from django.db import transaction
import logging
import numpy as np
from typing import Tuple, Dict, Any

from creditscorings.models import CreditScoreRecord
from loanapplications.ml.model_inputs import extract_features_from_mock

logger = logging.getLogger(__name__)


def score_and_record(loan_application) -> None:
    """
    Score a loan application and record the results.

    Args:
        loan_application: The loan application object to score

    Raises:
        ValueError: If mock report is missing or scoring fails
    """
    try:
        # Get the mock_experian report
        try:
            mock_report = loan_application.mock_experian.first()
            if not mock_report:
                logger.error(f"Missing mock_experian report for loan #{loan_application.id}")
                raise ValueError("No mock_experian report found for loan application.")
        except Exception:
            logger.error(f"Error accessing mock_experian for loan #{loan_application.id}")
            raise ValueError("No mock_experian report found for loan application.")

        features = extract_features_from_mock(mock_report)

        # Import the model for scoring
        import joblib
        import os

        # Load the model
        model_path = os.path.join('ml_models', 'xgboost_loan_model.pkl')
        if not os.path.exists(model_path):
            model_path = os.path.join('ml_models', 'lightgbm_loan_model.pkl')

        if not os.path.exists(model_path):
            raise ValueError("No ML model found. Run train_loan_model first.")

        MODEL = joblib.load(model_path)

        risk_score, decision, explanation = score_loan_application(features, MODEL=MODEL)

        with transaction.atomic():
            # Create credit score record
            CreditScoreRecord.objects.create(
                loan_application=loan_application,
                user=loan_application.user,
                model_name="xgboost_v1",
                risk_score=risk_score,
                decision=decision,
                scoring_inputs=features,
                scoring_output=explanation,
                credit_utilization_pct=features.get('credit_util_pct'),
                dpd_max=features.get('dpd_max'),
                emi_to_income_ratio=features.get('emi_to_income_ratio'),
            )

            # Update loan application
            loan_application.risk_score = risk_score
            loan_application.ai_decision = decision
            loan_application.ml_scoring_output = explanation
            loan_application.save()

        logger.info(f"Loan #{loan_application.id} scored successfully: {decision} (risk score: {risk_score})")

    except Exception as e:
        logger.error(f"Error scoring loan #{loan_application.id}: {str(e)}", exc_info=True)
        raise


def score_loan_application(features: Dict[str, Any], MODEL=None) -> Tuple[float, str, Dict[str, Any]]:
    """
    Score a loan application based on features.

    Args:
        features: Dictionary of loan features
        MODEL: ML model to use for prediction (optional)

    Returns:
        Tuple of (risk_score, decision, explanation)

    Raises:
        ValueError: If required features are missing or MODEL is None
    """
    if MODEL is None:
        raise ValueError("ML model not provided")

    required_keys = [
        'credit_score',
        'credit_util_pct',
        'dpd_max',
        'emi_to_income_ratio',
        'monthly_income',
        'existing_loans'
    ]

    # Validate features
    missing_keys = [key for key in required_keys if key not in features]
    if missing_keys:
        raise ValueError(f"Missing required features: {', '.join(missing_keys)}")

    # Validate feature values
    if features['credit_score'] < 0 or features['credit_score'] > 900:
        raise ValueError("Invalid credit score value")
    if features['credit_util_pct'] < 0 or features['credit_util_pct'] > 100:
        raise ValueError("Invalid credit utilization percentage")
    if features['monthly_income'] <= 0:
        raise ValueError("Invalid monthly income")

    input_array = np.array([[features[key] for key in required_keys]])

    # Predict and compute risk score
    try:
        prediction = MODEL.predict(input_array)[0]
        prob = MODEL.predict_proba(input_array)[0][1]
    except Exception as e:
        logger.error(f"Model prediction failed: {str(e)}")
        raise ValueError("Model prediction failed") from e

    risk_score = round((1 - prob) * 100, 2)
    decision = "approve" if prediction == 1 else "reject"

    return risk_score, decision, {
        "approval_probability": round(prob, 4),
        "risk_score": risk_score,
        "decision": decision,
        "model": "xgboost_loan_model",
        "features": features,
        "model_version": getattr(MODEL, 'version', 'unknown')
    }
