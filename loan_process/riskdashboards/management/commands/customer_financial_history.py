from django.core.management.base import BaseCommand
from users.models import CustomUser
from loanapplications.models import LoanApplication
from integrations.models import MockExperianReport
import json
from decimal import Decimal
from pathlib import Path


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
            self.stdout.write(self.style.ERROR(f"❌ User with ID {user_id} does not exist."))
            return

        # Get all loan applications for user
        loans = LoanApplication.objects.filter(user=user).order_by('-submitted_at')
        if not loans.exists():
            self.stdout.write(self.style.WARNING(f"⚠️ No loan applications found for user {user_id}"))
            return

        # Get most recent loan with Experian report
        loan_with_report = loans.filter(mock_experian__isnull=False).first()
        if not loan_with_report:
            self.stdout.write(self.style.WARNING("⚠️ No mock Experian report found for this user."))
            return

        report = loan_with_report.mock_experian.first()
        if not report:
            self.stdout.write(self.style.WARNING("⚠️ No valid mock Experian report found for this loan."))
            return

        try:
            summary = {
                "user": {
                    "username": user.username,
                    "credit_score": float(user.credit_score or 0),
                    "monthly_income": float(user.annual_income or 0) / 12,
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
                "experian": {
                    "dpd_max": report.dpd_max or 0,
                    "emi_to_income_ratio": float(report.emi_to_income_ratio or 0),
                    "credit_utilization_pct": float(report.credit_utilization_pct or 0),
                    "total_accounts": report.total_accounts or 0,
                }
            }

            report_filename = output_dir / f"user_{user.id}_financial_report.json"
            with open(report_filename, "w") as f:
                json.dump(summary, f, indent=2)

            self.stdout.write(self.style.SUCCESS(f"✅ Report generated: {report_filename}"))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error generating report: {str(e)}"))
            return
