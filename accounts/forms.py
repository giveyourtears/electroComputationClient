from django.contrib.auth import get_user_model
from django.db.models import Q

from django import forms

User = get_user_model()


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Подтверждение', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username']

    def clean_password(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Пароли не совпадают")
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    query = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        query = self.cleaned_data.get('query')
        password = self.cleaned_data.get('password')
        user_qs_final = User.objects.filter(
            Q(username__iexact=query)
        ).distinct()
        if not user_qs_final.exists() and user_qs_final.count != 1:
            raise forms.ValidationError("Неверные учетные данные - пользователь существует")
        user_obj = user_qs_final.first()
        if not user_obj.check_password(password):
            raise forms.ValidationError("Неверные учетные данные")
        self.cleaned_data["user_obj"] = user_obj
        return super(UserLoginForm, self).clean(*args, **kwargs)


class FilialForm(forms.Form):
    short_name = forms.CharField(label='Сокращенное название')
    long_name = forms.CharField(label='Полное название')

    def clean(self, *args, **kwargs):
        short_name = self.cleaned_data.get('short_name')
        long_name = self.cleaned_data.get('long_name')
        return super(FilialForm, self).clean(*args, **kwargs)


class PsForm(forms.Form):
    short_name = forms.CharField(label='Сокращенное название')
    long_name = forms.CharField(label='Полное название')

    def clean(self, *args, **kwargs):
        short_name = self.cleaned_data.get('short_name')
        long_name = self.cleaned_data.get('long_name')
        return super(PsForm, self).clean(*args, **kwargs)
