from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.db import models


class Membership(models.Model):
    membership_days = models.IntegerField(default=7)
    price = models.PositiveIntegerField(default=0)
    stripe_id = models.CharField(max_length=100 ,null=True, blank=True)

    def __str__(self):
        return str(self.membership_days)


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.payment_id)


class UserSubscription(models.Model):
    user = models.ForeignKey(User, related_name='sub_user', on_delete=models.CASCADE)
    membership = models.ForeignKey(Membership, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)

    def is_active(self, obj):
        return date.today() < obj.end_date
