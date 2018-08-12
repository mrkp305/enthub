from django.db import models
from django.utils.translation import ugettext_lazy as _
import uuid

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    folder_mask = str(uuid.uuid4())
    return 'avatar/{}{}{}/{}'.format(folder_mask[:4],instance.user.id,folder_mask[-4:], filename)

class Profile(models.Model):

    user = models.OneToOneField('authentication.User', verbose_name=_("Credentials"), on_delete=models.CASCADE)
    handle = models.CharField("Unique username", blank=True, unique=True, null=True, max_length=20)
    city = models.ForeignKey("utils.City", blank=True, null=True, on_delete=models.SET_NULL)
    phone = models.CharField("User phone number", blank=True, null=True, max_length=15)
    email_confirmed = models.BooleanField("Confirmation status", default=False)
    tags = models.ManyToManyField("utils.Tag", related_name='users', blank=True, verbose_name=_("User tags"))
    bio = models.TextField(blank=True, null=True)
    avatar = models.ImageField(_("Profile Picture"),blank=True, null=True, upload_to=user_directory_path, height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)
