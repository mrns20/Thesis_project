from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Concept, Question, StudentProgress, UserProfile

# 1. USER SERIALIZER
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

# 2. CONCEPT SERIALIZER
class ConceptSerializer(serializers.ModelSerializer):
    mastery = serializers.SerializerMethodField()
    is_unlocked = serializers.SerializerMethodField()

    class Meta:
        model = Concept
        fields = ['id', 'name', 'description', 'mastery', 'is_unlocked', 'remedial_resource']

    def get_mastery(self, obj):
        # Επιστρέφει το ποσοστό γνώσης (0-100)
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return 0
        try:
            p = StudentProgress.objects.get(user=request.user, concept=obj)
            return int(p.mastery_level * 100)
        except StudentProgress.DoesNotExist:
            return 0

    def get_is_unlocked(self, obj):
        # Ελέγχει προαπαιτούμενα
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return True 
        
        # Αν δεν έχει προαπαιτούμενα -> Ανοιχτό
        if not obj.prerequisites.exists():
            return True
            
        # Πρέπει να έχεις >50% σε όλα τα προαπαιτούμενα
        for prereq in obj.prerequisites.all():
            try:
                p = StudentProgress.objects.get(user=request.user, concept=prereq)
                if p.mastery_level < 0.5:
                    return False
            except StudentProgress.DoesNotExist:
                return False
        return True

# 3. QUESTION SERIALIZER (Η ΜΕΓΑΛΗ ΑΛΛΑΓΗ)
class QuestionSerializer(serializers.ModelSerializer):
    # Φτιάχνουμε ένα τεχνητό πεδίο 'options' που δεν υπάρχει στη βάση
    options = serializers.SerializerMethodField()
    remedial_resource = serializers.CharField(source='concept.remedial_resource', read_only=True)
    class Meta:
        model = Question
        # ΠΡΟΣΟΧΗ: Δεν στέλνουμε το 'correct_option' ούτε το 'explanation' εδώ!
        # Στέλνουμε μόνο ό,τι χρειάζεται για να εμφανιστεί η ερώτηση.
        fields = ['id', 'concept', 'text', 'code_snippet', 'question_type', 'difficulty', 'options', 'remedial_resource']

    def get_options(self, obj):
        # Πακετάρουμε τις επιλογές σε λίστα για το React
        choices = [
            {'id': 'A', 'text': obj.option_a},
            {'id': 'B', 'text': obj.option_b},
        ]
        # Προσθέτουμε C και D μόνο αν υπάρχουν (δεν είναι κενά)
        if obj.option_c:
            choices.append({'id': 'C', 'text': obj.option_c})
        if obj.option_d:
            choices.append({'id': 'D', 'text': obj.option_d})
            
        return choices

# 4. USER PROFILE SERIALIZER
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'phone', 'first_login']