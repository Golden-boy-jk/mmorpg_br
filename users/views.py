from django.shortcuts import render, redirect, get_object_or_404
from django.core.mail import EmailMultiAlternatives  # Новый способ отправки HTML-писем
from django.template.loader import render_to_string  # Подключение шаблона письма
from django.conf import settings
from django.contrib import messages
from .forms import RegistrationForm
from .models import CustomUser


def register_view(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Пользователь неактивен до подтверждения
            user.save()

            # Генерация полной ссылки подтверждения e-mail
            confirmation_link = request.build_absolute_uri(
                f"/users/confirm/{user.verification_code}/"
            )

            # 🔹 Генерация HTML-содержимого письма из шаблона
            html_content = render_to_string(
                "email/confirmation_email.html",
                {
                    "user": user,
                    "confirmation_link": confirmation_link,
                },
            )

            # 🔹 Резервный текст (на случай, если HTML не отображается)
            text_content = (
                f"Привет! Подтверди регистрацию, перейдя по ссылке: {confirmation_link}"
            )

            # 🔹 Создание объекта письма
            msg = EmailMultiAlternatives(
                subject="Подтверждение регистрации",
                body=text_content,  # текстовая часть
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )

            # 🔹 Добавление HTML-версии письма
            msg.attach_alternative(html_content, "text/html")

            # 🔹 Попытка отправки письма
            try:
                msg.send()
                messages.success(
                    request, "Письмо с подтверждением отправлено на e-mail."
                )
            except Exception as e:
                messages.error(request, f"Ошибка отправки письма: {str(e)}")

            return redirect("users:login")
    else:
        form = RegistrationForm()

    return render(request, "users/register.html", {"form": form})


def confirm_email(request, code):
    user = get_object_or_404(CustomUser, verification_code=code)

    if user.is_active:
        messages.info(request, "E-mail уже подтверждён.")
        return redirect("users:login")

    user.is_active = True
    user.verification_code = None  # Обнуляем код (если поле допускает null/blank)
    user.save()

    messages.success(request, "E-mail подтверждён, можешь войти.")
    return redirect("users:login")


def home_view(request):
    return render(request, "users/home.html")
