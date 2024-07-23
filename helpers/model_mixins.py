from django.db import models
from django.utils.translation import gettext as _


class TrackingTimeStampMixin(models.Model):
    created = models.DateTimeField(
        _("Created"),
        help_text = _("Record Created on specific date time"),
        auto_now_add = True,
    )
    modified = models.DateTimeField(
        _("Modified"),
        help_text = _("Record Modified on specific date time"),
        auto_now = True
    )

    class Meta:
        abstract = True