from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name='inr')
def inr(value):
    """
    Formats a number into Indian Rupee formatting with ₹ symbol.
    Examples:
    1000    -> ₹1,000
    10000   -> ₹10,000
    99999   -> ₹99,999
    100000  -> ₹1,00,000
    129999  -> ₹1,29,999
    1299999 -> ₹12,99,999
    """
    if value is None or value == '':
        return "₹0"
    try:
        if isinstance(value, str):
            value = value.replace('$', '').replace('₹', '').replace(',', '').strip()
        num = float(value)
        is_negative = num < 0
        num = abs(num)
        
        int_part = int(round(num))
        num_str = str(int_part)
        
        if len(num_str) <= 3:
            formatted = num_str
        else:
            last3 = num_str[-3:]
            rest = num_str[:-3]
            pairs = []
            while len(rest) > 2:
                pairs.append(rest[-2:])
                rest = rest[:-2]
            if rest:
                pairs.append(rest)
            pairs.reverse()
            formatted = ",".join(pairs) + "," + last3
            
        res = f"₹{formatted}"
        return f"-{res}" if is_negative else res
    except Exception:
        return f"₹{value}"


@register.filter(name='inr_raw')
def inr_raw(value):
    """
    Formats a number into Indian Rupee numbering format WITHOUT the ₹ symbol.
    Examples:
    129999  -> 1,29,999
    1299999 -> 12,99,999
    """
    if value is None or value == '':
        return "0"
    try:
        if isinstance(value, str):
            value = value.replace('$', '').replace('₹', '').replace(',', '').strip()
        num = float(value)
        is_negative = num < 0
        num = abs(num)
        
        int_part = int(round(num))
        num_str = str(int_part)
        
        if len(num_str) <= 3:
            formatted = num_str
        else:
            last3 = num_str[-3:]
            rest = num_str[:-3]
            pairs = []
            while len(rest) > 2:
                pairs.append(rest[-2:])
                rest = rest[:-2]
            if rest:
                pairs.append(rest)
            pairs.reverse()
            formatted = ",".join(pairs) + "," + last3
            
        return f"-{formatted}" if is_negative else formatted
    except Exception:
        return str(value)
