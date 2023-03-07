from django import template


register = template.Library()

CURRENCIES_SYMBOLS = {
   'Игры': '*',
}


@register.filter()
def currency(value, code='Игры'):

   postfix = CURRENCIES_SYMBOLS[code]

   return f'{value} {postfix}'
