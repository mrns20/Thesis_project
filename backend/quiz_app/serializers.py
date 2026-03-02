from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Concept, Question, StudentProgress, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ConceptSerializer(serializers.ModelSerializer):
    mastery = serializers.SerializerMethodField()
    is_unlocked = serializers.SerializerMethodField()

    class Meta:
        model = Concept
        fields = ['id', 'name', 'description', 'mastery', 'is_unlocked', 'remedial_resource']

    def get_mastery(self, obj):
        
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return 0
        try:
            p = StudentProgress.objects.get(user=request.user, concept=obj)
            return int(p.mastery_level * 100)
        except StudentProgress.DoesNotExist:
            return 0

    def get_is_unlocked(self, obj):
        
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return True 
        
        
        if not obj.prerequisites.exists():
            return True
            
        
        for prereq in obj.prerequisites.all():
            try:
                p = StudentProgress.objects.get(user=request.user, concept=prereq)
                if p.mastery_level < 0.5:
                    return False
            except StudentProgress.DoesNotExist:
                return False
        return True

class QuestionSerializer(serializers.ModelSerializer):
    
    options = serializers.SerializerMethodField()
    remedial_resource = serializers.CharField(source='concept.remedial_resource', read_only=True)
    class Meta:
        model = Question
        

        fields = ['id', 'concept', 'text', 'code_snippet', 'question_type', 'difficulty', 'options', 'remedial_resource']

    def get_options(self, obj):
        
        choices = [
            {'id': 'A', 'text': obj.option_a},
            {'id': 'B', 'text': obj.option_b},
        ]
        
        if obj.option_c:
            choices.append({'id': 'C', 'text': obj.option_c})
        if obj.option_d:
            choices.append({'id': 'D', 'text': obj.option_d})
            
        return choices


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'phone', 'first_login']