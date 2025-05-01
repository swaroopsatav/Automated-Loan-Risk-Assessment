from rest_framework import generics, permissions, status
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import RiskSnapshot, RiskTrend, ModelPerformanceLog
from .serializers import (
    RiskSnapshotSerializer,
    RiskTrendSerializer,
    ModelPerformanceLogSerializer
)
from rest_framework.permissions import IsAdminUser
from django.core.exceptions import ValidationError


# --- RiskSnapshot: Daily stats summary ---
class RiskSnapshotListView(generics.ListAPIView):
    serializer_class = RiskSnapshotSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['snapshot_date', 'model_version']
    ordering_fields = ['snapshot_date', 'total_applications', 'avg_risk_score']

    def get_queryset(self):
        return RiskSnapshot.objects.all().select_related().order_by('-snapshot_date')


# --- RiskTrend: Time series for charts ---
class RiskTrendListView(generics.ListAPIView):
    serializer_class = RiskTrendSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['date', 'model_version']
    ordering_fields = ['date', 'avg_score', 'approval_rate', 'rejection_rate']

    def get_queryset(self):
        queryset = RiskTrend.objects.all()
        model_version = self.request.query_params.get('model_version', None)
        if model_version:
            queryset = queryset.filter(model_version=model_version)
        return queryset.select_related().order_by('date')


# --- ModelPerformanceLog: Audit of model metrics --- 
class ModelPerformanceLogListView(generics.ListAPIView):
    serializer_class = ModelPerformanceLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['model_version']
    ordering_fields = ['timestamp', 'accuracy', 'precision', 'recall', 'auc_score']

    def get_queryset(self):
        return ModelPerformanceLog.objects.all().select_related().order_by('-timestamp')


# --- Optional: Admin can add performance logs ---
class ModelPerformanceLogCreateView(generics.CreateAPIView):
    serializer_class = ModelPerformanceLogSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
