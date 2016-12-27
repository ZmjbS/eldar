from django import template

register = template.Library()

@register.filter(name='get_abbreviation')
def get_abbreviation(input):
	output = ""
	for i in input.upper().split():
		output += i[0]
	
	return output