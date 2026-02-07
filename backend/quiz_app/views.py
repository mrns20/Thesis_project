from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Concept, Question, StudentProgress, UserAnswerLog
from .serializers import ConceptSerializer, QuestionSerializer, UserSerializer
import random

# 1. Εγγραφή Χρήστη (Sign Up)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    data = request.data
    try:
        user = User.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )
        return Response(UserSerializer(user).data)
    except Exception as e:
        return Response({'error': str(e)}, status=400)

# 2. Το Dashboard (Ο Χάρτης Γνώσης)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_concept_map(request):
    concepts = Concept.objects.all()
    serializer = ConceptSerializer(concepts, many=True, context={'request': request})
    return Response(serializer.data)

# 3. Ο ΑΛΓΟΡΙΘΜΟΣ: "Δώσε μου την επόμενη ερώτηση"
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_next_question(request):
    user = request.user
    
    # ΒΗΜΑ 1: Βρες ποιο Concept πρέπει να μάθει τώρα
    # Ψάχνουμε το πρώτο concept που είναι ξεκλείδωτο αλλά ΟΧΙ τελειωμένο (mastery < 100%)
    concepts = Concept.objects.all()
    target_concept = None
    
    for concept in concepts:
        # Check mastery
        prog, _ = StudentProgress.objects.get_or_create(user=user, concept=concept)
        
        # Αν το ξέρει τέλεια, πάμε στο επόμενο
        if prog.mastery_level >= 1.0:
            continue
            
        # Check prerequisites (Απλοποιημένο: Αν δεν το έχει ξεκλειδώσει, δεν το δίνουμε)
        # Εδώ θα μπορούσαμε να βάλουμε λογική "γύρνα πίσω στα προαπαιτούμενα"
        
        target_concept = concept
        break
    
    # Αν έχει μάθει τα πάντα!
    if not target_concept:
        return Response({'message': 'Συγχαρητήρια! Έχεις τερματίσει την ύλη!', 'completed': True})

    # ΒΗΜΑ 2: Διάλεξε μια ερώτηση από αυτό το Concept
    # Που δεν την έχει απαντήσει σωστά ακόμα
    questions = Question.objects.filter(concept=target_concept)
    
    # Φιλτράρουμε αυτές που έχει ήδη απαντήσει σωστά
    # (Εδώ κάνουμε μια απλή επιλογή random για τώρα)
    question = random.choice(questions)
    
    serializer = QuestionSerializer(question)
    return Response(serializer.data)

# 4. ΥΠΟΒΟΛΗ ΑΠΑΝΤΗΣΗΣ & ΑΝΑΔΡΑΣΗ
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_answer(request):
    user = request.user
    q_id = request.data.get('question_id')
    selected = request.data.get('selected_option') # 'A', 'B', 'C', 'D'
    
    question = get_object_or_404(Question, id=q_id)
    is_correct = (selected == question.correct_option)
    
    # Καταγραφή στο Log
    UserAnswerLog.objects.create(
        user=user, question=question, selected_option=selected, is_correct=is_correct
    )
    
    # Ενημέρωση Προόδου (The Learning Model)
    progress, _ = StudentProgress.objects.get_or_create(user=user, concept=question.concept)
    progress.total_attempts += 1
    
    recommendation = None
    
    if is_correct:
        progress.correct_attempts += 1
        # Αύξηση Mastery (Απλή λογική: +20% για κάθε σωστή)
        progress.mastery_level = min(1.0, progress.mastery_level + 0.2)
        message = "Σωστά! Συνέχισε έτσι."
    else:
        # Μείωση Mastery (αν κάνει λάθος, ίσως ξέχασε κάτι)
        progress.mastery_level = max(0.0, progress.mastery_level - 0.1)
        message = "Λάθος."
        # ΕΔΩ ΕΙΝΑΙ Η ΕΞΥΠΝΑΔΑ: Του δίνουμε το Link να διαβάσει
        if question.concept.remedial_resource:
            recommendation = {
                'text': f"Φαίνεται να δυσκολεύεσαι με: {question.concept.name}.",
                'link': question.concept.remedial_resource
            }
            
    progress.save()
    
    return Response({
        'correct': is_correct,
        'correct_option': question.correct_option, # Τώρα του λέμε ποιο ήταν το σωστό
        'message': message,
        'new_mastery': int(progress.mastery_level * 100),
        'recommendation': recommendation
    })