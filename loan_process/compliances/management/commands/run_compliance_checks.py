from django.core.management.base import BaseCommand
from django.utils.timezone import now
from django.db import transaction

from compliances.models import ComplianceCheck
from users.models import CustomUser
from loanapplications.models import LoanApplication


class Command(BaseCommand):
    """
    Management command to run compliance checks on loans and users.
    This script checks for KYC verification and required document submissions for loan applications.
    """
    help = "Run compliance checks on loans and users"

    def add_arguments(self, parser):
        """
        Adds command-line arguments for the compliance check script.
        """
        parser.add_argument(
            '--update', action='store_true',
            help='Update ComplianceCheck records in the database'
        )
        parser.add_argument(
            '--limit', type=int, default=1000,
            help='Limit the number of loans to check (default: 1000)'
        )

    def check_compliance(self, user):
        """
        Check user compliance and return issues list
        """
        issues = []

        if not user.is_kyc_verified:
            issues.append("KYC not verified")

        missing_docs = []
        required_docs = {
            'id_proof': 'ID Proof',
            'address_proof': 'Address Proof',
            'income_proof': 'Income Proof'
        }

        for field, doc_name in required_docs.items():
            if not getattr(user, field):
                missing_docs.append(doc_name)

        if missing_docs:
            issues.append(f"Missing documents: {', '.join(missing_docs)}")

        return issues

    def handle(self, *args, **options):
        """
        Main logic for running compliance checks.
        """
        update_mode = options['update']
        limit = options['limit']

        try:
            # Retrieve loan applications (limited by the `limit` argument)
            loans = (LoanApplication.objects
                     .select_related('user')
                     .order_by("-submitted_at")[:limit])

            total, compliant = 0, 0

            with transaction.atomic():
                for loan in loans:
                    user = loan.user
                    issues = self.check_compliance(user)
                    is_compliant = len(issues) == 0

                    if update_mode:
                        try:
                            ComplianceCheck.objects.update_or_create(
                                loan_application=loan,
                                defaults={
                                    "user": user,
                                    "is_compliant": is_compliant,
                                    "review_notes": "\n".join(issues) if issues else "All checks passed",
                                }
                            )
                        except Exception as e:
                            self.stderr.write(
                                self.style.ERROR(
                                    f"❌ Failed to update ComplianceCheck for Loan #{loan.id}: {str(e)}"
                                )
                            )
                            continue

                    if is_compliant:
                        compliant += 1
                    total += 1

            # Print summary
            if total > 0:
                percentage = (compliant / total) * 100
            else:
                percentage = 0

            self.stdout.write(
                self.style.SUCCESS(
                    f"✅ Checked {total} loans — {compliant} compliant ({percentage:.1f}%)"
                )
            )
            if not update_mode:
                self.stdout.write(
                    self.style.WARNING("⚠️ No records were updated. Use --update to save compliance results.")
                )

        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"❌ An error occurred: {str(e)}")
            )
