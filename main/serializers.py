from rest_framework import serializers

from .models import Company, Vehicle, PartType, Part, PartWheel, Repair, RepairWheel, Checklist, ChecklistQuestion


# class DynamicModelSerializer(serializers.ModelSerializer):
#     # https://stackoverflow.com/questions/37445248/how-to-dynamically-change-depth-in-django-rest-framework-nested-serializers
#     """
#     A ModelSerializer that takes an additional `fields` argument that
#     controls which fields should be displayed (displays all if not present),
#     takes in a `exclude` argument that controls which fields should be excluded,
#     and takes in a `nested` argument to return nested serializers (sets depth to 1)
#     """

#     def __init__(self, *args, **kwargs):
#         fields = kwargs.pop("fields", None)
#         exclude = kwargs.pop("exclude", None)
#         nested = kwargs.pop("nested", None)

#         if nested is not None:
#             if nested == True:
#                 self.Meta.depth = 1

#         super().__init__(*args, **kwargs)

#         if fields is not None:
#             # Drop any fields that are not specified in the `fields` argument.
#             allowed = set(fields)
#             existing = set(self.fields.keys())
#             for field_name in existing - allowed:
#                 self.fields.pop(field_name)

#         if exclude is not None:
#             for field_name in exclude:
#                 self.fields.pop(field_name)



class CompanySerializer(serializers.ModelSerializer):
    url_name = 'company'
    class Meta:
        model = Company
        depth = 1
        fields = '__all__'

class PartTypeSerializer(serializers.ModelSerializer):
    url_name = 'part_type'
    class Meta:
        model = PartType
        depth = 1
        fields = '__all__'

class PartSerializer(serializers.ModelSerializer):
    url_name = 'part'
    class Meta:
        model = Part
        depth = 0
        fields = '__all__'

class PartWheelSerializer(serializers.ModelSerializer):
    url_name = 'part_wheel'
    class Meta:
        model = PartWheel
        depth = 0
        fields = '__all__'

class VehicleSerializer(serializers.ModelSerializer):
    url_name = 'vehicle'
    parts = PartSerializer(source='part_set', many=True, read_only=True)
    part_wheels = PartWheelSerializer(source='partwheel_set', many=True, read_only=True)
    class Meta:
        model = Vehicle
        depth = 1
        fields = '__all__'

class RepairSerializer(serializers.ModelSerializer):
    url_name = 'repair'
    class Meta:
        model = Repair
        depth = 1
        fields = '__all__'

class RepairWheelSerializer(serializers.ModelSerializer):
    url_name = 'repair_wheel'
    class Meta:
        model = RepairWheel
        depth = 1
        fields = '__all__'

class ChecklistSerializer(serializers.ModelSerializer):
    url_name = 'checklist'
    class Meta:
        model = Checklist
        depth = 1
        fields = '__all__'

class ChecklistQuestionSerializer(serializers.ModelSerializer):
    url_name = 'checklist_question'
    class Meta:
        model = ChecklistQuestion
        depth = 1
        fields = '__all__'