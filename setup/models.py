import uuid
from django.db import models
from django_cron import CronJobBase, Schedule
 
from django.utils import formats, timezone
from datetime import datetime, timedelta       
from ckeditor_uploader.fields import RichTextUploadingField
from account.models import User

 
 
 