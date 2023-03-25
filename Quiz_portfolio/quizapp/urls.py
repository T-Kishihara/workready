from django.urls import path
from .views import QuizListView, QuizDetailView, MakeQuizView, DeleteQuizView
from . import views

app_name = 'quiz_app'


urlpatterns = [
    path('quiz_list', QuizListView.as_view(), name='quiz_list'),
    path('quiz_detail/<int:pk>', QuizDetailView.as_view(), name='quiz_detail'),
    path('make_quiz', MakeQuizView.as_view(), name='make_quiz'),
    path('edit_quiz/<int:id>', views.edit_quiz, name='edit_quiz'),
    path('delete_quiz/<int:pk>', DeleteQuizView.as_view(), name='delete_quiz'),
    path('make_choice/<int:pk>', views.make_inline_formset, name='make_choice'),
    path('result/<int:pk>', views.display_result, name='result'),
]
