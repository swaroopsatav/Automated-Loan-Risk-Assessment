"""
Management command to generate mock loan applications with AI-style approval/rejection logic.
This script creates realistic test data for loan applications with associated credit reports.
"""
from django.core.management.base import BaseCommand
from faker import Faker
import random
from decimal import Decimal, ROUND_HALF_UP

from users.models import CustomUser
from loanapplications.models import LoanApplication
from integrations.models import MockExperianReport

faker = Faker()


class Command(BaseCommand):
    help = "Generate mock loan applications with AI-style approval/rejection logic"

    def add_arguments(self, parser):
        parser.add_argument("count", type=int, help="Number of mock loans to create")
        parser.add_argument("--min-amount", type=int, default=50000, help="Minimum loan amount")
        parser.add_argument("--max-amount", type=int, default=1000000, help="Maximum loan amount")
        parser.add_argument("--auto-score-pct", type=int, default=30, 
                           help="Percentage of loans to create for auto-scoring (0-100)")

    def create_loan(self, user, amount_requested, term_months, purpose, monthly_income, existing_loans, approved, for_auto_scoring=False):
        """Create a loan application record with the given parameters."""
        if for_auto_scoring:
            # Create a loan application without ai_decision for auto-scoring
            return LoanApplication.objects.create(
                user=user,
                amount_requested=amount_requested,
                term_months=term_months,
                purpose=purpose,
                monthly_income=monthly_income,
                existing_loans=existing_loans,
                ai_decision=None,
                status=random.choice(["pending", "under_review"])
            )
        else:
            # Create a loan application with ai_decision already set
            return LoanApplication.objects.create(
                user=user,
                amount_requested=amount_requested,
                term_months=term_months,
                purpose=purpose,
                monthly_income=monthly_income,
                existing_loans=existing_loans,
                ai_decision="approve" if approved else "reject",
                status="approved" if approved else "rejected"
            )

    def create_experian_report(self, user, loan, credit_score, dpd, credit_util, emi_ratio, total_accounts, active_accounts, overdue_accounts):
        """Create a mock Experian credit report for the given loan and user."""
        amount_requested = loan.amount_requested
        return MockExperianReport.objects.create(
            user=user,
            loan_application=loan,
            bureau_score=credit_score,
            score_band="high" if credit_score >= 750 else "medium" if credit_score >= 650 else "low",
            report_status="mocked",
            total_accounts=total_accounts,
            active_accounts=active_accounts,
            overdue_accounts=overdue_accounts,
            dpd_max=dpd,
            credit_utilization_pct=credit_util,
            emi_to_income_ratio=float(emi_ratio),
            tradelines=[
                {"account_type": "credit_card", "dpd": dpd},
                {"account_type": "personal_loan", "dpd": 0}
            ],
            enquiries=[
                {"type": "loan", "amount": float(amount_requested * Decimal('0.1'))}
            ],
            mock_raw_report={
                "bureau_score": credit_score,
                "assessment_date": faker.date_this_year().isoformat(),
                "report_number": faker.uuid4()
            }
        )

    def handle(self, *args, **options):
        """Main command logic for generating mock loan applications."""

        count = options["count"]
        min_amount = options["min_amount"]
        max_amount = options["max_amount"]
        auto_score_pct = options["auto_score_pct"]

        # Validate parameters
        if count <= 0:
            self.stdout.write(self.style.ERROR("Count must be greater than zero"))
            return

        if min_amount <= 0:
            self.stdout.write(self.style.ERROR("Minimum amount must be greater than zero"))
            return

        if max_amount <= 0:
            self.stdout.write(self.style.ERROR("Maximum amount must be greater than zero"))
            return

        if min_amount >= max_amount:
            self.stdout.write(self.style.ERROR("Minimum amount must be less than maximum amount"))
            return

        if auto_score_pct < 0 or auto_score_pct > 100:
            self.stdout.write(self.style.ERROR("Auto-score percentage must be between 0 and 100"))
            return

        users = list(CustomUser.objects.filter(is_kyc_verified=True, credit_score__isnull=False))

        if not users:
            self.stdout.write("❌ No eligible users with credit_score and KYC verification found.\n")
            return

        created = 0
        created_for_auto_scoring = 0
        self.stdout.write(f"🚀 Generating {count} mock loan applications...")

        for i in range(count):
            user = random.choice(users)

            # Generate mock loan details with more realistic ranges
            amount_requested = Decimal(random.randint(min_amount, max_amount)).quantize(Decimal('0.01'), ROUND_HALF_UP)
            term_months = random.choice([12, 24, 36, 48, 60])

            if user.annual_income:
                monthly_income = Decimal(user.annual_income / 12).quantize(Decimal('0.01'), ROUND_HALF_UP)
            else:
                monthly_income = Decimal(random.randint(20000, 100000)).quantize(Decimal('0.01'), ROUND_HALF_UP)

            existing_loans = random.choice([True, False])
            purpose = random.choice(["home", "education", "business", "medical", "personal"])

            # Generate mock Experian-like report values with weighted probabilities
            dpd_choices = [0, 30, 60, 90]
            dpd_weights = [0.7, 0.2, 0.07, 0.03]  # 70% chance of 0 DPD
            dpd = random.choices(dpd_choices, dpd_weights)[0]

            credit_util = round(random.uniform(0, 100), 2)
            monthly_emi = (amount_requested / Decimal(term_months)).quantize(Decimal('0.01'), ROUND_HALF_UP)
            emi_ratio = (monthly_emi / monthly_income).quantize(Decimal('0.01'), ROUND_HALF_UP)

            # Enhanced AI-style approval logic
            approved = all([
                user.credit_score >= 700,  # Good credit score
                emi_ratio < Decimal('0.5'),  # EMI should be less than 50% of income
                credit_util < 80,  # Credit utilization under 80%
                dpd <= 30,  # Max 30 days past due acceptable
                monthly_income >= Decimal('15000'),  # Minimum income requirement
                amount_requested <= (monthly_income * Decimal(term_months) * Decimal('0.8'))  # Loan amount sanity check
            ])

            # Determine if this loan should be created for auto-scoring
            for_auto_scoring = random.randint(1, 100) <= auto_score_pct

            # Create LoanApplication instance
            loan = self.create_loan(
                user=user,
                amount_requested=amount_requested,
                term_months=term_months,
                purpose=purpose,
                monthly_income=monthly_income,
                existing_loans=existing_loans,
                approved=approved,
                for_auto_scoring=for_auto_scoring
            )

            if for_auto_scoring:
                created_for_auto_scoring += 1

            # Create MockExperianReport with more realistic data
            total_accounts = random.randint(1, 15)
            active_accounts = random.randint(1, min(total_accounts, 10))
            overdue_accounts = random.randint(0, min(3, active_accounts)) if dpd > 0 else 0

            self.create_experian_report(
                user=user,
                loan=loan,
                credit_score=user.credit_score,
                dpd=dpd,
                credit_util=credit_util,
                emi_ratio=emi_ratio,
                total_accounts=total_accounts,
                active_accounts=active_accounts,
                overdue_accounts=overdue_accounts
            )

            created += 1

            if created % 100 == 0:
                self.stdout.write(f"Created {created} mock loans...")

        self.stdout.write(f"✅ Created {created} mock loans with approval labels.\n")
        if created_for_auto_scoring > 0:
            self.stdout.write(f"✅ {created_for_auto_scoring} of these loans were created for auto-scoring (ai_decision=None).\n")
