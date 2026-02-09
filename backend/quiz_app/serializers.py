from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Concept, Question, StudentProgress
from .models import UserProfile # Μην ξεχάσεις το import

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
        # Επιστρέφει το ποσοστό γνώσης του χρήστη για αυτό το concept
        user = self.context.get('request').user
        if user.is_anonymous: return 0
        try:
            p = StudentProgress.objects.get(user=user, concept=obj)
            return int(p.mastery_level * 100)
        except StudentProgress.DoesNotExist:
            return 0

    def get_is_unlocked(self, obj):
        # Ελέγχει αν ο χρήστης έχει περάσει τα προαπαιτούμενα
        user = self.context.get('request').user
        if user.is_anonymous: return True # Για demo
        
        # Αν δεν έχει προαπαιτούμενα, είναι ανοιχτό
        if not obj.prerequisites.exists():
            return True
            
        # Ελέγχουμε αν έχει mastery > 50% σε όλα τα προαπαιτούμενα
        for prereq in obj.prerequisites.all():
            try:
                p = StudentProgress.objects.get(user=user, concept=prereq)
                if p.mastery_level < 0.5:
                    return False
            except StudentProgress.DoesNotExist:
                return False
        return True

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        # ΠΡΟΣΟΧΗ: Δεν στέλνουμε το 'correct_option' στο frontend για να μην κλέβουν!
        fields = ['id', 'text', 'code_snippet', 'question_type', 'difficulty', 
                  'option_a', 'option_b', 'option_c', 'option_d']
        

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'phone', 'first_login']       