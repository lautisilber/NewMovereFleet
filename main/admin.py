from django.contrib import admin

from .models import Company, Vehicle, PartWithoutLifespanAbs, PartTyreAbs, PartWithoutLifespanAbs, PartWithLifespan, PartTyre, PartWithoutLifespan

import sys, inspect
def print_classes():
    for name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            if hasattr(obj, 'Meta'):
                if hasattr(obj.Meta, 'abstract'):
                    if obj.Meta == True:
                        continue
            admin.site.register(obj)

# admin.site.register(Company)
# admin.site.register(Vehicle)
# admin.site.register(QuestionTemplate)
# admin.site.register(QuestionInstance)
# admin.site.register(AnswerSession)
# admin.site.register(QuestionType)
# admin.site.register(PartType)
# admin.site.register(Part)
# admin.site.register(PartWheel)
# admin.site.register(Repair)
# admin.site.register(RepairWheel)