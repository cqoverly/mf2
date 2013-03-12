from django.db import models


class FieldCategory(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(max_length=600)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Field(models.Model):
    name = models.CharField(max_length=20)
    category = models.ForeignKey(FieldCategory)
    description = models.TextField(max_length=600)

    class Meta:
        ordering = ['category', 'name']

    def __unicode__(self):
        return "{0}: {1}".format(self.name, self.category)

    def search(self, category=None):
        if category:
            queryset = self.objects.filter(category=category)
            return queryset
        else:
            return self.objects.all()

