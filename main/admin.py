from django.contrib import admin

from .models import \
    (
        Company,
        Vehicle,
        PartAbsProxy,
        PartWithLifespanAbs,
        PartTyreAbs,
        PartWithoutLifespanAbs,
        PartProxy,
        PartWithLifespan,
        PartTyre,
        PartWithoutLifespan,
        PartChangeNotice,
        PartFix,
        FormGroup,
        FormAbs,
        Form,
        QuestionGroup,
        QuestionAbs,
        Question
    )
from .forms import \
    (
        PartWithLifespanAbsForm, PartTyreAbsForm, PartWithoutLifespanAbsForm,
        PartWithLifespanForm, PartTyreForm, PartWithoutLifespanForm
    )

admin.site.register(Company)
admin.site.register(Vehicle)

class PartAbsProxyModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_object', 'object_id', 'content_type']
admin.site.register(PartAbsProxy, PartAbsProxyModelAdmin)

class PartWithLifespanAbsModelAdmin(admin.ModelAdmin):
    form = PartWithLifespanAbsForm
admin.site.register(PartWithLifespanAbs, PartWithLifespanAbsModelAdmin)

class PartTyreAbsModelAdmin(admin.ModelAdmin):
    form = PartTyreAbsForm
admin.site.register(PartTyreAbs, PartTyreAbsModelAdmin)

class PartWithoutLifespanAbsModelAdmin(admin.ModelAdmin):
    form = PartWithoutLifespanAbsForm
admin.site.register(PartWithoutLifespanAbs, PartWithoutLifespanAbsModelAdmin)

class PartProxyModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_object', 'object_id', 'content_type']
admin.site.register(PartProxy, PartProxyModelAdmin)

class PartWithLifespanModelAdmin(admin.ModelAdmin):
    form = PartWithLifespanForm
admin.site.register(PartWithLifespan, PartWithLifespanModelAdmin)

class PartTyreModelAdmin(admin.ModelAdmin):
    form = PartTyreForm
admin.site.register(PartTyre, PartTyreModelAdmin)

class PartWithoutLifespanModelAdmin(admin.ModelAdmin):
    form = PartWithoutLifespanForm
admin.site.register(PartWithoutLifespan, PartWithoutLifespanModelAdmin)