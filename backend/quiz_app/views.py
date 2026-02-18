from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Concept, Question, StudentProgress, UserAnswerLog
from .serializers import ConceptSerializer, QuestionSerializer, UserSerializer
import random
from django.contrib.auth.models import User
from .models import UserProfile
from .serializers import UserProfileSerializer

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
    
    # 1. ΕΛΕΓΧΟΣ: Ζήτησε ο χρήστης συγκεκριμένο μάθημα;
    requested_id = request.query_params.get('concept_id')
    active_concept = None

    if requested_id:
        # Αν ζήτησε συγκεκριμένο, προσπαθούμε να βρούμε αυτό
        active_concept = get_object_or_404(Concept, id=requested_id)
        
        # Ελέγχουμε αν είναι ξεκλειδωμένο
        progress, _ = StudentProgress.objects.get_or_create(user=user, concept=active_concept)
        if not progress.is_unlocked:
             return Response({'message': 'This module is locked.'}, status=403)
             
        # Αν είναι ολοκληρωμένο (Mastery 100%), στέλνουμε μήνυμα τέλους
        if progress.mastery_level >= 1.0:
            return Response({
                'message': 'Course completed!',
                'concept': active_concept.id, # Στέλνουμε το ID πίσω
                'options': None
            }, status=200)

    else:
        # 2. ADAPTIVE LOGIC (Αν δεν ζήτησε συγκεκριμένο)
        concepts = Concept.objects.all().order_by('id')
        for concept in concepts:
            progress, created = StudentProgress.objects.get_or_create(user=user, concept=concept)
            
            # Auto-Unlock Logic
            if not progress.is_unlocked:
                prereqs_met = True
                for req in concept.prerequisites.all():
                    req_prog = StudentProgress.objects.filter(user=user, concept=req).first()
                    if not req_prog or req_prog.mastery_level < 0.5:
                        prereqs_met = False
                        break
                if prereqs_met:
                    progress.is_unlocked = True
                    progress.save()
                else:
                    return Response({'message': 'Previous modules not completed yet.'}, status=403)

            if progress.mastery_level < 1.0:
                active_concept = concept
                break
    
    # 3. ΑΝ ΔΕΝ ΒΡΕΘΗΚΕ ΕΝΕΡΓΟ CONCEPT
    if active_concept is None:
        # Αν μας ζήτησε ID αλλά ήταν completed, το χειριστήκαμε πάνω.
        # Αν δεν μας ζήτησε και δεν βρέθηκε τίποτα, σημαίνει όλα τέλος.
        last_progress = StudentProgress.objects.filter(user=user).order_by('-last_updated').first()
        last_id = last_progress.concept.id if last_progress else None
        
        return Response({
            'message': 'Course completed!',
            'concept': last_id,
            'options': None
        }, status=200)

    # 4. ΕΠΙΛΟΓΗ ΕΡΩΤΗΣΗΣ (Για το active_concept)
    all_questions = Question.objects.filter(concept=active_concept)
    
    correctly_answered_ids = UserAnswerLog.objects.filter(
        user=user, 
        question__concept=active_concept,
        is_correct=True
    ).values_list('question_id', flat=True)
    
    candidates = all_questions.exclude(id__in=correctly_answered_ids)
    
    if not candidates.exists():
         # Αν δεν υπάρχουν ερωτήσεις αλλά το mastery < 1.0
         # Φέρνουμε όλες για επανάληψη
         candidates = all_questions

    attempted_ids = UserAnswerLog.objects.filter(
        user=user,
        question__concept=active_concept
    ).values_list('question_id', flat=True)
    
    fresh_questions = candidates.exclude(id__in=attempted_ids)
    
    if fresh_questions.exists():
        question = random.choice(list(fresh_questions))
    elif candidates.exists():
        question = random.choice(list(candidates))
    else:
        return Response({'message': 'No questions found.'}, status=404)

    serializer = QuestionSerializer(question)
    return Response(serializer.data)

# 4. ΥΠΟΒΟΛΗ ΑΠΑΝΤΗΣΗΣ & ΑΝΑΔΡΑΣΗ
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_answer(request):
    question_id = request.data.get('question_id')
    selected_option = request.data.get('selected_option')
    user = request.user

    # 1. Βρες την ερώτηση
    question = get_object_or_404(Question, id=question_id)
    
    # 2. Έλεγχος αν είναι σωστό
    is_correct = (selected_option == question.correct_option)
    
    # 3. Επεξήγηση (Αν υπάρχει στη βάση, αλλιώς default κείμενο)
    explanation = question.explanation 
    if not explanation:
        explanation = "Σωστή απάντηση!" if is_correct else f"Η σωστή απάντηση ήταν η {question.correct_option}."

    # 4. Καταγραφή στο Ιστορικό (Log)
    UserAnswerLog.objects.create(
        user=user,
        question=question,
        selected_option=selected_option,
        is_correct=is_correct
    )

    # --- ΥΠΟΛΟΓΙΣΜΟΣ MASTERY (ΠΡΟΟΔΟΥ) ---
    
    # Α. Πόσες ερωτήσεις έχει συνολικά αυτό το Concept;
    total_questions_count = Question.objects.filter(concept=question.concept).count()
    
    # Β. Πόσες ΜΟΝΑΔΙΚΕΣ ερωτήσεις έχει απαντήσει ΣΩΣΤΑ ο χρήστης σε αυτό το concept;
    correct_answers_count = UserAnswerLog.objects.filter(
        user=user,
        question__concept=question.concept,
        is_correct=True
    ).values('question_id').distinct().count()

    # Γ. Υπολογισμός ποσοστού (π.χ. 2 σωστές στις 4 ερωτήσεις = 0.5 mastery)
    if total_questions_count > 0:
        new_mastery = correct_answers_count / total_questions_count
    else:
        new_mastery = 1.0 # Αν δεν υπάρχουν ερωτήσεις, το θεωρούμε τελειωμένο

    # Δ. Ενημέρωση της προόδου
    StudentProgress.objects.update_or_create(
        user=user,
        concept=question.concept,
        defaults={
            'mastery_level': new_mastery,
            # Αν θες να κρατάς και πόσες προσπάθειες έκανε συνολικά:
            # 'total_attempts': F('total_attempts') + 1 
        }
    )

    return Response({
        'correct': is_correct,
        'explanation': explanation,
        'new_mastery': new_mastery
    })

# from .models import UserProfile from .serializers import UserProfileSerializer

# Ανάκτηση και Ενημέρωση Προφίλ
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'GET':
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    elif request.method == 'POST':
        # Ενημέρωση στοιχείων
        profile.bio = request.data.get('bio', profile.bio)
        profile.phone = request.data.get('phone', profile.phone)

        # ΣΗΜΑΝΤΙΚΟ: Μόλις πατήσει αποθήκευση, δεν είναι πια "πρώτη φορά"
        profile.first_login = False 
        profile.save()

        return Response({'message': 'Το προφίλ ενημερώθηκε!', 'first_login': False})
    
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def restart_concept(request):
    user = request.user
    concept_id = request.data.get('concept_id')
    
    if not concept_id:
        return Response({'error': 'Concept ID is required'}, status=400)

    # 1. Μηδενισμός Προόδου (StudentProgress)
    try:
        progress = StudentProgress.objects.get(user=user, concept_id=concept_id)
        progress.mastery_level = 0.0
        progress.correct_attempts = 0
        progress.total_attempts = 0
        progress.save()
    except StudentProgress.DoesNotExist:
        pass # Αν δεν υπάρχει πρόοδος, δεν πειράζει

    # 2. Διαγραφή Ιστορικού Απαντήσεων (UserAnswerLog)
    # Για να μπορεί ο αλγόριθμος να ξανα-επιλέξει τις ίδιες ερωτήσεις
    UserAnswerLog.objects.filter(user=user, question__concept_id=concept_id).delete()

    return Response({'message': 'Concept reset successfully'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_concept_history(request, concept_id):
    """Επιστρέφει το ιστορικό απαντήσεων του χρήστη για ένα concept"""
    user = request.user
    
    # Βρίσκουμε όλες τις απαντήσεις του χρήστη για αυτό το concept
    logs = UserAnswerLog.objects.filter(
        user=user, 
        question__concept_id=concept_id
    ).select_related('question')

    history_data = []
    for log in logs:
        history_data.append({
            'questionText': log.question.text,
            'userAnswer': log.selected_option,
            'isCorrect': log.is_correct,
            # Αν είναι σωστό, μήνυμα επιτυχίας, αλλιώς την εξήγηση
            'explanation': log.question.explanation if log.question.explanation else ("Σωστή απάντηση!" if log.is_correct else "Λάθος απάντηση."),
            'remedialLink': log.question.concept.remedial_resource if not log.is_correct else None
        })
    
    return Response(history_data)