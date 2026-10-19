from datetime import timedelta
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # 1. Información Personal y Profesional
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    profession = models.CharField(max_length=150, help_text="Ej. Arquitecta Principal")
    company = models.CharField(max_length=150, blank=True, null=True, help_text="Ej. Estudio Urbano GT")
    current_position = models.CharField(max_length=150, blank=True, null=True)
    about_me = models.TextField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    
    # 2. Contacto y Ubicación
    primary_email = models.EmailField()
    secondary_email = models.EmailField(blank=True, null=True)
    primary_phone = models.CharField(max_length=20)
    secondary_phone = models.CharField(max_length=20, blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, help_text="Número con código de país sin + (ej. 50255551234)")
    address = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, default=14.4828)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, default=-90.6125)
    website = models.URLField(blank=True, null=True)
    
    # 3. Intereses
    hobbies = models.CharField(max_length=255, blank=True, null=True, help_text="Separados por comas")
    
    #  CAMPOS DE MÉTRICAS Y ANALÍTICAS
    views_count = models.PositiveIntegerField(default=0)
    whatsapp_clicks = models.PositiveIntegerField(default=0)
    qr_scans = models.PositiveIntegerField(default=0)
    vcard_downloads = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Perfil de {self.first_name} {self.last_name} (@{self.user.username})"


class Experience(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='experiences')
    position = models.CharField(max_length=150)
    company = models.CharField(max_length=150)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.position} en {self.company}"


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('linkedin', 'LinkedIn'),
        ('instagram', 'Instagram'),
        ('twitter', 'Twitter / X'),
        ('facebook', 'Facebook'),
        ('github', 'GitHub'),
        ('youtube', 'YouTube'),
    ]

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='social_links')
    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField()

    def __str__(self):
        return f"{self.get_platform_display()} - {self.profile.user.username}"


class ProfileDesign(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='design')
    
    # Temas prediseñados
    THEME_CHOICES = [
        ('dark', 'Tema Oscuro'),
        ('light', 'Tema Claro'),
        ('minimal', 'Tema Minimalista'),
        ('professional', 'Tema Profesional'),
        ('colorful', 'Tema Colorido'),
        ('custom', 'Tema Personalizado'),
    ]
    theme = models.CharField(max_length=50, choices=THEME_CHOICES, default='light')
    
    # 1. Colores y apariencia general
    bg_color = models.CharField(max_length=7, default='#f8fafc', help_text="Fondo general")
    header_color = models.CharField(max_length=7, default='#0f172a', help_text="Color del encabezado")
    card_bg_color = models.CharField(max_length=7, default='#ffffff', help_text="Fondo de tarjetas")
    text_color = models.CharField(max_length=7, default='#1e293b', help_text="Texto principal")
    secondary_text_color = models.CharField(max_length=7, default='#64748b', help_text="Texto secundario")
    title_color = models.CharField(max_length=7, default='#0f172a', help_text="Títulos")
    button_color = models.CharField(max_length=7, default='#0d9488', help_text="Botones")
    link_color = models.CharField(max_length=7, default='#0d9488', help_text="Enlaces e iconos")
    border_color = models.CharField(max_length=7, default='#e2e8f0', help_text="Bordes")
    badge_color = models.CharField(max_length=7, default='#f1f5f9', help_text="Etiquetas o insignias")
    
    # 2. Tipografía y texto
    FONT_CHOICES = [
        ('Plus Jakarta Sans', 'Plus Jakarta Sans'),
        ('Inter', 'Inter'),
        ('Roboto', 'Roboto'),
        ('Poppins', 'Poppins'),
    ]
    font_family = models.CharField(max_length=50, choices=FONT_CHOICES, default='Plus Jakarta Sans')
    font_weight = models.CharField(max_length=50, choices=[('font-normal', 'Normal'), ('font-semibold', 'Seminegrita'), ('font-bold', 'Negrita')], default='font-bold')
    text_alignment = models.CharField(max_length=50, choices=[('text-left', 'Izquierda'), ('text-center', 'Centro'), ('text-right', 'Derecha')], default='text-left')
    
    # 3. Encabezado y foto de perfil
    header_bg_image = models.ImageField(upload_to='designs/headers/', blank=True, null=True, help_text="Imagen de fondo del encabezado")
    general_bg_image = models.ImageField(upload_to='designs/backgrounds/', blank=True, null=True, help_text="Imagen de fondo general")
    header_height = models.CharField(max_length=50, choices=[('py-10 md:py-14', 'Normal'), ('py-16 md:py-24', 'Alto'), ('py-8', 'Compacto')], default='py-10 md:py-14')
    avatar_shape = models.CharField(max_length=50, choices=[('rounded-2xl', 'Redondeado Rectangular'), ('rounded-full', 'Circular'), ('rounded-none', 'Cuadrado')], default='rounded-2xl')
    avatar_size = models.CharField(max_length=50, choices=[('w-28 h-28 md:w-36 md:h-36', 'Normal'), ('w-24 h-24 md:w-28 md:h-28', 'Pequeño'), ('w-36 h-36 md:w-44 md:h-44', 'Grande')], default='w-28 h-28 md:w-36 md:h-36')
    avatar_border_width = models.CharField(max_length=50, choices=[('border-0', 'Sin Borde'), ('border-2', 'Fino'), ('border-4', 'Grueso')], default='border-2')
    avatar_border_color = models.CharField(max_length=7, default='#0d9488', help_text="Color del borde de la foto")
    
    # 4. Tarjetas y contenedores
    card_border_radius = models.CharField(max_length=50, choices=[('rounded-xl', 'Moderado'), ('rounded-2xl', 'Redondeado'), ('rounded-none', 'Cuadrado')], default='rounded-2xl')
    card_shadow = models.CharField(max_length=50, choices=[('shadow-sm', 'Suave'), ('shadow-md', 'Media'), ('shadow-none', 'Sin Sombra')], default='shadow-sm')
    card_padding = models.CharField(max_length=50, choices=[('p-4', 'Compacto'), ('p-6', 'Normal'), ('p-8', 'Amplio')], default='p-6')
    card_style = models.CharField(max_length=50, choices=[('solid', 'Sólido'), ('bordered', 'Con Borde Destacado'), ('shadow', 'Con Sombra Intensa')], default='solid')
    
    # 5. Distribución y estructura
    layout_columns = models.CharField(max_length=50, choices=[('grid-cols-1 md:grid-cols-3', '2 Columnas (Bento Grid)'), ('grid-cols-1', '1 Columna')], default='grid-cols-1 md:grid-cols-3')
    content_max_width = models.CharField(max_length=50, choices=[('max-w-4xl', 'Ancho Estándar'), ('max-w-6xl', 'Ancho Amplio'), ('max-w-full', 'Pantalla Completa')], default='max-w-6xl')
    column_gap = models.CharField(max_length=50, choices=[('gap-4', 'Compacto'), ('gap-6', 'Normal'), ('gap-8', 'Amplio')], default='gap-6')
    
    # 6. Botones e interacciones
    button_border_radius = models.CharField(max_length=50, choices=[('rounded-xl', 'Redondeado'), ('rounded-full', 'Píldora'), ('rounded-none', 'Cuadrado')], default='rounded-xl')
    button_style = models.CharField(max_length=50, choices=[('solid', 'Sólido'), ('outline', 'Contorno'), ('transparent', 'Transparente')], default='solid')
    button_size = models.CharField(max_length=50, choices=[('py-2 px-4 text-xs', 'Pequeño'), ('py-2.5 px-5 text-sm', 'Normal'), ('py-3 px-6 text-base', 'Grande')], default='py-2.5 px-5 text-sm')
    
    # 7. Iconos y elementos visuales
    badge_shape = models.CharField(max_length=50, choices=[('rounded-lg', 'Moderado'), ('rounded-full', 'Píldora'), ('rounded-none', 'Cuadrado')], default='rounded-lg')
    icon_style = models.CharField(max_length=50, choices=[('line', 'Línea / Outline'), ('solid', 'Sólido')], default='line')
    qr_container_style = models.CharField(max_length=50, choices=[('standard', 'Estándar'), ('minimal', 'Minimalista'), ('bordered', 'Enmarcado')], default='standard')

    def save(self, *args, **kwargs):
        """Asigna automáticamente los colores según el tema seleccionado si no es personalizado."""
        if self.theme and self.theme != 'custom':
            themes_config = {
                'dark': {
                    'bg_color': '#0b0f19', 'header_color': '#111827', 'card_bg_color': '#1e293b',
                    'text_color': '#f1f5f9', 'secondary_text_color': '#94a3b8', 'title_color': '#ffffff',
                    'button_color': '#0d9488', 'link_color': '#2dd4bf', 'border_color': '#334155', 'badge_color': '#1e293b'
                },
                'light': {
                    'bg_color': '#f8fafc', 'header_color': '#ffffff', 'card_bg_color': '#ffffff',
                    'text_color': '#1e293b', 'secondary_text_color': '#64748b', 'title_color': '#0f172a',
                    'button_color': '#0d9488', 'link_color': '#0d9488', 'border_color': '#e2e8f0', 'badge_color': '#f1f5f9'
                },
                'minimal': {
                    'bg_color': '#ffffff', 'header_color': '#ffffff', 'card_bg_color': '#fafafa',
                    'text_color': '#262626', 'secondary_text_color': '#737373', 'title_color': '#171717',
                    'button_color': '#171717', 'link_color': '#171717', 'border_color': '#e5e5e5', 'badge_color': '#f5f5f5'
                },
                'professional': {
                    'bg_color': '#f4f6f9', 'header_color': '#102a43', 'card_bg_color': '#ffffff',
                    'text_color': '#334e68', 'secondary_text_color': '#627d98', 'title_color': '#102a43',
                    'button_color': '#243b53', 'link_color': '#243b53', 'border_color': '#bcccdc', 'badge_color': '#d9e2ec'
                },
                'colorful': {
                    'bg_color': '#faf5ff', 'header_color': '#7c3aed', 'card_bg_color': '#ffffff',
                    'text_color': '#4b5563', 'secondary_text_color': '#6b7280', 'title_color': '#6d28d9',
                    'button_color': '#7c3aed', 'link_color': '#8b5cf6', 'border_color': '#e9d5ff', 'badge_color': '#f3e8ff'
                }
            }
            
            if self.theme in themes_config:
                for key, value in themes_config[self.theme].items():
                    setattr(self, key, value)
                    
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Diseño de {self.profile.first_name}"


class Subscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    stripe_customer_id = models.CharField(max_length=255, blank=True, null=True)
    stripe_subscription_id = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    expires_at = models.DateTimeField(blank=True, null=True, help_text="Fecha de expiración de la suscripción")
    created_at = models.DateTimeField(auto_now_add=True)

    def check_status(self):
        """Verifica si la suscripción sigue activa por fecha."""
        if self.is_active and self.expires_at:
            if timezone.now() > self.expires_at:
                self.is_active = False
                self.save(update_fields=['is_active'])
        return self.is_active

    def __str__(self):
        status = 'Activa' if self.check_status() else 'Expirada/Inactiva'
        return f"Suscripción de {self.user.username} - {status}"