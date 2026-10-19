from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Experience, SocialLink, ProfileDesign

# ==========================================
# FORMULARIO DE PERFIL PRINCIPAL
# ==========================================

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            'first_name', 'last_name', 'profession', 'company', 'current_position',
            'about_me', 'avatar', 'primary_email', 'secondary_email',
            'primary_phone', 'secondary_phone', 'whatsapp_number',
            'address', 'latitude', 'longitude', 'website', 'hobbies'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'profession': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'company': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'current_position': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'about_me': forms.Textarea(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none', 'rows': 4}),
            'avatar': forms.FileInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 bg-white text-sm file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-sm file:font-semibold file:bg-teal-50 file:text-teal-700 hover:file:bg-teal-100'}),
            'primary_email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'secondary_email': forms.EmailInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'primary_phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'secondary_phone': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'whatsapp_number': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'address': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'latitude': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none', 'step': '0.000001'}),
            'website': forms.URLInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'hobbies': forms.TextInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
        }


# ==========================================
# FORMSETS (EXPERIENCIA Y REDES SOCIALES)
# ==========================================

ExperienceFormSet = inlineformset_factory(
    Profile, Experience,
    fields=['position', 'company', 'start_date', 'end_date', 'is_current'],
    extra=1, can_delete=True,
    widgets={
        'position': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg border border-slate-300 text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none', 'placeholder': 'Puesto'}),
        'company': forms.TextInput(attrs={'class': 'w-full px-3 py-2 rounded-lg border border-slate-300 text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none', 'placeholder': 'Empresa'}),
        'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 rounded-lg border border-slate-300 text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
        'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'w-full px-3 py-2 rounded-lg border border-slate-300 text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
        'is_current': forms.CheckboxInput(attrs={'class': 'w-4 h-4 text-teal-600 rounded border-slate-300 focus:ring-teal-500'}),
    }
)

SocialLinkFormSet = inlineformset_factory(
    Profile, SocialLink,
    fields=['platform', 'url'],
    extra=1, can_delete=True,
    widgets={
        'platform': forms.Select(attrs={'class': 'w-full px-3 py-2 rounded-lg border border-slate-300 text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
        'url': forms.URLInput(attrs={'class': 'w-full px-3 py-2 rounded-lg border border-slate-300 text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none', 'placeholder': 'https://...'}),
    }
)


# ==========================================
# FORMULARIO DE DISEÑO VISUAL
# ==========================================

class ProfileDesignForm(forms.ModelForm):
    class Meta:
        model = ProfileDesign
        fields = [
            'theme', 'bg_color', 'header_color', 'card_bg_color', 'text_color', 
            'secondary_text_color', 'title_color', 'button_color', 'link_color', 
            'border_color', 'badge_color', 'font_family', 'font_weight', 
            'text_alignment', 'header_bg_image', 'general_bg_image', 
            'header_height', 'avatar_shape', 'avatar_size', 'avatar_border_width', 
            'avatar_border_color', 'card_border_radius', 'card_shadow', 
            'card_padding', 'card_style', 'layout_columns', 'content_max_width', 
            'column_gap', 'button_border_radius', 'button_style', 'button_size', 
            'badge_shape', 'icon_style', 'qr_container_style'
        ]
        widgets = {
            'theme': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'bg_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 rounded-xl border border-slate-300 cursor-pointer'}),
            'header_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 rounded-xl border border-slate-300 cursor-pointer'}),
            'card_bg_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 rounded-xl border border-slate-300 cursor-pointer'}),
            'text_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 rounded-xl border border-slate-300 cursor-pointer'}),
            'secondary_text_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 rounded-xl border border-slate-300 cursor-pointer'}),
            'title_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 rounded-xl border border-slate-300 cursor-pointer'}),
            'button_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 rounded-xl border border-slate-300 cursor-pointer'}),
            'link_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 rounded-xl border border-slate-300 cursor-pointer'}),
            'border_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 rounded-xl border border-slate-300 cursor-pointer'}),
            'badge_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 rounded-xl border border-slate-300 cursor-pointer'}),
            'avatar_border_color': forms.TextInput(attrs={'type': 'color', 'class': 'w-16 h-10 p-1 rounded-xl border border-slate-300 cursor-pointer'}),
            'font_family': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'font_weight': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'text_alignment': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'header_bg_image': forms.FileInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 bg-white text-sm'}),
            'general_bg_image': forms.FileInput(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 bg-white text-sm'}),
            'header_height': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'avatar_shape': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'avatar_size': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'avatar_border_width': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'card_border_radius': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'card_shadow': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'card_padding': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'card_style': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'layout_columns': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'content_max_width': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'column_gap': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'button_border_radius': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'button_style': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'button_size': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'badge_shape': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'icon_style': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
            'qr_container_style': forms.Select(attrs={'class': 'w-full px-4 py-2 rounded-xl border border-slate-300 focus:ring-2 focus:ring-teal-500 focus:outline-none'}),
        }


# ==========================================
# FORMULARIOS DE AUTENTICACIÓN Y USUARIO
# ==========================================

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True, 
        label="Correo electrónico",
        widget=forms.EmailInput(attrs={'placeholder': 'tu@correo.com'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('email',)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este correo electrónico ya está registrado por otra cuenta.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True, label="Correo Electrónico")
    
    class Meta:
        model = User
        fields = ['username', 'email']
        
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            qs = User.objects.filter(email=email)
            if self.instance and self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            if qs.exists():
                raise forms.ValidationError("Este correo electrónico ya está registrado por otra cuenta.")
        return email