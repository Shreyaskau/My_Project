from django.db import models


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price_cents = models.PositiveIntegerField(default=0)
    max_students = models.PositiveIntegerField(default=0)
    max_teachers = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name


class SchoolSubscription(models.Model):
    school = models.OneToOneField('schools.School', on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.PROTECT, related_name='subscriptions')
    is_active = models.BooleanField(default=True)
    current_period_start = models.DateTimeField(null=True, blank=True)
    current_period_end = models.DateTimeField(null=True, blank=True)
    external_customer_id = models.CharField(max_length=255, blank=True, null=True)
    external_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.school} -> {self.plan}"

# Create your models here.
