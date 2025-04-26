from creditscorings.models import CreditScoreRecord
from django.db import transaction
from loanapplications.ml.scoring import score_loan_application


def score_and_record(loan_application):
    """
    Run ML scoring on a loan application and save both the result and a record.

    Args:
        loan_application: The LoanApplication instance to be scored.

    Raises:
        ValueError: If required fields for scoring are missing or invalid.
        Exception: If the scoring or database operations fail.
    """
    if not loan_application:
        raise ValueError("Loan application is required")

    user = loan_application.user
    if not user:
        raise ValueError("Loan application must have an associated user")

    # Prepare model inputs from loan data
    try:
        model_inputs = {
            'amount_requested': float(loan_application.amount_requested or 0),
            'term_months': int(loan_application.term_months or 0),
            'monthly_income': float(loan_application.monthly_income or 0),
            'existing_loans': int(loan_application.existing_loans or 0),
            'credit_score': int(loan_application.credit_score or 0),
            'credit_util_pct': float(loan_application.credit_util_pct or 0),
        }

        # Validate required fields
        required_fields = ['amount_requested', 'term_months', 'monthly_income']
        for field in required_fields:
            if not model_inputs[field]:
                raise ValueError(f"Required field {field} is missing or invalid")

    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid loan application data: {str(e)}")

    # Run the model scoring
    try:
        risk_score, decision, explanation = score_loan_application(model_inputs)
    except Exception as e:
        raise Exception(f"Error during ML scoring: {str(e)}")

    # Save the scoring result to CreditScoreRecord and update LoanApplication
    try:
        with transaction.atomic():
            # Save to CreditScoreRecord
            credit_score_record = CreditScoreRecord.objects.create(
                user=user,
                loan_application=loan_application,
                model_name='xgboost_v1',
                risk_score=risk_score,
                decision=decision,
                scoring_inputs=model_inputs,
                scoring_output=explanation,
            )

            # Update LoanApplication directly
            loan_application.risk_score = risk_score
            loan_application.ai_decision = decision
            loan_application.ml_scoring_output = explanation
            loan_application.save()

            return credit_score_record

    except Exception as e:
        raise Exception(f"Error saving scoring results: {str(e)}")
