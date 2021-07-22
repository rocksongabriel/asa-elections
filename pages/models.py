from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe


class ElectoralCommisionMember(models.Model):
    """Model to represent member of the EC board"""
    name = models.CharField(
        _("Name of Board Member"),
        max_length=50,
        null=False,
        blank=False,
        help_text="Enter the name of the board member"
    )
    position = models.CharField(
        _("Position of Board Member"),
        max_length=100,
        blank=False,
        null=False,
        help_text="Enter the position held by this member",
        default=""
    )
    picture = models.ImageField(
        _("Picture of Board Member"),
        upload_to="board-member/picture/",
        blank=False,
        null=False,
        help_text="Upload an image of the board member"
    )

    def __str__(self):
        return self.name

    # display picture in admin
    def image_tag(self):
        if self.picture:
            return mark_safe(
                '<img src="%s" style="width: 100px; height:100px;" />' %
                self.picture.url)
        else:
            return 'No Image Found'

    image_tag.short_description = 'Image'
