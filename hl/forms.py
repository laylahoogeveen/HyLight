from django import forms
from django.forms import ModelForm
from .models import Profile, Skill, StudyProgramme, Question, Comment
from django.contrib.auth.models import User

class RegisterForm1(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        '''Dynamic placeholders for all form fields'''
        super(RegisterForm1, self).__init__(*args, **kwargs)

        for f in self.fields:
            self.fields[f].widget.attrs['placeholder'] = self.fields[f].label
            self.fields[f].required = False
            self.fields[f].help_text = False

    confirm_password = forms.CharField(label="Confirm password", required=False,
                            widget=forms.PasswordInput(attrs={
                                'class': 'form-control',
                                'required': 'True' 
                                }))
    class Meta:
        model = User
  
        fields = ['first_name', 'last_name', 'username', 'email', 'password']
        widgets= {}
        for f in fields:
            widgets[f] = forms.TextInput(attrs={
                                        'class': 'form-control',
                                        'required': 'True',})

        widgets['password'] = forms.PasswordInput(attrs={
                                    'class': 'form-control',
                                    'required': 'True' 
                                    })


    def clean(self):
        
        cleaned_data = super(RegisterForm1, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        email = cleaned_data.get("email")
        errors = {}

        if User.objects.filter(email=email) and email != "":
            errors['email'] = "E-mail address already in use."

        if len(password) > 0:
            if len(password) < 8:
                errors['password'] = ["Password should contain at least 8 characters"]

            if any(char.isdigit() for char in password) == False:
                if "password" in errors:
                    errors['password'].append("Password should contain at least 1 number")
                else: 
                    errors['password'] = ["Password should contain at least 1 number"]

            if password != confirm_password:
                if "password" in errors:
                    errors['password'].append("Passwords do not match")
                else: 
                    errors['password'] = "Passwords do not match"

        if errors:
            raise forms.ValidationError(errors)
        
class RegisterForm2(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        '''Dynamic placeholders for all form fields'''
        super(RegisterForm2, self).__init__(*args, **kwargs)

        for f in self.fields:
            self.fields[f].required = False
            self.fields[f].help_text = False
            self.fields[f].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Profile

        fields = ['current_studies', 'past_studies', 'bio', 'title']
        widgets = {}
        widgets['bio'] = forms.Textarea(attrs={
                                        'required': 'True',
                                        'placeholder': 'Briefly describe yourself and your interests.'})
        widgets['title'] = forms.TextInput(attrs={
                                        'required': 'True',
                                        'placeholder': 'Your current study programme/most important skill'})
        widgets['current_studies'] = forms.CheckboxSelectMultiple()
        widgets['past_studies'] = forms.CheckboxSelectMultiple()

class RegisterForm3(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('skills',)
        widgets = {}
        widgets['skills'] = forms.CheckboxSelectMultiple()

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        '''Dynamic placeholders for all form fields'''
        super(ProfileForm, self).__init__(*args, **kwargs)

        for f in self.fields:
            self.fields[f].required = False
            self.fields[f].help_text = False
            self.fields[f].widget.attrs['class'] = 'default_value availability'

    class Meta:
        model = Profile
        fields = ['available', 'location']
        widgets = {}
        # widgets['available'] = forms.RadioSelect()

class QuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        '''Dynamic placeholders for all form fields'''
        super(QuestionForm, self).__init__(*args, **kwargs)

        for f in self.fields:
            self.fields[f].required = False
            self.fields[f].help_text = False
            self.fields['skills'].widget.attrs['class'] = 'li ul question django-select2'
            self.fields['study'].widget.attrs['class'] = 'li ul question django-select2'
            self.fields['online'].widget.attrs['class'] = 'switch-button-checkbox'

    class Meta:
        model = Question
  
        fields = [ 'title', 'study', 'description', 'skills', 'online']
        widgets= {}
        widgets['description'] = forms.Textarea(attrs={
                                        'required': 'True',
                                         'class': 'form-control question_area question',
                                        'placeholder': 'Description of your question. Try to include relevant details.'})
        widgets['title'] = forms.TextInput(attrs={
                                        'class': 'form-control-sm form-control question',
                                        'required': 'True',
                                        'placeholder': 'Title of your question'})

        
        widgets['skills'] = forms.SelectMultiple()
        widgets['study'] = forms.SelectMultiple()


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        '''Dynamic placeholders for all form fields'''
        super(CommentForm, self).__init__(*args, **kwargs)

        for f in self.fields:
            self.fields[f].required = False
            self.fields[f].help_text = False

    class Meta:
        model = Comment
  
        fields = ('description', )
        widgets= {}
        widgets['description'] = forms.Textarea(attrs={
                                        'required': 'True',
                                         'class': 'form-control comment_area',
                                        'placeholder': 'Your comment on this'\
                                                        ' question. This could'\
                                                        ' be an answer/solution or a clarifying question'})

class ChangeQuestionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        '''Dynamic placeholders for all form fields'''
        super(ChangeQuestionForm, self).__init__(*args, **kwargs)

        for f in self.fields:
            self.fields[f].required = False
            self.fields[f].help_text = False
            self.fields['status'].widget.attrs['class'] = 'remove radio'
            self.fields['online'].widget.attrs['class'] = 'switch-button-checkbox'
            # self.fields['title'].initial = self.get_formtitle
            # form = form

    # def get_form(self):
    #     form = self.form_class(instance=self.object)
    #     return form

    class Meta:
        model = Question
  
        fields = ['status', 'title', 'description', 'online',]
        widgets= {}
        widgets['description'] = forms.Textarea(attrs={
                                        'required': 'True',
                                         'class': 'form-control question_area question default_value',
                                        'placeholder': 'Description of your question. Try to include relevant details.'})
        widgets['title'] = forms.TextInput(attrs={
                                        'class': 'form-control-sm form-control question default_value',
                                        'required': 'True',
                                        'placeholder': 'Title of your question'})

        widgets['status'] = forms.RadioSelect()


class ChangeAvailability(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        '''Dynamic placeholders for all form fields'''
        super(ChangeAvailability, self).__init__(*args, **kwargs)

        for f in self.fields:
            self.fields[f].required = False
            self.fields[f].help_text = False
            self.fields[f].widget.attrs['class'] = 'default_value availability'
            # self.fields['online'].widget.attrs['class'] = 'switch-button-checkbox'
            # self.fields['title'].initial = self.get_formtitle

    class Meta:
        model = Profile
  
        fields = ['available', 'location']
        


