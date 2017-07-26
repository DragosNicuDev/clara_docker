from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import CreateView
from .forms import PhotoUploadForm
from .models import PhotoUpload


class PhotoUploadCreate(CreateView):
    model = PhotoUpload
    form_class = PhotoUploadForm
    # template_name = 'upload_photo.html'

    def get_template_names(self):
        check_object = PhotoUpload.objects.filter(
            user=self.request.user
        ).order_by('-pause_upload').exists()

        if check_object is False:
            return ['upload_photo.html']

        else:
            photo_upload_object = PhotoUpload.objects.filter(
                user=self.request.user
            ).latest('pause_upload')

            if photo_upload_object.pause_upload < timezone.now()\
                    and photo_upload_object.pause_upload is not None:
                return ['upload_photo.html']

            else:
                return ['counter.html']

    def form_valid(self, form):
        check_object = PhotoUpload.objects.filter(
            user=self.request.user
        ).order_by('-pause_upload').exists()

        if check_object is False:
            form.instance.user = self.request.user
            return super(PhotoUploadCreate, self).form_valid(form)

        else:
            photo_upload_object = PhotoUpload.objects.filter(
                user=self.request.user
            ).latest('pause_upload')

            if photo_upload_object.pause_upload < timezone.now()\
                    and photo_upload_object.pause_upload is not None:
                form.instance.user = self.request.user
                return super(PhotoUploadCreate, self).form_valid(form)

            else:
                return render(self.request, 'counter.html')

    def get_context_data(self, **kwargs):
        context = super(PhotoUploadCreate, self).get_context_data(**kwargs)
        context['photo'] = PhotoUpload.objects.filter(
            user=self.request.user
        ).order_by('-pause_upload')
        return context

    def get_success_url(self):
        return reverse('success')
