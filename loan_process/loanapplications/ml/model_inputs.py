def extract_features_from_mock(mock_report):
    if not mock_report:
        raise ValueError("mock_report cannot be None")

    try:
        return {
            'bureau_score': int(mock_report.bureau_score or 0),
            'credit_utilization_pct': float(mock_report.credit_utilization_pct or 0),
            'dpd_max': int(mock_report.dpd_max or 0),
            'emi_to_income_ratio': float(mock_report.emi_to_income_ratio or 0),
            'total_accounts': int(mock_report.total_accounts or 0),
            'overdue_accounts': int(mock_report.overdue_accounts or 0),
        }
    except (AttributeError, ValueError, TypeError) as e:
        raise ValueError(f"Invalid mock_report object or invalid data: {str(e)}")
