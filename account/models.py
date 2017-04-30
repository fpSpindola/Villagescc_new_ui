from decimal import Decimal as D
from datetime import datetime

from django.db import models
from django.db.models.signals import post_delete, post_save

from ripple import PRECISION, SCALE
from general.util import cache_on_object

OVERALL_BALANCE_SQL = """
select sum(balance) from (
	select ac.balance * cl.bal_mult as balance
	from account_creditline as cl
	join account_account as ac on cl.account_id = ac.id
	where cl.node_id = %s) as cl_balances
"""

TRUSTED_BALANCE_SQL = """
select sum(trusted_balance) from (
	select (case when ac.balance * cl.bal_mult <= partner_cl.limit
		then ac.balance * cl.bal_mult
		else partner_cl.limit end) as trusted_balance
	from account_creditline as cl
	join account_account as ac on cl.account_id = ac.id
	join account_creditline as partner_cl
		on partner_cl.account_id = cl.account_id and
			partner_cl.node_id != cl.node_id
	where cl.node_id = %s) as trusted_balances
"""

class AmountField(models.DecimalField):
    "Field for value amounts."
    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = PRECISION
        kwargs['decimal_places'] = SCALE
        super(AmountField, self).__init__(*args, **kwargs)


class Node(models.Model):
    "A node in the Ripple graph."
    alias = models.PositiveIntegerField(unique=True)  # Profile ID.

    def __unicode__(self):
        return u"Node %d" % self.alias

    def __repr__(self):
        return "Node(%d)" % self.alias

    def out_creditlines(self):
        return self.creditlines.all()

    def _balance_query(self, sql_template):
        from django.db import connections
        cursor = connections['ripple'].cursor()
        cursor.execute(sql_template, (self.id,))
        row = cursor.fetchone()
        return row[0] or D('0')

    def overall_balance(self):
        return self._balance_query(OVERALL_BALANCE_SQL)

    def trusted_balance(self):
        """
        Return sum of all negative balances and all positive balances within
        credit limits.
        """
        return self._balance_query(TRUSTED_BALANCE_SQL)


class AccountManager(models.Manager):
    def create_account(self, node1, node2):
        """
        Create account between two nodes.
        Also creates the required CreditLine records.
        """
        acct = self.create()
        pos_cl = CreditLine.objects.create(
            account=acct, node=node1, bal_mult=1)
        neg_cl = CreditLine.objects.create(
            account=acct, node=node2, bal_mult=-1)

        # Manually update new creditlines in cached graphs.
        from payment import flow
        flow.update_creditline_in_cached_graphs(pos_cl)
        flow.update_creditline_in_cached_graphs(neg_cl)
        return acct

    def get_account(self, node1, node2):
        "Gets account between node1 and node2."
        # TODO: Test this thoroughly.
        acct_list = list(self.raw(
            "select a.* from account_account a "
            "join account_creditline c1 on c1.account_id = a.id "
            "join account_creditline c2 on c2.account_id = a.id "
            "where c1.node_id = %s "
            "and c2.node_id = %s", (node1.id, node2.id)))
        if len(acct_list) == 0:
            return None
        elif len(acct_list) == 1:
            acct = acct_list[0]
        else:
            raise Account.MultipleObjectsReturned()
        return acct

    def get_or_create_account(self, node1, node2):
        acct = self.get_account(node1, node2)
        if acct is None:
            acct = self.create_account(node1, node2)
        return acct


class Account(models.Model):
    """
    A mutual credit account that tracks IOUs between two nodes.
    This table stores the balance and other data shared between the nodes.
    CreditLine below stores symmetric data that each node has about
    the account.  Each account has two CreditLines.
    """
    balance = AmountField(default=D('0'))
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()

    def __unicode__(self):
        return u"Account %s" % self.id

    @property
    def pos_creditline(self):
        return self.creditlines.get(bal_mult=1)

    @property
    def neg_creditline(self):
        return self.creditlines.get(bal_mult=-1)

    @property
    def pos_node(self):
        return self.pos_creditline.node

    @property
    def neg_node(self):
        return self.neg_creditline.node

class CreditLine(models.Model):
    """
    One node's data for and view on a mutual credit account.
    """
    account = models.ForeignKey(Account, related_name='creditlines')
    node = models.ForeignKey(Node, related_name='creditlines')
    bal_mult = models.SmallIntegerField(
        choices=((1, '+1'), (-1, '-1')))
    # Max obligations node can emit to partner.
    limit = AmountField(default=D('0'), null=True, blank=True)

    def __unicode__(self):
        return u"%s's credit line for account %s" % (self.node, self.account_id)

    @property
    def balance(self):
        "Node's balance."
        return self.account.balance * self.bal_mult

    @property
    @cache_on_object
    def partner_creditline(self):
        return CreditLine.objects.exclude(
            node__pk=self.node_id).get(account__pk=self.account_id)

    @property
    def partner(self):
        return self.partner_creditline.node

    @property
    def in_limit(self):
        "Max obligations node will accept from partner."
        return self.partner_creditline.limit

    @classmethod
    def post_save(cls, sender, instance, created, **kwargs):
        if created:
            # Newly-created creditlines may not have a partner yet,
            # so updating them will blow up.  Update new creditlines
            # manually.
            return

        from payment import flow

        # TODO: Call from single external process -- not threadsafe!

        flow.update_creditline_in_cached_graphs(instance)

    @classmethod
    def post_delete(cls, sender, instance, **kwargs):
        # Delete partner creditline and account itself.
        try:
            instance.account.delete()
        except Account.DoesNotExist:
            pass

        # Remove from cached flow graph.
        from payment import flow

        # TODO: Call from single external process -- not threadsafe!

        # XXX: This is broken - tries to load partner creditline, which
        #      may already be (is?) deleted.
        flow.update_creditline_in_cached_graphs(instance)

post_save.connect(CreditLine.post_save, CreditLine,
                  dispatch_uid='account.models')
post_delete.connect(CreditLine.post_delete, CreditLine,
                    dispatch_uid='account.models')
