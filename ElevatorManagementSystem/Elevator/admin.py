from django.contrib import admin
from .models import Lift,Floor,LiftDetails

# Register your models here.
admin.site.register(Lift)
admin.site.register(Floor)
admin.site.register(LiftDetails)