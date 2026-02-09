from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 1. ΤΟ ΜΟΝΤΕΛΟ ΓΝΩΣΗΣ
class Concept(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='unlocks')
    remedial_resource = models.URLField(blank=True, null=True, help_text="Link για θεωρία αν ο χρήστης κολλήσει")

    def __str__(self):
        return self.name

# 2. Η ΕΡΩΤΗΣΗ (Πολλαπλής ή Σωστό/Λάθος)
class Question(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    TYPE_CHOICES = [
        ('MC', 'Πολλαπλής Επιλογής'),
        ('TF', 'Σωστό / Λάθος'),
    ]
    
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField(help_text="Η εκφώνηση της ερώτησης")
    code_snippet = models.TextField(blank=True, null=True, help_text="Κώδικας Python (αν υπάρχει)")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    
    # Τύπος Ερώτησης
    question_type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='MC')

    # Επιλογές: Τα C και D είναι πλέον προαιρετικά
    option_a = models.CharField(max_length=200, help_text="Για Σωστό/Λάθος, βάλε 'Σωστό'")
    option_b = models.CharField(max_length=200, help_text="Για Σωστό/Λάθος, βάλε 'Λάθος'")
    option_c = models.CharField(max_length=200, blank=True, null=True)
    option_d = models.CharField(max_length=200, blank=True, null=True)
    
    correct_option = models.CharField(max_length=1, choices=[('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D')])

    def __str__(self):
        return f"[{self.concept.name}] ({self.question_type}) {self.text[:30]}..."

# 3. ΠΡΟΟΔΟΣ ΜΑΘΗΤΗ
class StudentProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='progress')
    concept = models.ForeignKey(Concept, on_delete=models.CASCADE)
    mastery_level = models.FloatField(default=0.0)
    correct_attempts = models.IntegerField(default=0)
    total_attempts = models.IntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'concept')

    def __str__(self):
        return f"{self.user.username} - {self.concept.name}: {int(self.mastery_level*100)}%"

# 4. ΙΣΤΟΡΙΚΟ
class UserAnswerLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1)
    is_correct = models.BooleanField()
    timestamp = models.DateTimeField(auto_now_add=True)


# ... (Τα υπόλοιπα μοντέλα σου Concept, Question κλπ μένουν ως έχουν) ...

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    # ΑΥΤΟ ΕΙΝΑΙ ΤΟ ΚΛΕΙΔΙ:
    first_login = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username

# Αυτόματος μηχανισμός: Όταν φτιάχνεται User, φτιάχνει και UserProfile
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()