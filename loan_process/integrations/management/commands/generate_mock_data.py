"""
Management command to generate mock KYC and Experian data for eligible users and loans.
This script creates realistic mock data for testing and development purposes.
"""
from django.core.management.base import BaseCommand
from faker import Faker
import random
from collections.abc import Sequence

from users.models import CustomUser
from loanapplications.models import LoanApplication
from integrations.models import MockKYCRecord, MockExperianReport

faker = Faker()

class Command(BaseCommand):
    help = 'Generate mock KYC and Experian data for eligible users and loans'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='Number of mock records to generate')
        parser.add_argument('--verbose', action='store_true', help='Show detailed logs per record')

    def get_eligible_records(self) -> tuple[Sequence[CustomUser], Sequence[LoanApplication]]:
        """Get eligible users and loan applications that don't have mock records yet"""
        eligible_users = list(CustomUser.objects.exclude(
            id__in=MockKYCRecord.objects.values_list('user_id', flat=True)
        ))
        eligible_loans = list(LoanApplication.objects.exclude(
            id__in=MockExperianReport.objects.values_list('loan_application_id', flat=True)
        ))
        return eligible_users, eligible_loans

    def create_mock_kyc(self, user: CustomUser) -> MockKYCRecord:
        """Create mock KYC record and update user compliance fields"""
        # Update user to pass compliance
        user.is_kyc_verified = True
        user.id_proof = "mock_id.pdf"
        user.address_proof = "mock_address.pdf"
        user.income_proof = "mock_income.pdf"
        user.save(update_fields=["is_kyc_verified", "id_proof", "address_proof", "income_proof"])

        return MockKYCRecord.objects.create(
            user=user,
            pan_number=faker.bothify(text='?????####?').upper(),
            pan_holder_name=faker.name().upper(),
            pan_verified=True,
            aadhaar_last_4=str(faker.random_int(min=1000, max=9999)),
            aadhaar_verified=True,
            dob=faker.date_of_birth(minimum_age=21, maximum_age=60),
            kyc_type='full',
            verification_status='verified',
            verification_source="mock_provider",
            mock_response={"mock": "kyc_data", "timestamp": faker.iso8601()}
        )

    def create_mock_experian(self, user: CustomUser, loan: LoanApplication) -> MockExperianReport:
        """Create mock Experian report for a user and loan"""
        score = random.randint(300, 850)
        dpd = random.choice([0, 30, 60, 90])
        util = round(random.uniform(5, 90), 2)

        active_accounts = random.randint(0, 10)
        total_accounts = active_accounts + random.randint(0, 5)
        overdue_accounts = min(random.randint(0, 4), active_accounts)

        return MockExperianReport.objects.create(
            user=user,
            loan_application=loan,
            bureau_score=score,
            score_band=self.get_score_band(score),
            report_status="mocked",
            total_accounts=total_accounts,
            active_accounts=active_accounts,
            overdue_accounts=overdue_accounts,
            dpd_max=dpd,
            credit_utilization_pct=util,
            emi_to_income_ratio=round(random.uniform(0.1, 1.5), 2),
            tradelines=[
                {
                    "account_type": random.choice(["credit_card", "personal_loan", "home_loan"]),
                    "dpd": dpd,
                    "outstanding": random.randint(1000, 100000)
                } for _ in range(active_accounts)
            ],
            enquiries=[
                {
                    "type": random.choice(["loan", "credit_card"]),
                    "amount": random.randint(10000, 500000),
                    "date": faker.date_this_year().isoformat()
                } for _ in range(random.randint(0, 3))
            ],
            mock_raw_report={
                "bureau_score": score,
                "report_date": faker.date_this_month().isoformat()
            }
        )

    @staticmethod
    def get_score_band(score: int) -> str:
        """Determine credit score band"""
        if score < 550:
            return "low"
        elif score < 700:
            return "medium"
        return "high"

    def handle(self, *args, **options):
        count = options['count']
        verbose = options['verbose']

        eligible_users, eligible_loans = self.get_eligible_records()

        if not eligible_users:
            self.stdout.write(self.style.ERROR("❌ No eligible users available for mock KYC data generation."))
            return

        if not eligible_loans:
            self.stdout.write(self.style.ERROR("❌ No eligible loans available for mock Experian data generation."))
            return

        max_records = min(len(eligible_users), len(eligible_loans), count)
        if max_records == 0:
            self.stdout.write(self.style.ERROR("❌ No records can be generated with the current data."))
            return

        self.stdout.write(f"🚀 Generating {max_records} mock KYC and Experian records...")

        try:
            for i in range(max_records):
                user = eligible_users[i]
                loan = eligible_loans[i]

                kyc = self.create_mock_kyc(user)
                experian = self.create_mock_experian(user, loan)

                if verbose:
                    self.stdout.write(
                        f"✅ User {user.username} → Loan #{loan.id} → "
                        f"KYC Status: {kyc.verification_status} → Score: {experian.bureau_score}"
                    )

            self.stdout.write(self.style.SUCCESS(
                f"🎉 Successfully created {max_records} mock KYC + Experian records."
            ))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Error generating mock data: {str(e)}"))
            return
