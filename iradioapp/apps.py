from django.apps import AppConfig
from . import mpcclient
class IRadioAppConfig(AppConfig):
	name = "iradioapp"
	verbose_name = "FunkyRadio"
	def ready(self):
		pass
