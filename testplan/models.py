from django.db import models


class TestPlan(models.Model):
    version = models.CharField(max_length=30)
    name = models.CharField(max_length=500)

    def __str__(self):
        return str(self.name) + ' (' + str(self.version) + ')'


class Test(models.Model):
    testplan = models.ForeignKey(TestPlan, on_delete=models.CASCADE)
    category = models.CharField(max_length=300)
    url = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    procedure = models.TextField()
    expected = models.TextField()

    def __str__(self):
        return self.name
