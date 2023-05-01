from django.contrib import admin

from .models import Company, Vehicle, QuestionTemplate, QuestionInstance, QuestionAnswerSession #PartType, Part, PartWheel, Repair, RepairWheel
                    
admin.site.register(Company)
admin.site.register(Vehicle)
admin.site.register(QuestionTemplate)
admin.site.register(QuestionInstance)
admin.site.register(QuestionAnswerSession)
# admin.site.register(PartType)
# admin.site.register(Part)
# admin.site.register(PartWheel)
# admin.site.register(Repair)
# admin.site.register(RepairWheel)