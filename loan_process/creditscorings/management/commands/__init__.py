from django.core.management.base import BaseCommand
import csv
from loanapplications.models import LoanApplication
from integrations.models import MockExperianReport
from users.models import CustomUser

class Command(BaseCommand):
    help = "Export loan training data to CSV"

    def handle(self, *args, **options):
        with open("loan_training_data.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                'credit_score', 'credit_util_pct', 'dpd_max', 'emi_to_income_ratio',
                'monthly_income', 'existing_loans', 'loan_approved'
            ])

            count = 0
            for loan in LoanApplication.objects.filter(status__in=["approved", "rejected"]):
                try:
                    report = loan.mock_experian
                    user = loan.user

                    writer.writerow([
                        user.credit_score or 0,
                        report.credit_utilization_pct or 0,
                        report.dpd_max or 0,
                        report.emi_to_income_ratio or 0,
                        loan.monthly_income or 0,
                        int(loan.existing_loans),
                        1 if loan.status == "approved" else 0
                    ])
                    count += 1
                except Exception:
                    continue

        self.stdout.write(self.style.SUCCESS(f"✅ Exported {count} records to loan_training_data.csv"))
