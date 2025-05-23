from django.urls import path
from . import views
from .views import (
    AdListView,
    AdDetailView,
    AdUpdateView,
    AdDeleteView,
    MyAdsView,
    add_response,
    accept_response,
    delete_response,
    send_newsletter,
    newsletter_success,
)

app_name = "ads"

urlpatterns = [
    # Главная и список объявлений
    path("", AdListView.as_view(), name="list"),
    # Создание и подтверждение
    path("create/", views.create_ad, name="create_ad"),
    path("verify/<uuid:code>/", views.verify_email, name="verify_email"),
    # Детали, редактирование, удаление объявления
    path("<int:pk>/", AdDetailView.as_view(), name="ad_detail"),
    path("<int:pk>/edit/", AdUpdateView.as_view(), name="edit_ad"),
    path("<int:pk>/delete/", AdDeleteView.as_view(), name="delete_ad"),
    # Отклики к объявлениям
    path("<int:pk>/respond/", add_response, name="add_response"),
    path("responses/", views.user_responses, name="user_responses"),
    path("responses/<int:pk>/accept/", accept_response, name="accept_response"),
    path("responses/<int:pk>/delete/", delete_response, name="delete_response"),
    # Мои объявления
    path("my_ads/", MyAdsView.as_view(), name="my_ads"),
    # Рассылка новостей
    path("newsletter/send/", send_newsletter, name="send_newsletter"),
    path("newsletter/success/", newsletter_success, name="newsletter_success"),
]
