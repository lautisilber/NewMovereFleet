from django.contrib import admin

from .models import Company, Vehicle, PartType, Part, PartWheel, Repair, RepairWheel, CheckupForm, CheckupQuestion

admin.site.register(Company)
admin.site.register(Vehicle)
admin.site.register(PartType)
admin.site.register(Part)
admin.site.register(PartWheel)
admin.site.register(Repair)
admin.site.register(RepairWheel)
admin.site.register(CheckupForm)
admin.site.register(CheckupQuestion)