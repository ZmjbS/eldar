from django import template

register = template.Library()

@register.filter(name='percentage')
def percentage(input, arg):
	return str(int(float(input) / float(arg) * 100))
