import base64
from django import template

register = template.Library()

@register.filter
def to_base64(image_bytes):
    if image_bytes is None:
        return ""
    return base64.b64encode(image_bytes).decode('utf-8')
