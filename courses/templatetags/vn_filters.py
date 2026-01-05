from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def vn_thousand(value):
    """Format a number with dot as thousands separator and no decimal places.
    Examples: 200000 -> '200.000', 1000000 -> '1.000.000'
    Works with int, float, Decimal, or numeric string.
    """
    if value is None:
        return ''
    try:
        # convert to int (round if Decimal)
        if isinstance(value, Decimal):
            val = int(value.quantize(Decimal('1')))
        else:
            val = int(round(float(value)))
    except Exception:
        try:
            val = int(str(value))
        except Exception:
            return value
    s = f"{val:,}"  # uses comma as thousands
    # replace comma with dot for VN style
    return s.replace(',', '.')


@register.filter
def replace(value, arg):
    """Replace occurrences of `old` with `new` in the given string.

    Usage in template: {{ value|replace:"old|new" }}
    Example: {{ value|replace:"watch?v=|embed/" }}
    """
    try:
        if value is None:
            return ''
        parts = str(arg).split('|', 1)
        if len(parts) != 2:
            return value
        old, new = parts
        return str(value).replace(old, new)
    except Exception:
        return value


@register.filter
def resource_url(value):
    """Normalize a resource string to a usable URL.

    - If value already starts with http/https, return it unchanged.
    - If value looks like a youtube id (11 chars, alnum), return https://youtu.be/<id>
    - If value contains 'youtube' or 'youtu.be', ensure it has scheme and return it.
    - Otherwise, prefix with 'http://' to avoid relative links.
    """
    try:
        if not value:
            return ''
        s = str(value).strip()
        lower = s.lower()
        # Absolute path on same host
        if s.startswith('/'):
            return s
        # Already absolute URL
        if lower.startswith('http://') or lower.startswith('https://'):
            return s
        # YouTube full links or short links
        if 'youtube' in lower or 'youtu.be' in lower:
            return ('https://' + s) if not lower.startswith('http') else s
        # Heuristic: YouTube IDs are typically 11 chars alphanumeric
        if len(s) == 11 and s.isalnum():
            return f'https://youtu.be/{s}'
        # If contains a dot, assume it's a domain or path-like and add scheme
        if '.' in s:
            return 'http://' + s
        # Unknown/short token (e.g., '121' or 'qq') -> do not fabricate an absolute URL
        return ''
    except Exception:
        return value


@register.filter
def resource_embed(value):
    """Return an embeddable URL for iframe when possible.

    - Converts YouTube watch or short links to embed URLs.
    - If not a YouTube link, returns the normalized `resource_url` value.
    """
    try:
        url = resource_url(value)
        if not url:
            return ''
        lower = url.lower()
        # YouTube -> embed
        if 'watch?v=' in lower:
            return url.replace('watch?v=', 'embed/')
        if 'youtu.be/' in lower:
            return url.replace('youtu.be/', 'www.youtube.com/embed/')

        # Google Drive: convert to /preview when possible
        if 'drive.google.com' in lower:
            # Patterns:
            # - https://drive.google.com/file/d/<id>/view?usp=sharing
            # - https://drive.google.com/open?id=<id>
            # - other variants with /view -> /preview
            import re
            m = re.search(r'/file/d/([A-Za-z0-9_-]+)/', url)
            if m:
                fid = m.group(1)
                return f'https://drive.google.com/file/d/{fid}/preview'
            m2 = re.search(r'[?&]id=([A-Za-z0-9_-]+)', url)
            if m2:
                fid = m2.group(1)
                return f'https://drive.google.com/file/d/{fid}/preview'
            # fallback: replace /view with /preview
            if '/view' in url:
                return url.replace('/view', '/preview')

        # PDF can be embedded in iframe
        if lower.endswith('.pdf'):
            return url

        # Other file types (docx, xlsx, pptx) are not reliably embeddable in iframe.
        # Return empty so template will render a download/open link instead.
        return ''
    except Exception:
        return value
