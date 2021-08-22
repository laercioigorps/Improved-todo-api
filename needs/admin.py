from django.contrib import admin

from .models import Need, Goal, Step, Delivery, Iteration

# Register your models here.

admin.site.register(Need)
admin.site.register(Goal)
admin.site.register(Step)
admin.site.register(Delivery)
admin.site.register(Iteration)

