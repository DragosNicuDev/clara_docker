from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.conf import settings


# Admin option to select from
PHOTO_STATUS = (
    ('ir', 'In Review'),
    ('ap', 'Approved'),
    ('tr', 'Trash'),
)


def pause():
    return timezone.now() + timezone.timedelta(minutes=5)


# Main photo upload app
class PhotoUpload(models.Model):
    '''After the user finishes the challenge
    he can upload a photo using this app'''
    # The date when a user uploads a photo
    date_upload = models.DateTimeField(default=timezone.now)
    # The date when user can upload another photo

    # pause = date_upload + timezone.timedelta(minutes=20)
    pause_upload = models.DateTimeField(default=pause)
    # The status of the photo
    status = models.CharField(max_length=2, default='ir', choices=PHOTO_STATUS)
    # The date when the admin aproves the photo
    date_approved = models.DateTimeField(default=timezone.now,
                                         blank=True,
                                         null=True)
    # The date when the admin soft-deletes the photo
    date_deleted = models.DateTimeField(default=timezone.now,
                                        blank=True,
                                        null=True)
    user = models.ForeignKey(User)

    # A function that defines the path where the photo
    # will be uploaded and that will change the filename.
    def path_and_rename(instance, filename):
        extension = filename.split('.')[-1]
        if User.is_authenticated:
            # print(instance._user.username)
            return 'uploads/{}-{}.{}'.format(instance.user.username,
                                             instance.date_upload,
                                             extension)
        else:
            return 'uploads/{}.{}'.format(instance.date_upload, extension)

    # Application side file size check
    def file_size(value):
        limit = 2 * 1024 * 1024
        if value.size > limit:
            raise ValidationError(
                'File too large. Size should not exceed 2 MB.')

    image = models.ImageField(upload_to=path_and_rename,
                              validators=[file_size],
                              null=True,
                              blank=True)

    def __str__(self):
        return str(self.pause_upload)


@receiver(pre_delete, sender=PhotoUpload)
def mymodel_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.image.delete(True)
