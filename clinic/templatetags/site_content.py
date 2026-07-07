from django import template
from django.templatetags.static import static
from django.utils.html import escape
from django.utils.safestring import mark_safe
import re

from clinic.utils.block_render import get_block_image_url, get_block_text, is_section_visible

register = template.Library()


@register.filter
def initials(value):
    if not value:
        return ''
    parts = str(value).split()
    if len(parts) >= 2:
        return f'{parts[0][:1]}{parts[1][:1]}'.upper()
    return parts[0][:1].upper() if parts[0] else ''


@register.filter
def lines(value):
    if not value:
        return []
    return [line.strip() for line in str(value).splitlines() if line.strip()]


@register.filter
def first_sentences(value, count=2):
    if not value:
        return ''
    text = str(value).strip()
    sentences = [part.strip() for part in re.split(r'(?<=[.!?…])\s+', text) if part.strip()]
    if not sentences:
        return text
    try:
        limit = int(count)
    except (TypeError, ValueError):
        limit = 2
    return ' '.join(sentences[:limit])


@register.filter
def hero_title_suffix(value):
    text = str(value or '').strip()
    upper = text.upper()
    if upper.startswith('TEN '):
        return text[4:]
    if upper.startswith('TEN'):
        return text[3:].lstrip()
    return text


def _strip_leading_dash(value):
    rest = value.lstrip()
    dashes = ('—', '–', '-')
    prefix = ''
    while rest:
        matched = False
        for dash in dashes:
            if rest.startswith(dash):
                prefix = f'{prefix}{dash} '
                rest = rest[len(dash):].lstrip()
                matched = True
                break
        if not matched:
            break
    return prefix.rstrip(), rest


def _parse_hero_title(raw):
    text = hero_title_suffix(raw)
    if text.lower().startswith('clinic'):
        rest = text[6:].lstrip()
        dash, rest = _strip_leading_dash(rest)
        clinic_part = 'clinic'
        if dash:
            clinic_part = f'clinic {dash}'
        return clinic_part, rest
    return '', text


@register.simple_tag(takes_context=True)
def hero_title_clinic(context):
    raw = get_block_text(
        'home',
        'hero_title',
        site_blocks=context.get('site_blocks'),
        fallback='TEN clinic — новий стандарт медичної допомоги',
    )
    clinic, _ = _parse_hero_title(raw)
    return clinic


@register.simple_tag(takes_context=True)
def hero_title_rest(context):
    raw = get_block_text(
        'home',
        'hero_title',
        site_blocks=context.get('site_blocks'),
        fallback='TEN clinic — новий стандарт медичної допомоги',
    )
    _, rest = _parse_hero_title(raw)
    return rest


@register.simple_tag(takes_context=True)
def block_plain(context, page, key, fallback=''):
    return get_block_text(page, key, site_blocks=context.get('site_blocks'), fallback=fallback)


@register.simple_tag(takes_context=True)
def section_visible(context, page, key):
    return is_section_visible(page, key, site_blocks=context.get('site_blocks'))


@register.simple_tag(takes_context=True)
def block_image_url(context, page, key, fallback_static=''):
    url = get_block_image_url(page, key, site_blocks=context.get('site_blocks'))
    if url:
        return url
    if fallback_static:
        return static(fallback_static)
    return ''


@register.simple_tag(takes_context=True)
def block_image(
    context,
    page,
    key,
    css_class='',
    fallback_static='',
    alt='',
    width='',
    height='',
    loading='lazy',
    decoding='async',
):
    url = get_block_image_url(page, key, site_blocks=context.get('site_blocks'))
    if not url and fallback_static:
        url = static(fallback_static)
    if not url:
        return ''

    attrs = [f'src="{escape(url)}"']
    if alt:
        attrs.append(f'alt="{escape(alt)}"')
    else:
        attrs.append('alt=""')
    if css_class:
        attrs.append(f'class="{escape(css_class)}"')
    if width:
        attrs.append(f'width="{escape(str(width))}"')
    if height:
        attrs.append(f'height="{escape(str(height))}"')
    if loading:
        attrs.append(f'loading="{escape(loading)}"')
    if decoding:
        attrs.append(f'decoding="{escape(decoding)}"')
    return mark_safe(f'<img {" ".join(attrs)}>')


@register.simple_tag(takes_context=True)
def site_logo_url(context):
    settings_obj = context.get('site_settings')
    if settings_obj and settings_obj.logo:
        return settings_obj.logo.url
    return static('images/logo.png')
