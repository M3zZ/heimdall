from django import template

register = template.Library()


@register.filter('klass')
def klass(ob):
    return ob.__class__.__name__


@register.filter('type')
def gettype(ob):
    return type(ob)


@register.filter('is_choice')
def is_choice(ob):
    print ob
    if klass(ob) == 'ModelMultipleChoiceField' or klass(ob) == 'ModelChoiceField':
        return True
    else:
        return False
