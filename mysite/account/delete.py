from threading import Thread
from time import sleep
import models
def async(f):
	def wrapper(*args, **kwargs):
		thr = Thread(target=f, args=args, kwargs=kwargs)
	thr.start()
	return wrapper



def delete_db(table,mail):
	sleep(60)
	user = table.objects.get(r_email=mail)
	if user:
		user.delete
