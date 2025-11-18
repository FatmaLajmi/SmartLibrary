import base64
from django import template

register = template.Library()

@register.filter(name='b64encode')
def b64encode(value):
    """Convert binary image data to base64 string for img src"""
    if value:
        try:
            return base64.b64encode(value).decode('utf-8')
        except:
            return ''
    return ''