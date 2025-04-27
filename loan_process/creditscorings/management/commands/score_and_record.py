from django.core.management.base import BaseCommand
from loanapplications.models import LoanApplication
from loanapplications.ml.scoring import score_loan_application
import logging
from django.db import transaction
from django.core.exceptions import ObjectDoesNotExist

# Configure logging
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Score and record AI decisions for eligible loan applications"

    def add_arguments(self, parser):
        """
        Adds command-line arguments to the management command.
        """
        parser.add_argument(
            '--all', action='store_true',
            help='Score all applications (even if already scored)'
        )
        parser.add_argument(
            '--batch-size', type=int, default=100,
            help='Number of applications to process in each batch'
        )

    def handle(self, *args, **options):
        """
        Main logic for scoring loan applications.
        """
        # Filter loans based on the --all flag
        base_queryset = LoanApplication.objects.select_related('user', 'mock_experian')
        loans = base_queryset.all() if options['all'] else base_queryset.filter(
            ai_decision__isnull=True,
            status__in=["pending", "under_review"]
        )

        if not loans.exists():
            self.stdout.write("✅ No loan applications to score.")
            return

        scored_count = 0
        failed_count = 0
        batch_size = options['batch_size']

        # Process in batches
        for i in range(0, loans.count(), batch_size):
            batch = loans[i:i + batch_size]

            for loan in batch:
                try:
                    with transaction.atomic():
                        try:
                            report = loan.mock_experian
                            if not report:
                                raise ObjectDoesNotExist
                        except ObjectDoesNotExist:
                            raise ValueError("No Experian report found")

                        user = loan.user

                        # Validate required data
                        if not all([user, report, loan.monthly_income is not None]):
                            raise ValueError("Missing required loan application data")

                        # Prepare features for scoring with data validation
                        features = {
                            'credit_score': max(0, user.credit_score or 0),
                            'credit_util_pct': max(0, min(100, report.credit_utilization_pct or 0)),
                            'dpd_max': max(0, report.dpd_max or 0),
                            'emi_to_income_ratio': max(0, report.emi_to_income_ratio or 0),
                            'monthly_income': float(max(0, loan.monthly_income)),
                            'existing_loans': int(loan.existing_loans),
                        }

                        # Call scoring function
                        risk_score, decision, explanation = score_loan_application(features)

                        # Validate scoring results
                        if risk_score is None or not isinstance(risk_score, (int, float)):
                            raise ValueError("Invalid risk score")
                        if decision not in ['approve', 'reject', 'manual_review']:
                            raise ValueError("Invalid decision")
                        if not explanation or not isinstance(explanation, dict):
                            raise ValueError("Invalid explanation")

                        # Update loan fields with AI decision and scoring results
                        loan.risk_score = float(risk_score)
                        loan.ai_decision = decision
                        loan.ml_scoring_output = explanation

                        # Update loan status based on AI decision
                        if loan.status in ["pending", "under_review"]:
                            loan.status = "approved" if decision == "approve" else "rejected"

                        # Save loan updates
                        loan.save()
                        scored_count += 1

                        # Log success
                        logger.info(f"Loan #{loan.id} scored: Decision={decision}, Risk Score={risk_score}")

                except ValueError as e:
                    failed_count += 1
                    error_message = f"⚠️ Loan #{loan.id} skipped: {str(e)}"
                    self.stdout.write(self.style.WARNING(error_message))
                    logger.warning(error_message)

                except Exception as e:
                    failed_count += 1
                    error_message = f"⚠️ Loan #{loan.id} failed: {str(e)}"
                    self.stdout.write(self.style.ERROR(error_message))
                    logger.error(error_message, exc_info=True)

        # Final summary message
        self.stdout.write(self.style.SUCCESS(
            f"✅ Processing complete:\n"
            f"Successfully scored: {scored_count} loan(s)\n"
            f"Failed/Skipped: {failed_count} loan(s)"
        ))
