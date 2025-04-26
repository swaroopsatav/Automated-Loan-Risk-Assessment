from django.urls import path
from .views import (
    RiskSnapshotListView,
    RiskTrendListView,
    ModelPerformanceLogListView,
    ModelPerformanceLogCreateView,
)

app_name = 'riskdashboards'

urlpatterns = [
    # List of risk snapshots 
    path('snapshots/', RiskSnapshotListView.as_view(), name='snapshots'),

    # List of risk trends over time
    path('trends/', RiskTrendListView.as_view(), name='trends'),

    # Model performance endpoints
    path('models/', ModelPerformanceLogListView.as_view(), name='model-list'),
    path('models/create/', ModelPerformanceLogCreateView.as_view(), name='model-create'),
]
