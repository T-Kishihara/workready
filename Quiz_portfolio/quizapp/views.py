from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.views.generic.edit import (
    DeleteView, CreateView
)
from django.urls import reverse_lazy
from .forms import MakeQuizForm, EditQuizForm
import os
from .models import(
    Quiz, Choices
)
from django import forms

# Create your views here.
class QuizListView(ListView):
    model = Quiz
    template_name = os.path.join('quizapp', 'quiz_list.html')

class QuizDetailView(DetailView):
    model = Quiz
    template_name = os.path.join('quizapp', 'quiz_detail.html')

class MakeQuizView(LoginRequiredMixin, CreateView):
    template_name = os.path.join('quizapp', 'make_quiz.html')
    form_class = MakeQuizForm
    success_url = reverse_lazy('quiz_app:quiz_list')

    def form_valid(self, form):
        form.user = self.request.user
        return super().form_valid(form)
    
class DeleteQuizView(LoginRequiredMixin,DeleteView):
    model = Quiz
    template_name = os.path.join('quizapp', 'delete_quiz.html')
    success_url = reverse_lazy('quiz_app:quiz_list')

@login_required
def make_inline_formset(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    ChoiceFormSet = forms.inlineformset_factory(
            parent_model=Quiz,
            model=Choices,
            fields=('sentence','is_correct','description',),
            extra=4,
            max_num=4,
            can_delete=False,
    )
    if request.method == 'POST':
        formset = ChoiceFormSet(
            data=request.POST, 
            instance=quiz,
            queryset=Choices.objects.none()
        )
        if formset.is_valid():
            choice = quiz.choices_set.all()
            choice.delete()
            formset.save()
            return redirect('quiz_app:quiz_list')
    else:
        formset = ChoiceFormSet(
                instance=quiz,
                queryset=Choices.objects.none(),
        )
    return render(request, 'quizapp/make_choice.html', {'formset': formset})


def display_result(request, pk):
    choice = Choices.objects.get(pk=pk)
    return render(request, 'quizapp/display_result.html', {'choice': choice})

@login_required
def edit_quiz(request, id):
    quiz = get_object_or_404(Quiz, id=id)
    if quiz.created_by.id != request.user.id:
        return Http404
    edit_quiz_form = EditQuizForm(request.POST or None, instance=quiz)
    if edit_quiz_form.is_valid():
        edit_quiz_form.save()
        return redirect('quiz_app:quiz_list')
    return render(request, 'quizapp/edit_quiz.html', {'edit_quiz_form':edit_quiz_form})