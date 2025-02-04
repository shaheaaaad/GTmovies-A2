from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import SecurityQuestion

class UserRegistrationForm(UserCreationForm):
    security_question = forms.ChoiceField(choices=SecurityQuestion.SECURITY_QUESTIONS)
    security_answer = forms.CharField(widget=forms.PasswordInput, label="Security Answer")

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2", "security_question", "security_answer"]

    def save(self, commit=True):
        """Saves user and security question securely"""
        user = super().save(commit=False)
        if commit:
            user.save()

            # Save security question securely
            security_question = SecurityQuestion(
                user=user,
                question=self.cleaned_data["security_question"]
            )
            security_question.set_answer(self.cleaned_data["security_answer"])  # Hash answer before saving
            security_question.save()
        return user


class SecurityQuestionForm(forms.ModelForm):
    answer = forms.CharField(widget=forms.PasswordInput, label="Security Answer")

    class Meta:
        model = SecurityQuestion
        fields = ["question", "answer"]

    def save(self, commit=True):
        """Hashes the security answer before saving."""
        security_question = super().save(commit=False)
        security_question.set_answer(self.cleaned_data["answer"])  # Hash answer before saving
        if commit:
            security_question.save()
        return security_question
