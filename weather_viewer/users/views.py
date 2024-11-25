from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import LogoutView
from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import UserRegistrationForm, UserAuthorizationForm


class NotAuthenticatedRequiredMixin(AccessMixin):
    """Миксин для ограничения доступа аутентифицированным пользователям"""
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')  # Замените 'home' на вашу целевую страницу
        return super().dispatch(request, *args, **kwargs)


class LogoutUser(LogoutView):
    next_page = reverse_lazy('home')


class UserRegistrationView(NotAuthenticatedRequiredMixin, FormView):
    form_class = UserRegistrationForm  # Ваша форма
    template_name = 'users/registration.html'  # Шаблон для рендеринга формы
    success_url = reverse_lazy('users:login')  # URL для перенаправления после успешной регистрации

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)


class UserAuthorizationView(NotAuthenticatedRequiredMixin, FormView):
    template_name = 'users/login.html'
    form_class = UserAuthorizationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
