import json
from django import template

register = template.Library()

@register.filter(name='last_message')
def last_message(messages):
    if messages:
        last_message = messages[-1]
        return f'{"You: "+last_message.content if last_message.type == "sent" else last_message.content}'
    else:
        return "No messages yet"

@register.filter
def to_json(value):
    return json.dumps(value)