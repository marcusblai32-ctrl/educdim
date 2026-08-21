from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import Theme
import logging

logger = logging.getLogger(__name__)


def dynamic_css(request):
    """Jeneri CSS dinamik selon tema aktif la"""
    try:
        theme = Theme.objects.filter(actif=True).first()
        if not theme:
            # CSS default si pa gen tema
            css = """
            :root {
              --primary: #1a1a2e;
              --primary-hover: #2d2d4a;
              --secondary: #16213e;
              --secondary-hover: #2a3a6a;
              --success: #28a745;
              --success-hover: #218838;
              --danger: #dc3545;
              --danger-hover: #c82333;
              --warning: #ffc107;
              --warning-hover: #e0a800;
              --info: #17a2b8;
              --info-hover: #138496;
              --light: #f8f9fa;
              --dark: #1a1a2e;
              --body-bg: #f8f9fa;
              --text: #212529;
              --text-muted: #6c757d;
              --white: #ffffff;
              --border: #dee2e6;
              --font-family: 'Inter', sans-serif;
              --radius: 8px;
              --shadow: 0 4px 20px rgba(0,0,0,0.08);
            }
            """
            return HttpResponse(css, content_type='text/css')
            
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
    except Exception as e:
        logger.error(f"Error generating dynamic CSS: {e}")
        return HttpResponse("", content_type='text/css')


def theme_preview(request):
    """Preview tema aktif la"""
    try:
        theme = Theme.objects.filter(actif=True).first()
        return render(request, 'theme_manager/theme_preview.html', {'theme': theme})
    except Exception:
        return render(request, 'theme_manager/theme_preview.html', {'theme': None})


# ============================================
# IMAJ VIEWS
# ============================================
def serve_theme_image(request, field_name):
    """Sèvi imaj tema yo"""
    try:
        theme = Theme.objects.filter(actif=True).first()
        if theme:
            image_field = getattr(theme, field_name, None)
            if image_field and image_field.name:
                try:
                    content_type = 'image/' + image_field.name.split('.')[-1].lower()
                    if content_type == 'image/jpg':
                        content_type = 'image/jpeg'
                    response = HttpResponse(image_field.read(), content_type=content_type)
                    response['Cache-Control'] = 'max-age=86400'
                    return response
                except Exception as e:
                    logger.error(f"Error serving image {field_name}: {e}")
    except Exception as e:
        logger.error(f"Error in serve_theme_image: {e}")
    raise Http404("Image not found")


def theme_logo(request):
    return serve_theme_image(request, 'logo')


def theme_favicon(request):
    return serve_theme_image(request, 'favicon')


def theme_hero_image(request):
    return serve_theme_image(request, 'hero_image')


def theme_about_image(request):
    return serve_theme_image(request, 'about_image')


def theme_evenement_banner(request):
    return serve_theme_image(request, 'evenement_banner')


def theme_evenement_logo(request):
    return serve_theme_image(request, 'evenement_logo')