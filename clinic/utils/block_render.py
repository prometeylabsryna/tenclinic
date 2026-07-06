from clinic.block_defaults import BLOCK_DEFAULTS
from clinic.models import SiteBlock


def build_blocks_map():
    result = {}
    for block in SiteBlock.objects.filter(is_active=True):
        result[block.cache_key] = block
    return result


def _get_block(page, key, site_blocks=None):
    cache_key = f'{page}.{key}'
    if site_blocks and cache_key in site_blocks:
        return site_blocks[cache_key]
    return SiteBlock.objects.filter(page=page, key=key, is_active=True).first()


def get_block_text(page, key, site_blocks=None, fallback=''):
    block = _get_block(page, key, site_blocks=site_blocks)
    if block and block.text_html:
        return block.text_html
    if fallback:
        return fallback
    return BLOCK_DEFAULTS.get((page, key), '')


def get_block_image_url(page, key, site_blocks=None):
    block = _get_block(page, key, site_blocks=site_blocks)
    if block and block.image:
        return block.image.url
    return ''


def is_section_visible(page, visibility_key, site_blocks=None) -> bool:
    value = get_block_text(page, visibility_key, site_blocks=site_blocks, fallback='1')
    return value not in {'0', 'false', 'False', ''}
