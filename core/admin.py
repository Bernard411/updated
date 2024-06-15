from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Medicine)
admin.site.register(HealthRecord)
admin.site.register(UserProfile)
admin.site.register(Alert)
admin.site.register(Device)

