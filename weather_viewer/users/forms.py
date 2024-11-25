from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator


password_characters_validator = RegexValidator(
    regex=r'[a-zA-Zа-яА-Я0-9_!@#$%^&*_]',
    message='Пароль может содержать только буквы латинского алфавита, цифры и специальные символы(!@#$%^&*_)'
)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True,
        validators=[
            MinLengthValidator(4, message="Логин должен быть не короче 4 символов"),
            MaxLengthValidator(18, message="Логин должен быть не длиннее 18 символов"),
            UnicodeUsernameValidator(message='Логин может содержать только буквы, цифры и символ подчёркивания')
        ],
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True,
        validators=[
            MinLengthValidator(6, message="Пароль должен быть не короче 6 символов"),
            MaxLengthValidator(18, message="Пароль должен быть не длиннее 18 символов"),
            password_characters_validator
        ]
    )

    password2 = forms.CharField(
        label='Подтвердите пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])

        if commit:
            user.save()
        return user

    def clean_username(self):
        """
        Проверяет, уникальность логина
        """
        username = self.cleaned_data['username'].strip()
        if not username:
            raise forms.ValidationError("Поле логин не может быть пустым")

        if get_user_model().objects.filter(username=username).exists():
            raise forms.ValidationError("Этот логин уже занят. Пожалуйста, выберите другой")

        return username

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1', '')

        if not password1:
            raise forms.ValidationError("Поле пароля не может быть пустым")

        return password1

    def clean_password2(self):
        """
        Проверяет, что пароли совпадают
        """
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 is not None:
            password1 = password1.strip()
        if password2 is not None:
            password2 = password2.strip()

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'Пароли не совпадают'
            )

        return password2


class UserAuthorizationForm(forms.Form):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={"class": "form-control"}),
        required=True
    )

    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=True
    )

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super().__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username').strip()
        if not username:
            raise forms.ValidationError("Поле логин не может быть пустым")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')

        if not password:
            raise forms.ValidationError("Поле пароля не может быть пустым")

        return password

    def clean(self):
        """
        Проверяет корректность пары логин+пароль.
        """
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        password = cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)

            if self.user_cache is None:
                raise forms.ValidationError("Неверный логин или пароль")

        return cleaned_data

    def get_user(self):
        return self.user_cache

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


