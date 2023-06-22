from django import template

register = template.Library()

@register.filter
def multiply_by_ten(value):
	return value * 10