# -*- coding: utf-8 -*-
u"""Modelos gerais do Gestão Livre."""

from datetime import date
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import F
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import dateformat
from django.utils.translation import ugettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey

from gestaolivre.apps.geral.models import EmpresaModel


leaf_nodes = Q(rght=F('lft') + 1)


def open_period_validator(value):
    from .models import Period
    period = Period.objects.filter(status=Period.OPEN, start_date__lte=value, end_date__gte=value).first()
    if not period:
        raise ValidationError(
            _('There is no open calendar for %(date)s'),
            params={'date': dateformat.format(value, _('m/d/Y'))},
        )


class Conta(EmpresaModel, MPTTModel):
    CREDITO = 'C'
    DEBITO = 'D'
    ANALITICA = 'A'
    SINTETICA = 'S'
    NATUREZA_CHOICES = (
        (CREDITO, 'Credito'),
        (DEBITO, 'Débito'),
    )
    TIPO_CHOICES = (
        (ANALITICA, _('Analytical')),
        (SINTETICA, _('Synthetic')),
    )
    codigo = models.CharField(max_length=20, verbose_name='código',
                              validators=[RegexValidator(
                                regex='^[1-9](\.[1-9](\.[1-9](\.\d{2}(\.\d{4})?)?)?)?$',
                                message='O código deve estar no formato 9.9.9.99.9999')])
    nome = models.CharField(max_length=50, verbose_name=_('name'))
    nature = models.CharField(max_length=1, choices=NATUREZA_CHOICES, default=CREDITO, verbose_name=_('nature'))
    type = models.CharField(max_length=1, choices=TIPO_CHOICES, default=ANALITICA, verbose_name=_('type'))
    parent = TreeForeignKey('self', blank=True, null=True, related_name='children', verbose_name=_('parent'))

    def __str__(self):
        return self.codigo + ' - ' + self.nome

    def clean(self):
        if self.type == Conta.ANALITICA:
            if not self.parent or self.parent.level < 2:
                raise ValidationError(_('An analytical account level must be 4 or greater.'))

    class Meta:
        verbose_name = _('account')
        verbose_name_plural = _('accounts')
        unique_together = (('domain', 'code'),)
        ordering = ['code']

    class MPTTMeta:
        order_insertion_by = ['code']


class Entry(EmpresaModel):
    DRAFT = 'D'
    PENDING = 'P'
    APPROVED = 'A'
    FROZEN = 'F'
    STATUS_CHOICES = (
        (DRAFT, _('Draft')),
        (PENDING, _('Pending')),
        (APPROVED, _('Approved')),
        (FROZEN, _('Frozen')),
    )
    date = models.DateField(default=date.today, verbose_name=_('date'), validators=[open_period_validator])
    memo = models.CharField(max_length=150, verbose_name=_('memo'))
    value = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)],
                                default=0, verbose_name=_('value'))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=DRAFT, verbose_name=_('status'))

    def __str__(self):
        return '{0}: {1}: {2}'.format(self.date, self.memo, self.value)

    class Meta:
        verbose_name = _('entry')
        verbose_name_plural = _('entries')


class EntryItem(EmpresaModel):
    entry = models.ForeignKey(Entry, related_name='items', verbose_name=_('entry'))
    account = models.ForeignKey(Conta, related_name='items', verbose_name=_('account'), limit_choices_to=leaf_nodes)
    debit_value = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)],
                                      default=0, verbose_name=_('debit value'))
    credit_value = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)],
                                       default=0, verbose_name=_('credit value'))

    def __str__(self):
        return '{0}: -{1} +{2}'.format(self.account, self.debit_value, self.credit_value)

    class Meta:
        verbose_name = _('entry item')
        verbose_name_plural = _('entry items')
        ordering = ('account__code',)

    def clean(self):
        super().clean()
        if self.debit_value > 0 and self.credit_value > 0:
            raise ValidationError(_('You must inform only debit or credit value, not both.'))
        if self.debit_value == 0 and self.credit_value == 0:
            raise ValidationError(_('You must inform debit or credit value.'))


class FiscalYear(EmpresaModel):
    OPEN = 'O'
    CLOSED = 'C'
    STATUS_CHOICES = (
        (OPEN, _('Open')),
        (CLOSED, _('Closed')),
    )
    year = models.IntegerField(verbose_name=_('year'), validators=[MinValueValidator(2000), MaxValueValidator(2100)])
    start_date = models.DateField(verbose_name=_('start date'))
    end_date = models.DateField(verbose_name=_('end date'))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=OPEN, verbose_name=_('status'))

    class Meta:
        verbose_name = _('fiscal year')
        verbose_name_plural = _('fiscal years')
        ordering = ('year',)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError(_('Start date must not be greater than end date.'))

    def __str__(self):
        return str(self.year)


@receiver(post_save, sender=FiscalYear)
def new_year(sender, created, instance, **kwargs):
    if not created:
        return
    fiscal_year = instance
    year = fiscal_year.year
    import calendar
    for month in range(1, 13):
        last_day_in_month = calendar.monthrange(year, month)[1]
        period = Period(year=fiscal_year,
                        start_date=date(year, month, 1),
                        end_date=date(year, month, last_day_in_month))
        period.save()


class Period(EmpresaModel):
    OPEN = 'O'
    CLOSED = 'C'
    STATUS_CHOICES = (
        (OPEN, _('Open')),
        (CLOSED, _('Closed')),
    )
    STANDARD = 'S'
    ADJUSTMENT = 'A'
    TYPE_CHOICES = (
        (STANDARD, _('Standard')),
        (ADJUSTMENT, _('Adjustment')),
    )
    year = models.ForeignKey(FiscalYear, related_name='periods', verbose_name=_('year'))
    start_date = models.DateField(verbose_name=_('start date'))
    end_date = models.DateField(verbose_name=_('end date'))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default=OPEN, verbose_name=_('status'))
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default=STANDARD, verbose_name=_('type'))

    class Meta:
        verbose_name = _('period')
        verbose_name_plural = _('periods')
        ordering = ('start_date', 'end_date',)

    def __str__(self):
        return _('%(start)s to %(end)s') % {'start': dateformat.format(self.start_date, _('m/d/Y')),
                                            'end': dateformat.format(self.end_date, _('m/d/Y'))}

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError(_('Start date must not be greater than end date.'))

    def next(self):
        return Period.objects.filter(start_date=self.end_date + timedelta(days=1)).first()

    def previous(self):
        return Period.objects.filter(end_date=self.start_date - timedelta(days=1)).first()


class PeriodicBalance(EmpresaModel):
    account = models.ForeignKey(Conta, verbose_name=_('account'))
    period = models.ForeignKey(Period, verbose_name=_('period'))
    initial_balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('initial balance'))
    final_balance = models.DecimalField(max_digits=12, decimal_places=2, verbose_name=_('final balance'))
    debit_value = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)],
                                      default=0, verbose_name=_('debit value'))
    credit_value = models.DecimalField(max_digits=12, decimal_places=2, validators=[MinValueValidator(0)],
                                       default=0, verbose_name=_('credit value'))

    class Meta:
        verbose_name = _('periodic balance')
        verbose_name_plural = _('periodic balances')
        ordering = ('period__start_date',)

    def __str__(self):
        return '{0}: {1} {2}'.format(self.account, self.period.start_date, self.initial_balance)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('accounting:balance_sheet', kwargs={'pk': self.period.id})

    @staticmethod
    def calculate_for(period, include_results=True):
        def create_for(account, period):
            pb = PeriodicBalance.objects.filter(period=period.previous(), account=account).first()
            return PeriodicBalance(account=account,
                                   period=period,
                                   initial_balance=pb.final_balance if pb else 0,
                                   final_balance=0,
                                   debit_value=0,
                                   credit_value=0)

        for periodic_balance in PeriodicBalance.objects.filter(period=period):
            periodic_balance.delete()

        accounts_balance = dict([(a, create_for(a, period)) for a in Conta.objects.all()])

        if include_results:
            query = Q(entry__date__gte=period.start_date) & \
                Q(entry__date__lte=period.end_date)
        else:
            query = ~Q(entry__memo='APURAÇÃO RESULTADO 12/2014') & \
                    ~Q(entry__memo='VLR.DISTRIBUIÇÃO DE LUCROS AO SÓCIO SERGIO RAFAEL GARCIA') & \
                Q(entry__date__gte=period.start_date) & \
                Q(entry__date__lte=period.end_date)

        for entry_item in EntryItem.objects.filter(query).all():
            account = entry_item.account
            while account:
                account_balance = accounts_balance[account]
                account_balance.debit_value += entry_item.debit_value
                account_balance.credit_value += entry_item.credit_value
                account = account.parent

        for ab in accounts_balance.values():
            ab.final_balance = ab.initial_balance + ab.credit_value - ab.debit_value
            ab.save()

