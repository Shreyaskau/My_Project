from rest_framework import serializers

from .models import SubscriptionPlan, SchoolSubscription


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'price_cents', 'max_students', 'max_teachers', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class SchoolSubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchoolSubscription
        fields = [
            'id', 'school', 'plan', 'is_active', 'current_period_start', 'current_period_end',
            'external_customer_id', 'external_subscription_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']





