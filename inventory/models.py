from django.db import models


class InventoryItem(models.Model):
	picture = models.ImageField(blank=True, null=True)
	name = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	quantity_per_ctn = models.IntegerField(blank=True, null=True, default=0)
	quantity_in_ctn = models.IntegerField(blank=True, null=True, default=0)
	category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
	date_created = models.DateTimeField(auto_now_add=True)
	

	def __str__(self):
		return self.name

class Category(models.Model):
	name = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = 'categories'

	def __str__(self):
		return self.name