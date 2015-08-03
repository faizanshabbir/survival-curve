from django.db import models

# Create Email list here.
class subscribeList(models.Model):
	name = models.CharField(max_length=255,)
	#last_name = models.CharField(max_length=255,)

	email = models.EmailField()

	def __str__(self):
		return ' '.join([self.first_name,self.last_name,])

# Contact form model
class contactForm(models.Model):
	name = models.CharField(max_length=255,)
	email = models.EmailField()

	message = models.TextField()


