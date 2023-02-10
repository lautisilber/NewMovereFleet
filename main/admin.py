from django.contrib import admin

from .models import Company, Vehicle, PartType, Part, PartWheel

admin.site.register(Company)
admin.site.register(Vehicle)
admin.site.register(PartType)
admin.site.register(Part)
admin.site.register(PartWheel)