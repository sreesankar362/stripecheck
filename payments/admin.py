from django.contrib import admin

from payments.models import Membership,UserSubscription,Payment

# Register your models here.
admin.site.register(Membership)
admin.site.register(UserSubscription)
admin.site.register(Payment)


