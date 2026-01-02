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
