from django.contrib import admin
from .models import Concept, Question, StudentProgress, UserProfile, UserMistake

# Εμφάνιση των πινάκων στο Admin panel
admin.site.register(Concept)
admin.site.register(Question)
admin.site.register(StudentProgress)
admin.site.register(UserProfile)
admin.site.register(UserMistake)

# Αν έχεις και το UserAnswerLog στο models.py, βγάλε το σχόλιο από την παρακάτω γραμμή:
from .models import UserAnswerLog
admin.site.register(UserAnswerLog)