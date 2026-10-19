from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    
    #  Páginas Públicas y Autenticación
    path('', views.landing_page, name='landing'),
    path('registro/', views.register_view, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='profiles/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='landing'), name='logout'),
    path('settings/account/', views.account_settings_view, name='account_settings'),
    path('account/close/', views.close_account_view, name='close_account'),
    
    #  Flujo de Recuperación de Contraseña
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='profiles/password_reset_form.html',
        email_template_name='profiles/password_reset_email.txt',       # Versión texto plano
        html_email_template_name='profiles/password_reset_email.html', # Versión con diseño HTML
        subject_template_name='profiles/password_reset_subject.txt'
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='profiles/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='profiles/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='profiles/password_reset_complete.html'), name='password_reset_complete'),
    
    #  Panel Privado (Dashboard y Diseño)
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/diseno/', views.dashboard_diseno, name='dashboard_diseno'),
    path('dashboard/diseno/reset/', views.dashboard_diseno_reset, name='dashboard_diseno_reset'),

    #  Suscripciones y Pagos (Stripe)
    path('crear-pago/', views.create_checkout_session, name='create_checkout_session'),
    path('dashboard/pago-exitoso/', views.payment_success, name='payment_success'),
    path('dashboard/suscripcion/', views.dashboard_suscripcion, name='dashboard_suscripcion'),
    path('dashboard/cancelar-suscripcion/', views.cancel_subscription, name='cancel_subscription'),
    
    #  Perfiles Públicos y Métricas de Analítica 
    path('track/whatsapp/<str:username>/', views.track_whatsapp, name='track_whatsapp'),
    path('track/qr/<str:username>/', views.track_qr, name='track_qr'),
    path('<str:username>/vcard/', views.download_vcard, name='download_vcard'),
    path('<str:username>/', views.public_profile, name='public_profile'),

]