from django.contrib import admin
from .models import MockKYCRecord, MockExperianReport
from django.utils.html import format_html
import json


@admin.register(MockKYCRecord)
class MockKYCAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'pan_number', 'aadhaar_last_4',
        'pan_verified', 'aadhaar_verified',
        'verification_status', 'created_at',
    )
    list_filter = ('pan_verified', 'aadhaar_verified', 'verification_status')
    search_fields = ('user__username', 'user__email', 'pan_number', 'aadhaar_last_4')
    readonly_fields = (
        'user', 'pan_number', 'pan_holder_name',
        'aadhaar_last_4', 'aadhaar_verified', 'dob',
        'kyc_type', 'verification_status', 'verification_source',
        'pretty_mock_response', 'created_at'
    )

    fieldsets = (
        ("KYC Data", {
            'fields': (
                'user', 'pan_number', 'pan_holder_name', 'aadhaar_last_4',
                'dob', 'pan_verified', 'aadhaar_verified',
                'verification_status', 'kyc_type', 'verification_source',
            )
        }),
        ("Raw Mock Response", {
            'fields': ('pretty_mock_response',)
        }),
        ("Meta", {
            'fields': ('created_at',)
        }),
    )

    def pretty_mock_response(self, obj):
        """
        Formats the mock_response field as a collapsible <details> block with JSON formatting.
        """
        if not obj or not obj.mock_response:
            return "-"

        try:
            formatted_json = json.dumps(obj.mock_response, indent=2, ensure_ascii=False)
            return format_html(
                '<details><summary>Click to expand</summary><pre style="white-space: pre-wrap;">{}</pre></details>',
                formatted_json
            )
        except (TypeError, ValueError) as e:
            return f"Invalid JSON format: {str(e)}"

    pretty_mock_response.short_description = "Mock API Response"


@admin.register(MockExperianReport)
class MockExperianReportAdmin(admin.ModelAdmin):
    list_display = (
        'loan_application', 'user', 'bureau_score', 'score_band',
        'total_accounts', 'overdue_accounts', 'dpd_max', 'created_at'
    )
    list_filter = ('score_band', 'report_status')
    search_fields = ('user__username', 'user__email', 'loan_application__id')
    readonly_fields = (
        'loan_application', 'user', 'bureau_score', 'score_band',
        'report_status', 'total_accounts', 'active_accounts',
        'overdue_accounts', 'dpd_max', 'credit_utilization_pct',
        'emi_to_income_ratio', 'pretty_tradelines', 'pretty_enquiries',
        'pretty_mock_raw_report', 'created_at'
    )

    fieldsets = (
        ("Report Summary", {
            'fields': (
                'loan_application', 'user', 'bureau_score', 'score_band', 'report_status',
                'total_accounts', 'active_accounts', 'overdue_accounts',
                'dpd_max', 'credit_utilization_pct', 'emi_to_income_ratio'
            )
        }),
        ("Details", {
            'fields': ('pretty_tradelines', 'pretty_enquiries')
        }),
        ("Raw Report", {
            'fields': ('pretty_mock_raw_report',)
        }),
        ("Meta", {
            'fields': ('created_at',)
        }),
    )

    def pretty_tradelines(self, obj):
        """
        Formats the tradelines field as a collapsible <details> block with JSON formatting.
        """
        if not obj or not obj.tradelines:
            return "-"

        try:
            formatted_json = json.dumps(obj.tradelines, indent=2, ensure_ascii=False)
            return format_html(
                '<details><summary>Tradelines</summary><pre style="white-space: pre-wrap;">{}</pre></details>',
                formatted_json
            )
        except (TypeError, ValueError) as e:
            return f"Invalid JSON format: {str(e)}"

    pretty_tradelines.short_description = "Tradelines"

    def pretty_enquiries(self, obj):
        """
        Formats the enquiries field as a collapsible <details> block with JSON formatting.
        """
        if not obj or not obj.enquiries:
            return "-"

        try:
            formatted_json = json.dumps(obj.enquiries, indent=2, ensure_ascii=False)
            return format_html(
                '<details><summary>Enquiries</summary><pre style="white-space: pre-wrap;">{}</pre></details>',
                formatted_json
            )
        except (TypeError, ValueError) as e:
            return f"Invalid JSON format: {str(e)}"

    pretty_enquiries.short_description = "Enquiries"

    def pretty_mock_raw_report(self, obj):
        """
        Formats the mock_raw_report field as a collapsible <details> block with JSON formatting.
        """
        if not obj or not obj.mock_raw_report:
            return "-"

        try:
            formatted_json = json.dumps(obj.mock_raw_report, indent=2, ensure_ascii=False)
            return format_html(
                '<details><summary>Raw Report</summary><pre style="white-space: pre-wrap;">{}</pre></details>',
                formatted_json
            )
        except (TypeError, ValueError) as e:
            return f"Invalid JSON format: {str(e)}"

    pretty_mock_raw_report.short_description = "Mock Raw API Report"
