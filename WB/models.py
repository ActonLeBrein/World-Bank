from django.db import models
import datetime

# Create your models here.

class WB_Category(models.Model):
	Theme = models.CharField(unique=True, max_length=100)
	def __unicode__(self):
		return u'%s' % (self.Theme)

class Indicator_Type(models.Model):
	Types = (
		('n/a', 'n/a'),
		('SbPb','SbPb'),
		('Ops','Ops'),
		)
	Type = models.CharField(primary_key=True, max_length=5, choices=Types)
	def __unicode__(self):
		return u'%s' % (self.Type)

class Indicator_Country(models.Model):
	Country = models.CharField(primary_key=True, max_length=100)
	def __unicode__(self):
		return u'%s' % (self.Country)

class Indicator(models.Model):
	Grades = (
		('n/a','n/a'),
		('g','Green'),
		('y','Yellow'),
		('r','Red'),
		)
	Description = models.TextField(max_length=500, blank=True, null=True)
	Quality = models.CharField(max_length=3, choices=Grades)
	DataSets_Availables = models.URLField(max_length=1000, blank=True, null=True)
	created = models.DateField()
	modified = models.DateTimeField()
	PBSB = models.TextField()
	Source = models.TextField()
	ID_WB_Category = models.ForeignKey(WB_Category)
	ID_Indicator_Type = models.ForeignKey(Indicator_Type)
	ID_Indicator_Country = models.ForeignKey(Indicator_Country)

	def save(self, *args, **kwargs):
		''' On save, update timestamps '''
		if not self.id:
			self.created = datetime.date.today()
		self.modified = datetime.datetime.today()
		return super(Indicator, self).save(*args, **kwargs)
	def __unicode__(self):
		return u'%s, %s' % (self.id, self.Description)

class Indicator_Comments(models.Model):
	Comment = models.TextField(max_length=500)
	ID_Indicator = models.ForeignKey(Indicator, blank=True, null=True)
	def __unicode__(self):
		return u'%s' % (self.Comment)

class Indicator_Notes(models.Model):
	Note = models.CharField(max_length=200)
	ID_Indicator = models.ForeignKey(Indicator, blank=True, null=True)
	def __unicode__(self):
		return u'%s' % (self.Note)