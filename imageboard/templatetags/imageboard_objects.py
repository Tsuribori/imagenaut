from django import template

register = template.Library()

@register.inclusion_tag('imageboard/includes/thread_template.html', takes_context=True)
def thread_format(context, thread):
    return {
        'thread': thread,
        'moderation_view': context.get('moderation_view'),
        'perms': context.get('perms'),
    }

@register.inclusion_tag('imageboard/includes/userpost_template.html', takes_context=True)
def post_format(context, post):
    return {
      'post': post,
      'moderation_view': context.get('moderation_view'),
      'perms': context.get('perms'),
    }
