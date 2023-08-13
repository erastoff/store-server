from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from products.models import Basket
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    title = "Store - Авторизация"
    #     redirect path specified in settings.py


# def login(request):
#     if request.method == "POST":
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST["username"]
#             password = request.POST["password"]
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse("index"))
#     else:
#         form = UserLoginForm()
#     context = {"form": form}
#     return render(request, "users/login.html", context)


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("users:login")
    success_message = "Поздравляем! Вы успешно зарегистрированы!"
    title = "Store - Регистрация"


# def registration(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Поздравляем! Вы успешно зарегистрированы!")
#             return HttpResponseRedirect(reverse("users:login"))
#     else:
#         form = UserRegistrationForm()
#     context = {"form": form}
#     print(context)
#     return render(request, "users/registration.html", context)


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"
    title = "Store - Личный кабинет"

    def get_success_url(self):
        return reverse_lazy("users:profile", args=(self.object.id,))

    # def get_context_data(self, **kwargs): # Can be deleted after adding basket in context_processors
    #     context = super(UserProfileView, self).get_context_data()
    #     context["baskets"] = Basket.objects.filter(user=self.object)
    #     return context


# @login_required
# def profile(request):
#     if request.method == "POST":
#         form = UserProfileForm(
#             instance=request.user, data=request.POST, files=request.FILES
#         )
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse("users:profile"))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#
#     """
#     the easiest method to add sum and quantity for each element in basket
#
#     baskets = Basket.objects.filter(user=request.user)
#     # 1
#     total_sum = sum(basket.sum() for basket in baskets)
#     total_quantity = sum(basket.quantity for basket in baskets)
#     # 2
#     total_sum = 0
#     total_quantity = 0
#     for basket in baskets:
#         total_sum = total_sum + basket.sum()
#         total_quantity = total_quantity + basket.quantity
#         """
#
#     context = {
#         "title": "Store - Профиль",
#         "form": form,
#         "baskets": Basket.objects.filter(user=request.user),
#         # "total_sum": sum(basket.sum() for basket in baskets),
#         # "total_quantity": sum(basket.quantity for basket in baskets),
#     }
#     return render(request, "users/profile.html", context)


# LogoutView imported directly in urls.py
# def logout(request):
#     auth.logout(request)
#     return HttpResponseRedirect(reverse("index"))


class EmailVerificationView(TitleMixin, TemplateView):
    title = "Store - Подтверждение электронной почты"
    template_name = "users/email_verification.html"

    def get(self, request, *args, **kwargs):
        code = kwargs["code"]
        user = User.objects.get(email=kwargs["email"])
        email_verifications = EmailVerification.objects.filter(user=user, code=code)
        if (
            email_verifications.exists()
            and not email_verifications.first().is_expired()
        ):
            user.is_verified_email = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return HttpResponseRedirect(reverse("index"))
