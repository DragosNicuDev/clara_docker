from django import template
from ..models import PhotoUpload
from ..forms import PhotoUploadForm

register = template.Library()


@register.inclusion_tag('photos/photos_tags.html')
def photos_up(request, number=1):
    a = PhotoUpload.objects.filter(user__username=request).exists()
    if a:
        return {'form': PhotoUploadForm(),
                'photos': PhotoUpload.objects.filter(
                    user__username=request
        ).order_by(
                    '-pause_upload')[:number]
        }
    else:
        return {'form': PhotoUploadForm(),
                'photos': PhotoUpload.objects.all()[:number]
                }
