from django import template
from django.utils.translation import ugettext_lazy as _

import ripple.api as ripple

register = template.Library()

@register.simple_tag
def reputation(profile, asker):
    return profile.reputation(asker)

@register.tag
def load_user_account(parser, token):
    """
    Loads a UserAccount Ripple API object into the current context.

    Example:
    {% load_user_account profile partner as target_var %}
    """
    try:
        tag_name, profile_var, partner_var, as_token, target_var = (
            token.split_contents())
    except ValueError:
        raise template.TemplateSyntaxError(
            "load_user_account tag must contain five elements.")
    if as_token != 'as':
        raise template.TemplateSyntaxError(
            "load_user_account tag must have 'as' as the 4th element.")
    return LoadUserAccountNode(profile_var, partner_var, target_var)

class LoadUserAccountNode(template.Node):
    def __init__(self, profile_var, partner_var, target_var):
        self.profile_var = template.Variable(profile_var)
        self.partner_var = template.Variable(partner_var)
        self.target_var_name = target_var

    def render(self, context):
        profile = self.profile_var.resolve(context)
        partner = self.partner_var.resolve(context)
        user_account = ripple.get_account(profile, partner)
        context[self.target_var_name] = user_account
        return ''

@register.simple_tag
def entry_description(entry, profile):
    if entry.payment.payer == profile:
        desc = _("Sent acknowledgement to %s") % entry.payment.recipient
    elif entry.payment.recipient == profile:
        desc = _("Received acknowledgement from %s") % entry.payment.payer
    else:

        # TODO: Maybe "acknowledged %s in exchange for acknowledgement from %s"?
        # Something else with "exchanged"?
        
        desc = _("Helped route acknowledgement from %(from)s to %(to)s") % {
		'from': entry.payment.payer, 'to': entry.payment.recipient }
    return desc
