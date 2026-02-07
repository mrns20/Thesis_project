from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    # Auth
    path('register/', views.register_user, name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # App Logic
    path('concept-map/', views.get_concept_map, name='concept-map'),
    path('question/next/', views.get_next_question, name='next-question'),
    path('submit/', views.submit_answer, name='submit-answer'),
]