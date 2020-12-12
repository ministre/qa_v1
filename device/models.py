from django.db import models


class DeviceType(models.Model):
    main_type = models.CharField(max_length=50)
    sub_type = models.CharField(max_length=50, blank=True, null=True)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Device(models.Model):
    project_id = models.CharField(max_length=50)
    type = models.ForeignKey(DeviceType, on_delete=models.CASCADE)
    vendor = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    hw = models.CharField(max_length=50, blank=True, null=True)
    interfaces = models.CharField(max_length=300)
    leds = models.CharField(max_length=300)
    buttons = models.CharField(max_length=300)
    chipsets = models.CharField(max_length=300)
    memory = models.CharField(max_length=50)

    class Meta:
        ordering = ["model"]

    def __str__(self):
        return self.model
