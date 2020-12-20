from django.db import models


class TestPlan(models.Model):
    name = models.CharField(max_length=500)
    version = models.CharField(max_length=30)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return str(self.name) + ' (' + str(self.version) + ')'

    def protocols_count(self):
        from protocol.models import Protocol
        count = Protocol.objects.filter(testplan=self).count()
        return count


class Test(models.Model):
    testplan = models.ForeignKey(TestPlan, on_delete=models.CASCADE)
    category = models.CharField(max_length=300)
    name = models.CharField(max_length=300)
    url = models.CharField(max_length=300, null=True, blank=True)
    procedure = models.TextField()
    expected = models.TextField()

    def __str__(self):
        return self.name
