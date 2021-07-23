from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe


class ElectoralCommisionMember(models.Model):
    """Model to represent member of the EC board"""

    MAIN_CAMPUS = "MC"
    CITY_CAMPUS = "CC"

    CAMPUS = (
        (MAIN_CAMPUS, "Main Campus",),
        (CITY_CAMPUS, "City Campus",),
    )

    class POSITION_LEVEL(models.IntegerChoices):

        LEVEL_ONE = 1, "One"
        LEVEL_TWO = 2, "Two"
        LEVEL_THREE = 3, "Three"
        LEVEL_FOUR = 4, "Four"
        LEVEL_FIVE = 5, "Five"


    campus = models.CharField(_("Campus"), choices=CAMPUS, default=MAIN_CAMPUS, max_length=20,
                              help_text="Select the campus the student is on", null=False, blank=False)

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
    position_level = models.IntegerField(choices=POSITION_LEVEL.choices, default=POSITION_LEVEL.LEVEL_FIVE,
                                      help_text="Select how high in the order of power this board member is, 1 is highest")
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

    class Meta:
        ordering = ["position_level"]
        verbose_name = "Electoral Commission Board Member"
        verbose_name_plural = "Electoral Commission Board Members"