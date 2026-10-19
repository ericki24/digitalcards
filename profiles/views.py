from datetime import timedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash, login as auth_login
from django.contrib.auth.forms import PasswordChangeForm
import stripe
from django.conf import settings

from .models import Profile, ProfileDesign, Subscription
from .forms import (
    ProfileForm, 
    ExperienceFormSet, 
    SocialLinkFormSet, 
    ProfileDesignForm, 
    CustomUserCreationForm,
    UserUpdateForm
)

stripe.api_key = settings.STRIPE_SECRET_KEY


# ==========================================
# UTILIDADES INTERNAS
# ==========================================

def _get_or_create_profile(user):
    """Obtiene o crea el perfil de usuario con valores por defecto seguros."""
    profile, _ = Profile.objects.get_or_create(
        user=user,
        defaults={
            'first_name': user.first_name or user.username,
            'last_name': '',
            'primary_email': user.email or 'correo@ejemplo.com',
            'primary_phone': '50200000000',
            'whatsapp_number': '50200000000',
            'profession': 'Profesional'
        }
    )
    return profile


# ==========================================
# VISTAS PÚBLICAS Y DE MARKETING
# ==========================================

def landing_page(request):
    """Página pública de bienvenida del SaaS."""
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'profiles/landing.html')


def register_view(request):
    """Vista de registro que solicita y crea el usuario, perfil y suscripción."""
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            Profile.objects.create(
                user=user,
                first_name=user.username,
                primary_email=user.email,
                profession="Profesional Digital"
            )
            Subscription.objects.create(user=user)
            
            auth_login(request, user)
            messages.success(request, "¡Cuenta creada con éxito. Bienvenido a ProfileSaaS!")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
        
    return render(request, 'profiles/register.html', {'form': form})


def public_profile(request, username):
    """Vista pública de la tarjeta/perfil digital del usuario."""
    user_obj = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user_obj)
    
    # Incrementa la visita solo si un tercero ve el perfil
    if request.user != user_obj:
        profile.views_count += 1
        profile.save(update_fields=['views_count'])

    design, _ = ProfileDesign.objects.get_or_create(profile=profile)
    subscription = getattr(user_obj, 'subscription', None)
    is_active = subscription.check_status() if subscription else False

    hobbies_list = [h.strip() for h in profile.hobbies.split(',')] if profile.hobbies else []

    context = {
        'profile': profile,
        'user_obj': user_obj,
        'is_active': is_active,
        'hobbies_list': hobbies_list,
        'profile_url': request.build_absolute_uri(),
        'design': design,
    }
    return render(request, 'profiles/public_profile.html', context)


def download_vcard(request, username):
    """Genera y descarga el archivo de contacto vCard (.vcf)."""
    user_obj = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user_obj)
    
    profile.vcard_downloads += 1
    profile.save(update_fields=['vcard_downloads'])

    vcard_content = f"""BEGIN:VCARD
VERSION:3.0
FN:{profile.first_name} {profile.last_name}
TITLE:{profile.profession}
ORG:{profile.company or ''}
TEL;TYPE=CELL:{profile.primary_phone}
EMAIL:{profile.primary_email}
URL:{profile.website or ''}
END:VCARD"""

    response = HttpResponse(vcard_content, content_type='text/vcard')
    response['Content-Disposition'] = f'attachment; filename="{username}_contacto.vcf"'
    return response


def track_whatsapp(request, username):
    """Registra clics en WhatsApp y redirige al chat."""
    user_obj = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user_obj)
    
    profile.whatsapp_clicks += 1
    profile.save(update_fields=['whatsapp_clicks'])
    
    wa_number = profile.whatsapp_number or profile.primary_phone
    return redirect(f"https://wa.me/{wa_number}")


def track_qr(request, username):
    """Registra escaneos de código QR y redirige al perfil público."""
    user_obj = get_object_or_404(User, username=username)
    profile = get_object_or_404(Profile, user=user_obj)
    
    profile.qr_scans += 1
    profile.save(update_fields=['qr_scans'])
    
    return redirect('public_profile', username=username)


# ==========================================
# PANEL DE CONTROL (DASHBOARD & HOME)
# ==========================================

@login_required
def home(request):
    """Panel principal de usuario autenticado con directorio de búsqueda."""
    profile = _get_or_create_profile(request.user)
    subscription, _ = Subscription.objects.get_or_create(user=request.user)
    design, _ = ProfileDesign.objects.get_or_create(profile=profile)

    search_query = request.GET.get('q', '').strip()
    directory_profiles = Profile.objects.select_related('user').exclude(user=request.user)

    if search_query:
        query_words = search_query.split()
        q_filters = Q()
        for word in query_words:
            q_filters |= (
                Q(first_name__icontains=word) |
                Q(last_name__icontains=word) |
                Q(profession__icontains=word) |
                Q(company__icontains=word) |
                Q(address__icontains=word) |
                Q(user__username__icontains=word)
            )
        directory_profiles = directory_profiles.filter(q_filters)

    public_profile_url = request.build_absolute_uri(f'/{request.user.username}/')

    context = {
        'profile': profile,
        'subscription': subscription,
        'design': design,
        'directory_profiles': directory_profiles[:6],
        'search_query': search_query,
        'public_profile_url': public_profile_url,
    }
    return render(request, 'profiles/home.html', context)


@login_required
def dashboard(request):
    """Edición de información general, experiencia y enlaces sociales del perfil."""
    profile = _get_or_create_profile(request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        experience_formset = ExperienceFormSet(request.POST, instance=profile)
        social_formset = SocialLinkFormSet(request.POST, instance=profile)
        
        if form.is_valid() and experience_formset.is_valid() and social_formset.is_valid():
            form.save()
            experience_formset.save()
            social_formset.save()
            messages.success(request, "¡Tu información de perfil se ha guardado y actualizado con éxito!")
            return redirect('dashboard')
        else:
            messages.error(request, "Por favor corrige los errores señalados en el formulario.")
    else:
        form = ProfileForm(instance=profile)
        experience_formset = ExperienceFormSet(instance=profile)
        social_formset = SocialLinkFormSet(instance=profile)
        
    context = {
        'form': form,
        'experience_formset': experience_formset,
        'social_formset': social_formset,
        'profile': profile,
    }
    return render(request, 'profiles/dashboard.html', context)


@login_required
def dashboard_diseno(request):
    """Personalización visual y de diseño del perfil."""
    profile = _get_or_create_profile(request.user)
    design, _ = ProfileDesign.objects.get_or_create(profile=profile)
    
    if request.method == 'POST':
        form = ProfileDesignForm(request.POST, request.FILES, instance=design)
        if form.is_valid():
            form.save()
            messages.success(request, "¡Las preferencias de diseño visual han sido actualizadas con éxito!")
            return redirect('dashboard_diseno')
        else:
            messages.error(request, "Hubo un problema al guardar la configuración de diseño.")
    else:
        form = ProfileDesignForm(instance=design)
        
    context = {
        'form': form,
        'profile': profile,
    }
    return render(request, 'profiles/dashboard_diseno.html', context)


@login_required
def dashboard_diseno_reset(request):
    """Restablece el diseño del perfil a los valores predeterminados."""
    profile = get_object_or_404(Profile, user=request.user)
    ProfileDesign.objects.filter(profile=profile).delete()
    ProfileDesign.objects.create(profile=profile)
    messages.success(request, "¡El diseño ha sido restablecido a los valores predeterminados!")
    return redirect('dashboard_diseno')


# ==========================================
# SUSCRIPCIÓN Y PAGOS (STRIPE)
# ==========================================

@login_required
def dashboard_suscripcion(request):
    """Panel de gestión de planes y facturación."""
    profile = _get_or_create_profile(request.user)
    subscription, _ = Subscription.objects.get_or_create(user=request.user)
    
    context = {
        'profile': profile,
        'subscription': subscription,
    }
    return render(request, 'profiles/dashboard_suscripcion.html', context)


@login_required
def create_checkout_session(request):
    """Crea una sesión de pago en Stripe para la suscripción anual."""
    try:
        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': 'Suscripción Premium Anual - Tarjeta Digital SaaS',
                    },
                    'unit_amount': 9900,
                    'recurring': {
                        'interval': 'year',
                    },
                },
                'quantity': 1,
            }],
            mode='subscription',
            success_url=request.build_absolute_uri('/dashboard/pago-exitoso/'),
            cancel_url=request.build_absolute_uri('/home/?cancelado=true'),
            client_reference_id=str(request.user.id),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return HttpResponse(f"Error al conectar con Stripe: {str(e)}", status=400)


@login_required
def payment_success(request):
    """Activa la suscripción tras un pago exitoso."""
    subscription, _ = Subscription.objects.get_or_create(user=request.user)
    subscription.is_active = True
    subscription.expires_at = timezone.now() + timedelta(days=365)
    subscription.save()
    messages.success(request, "¡Pago exitoso! Tu suscripción Premium ya está activa.")
    return redirect('dashboard_suscripcion')


@login_required
def cancel_subscription(request):
    """Anula o desactiva la suscripción actual del usuario."""
    if request.method == 'POST':
        subscription, _ = Subscription.objects.get_or_create(user=request.user)
        subscription.is_active = False
        subscription.save()
        messages.info(request, "Tu suscripción ha sido cancelada.")
    return redirect('dashboard_suscripcion')


# ==========================================
# CONFIGURACIÓN DE CUENTA Y USUARIO
# ==========================================

@login_required
def account_settings_view(request):
    """Gestión de datos de acceso (usuario, correo y contraseña)."""
    if request.method == 'POST':
        if 'update_profile_info' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=request.user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "¡Tu nombre de usuario y correo han sido actualizados con éxito!")
                return redirect('account_settings')
            else:
                messages.error(request, "Por favor corrige los errores en el formulario de usuario.")

        elif 'change_password' in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, "¡Tu contraseña ha sido actualizada correctamente!")
                return redirect('account_settings')
            else:
                messages.error(request, "Por favor corrige los errores al cambiar la contraseña.")
    
    context = {
        'user_form': UserUpdateForm(instance=request.user),
        'password_form': PasswordChangeForm(user=request.user),
    }
    return render(request, 'profiles/account_settings.html', context)


@login_required
def close_account_view(request):
    """Elimina permanentemente la cuenta del usuario y sus datos."""
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, "Tu cuenta ha sido eliminada permanentemente.")
        return redirect('landing')
    return redirect('account_settings')