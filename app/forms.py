from django import forms
from django.contrib.auth.models import User
from app.models import Question, Answer


MAX_USERNAME_LENGTH = 50
MAX_PASSWORD_LENGTH = 20


class LoginForm(forms.Form):
    username = forms.CharField(max_length=MAX_USERNAME_LENGTH,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
                               error_messages={'required': 'Input login'})

    password = forms.CharField(max_length=MAX_PASSWORD_LENGTH,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '******'}),
                               error_messages={'required': 'Input password'})


class SignupForm(forms.Form):
    username = forms.CharField(max_length=MAX_USERNAME_LENGTH,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Логин'}),
                               error_messages={'required': 'Введите логин'})

    password = forms.CharField(max_length=MAX_PASSWORD_LENGTH,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}),
                               error_messages={'required': 'Введите пароль'})

    confirm_password = forms.CharField(max_length=MAX_PASSWORD_LENGTH,
                                       widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                         'placeholder': 'Input password'}),
                                       error_messages={'required': 'Confirm your password'})

    nickname = forms.CharField(max_length=MAX_USERNAME_LENGTH,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nick on the site'}),
                               error_messages={'required': 'Input nick'})

    profile_pic = forms.ImageField(required=False,
                                   widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'user-avatar'}))

    def clean_username(self):
        cleaned_data = super(SignupForm, self).clean()
        if User.objects.filter(username=cleaned_data['username']).exists():
            raise forms.ValidationError('This login has already exist')

        return cleaned_data['username']

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()

        password = cleaned_data['password']
        confirm_password = cleaned_data['confirm_password']
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords dont match')

        return cleaned_data


class EditForm(forms.Form):
    username = forms.CharField(max_length=MAX_USERNAME_LENGTH,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Login'}),
                               error_messages={'required': 'Input login'})

    nickname = forms.CharField(max_length=MAX_USERNAME_LENGTH,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nick on the site'}),
                               error_messages={'required': 'Input nick'})

    profile_pic = forms.ImageField(required=False,
                                   widget=forms.FileInput(attrs={'class': 'custom-file-input', 'id': 'user-avatar'}))


class AskForm(forms.ModelForm):
    tags = forms.CharField(max_length=250, label='Теги',
                           widget=forms.TextInput(attrs={"class": "form-control",
                                                         "placeholder": "Enter the tags separated by a space"}),
                           error_messages={'required': 'Enter at least one tag'})

    class Meta:
        model = Question
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Input a title'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Input the question text'}),
        }
        error_messages = {'title': {'required': 'Input a title'},
                          'content': {'required': 'Input the question text'}}

    def clean(self):
        cleaned_data = super(AskForm, self).clean()

        if len(cleaned_data['tags'].split()) > 8:
            raise forms.ValidationError("You can't add more than 8 tags")

        return cleaned_data


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {'content': forms.Textarea(attrs={'class': 'form-control mb-3',
                                                    'placeholder': 'Input text of answer'})}
        error_messages = {'content': {'required': 'Input text of answer'}}
