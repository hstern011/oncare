from rest_framework import serializers

from .models import Revision, Visit

# Define how a model class is displayed in the API response
class VisitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visit
        fields = ['public_id', 'create_date_time', 'start_date_time', 'end_date_time', 'client','carer']

class RevisionSerializer(serializers.ModelSerializer):
    visit_set = VisitSerializer(many=True)
    
    class Meta:
        model = Revision
        fields = '__all__'