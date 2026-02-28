from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 1. ΤΟ ΜΟΝΤΕΛΟ ΓΝΩΣΗΣ (Concept)
class Concept(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    # Ποια μαθήματα πρέπει να ξέρεις πριν δεις αυτό
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='unlocks')
    # Link βοηθείας αν κολλήσεις
    remedial_resource = models.URLField(blank=True, null=True, help_text="Link για θεωρία αν ο χρήστης κολλήσει")

    def __str__(self):
        return self.name

# 2. Η ΕΡΩΤΗΣΗ
class Question(models.Model):
    # Επιλογές Δυσκολίας
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    # Τύπος Ερώτησης
    TYPE_CHOICES = [
        ('MC', 'Πολλαπλής Επιλογής'),
        ('TF', 'Σωστό / Λάθος'),
    ]
    
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(help_text="Η εκφώνηση της ερώτησης")
    code_snippet = models.TextField(blank=True, null=True, help_text="Κώδικας Python (αν υπάρχει)")

    remedial_resource = models.URLField(blank=True, null=True, help_text="Link θεωρίας για διάβασμα")
    video_resource = models.URLField(blank=True, null=True, help_text="Link για βίντεο αν ο χρήστης είναι οπτικός τύπος")
    
    # ΝΕΟ: Επεξήγηση (Εμφανίζεται μετά την απάντηση)
    explanation = models.TextField(blank=True, null=True, help_text="Εμφανίζεται στον χρήστη μετά την απάντηση (π.χ. γιατί είναι σωστό/λάθος)")
    
    # ΝΕΟ: Βαθμός Δυσκολίας
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    
    question_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='MC')

    # Επιλογές Απαντήσεων
    option_a = models.CharField(max_length=200, help_text="Για Σωστό/Λάθος, βάλε 'Σωστό'")
    option_b = models.CharField(max_length=200, help_text="Για Σωστό/Λάθος, βάλε 'Λάθος'")
    option_c = models.CharField(max_length=200, blank=True, null=True)
    option_d = models.CharField(max_length=200, blank=True, null=True)
    
    # Ποια είναι η σωστή (A, B, C ή D)
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

    def __str__(self):
        return f"[{self.concept.name}] ({self.difficulty}) {self.text[:30]}..."

# 3. ΠΡΟΟΔΟΣ ΜΑΘΗΤΗ
class StudentProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    mastery_level = models.FloatField(default=0.0) # Από 0.0 έως 1.0 (100%)
    correct_attempts = models.IntegerField(default=0)
    total_attempts = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)
    
    # Πεδίο για το αν έχει "ξεκλειδώσει" το μάθημα (βάσει προαπαιτούμενων)
    is_unlocked = models.BooleanField(default=False) 

    class Meta:
        unique_together = ('user', 'concept')

    def __str__(self):
        status = "🔓" if self.is_unlocked else "🔒"
        return f"{status} {self.user.username} - {self.concept.name}: {int(self.mastery_level*100)}%"

# 4. ΙΣΤΟΡΙΚΟ ΑΠΑΝΤΗΣΕΩΝ (Log)
class UserAnswerLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1)
    is_correct = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} -> {self.question.id} ({'Correct' if self.is_correct else 'Wrong'})"

# 5. ΠΡΟΦΙΛ ΧΡΗΣΤΗ (User Profile)
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    first_login = models.BooleanField(default=True)
    learning_style = models.CharField(max_length=20, default='visual')

    def __str__(self):
        return self.user.username

# --- SIGNALS (Αυτοματισμοί) ---

# Όταν δημιουργείται User -> Φτιάξε αυτόματα UserProfile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

# Όταν σώζεται ο User -> Σώσε και το UserProfile
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Ελέγχουμε αν υπάρχει το profile πριν το σώσουμε (για αποφυγή λαθών)
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()


# backend/quiz_app/models.py

# Πρόσθεσε αυτό στο τέλος του models.py
class UserMistake(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question') # Για να μην αποθηκεύεται το ίδιο λάθος 100 φορές