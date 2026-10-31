from django.shortcuts import render, redirect
from .models import EmployeeProfile
from .forms import EmployeeCreateForm
from django.contrib.auth.models import User

from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, View
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import secrets
from django.core.mail import send_mail
from django.conf import settings



# class RegisterView(CreateView):
#     model = User
#     form_class = RegisterForm
#     template_name = 'register.html'
#     success_url = reverse_lazy('login')

#     def form_valid(self, form):
#         user = form.save(commit=False)
#         user.is_active = False
#         user.save()

#         EmployeeProfile.objects.create(
#             user=user,
#             position='warehouse_worker'
#         )

#         token = default_token_generator.make_token(user)
#         uid = urlsafe_base64_encode(force_bytes(user.pk))


#         verification_url = self.request.build_absolute_uri(
#             reverse(
#                 'activate',
#                 kwargs={
#                     'uidb64': uid,
#                     'token': token
#                 }
#             )
#         )

#         send_mail(
#             subject='Email confirmation',
#             message=(
#                 f'Hello {user.username}\n\n'
#                 f'Click here {verification_url} to activate your account!'
#             ),
#             from_email=settings.EMAIL_HOST_USER,
#             recipient_list=[user.email],
#             fail_silently=False
#         )

#         return render(self.request, 'email_sent.html', {'email': user.email})


# class ActivateView(View):
#     def get(self, request, uidb64, token):
#         try:
#             uid = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(pk=uid)
#         except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#             user = None


#         if user and default_token_generator.check_token(user, token):
#             user.is_active = True
#             user.save(update_fields=['is_active'])
#             return redirect('login')
#         return HttpResponse('<h1>Token is not valid!</h1>')


class LoginUserView(LoginView):
    template_name = 'accounts/login.html'
    next_page = reverse_lazy('profile')


class LogoutUserView(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy('login')


class ProfileView(LoginRequiredMixin, DetailView):
    model = EmployeeProfile
    template_name = 'accounts/profile.html'
    context_object_name = 'profile'

    def get_object(self):
        return self.request.user.employee_profile


class EmployeeListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = EmployeeProfile
    template_name = 'accounts/employees.html'
    context_object_name = 'employees'

    def test_func(self):
        user = self.request.user    
        return (user.is_superuser or (hasattr(user, 'employee_profile')
                        and user.employee_profile.position == 'manager'))
    

class EmployeeDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = EmployeeProfile
    template_name = 'accounts/employee_detail.html'
    context_object_name = 'employee'

    def test_func(self):
        user = self.request.user
        return (user.is_superuser or (hasattr(user, 'employee_profile')
                        and user.employee_profile.position == 'manager'))


class CreateEmployeeView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = EmployeeCreateForm
    template_name = 'accounts/create_employee.html'
    success_url = reverse_lazy('employee_list')

    def test_func(self):
        user = self.request.user
        return (user.is_superuser or (hasattr(user, 'employee_profile')
                        and user.employee_profile.position == 'manager'))
    

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']

        if User.objects.filter(username=username).exists():
            form.add_error('username', 'Такой username уже существует.')
            return self.form_invalid(form)

        password = str(secrets.randbelow(90000) + (10000))

        user = User.objects.create_user(
            username=username, 
            email=email,
            password=password
        )

        profile = form.save(commit=False)
        profile.user = user
        profile.save()

        send_mail(
            subject='Ваш аккаунт Smart Stock',
            message=(
                f'Здравствуйте, {username}!\n'
                f'Ваш username: {username}\n'
                f'Ваш пароль: {password}\n'
                f'Войдите в систему Smart Stock.'
            ),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
        )

        return redirect(self.success_url)


class UpdateEmployeeView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EmployeeProfile
    form_class = EmployeeCreateForm
    template_name = 'accounts/update_employee.html'
    context_object_name = 'employee'
    success_url = reverse_lazy('employee_list')

    def test_func(self):
        user = self.request.user
        return (user.is_superuser or (hasattr(user, 'employee_profile')
                        and user.employee_profile.position == 'manager'))


class DeleteEmployeeView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = EmployeeProfile
    success_url = reverse_lazy('employee_list')

    def test_func(self):
        user = self.request.user
        return (user.is_superuser or (hasattr(user, 'employee_profile')
                        and user.employee_profile.position == 'manager'))  