from django import template

register = template.Library()

@register.filter
def get_progress_color(pages_read, total_pages):
    try:
        percent = (int(pages_read) / int(total_pages)) * 100
    except (ZeroDivisionError, ValueError):
        return "#ccc"

    if percent == 100:
        return "#00cc44"   # Green for complete
    elif percent >= 75:
        return "#80c904"   # Yellow-green
    elif percent >= 50:
        return "#ffcc00"   # Yellow
    elif percent >= 25:
        return "#ff8800"   # Orange
    else:
        return "#ff3300"   # Red

@register.filter
def divided_by(value, arg):
    try:
        return (float(value) / float(arg)) * 100
    except (ValueError, ZeroDivisionError):
        return 0
