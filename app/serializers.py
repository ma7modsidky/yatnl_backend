from asyncore import read
from dataclasses import fields
from random import choices
from rest_framework import serializers
from .models import Leader
from users.models import NewUser
from .utils import LEADER_TYPES

class MainAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewUser
        fields = ['id','user_name', 'email']

class LeaderSerializer(serializers.ModelSerializer):
    leader_type = serializers.ChoiceField(choices=LEADER_TYPES)
    # main_account = MainAccountSerializer()
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Leader.objects.all(), required=False)
    parent_relation_numbre = serializers.IntegerField(read_only=True)
    children_count = serializers.IntegerField(read_only=True)
    points = serializers.IntegerField(read_only=True)
    earnings = serializers.IntegerField(read_only=True)
    
    def to_representation(self, instance):
        self.fields['main_account'] = MainAccountSerializer(read_only=True)
        return super().to_representation(instance)
        
    # def create(self, validated_data):
    #     main_account = validated_data.get('main_account', None)
    #     print(main_account)
    #     instance = self.Meta.model(**validated_data)
    #     if main_account is not None:
    #         instance.save()
    #     return instance

    class Meta:
        model = Leader
        fields = ['id','leader_type', 'main_account', 'parent',
                  'parent_relation_numbre', 'children_count', 'points', 'earnings', 'uuid', 'get_next_relation', 'is_eligible','is_same_type', 'created' , 'bonus_from']
        # depth = 1

class LeaderRetrieveSerializer(serializers.ModelSerializer):
    leader_type = serializers.ChoiceField(choices=LEADER_TYPES)
    main_account = MainAccountSerializer(read_only=True)
    parent = serializers.PrimaryKeyRelatedField(
        queryset=Leader.objects.all(), required=False)
    parent_relation_numbre = serializers.IntegerField(required=False)
    children_count = serializers.IntegerField(required=False)
    points = serializers.IntegerField(required=False)
    earnings = serializers.IntegerField(required=False)

    class Meta:
        model = Leader
        fields = ['leader_type', 'main_account', 'parent',
                  'parent_relation_numbre', 'children_count', 'points', 'earnings', 'uuid']

