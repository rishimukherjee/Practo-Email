from django.db import models

class Email(models.Model):
     """Table to store email information."""
     mail_date = models.DateTimeField(auto_now_add=True)
     mail_content = models.CharField(max_length=10240)
     mail_users = models.CharField(max_length=2048)
     mail_subject = models.CharField(max_length=512)
     mail_attachment = models.FileField(upload_to = 'attachments/%Y/%m/%d')

     def __unicode__(self):
        return self.mail_subject