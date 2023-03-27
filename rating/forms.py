from core.forms import BootstrapForm
from .models import Rating


class RatingForm(BootstrapForm):
    class Meta:
        model = Rating
        fields = (Rating.rating.field.name,)
