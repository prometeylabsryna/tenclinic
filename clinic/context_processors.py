from django.core.cache import cache
from django.conf import settings

from clinic.models import SiteBlock, SiteSettings, WorkingHours
from clinic.utils.block_render import build_blocks_map


def _compact_hours_summary():
    rows = list(WorkingHours.objects.order_by('day_of_week'))
    if not rows:
        return 'Пн–Пт 9:00–18:00 · Сб 9:00–14:00 · Нд: вихідний'

    parts = []
    weekdays = [r for r in rows if r.day_of_week < 5]
    if weekdays and all(not r.is_closed for r in weekdays):
        open_t = weekdays[0].open_time
        close_t = weekdays[0].close_time
        if all(r.open_time == open_t and r.close_time == close_t for r in weekdays):
            parts.append(f'Пн–Пт {open_t:%H:%M}–{close_t:%H:%M}')

    saturday = next((r for r in rows if r.day_of_week == 5), None)
    if saturday:
        if saturday.is_closed:
            parts.append('Сб: вихідний')
        else:
            parts.append(f'Сб {saturday.open_time:%H:%M}–{saturday.close_time:%H:%M}')

    sunday = next((r for r in rows if r.day_of_week == 6), None)
    if sunday:
        parts.append('Нд: вихідний' if sunday.is_closed else f'Нд {sunday.open_time:%H:%M}–{sunday.close_time:%H:%M}')

    return ' · '.join(parts) if parts else ''


def site_context(request):
    settings_obj = SiteSettings.get_solo()
    blocks = cache.get(settings.SITE_BLOCKS_CACHE_KEY)
    if blocks is None:
        blocks = build_blocks_map()
        cache.set(settings.SITE_BLOCKS_CACHE_KEY, blocks, settings.SITE_BLOCKS_CACHE_TIMEOUT)
    return {
        'site_settings': settings_obj,
        'site_blocks': blocks,
        'footer_hours': _compact_hours_summary(),
    }
