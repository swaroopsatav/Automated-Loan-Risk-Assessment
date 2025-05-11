"""
Management command to run all management commands in sequence.
This script executes all the management commands in the correct order to set up and process loan data.
"""
from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.utils.timezone import now
import logging
import time

# Get logger
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Run all management commands in sequence"

    def add_arguments(self, parser):
        """
        Add command-line arguments for controlling the execution.
        """
        parser.add_argument(
            '--mock-count', type=int, default=100,
            help='Number of mock records to generate (default: 100)'
        )
        parser.add_argument(
            '--skip-training', action='store_true',
            help='Skip the model training step'
        )
        parser.add_argument(
            '--verbose', action='store_true',
            help='Show detailed output from each command'
        )
        parser.add_argument(
            '--mock-only', action='store_true',
            help='Run only the mock data generation commands (generate_mock_users, generate_mock_loans, generate_mock_data)'
        )

    def handle(self, *args, **options):
        """
        Main logic for running all commands in sequence.
        """
        mock_count = options['mock_count']
        skip_training = options['skip_training']
        verbose = options['verbose']
        mock_only = options['mock_only']

        start_time = now()

        if mock_only:
            self.stdout.write(self.style.SUCCESS(f"🚀 Starting mock data generation commands at {start_time}"))

            try:
                # Step 1: Generate mock users
                self.stdout.write(self.style.NOTICE("\n[1/3] Generating mock users..."))
                call_command('generate_mock_users', mock_count)

                # Step 2: Generate mock loans
                self.stdout.write(self.style.NOTICE("\n[2/3] Generating mock loan applications..."))
                call_command('generate_mock_loans', mock_count)

                # Step 3: Generate mock KYC and Experian data
                self.stdout.write(self.style.NOTICE("\n[3/3] Generating mock KYC and Experian data..."))
                call_command('generate_mock_data', mock_count, verbose=verbose)

                # Calculate execution time
                end_time = now()
                duration = (end_time - start_time).total_seconds()
                minutes, seconds = divmod(duration, 60)

                # Final success message
                self.stdout.write(self.style.SUCCESS(
                    f"\n✅ Mock data generation commands completed successfully in {int(minutes)} minutes and {int(seconds)} seconds!"
                ))

                return
            except Exception as e:
                self.stderr.write(
                    self.style.ERROR(f"❌ An error occurred during mock data generation: {str(e)}")
                )
                logger.error(f"Error in run_all_commands (mock-only mode): {str(e)}", exc_info=True)
                return

        # Run all commands if --mock-only is not specified
        self.stdout.write(self.style.SUCCESS(f"🚀 Starting command sequence at {start_time}"))

        try:
            # Step 1: Generate mock KYC and Experian data
            self.stdout.write(self.style.NOTICE("\n[1/6] Generating mock KYC and Experian data..."))
            call_command('generate_mock_data', mock_count, verbose=verbose)

            # Step 2: Generate mock loan applications
            self.stdout.write(self.style.NOTICE("\n[2/6] Generating mock loan applications..."))
            call_command('generate_mock_loans', mock_count)

            # Step 3: Score loan applications using AI models
            self.stdout.write(self.style.NOTICE("\n[3/6] Scoring loan applications..."))
            call_command('score_and_record', '--all')

            # Step 4: Run compliance checks
            self.stdout.write(self.style.NOTICE("\n[4/6] Running compliance checks..."))
            call_command('run_compliance_checks', '--update')

            # Step 5: Export training data
            self.stdout.write(self.style.NOTICE("\n[5/6] Exporting training data..."))
            call_command('export_training_data')

            # Step 6: Train loan models (optional)
            if not skip_training:
                self.stdout.write(self.style.NOTICE("\n[6/6] Training loan models..."))
                call_command('train_loan_model')
            else:
                self.stdout.write(self.style.WARNING("\n[6/6] Skipping model training (--skip-training flag used)"))

            # Calculate execution time
            end_time = now()
            duration = (end_time - start_time).total_seconds()
            minutes, seconds = divmod(duration, 60)

            # Final success message
            self.stdout.write(self.style.SUCCESS(
                f"\n✅ All commands completed successfully in {int(minutes)} minutes and {int(seconds)} seconds!"
            ))

        except Exception as e:
            self.stderr.write(
                self.style.ERROR(f"❌ An error occurred during command execution: {str(e)}")
            )
            logger.error(f"Error in run_all_commands: {str(e)}", exc_info=True)
            return
