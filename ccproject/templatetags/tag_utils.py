from django import template

register = template.Library()


@register.filter(name='check_is_trusted')
def is_trusted(profile, recipient):
    return profile.profile.trusts(recipient.user.profile)


@register.filter(name='check_is_trusted_listing')
def is_trusted_listing(listing, profile):
    return listing.user.profile.trusts(profile)
