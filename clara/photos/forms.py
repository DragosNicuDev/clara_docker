from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from .models import PhotoUpload


class PhotoUploadForm(forms.ModelForm):

    class Meta:
        model = PhotoUpload
        fields = ('image',)

    # crispy form code for id and class insert in field
    def __init__(self, *args, **kwargs):
        super(PhotoUploadForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.fields['image'].label = '<br>'
        self.helper.layout = Layout(
            Field('image',
                  css_class='file',
                  id='upload-image',
                  data_allowed_file_extensions='["jpg", "jpeg", "png", "gif"]',
                  data_show_preview='false',
                  )
        )
