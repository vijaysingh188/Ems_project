from rest_framework import serializers
from .models import Lift,Floor,LiftDetails

class LiftSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lift
        fields = ['liftname']

class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Floor
        fields = ['floornumber']


class LiftDetailsSerializer(serializers.ModelSerializer):
    lift_det = LiftSerializer() 
    class Meta:
        model = LiftDetails
        fields = ['lift_det']

        # fields = ['lift_det','whichfloor','runnning','door_status','move_status','lift_status','current_status']
