from django.conf import settings
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail, send_mass_mail
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth import get_user_model

from .forms import AdForm, ResponseForm, NewsletterForm
from .models import Ad, Response, Category, EmailVerificationCode


def is_ajax(request):
    return request.headers.get("x-requested-with") == "XMLHttpRequest"


@login_required
def create_ad(request):
    if request.method == "POST":
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.save()
            messages.success(request, "Объявление успешно создано!")
            return redirect("ads:my_ads")
    else:
        form = AdForm()
    return render(request, "board/create_ad.html", {"form": form})


class AdListView(ListView):
    model = Ad
    template_name = "board/ad_list.html"
    context_object_name = "ads"
    ordering = ["-created_at"]
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.choices
        context["selected_category"] = self.request.GET.get("category", "")
        return context


class AdDetailView(DetailView):
    model = Ad
    template_name = "board/ad_detail.html"
    context_object_name = "ad"


class AdUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ad
    form_class = AdForm
    template_name = "board/edit_ad.html"

    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return self.object.get_absolute_url()


class AdDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ad
    template_name = "board/delete_ad.html"
    success_url = reverse_lazy("ads:list")

    def test_func(self):
        return self.request.user == self.get_object().author


@login_required
def add_response(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if request.method == "POST":
        if Response.objects.filter(ad=ad, user=request.user).exists():
            messages.error(request, "Вы уже откликались на это объявление.")
            return redirect("ads:ad_detail", pk=ad.pk)

        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.ad = ad
            response.user = request.user
            response.save()

            try:
                send_mail(
                    f"Новый отклик на ваше объявление '{ad.title}'",
                    f"Пользователь {request.user.email} оставил отклик: {response.content}",
                    settings.DEFAULT_FROM_EMAIL,
                    [ad.author.email],
                    fail_silently=False,
                )
            except Exception as e:
                if is_ajax(request):
                    return JsonResponse({"success": False, "error": str(e)}, status=500)

            if is_ajax(request):
                return JsonResponse({"success": True})

            messages.success(request, "Отклик успешно оставлен!")
            return redirect("ads:ad_detail", pk=ad.pk)

        if is_ajax(request):
            return JsonResponse({"success": False, "errors": form.errors}, status=400)

    else:
        form = ResponseForm()

    return render(request, "board/add_response.html", {"form": form, "ad": ad})


@login_required
def accept_response(request, pk):
    response = get_object_or_404(Response, pk=pk)
    if response.ad.author == request.user:
        response.status = "accepted"
        response.save()

        try:
            send_mail(
                f"Ваш отклик на '{response.ad.title}' принят!",
                f"Ваш отклик: {response.content} был принят владельцем объявления.",
                settings.DEFAULT_FROM_EMAIL,
                [response.user.email],
                fail_silently=False,
            )
            messages.success(request, "Отклик принят и уведомление отправлено!")
        except Exception as e:
            messages.error(request, f"Ошибка отправки письма: {str(e)}")

    return redirect("ads:user_responses")


@login_required
@require_POST
def delete_response(request, pk):
    response = get_object_or_404(Response, pk=pk)

    if response.ad.author != request.user:
        messages.error(request, "Вы не можете удалить этот отклик.")
        return redirect("ads:user_responses")

    user_email = response.user.email
    content = response.content
    ad_title = response.ad.title
    response.delete()

    try:
        send_mail(
            f"Ваш отклик на '{ad_title}' был удалён",
            f"Ваш отклик: {content} был удалён автором объявления.",
            settings.DEFAULT_FROM_EMAIL,
            [user_email],
            fail_silently=False,
        )
        messages.success(request, "Отклик успешно удалён и уведомление отправлено.")
    except Exception as e:
        messages.error(request, f"Ошибка отправки письма: {str(e)}")

    return redirect("ads:user_responses")


@staff_member_required
def send_newsletter(request):
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            newsletter = form.save()

            User = get_user_model()
            users = User.objects.filter(is_email_verified=True)

            emails = [
                (
                    newsletter.subject,
                    newsletter.message,
                    settings.DEFAULT_FROM_EMAIL,
                    [user.email],
                )
                for user in users
                if user.email
            ]

            if emails:
                try:
                    send_mass_mail(emails, fail_silently=False)
                    messages.success(request, "Рассылка успешно отправлена!")
                    return redirect("ads:newsletter_success")
                except Exception as e:
                    messages.error(request, f"Ошибка отправки рассылки: {str(e)}")
            else:
                messages.error(request, "Нет пользователей с email для рассылки.")
    else:
        form = NewsletterForm()
    return render(request, "board/send_newsletter.html", {"form": form})


@login_required
def responses_to_my_ads(request):
    status_filter = request.GET.get("status", "")
    responses = Response.objects.filter(ad__author=request.user)

    if status_filter in ["pending", "accepted", "rejected"]:
        responses = responses.filter(status=status_filter)

    return render(
        request,
        "board/user_responses.html",
        {
            "responses": responses,
            "status_filter": status_filter,
        },
    )


class MyAdsView(LoginRequiredMixin, ListView):
    model = Ad
    template_name = "board/my_ads.html"
    context_object_name = "ads"
    paginate_by = 5

    def get_queryset(self):
        queryset = Ad.objects.filter(author=self.request.user)
        category = self.request.GET.get("category")
        if category:
            queryset = queryset.filter(category=category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.choices
        context["selected_category"] = self.request.GET.get("category", "")
        return context


def newsletter_success(request):
    return render(request, "board/newsletter_success.html")


def verify_email(request, code):
    verification = get_object_or_404(EmailVerificationCode, code=code)
    user = verification.user

    if user.is_email_verified:
        return render(request, "registration/already_verified.html")

    user.is_email_verified = True
    user.save()
    verification.delete()
    return render(request, "registration/verification_success.html")


def user_responses(request):
    responses = Response.objects.filter(user=request.user)
    return render(request, "board/user_responses.html", {"responses": responses})
