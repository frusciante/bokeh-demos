import numpy as np

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=20)
    manager = models.OneToOneField(User)

    def __str__(self):
        return '%s (%s)' % (self.name, self.manager.first_name)


class Employee(models.Model):
    user = models.OneToOneField(User)
    teams = models.ManyToManyField('happiness.Team')

    def __str__(self):
        return '%s (%s)' % (self.user.first_name, self.teams_list)

    @property
    def teams_list(self):
        return ', '.join([team.name for team in self.teams.all()])

    def _get_happiness(self, start_date, end_date):
        h_set = self.happiness_set.order_by('date')
        if start_date:
            h_set = h_set.filteR(date__gte=start_date)
        if end_date:
            h_set = h_set.filteR(date__lte=end_date)
        return h_set

    def get_happiness_dates(self, start_date=None, end_date=None):
        h_set = self._get_happiness(start_date, end_date)
        dates = h_set.values_list('date', flat=True)
        return np.array(dates)

    def get_happiness_values(self, start_date=None, end_date=None):
        h_set = self._get_happiness(start_date, end_date)
        happinesses = h_set.values_list('happiness', flat=True)
        return np.array(happinesses)


class Happiness(models.Model):
    employee = models.ForeignKey(Employee)
    date = models.DateField()
    happiness = models.DecimalField(decimal_places=0, max_digits=1)

    unique_together = (('employee', 'date'),)

    def get_absolute_url(self):
        return reverse('individual', kwargs={'pk': self.employee.user.pk})

    def __str__(self):
        return '%s %s %s' % (self.employee.user.first_name, self.happiness, self.date)