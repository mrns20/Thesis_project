

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
from .models import Concept, Question, StudentProgress 
from .models import UserMistake,UserAnswerLog


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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_concept_map(request):
    concepts = Concept.objects.all()
    serializer = ConceptSerializer(concepts, many=True, context={'request': request})
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_next_question(request):
    user = request.user
    
    requested_id = request.query_params.get('concept_id')
    active_concept = None

    if requested_id:
        
        active_concept = get_object_or_404(Concept, id=requested_id)
        progress, _ = StudentProgress.objects.get_or_create(user=user, concept=active_concept)
        
        
        if not progress.is_unlocked:
            prereqs_met = True
            for req in active_concept.prerequisites.all():
                req_prog = StudentProgress.objects.filter(user=user, concept=req).first()
                if not req_prog or req_prog.mastery_level < 0.5:
                    prereqs_met = False
                    break
            
            if prereqs_met:
                progress.is_unlocked = True
                progress.save()
            else:
                 return Response({'message': 'This module is locked.'}, status=403)
        

        if progress.mastery_level >= 1.0:
            return Response({
                'message': 'Course completed!',
                'concept': active_concept.id,
                'options': None
            }, status=200)

    else:
        concepts = Concept.objects.all().order_by('id')
        for concept in concepts:
            progress, created = StudentProgress.objects.get_or_create(user=user, concept=concept)
            
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
    
    if active_concept is None:
        last_progress = StudentProgress.objects.filter(user=user).order_by('-last_updated').first()
        last_id = last_progress.concept.id if last_progress else None
        
        return Response({
            'message': 'Course completed!',
            'concept': last_id,
            'options': None
        }, status=200)

    all_questions = Question.objects.filter(concept=active_concept)
    
    correctly_answered_ids = UserAnswerLog.objects.filter(
        user=user, 
        question__concept=active_concept,
        is_correct=True
    ).values_list('question_id', flat=True)
    
    candidates = all_questions.exclude(id__in=correctly_answered_ids)
    
    if not candidates.exists():
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_answer(request):
    question_id = request.data.get('question_id')
    selected_option = request.data.get('selected_option')
    user = request.user

    
    question = get_object_or_404(Question, id=question_id)
    
    is_correct = (selected_option == question.correct_option)
    if not is_correct:
        UserMistake.objects.get_or_create(user=user, question=question)

    
    
    explanation = question.explanation 
    if not explanation:
        explanation = "Σωστή απάντηση!" if is_correct else f"Η σωστή απάντηση ήταν η {question.correct_option}."

    
    UserAnswerLog.objects.create(
        user=user,
        question=question,
        selected_option=selected_option,
        is_correct=is_correct
    )

    # --- ΥΠΟΛΟΓΙΣΜΟΣ MASTERY ---
    
    
    total_questions_count = Question.objects.filter(concept=question.concept).count()
    
    correct_answers_count = UserAnswerLog.objects.filter(
        user=user,
        question__concept=question.concept,
        is_correct=True
    ).values('question_id').distinct().count()

    if total_questions_count > 0:
        new_mastery = correct_answers_count / total_questions_count
    else:
        new_mastery = 1.0 # Αν δεν υπάρχουν ερωτήσεις, το θεωρούμε τελειωμένο

    
    StudentProgress.objects.update_or_create(
        user=user,
        concept=question.concept,
        defaults={
            'mastery_level': new_mastery,
            
        }
    )

    return Response({
        'correct': is_correct,
        'explanation': explanation,
        'new_mastery': new_mastery
    })



# Ανάκτηση και Ενημέρωση Προφίλ
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    profile, created = UserProfile.objects.get_or_create(user=user)

    if request.method == 'GET':
        
        return Response({
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'bio': profile.bio,
            'phone': profile.phone,
            'learning_style': getattr(profile, 'learning_style', 'visual'),
            'first_login': getattr(profile, 'first_login', False),
        })

    elif request.method == 'POST':
        data = request.data
        
        
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            user.email = data['email']
        user.save()

        
        profile.bio = data.get('bio', profile.bio)
        profile.phone = data.get('phone', profile.phone) 
        if 'learning_style' in data:
            profile.learning_style = data['learning_style']

        
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

    # Για να μπορεί ο αλγόριθμος να ξαναεπιλέξει τις ίδιες ερωτήσεις
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

    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def submit_quiz(request):
    user = request.user
    concept_id = request.data.get('concept_id')
    score = request.data.get('score')

    try:
       
        progress, created = StudentProgress.objects.get_or_create(
            user=user, 
            concept_id=concept_id
        )
        
        if score > progress.mastery:
            progress.mastery = score
        progress.save()

        next_concept_id = None
        
        
        if score >= 50:
            
            next_concept = Concept.objects.filter(id__gt=concept_id).order_by('id').first()
            
            if next_concept:
                
                next_prog, _ = StudentProgress.objects.get_or_create(user=user, concept=next_concept)
                next_prog.is_unlocked = True
                next_prog.save()
                
                
                next_concept_id = next_concept.id

        return Response({
            'message': 'Quiz completed', 
            'score': score,
            'next_concept_id': next_concept_id 
        }, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mistake_links(request):
    user = request.user
    mistakes = UserMistake.objects.filter(user=user).select_related('question')
    
    
    try:
        user_profile = UserProfile.objects.get(user=user)
        learning_style = user_profile.learning_style
    except UserProfile.DoesNotExist:
        learning_style = 'visual'

    
    links_data = []
    for m in mistakes:
        link = getattr(m.question, 'remedial_resource', "") or ""
        video_link = getattr(m.question, 'video_resource', "") or ""
        
        links_data.append({
            'question': m.question.text,
            'link': link,
            'video_link': video_link,
            'learning_style': learning_style
        })

    
    
    
    total_unique_answered = UserAnswerLog.objects.filter(user=user).values('question').distinct().count()
    
    evaluation = {
        "score": 0,
        "message": "Δεν υπάρχουν αρκετά δεδομένα για αξιολόγηση. Λύσε μερικά quiz ακόμα!"
    }

    if total_unique_answered > 0:
        penalty = 0.0
        
        
        for m in mistakes:
            diff = m.question.difficulty
            if diff == 'easy':
                penalty += 1.5   # Μεγάλη ποινή στα εύκολα
            elif diff == 'medium':
                penalty += 1.0   # Κανονική ποινή στα μεσαία
            elif diff == 'hard':
                penalty += 0.5   # Μικρή ποινή στα δύσκολα
            else:
                penalty += 1.0

        
        raw_score = 100.0 - ((penalty / total_unique_answered) * 100.0)
        final_score = max(0.0, min(100.0, raw_score)) 
        
        
        if final_score >= 80:
            msg = " Άριστο επίπεδο! Τα λάθη σου είναι ελάχιστα ή αφορούν κυρίως πολύ δύσκολες ερωτήσεις."
        elif final_score >= 50:
            msg = " Σε καλό δρόμο! Έχεις κατανοήσει τα βασικά, αλλά χρειάζεται λίγη επανάληψη στις μεσαίες δυσκολίες."
        else:
            msg = " Χρειάζεται προσοχή. Έχεις αρκετά κενά, ίσως και σε βασικές έννοιες."

        evaluation = {
            "score": round(final_score),
            "message": msg
        }

    
    return Response({
        "links": links_data,
        "evaluation": evaluation
    }, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reset_global_progress(request):
    user = request.user
    
    
    StudentProgress.objects.filter(user=user).delete()
    
    
    UserMistake.objects.filter(user=user).delete()
    
    
    
    if 'UserAnswerLog' in globals():
        UserAnswerLog.objects.filter(user=user).delete()

    return Response({'message': 'Όλα τα δεδομένα προόδου διαγράφηκαν επιτυχώς.'}, status=200)