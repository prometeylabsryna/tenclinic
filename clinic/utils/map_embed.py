import re
from urllib.parse import urlparse

IFRAME_SRC_RE = re.compile(
    r'<iframe\b[^>]*\bsrc=["\']([^"\']+)["\']',
    re.IGNORECASE | re.DOTALL,
)

ALLOWED_MAP_HOSTS = frozenset({
    'www.google.com',
    'google.com',
    'maps.google.com',
})


def normalize_map_embed(raw: str) -> str:
    value = (raw or '').strip()
    if not value:
        return ''

    if '<iframe' in value.lower():
        match = IFRAME_SRC_RE.search(value)
        return match.group(1).strip() if match else ''

    return value


def is_allowed_map_embed_url(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.scheme not in {'http', 'https'}:
        return False

    host = (parsed.netloc or '').lower().split(':', 1)[0]
    if host not in ALLOWED_MAP_HOSTS:
        return False

    path = (parsed.path or '').lower()
    return path.startswith('/maps/embed') or path.startswith('/maps/')


def resolve_map_embed_src(raw_embed: str, *, lat=None, lng=None, address: str = '') -> str:
    embed_url = normalize_map_embed(raw_embed)
    if embed_url and is_allowed_map_embed_url(embed_url):
        return embed_url

    if lat is not None and lng is not None:
        return (
            f'https://maps.google.com/maps?q={lat},{lng}'
            f'&hl=uk&z=16&output=embed'
        )

    if address:
        from urllib.parse import quote
        return (
            f'https://maps.google.com/maps?q={quote(address)}'
            f'&hl=uk&z=16&output=embed'
        )

    return ''
