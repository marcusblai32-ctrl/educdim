from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def render_banner_carousel(banners, width='100%', height='auto'):
    if not banners:
        return ''
    html = '<div class="swiper banner-swiper" style="width:%s; height:%s;">' % (width, height)
    html += '<div class="swiper-wrapper">'
    for banner in banners:
        html += '<div class="swiper-slide">'
        if banner.lien:
            html += '<a href="%s" target="_blank">' % banner.lien
        html += '<img src="%s" alt="%s" style="width:100%%; height:100%%; object-fit:cover;">' % (banner.image.url, banner.titre)
        if banner.lien:
            html += '</a>'
        html += '</div>'
    html += '</div>'
    html += '<div class="swiper-pagination"></div>'
    html += '<div class="swiper-button-next"></div>'
    html += '<div class="swiper-button-prev"></div>'
    html += '</div>'
    return mark_safe(html)
