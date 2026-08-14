from django.shortcuts import render
from django.http import HttpResponse
from .models import Theme

def dynamic_css(request):
    theme = Theme.objects.filter(actif=True).first()
    if not theme:
        theme = Theme.objects.create(actif=True)
    css = f"""
:root {{
  --primary: {theme.primary};
  --primary-hover: {theme.primary_hover};
  --secondary: {theme.secondary};
  --secondary-hover: {theme.secondary_hover};
  --success: {theme.success};
  --success-hover: {theme.success_hover};
  --danger: {theme.danger};
  --danger-hover: {theme.danger_hover};
  --warning: {theme.warning};
  --warning-hover: {theme.warning_hover};
  --info: {theme.info};
  --info-hover: {theme.info_hover};
  --light: {theme.light};
  --dark: {theme.dark};
  --body-bg: {theme.body_bg};
  --text: {theme.text_color};
  --text-muted: {theme.text_muted};
  --white: {theme.white};
  --border: {theme.border};
  --font-family: {theme.font_family};
  --radius: {theme.border_radius};
  --shadow: {theme.box_shadow};
}}
"""
    return HttpResponse(css, content_type='text/css')

def theme_preview(request):
    theme = Theme.objects.filter(actif=True).first()
    return render(request, 'theme_manager/theme_preview.html', {'theme': theme})

