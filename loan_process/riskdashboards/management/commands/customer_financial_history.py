from django.core.management.base import BaseCommand
from users.models import CustomUser
from loanapplications.models import LoanApplication
from integrations.models import MockExperianReport
import json
from decimal import Decimal
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Generate financial report for a specific user"

    def add_arguments(self, parser):
        parser.add_argument('--user_id', type=int, required=True, help="User ID to generate report for")
        parser.add_argument('--output_dir', type=str, default='reports', help="Directory to save report")

    def handle(self, *args, **options):
        user_id = options['user_id']
        output_dir = Path(options['output_dir'])
        output_dir.mkdir(exist_ok=True)

        try:
            user = CustomUser.objects.get(id=user_id)
        except CustomUser.DoesNotExist:
            logger.error(f"User with ID {user_id} does not exist.")
            self.stdout.write(self.style.ERROR(f"❌ User with ID {user_id} does not exist."))
            return

        # Get all loan applications for user
        loans = LoanApplication.objects.filter(user=user).order_by('-submitted_at')
        if not loans.exists():
            logger.warning(f"No loan applications found for user {user_id}")
            self.stdout.write(self.style.WARNING(f"⚠️ No loan applications found for user {user_id}"))
            # Create an empty report with just user info
            summary = {
                "user": {
                    "username": user.username,
                    "credit_score": float(user.credit_score or 0),
                    "annual_income": float(user.annual_income or 0),
                    "employment_status": user.employment_status or "Unknown",
                },
                "loan_history": [],
                "experian": {}
            }
            report_filename = output_dir / f"user_{user.id}_financial_report.json"
            with open(report_filename, "w") as f:
                json.dump(summary, f, indent=2)
            self.stdout.write(self.style.SUCCESS(f"✅ Report generated: {report_filename}"))
            return

        # Get most recent loan with Experian report
        loan_with_report = loans.filter(mock_experian__isnull=False).first()
        report = None
        if loan_with_report:
            report = loan_with_report.mock_experian.first()

        if not loan_with_report or not report:
            logger.warning("No mock Experian report found for this user.")
            self.stdout.write(self.style.WARNING("⚠️ No mock Experian report found for this user."))

        try:
            summary = {
                "user": {
                    "username": user.username,
                    "credit_score": float(user.credit_score or 0),
                    "annual_income": float(user.annual_income or 0),
                    "employment_status": user.employment_status or "Unknown",
                },
                "loan_history": [
                    {
                        "amount": float(loan.amount_requested or 0),
                        "status": loan.status,
                        "ai_decision": loan.ai_decision,
                        "risk_score": float(loan.risk_score or 0),
                        "submitted_at": loan.submitted_at.strftime('%Y-%m-%d')
                    } for loan in loans
                ],
                "experian": {}
            }

            # Add Experian data if available
            if report:
                summary["experian"] = {
                    "dpd_max": report.dpd_max or 0,
                    "emi_to_income_ratio": float(report.emi_to_income_ratio or 0),
                    "credit_utilization_pct": float(report.credit_utilization_pct or 0),
                    "total_accounts": report.total_accounts or 0,
                }

            report_filename = output_dir / f"user_{user.id}_financial_report.json"
            with open(report_filename, "w") as f:
                json.dump(summary, f, indent=2)

            self.stdout.write(self.style.SUCCESS(f"✅ Report generated: {report_filename}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error generating report: {str(e)}"))
            return
