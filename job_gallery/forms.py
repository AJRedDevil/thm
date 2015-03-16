from django.utils.translation import ugettext_lazy as _
from django.contrib.gis import forms
from django.template.defaultfilters import filesizeformat

from .models import JobGalleryImages
import os


class JobGalleryImageForm(forms.ModelForm):
    class Meta:
        model = JobGalleryImages
        field = ['image', 'img_type']

    def __init__(self, *args, **kwargs):
        super(JobGalleryImageForm, self).__init__(*args, **kwargs)
        del self.fields['job']
        self.fields['image'].widget.attrs = {'class': 'form-control'}
        self.fields['img_type'].widget.attrs = {'class': 'form-control'}

    def clean_image(self):
        image = self.cleaned_data['image']
        # upload file data is of type bool if is cleared
        if type(image) is not bool and image is not None:
            ALLOWED_FILE_EXTS = ['.png', '.jpg', '.jpeg']
            IMAGE_MAX_SIZE = 2097152
            root, ext = os.path.splitext(image.name.lower())
            if ext not in ALLOWED_FILE_EXTS:
                valid_exts = ", ".join(ALLOWED_FILE_EXTS)
                error = _("%(ext)s is an invalid file extension. \
                    Allowed file types are : %(valid_exts_list)s")
                raise forms.ValidationError(error %
                                            {'ext': ext,
                                            'valid_exts_list': valid_exts})
            try:
                if image.size > IMAGE_MAX_SIZE:
                    error = _("Your profile picture is too big (%(size)s), "
                              "the maximum allowed size is %(max_valid_size)s")
                    raise forms.ValidationError(error % {
                        'size': filesizeformat(image.size),
                        'max_valid_size': filesizeformat(IMAGE_MAX_SIZE)
                    })
            except Exception:
                # returned because of a possibility where by the profile
                # image is removed for some reason either manually or by mistake
                return image

            return image
        return image
