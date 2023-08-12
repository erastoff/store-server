from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin


from products.models import Basket
from users.models import User
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from common.views import TitleMixin


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

    def get_context_data(self, **kwargs):
        context = super(UserProfileView, self).get_context_data()
        context["baskets"] = Basket.objects.filter(user=self.object)
        return context


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
