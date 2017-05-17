from django import template

register = template.Library()


@register.filter(name='check_is_trusted')
def is_trusted(profile, recipient):
    return profile.profile.trusts(recipient.user.profile)

