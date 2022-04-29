from django import forms
from django.conf import settings

from django.template.defaultfilters import filesizeformat
from django.core.files.uploadedfile import UploadedFile
from django.db.models.fields.files import ImageFieldFile

from django_summernote.widgets import SummernoteWidget
from django.core.files.images import get_image_dimensions

from .models import Faq, Slide
from panel.accounts.models import User



class FaqForm(forms.ModelForm):
    question = forms.CharField(
        label = 'Pregunta',
        error_messages = {'required':'Debe capturar la pregunta'},
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
            }
        )
    )
    answer = forms.CharField(
        label = 'Respuesta',
        error_messages = {'required':'Debe capturar la respuesta'},
        widget = forms.Textarea(
            attrs = {
                'class' : 'form-control',
            }
        )
    )

    class Meta:
        model = Faq
        fields = ('question','answer')


class SlideForm(forms.ModelForm):
    title = forms.CharField(
        label = 'Título',
        required = False,
        help_text = 'Opcional',
        widget = forms.TextInput(
            attrs = {
                'class' : 'form-control',
                'placeholder': 'Título'
            }
        )
    )
    url = forms.URLField(
        label = 'URL',
        required = False,
        help_text = 'Opcional',
        widget = forms.URLInput(
            attrs = {
                'class' : 'form-control',
                'placeholder': 'Link'

            }
        )
    )
    image = forms.ImageField(
        label = 'Slide',
        required = False,
        widget = forms.FileInput(
            attrs = {
                'class' : 'custom-file-input',
            }
        )
    )
    class Meta:
        model = Slide
        fields = ('title','url','image')
    def clean(self):
        super(SlideForm,self).clean()
        if self.instance:
            if self.cleaned_data.get('image') is not None and self.cleaned_data.get('image') != '' and self.instance.image != self.cleaned_data.get('image'):
                width, height = get_image_dimensions(self.cleaned_data.get('image'))
                if width > 1350:
                    self._errors['image'] = self.error_class(['Resolución de ancho máxima de 1350 px.'])
        else:
            if self.cleaned_data.get('image') is not None and self.cleaned_data.get('image') != '':
                width, height = get_image_dimensions(self.cleaned_data.get('image'))
                if width > 1350:
                    self._errors['image'] = self.error_class(['Resolución de ancho máxima de 1350 px.'])
            else:
                self._errors['image'] = self.error_class(['Captura la imagen'])
        return self.cleaned_data

    def clean_image(self):
        cd = self.cleaned_data

        if isinstance(cd['image'],UploadedFile):
            content_type = cd['image'].content_type.split('/')[0]

            if content_type in settings.CONTENT_TYPES_IMAGE:
                if cd['image'].size > int(settings.MAX_UPLOAD_SIZE):
                    raise forms.ValidationError(f"El tamaño de la imagen es de {filesizeformat(cd['image'].size)} y excede el permitido de {filesizeformat(settings.MAX_UPLOAD_SIZE)}")
            else:
                raise forms.ValidationError('El tipo de formato no es soportado')
        elif isinstance(cd['image'],ImageFieldFile):
            pass

        return cd['image']

class SearchCustomerForm(forms.Form):
    query = forms.CharField(
        label = 'Buscar cliente',
        required = False,
        widget = forms.TextInput(
            attrs = {
                'class': 'input-sm form-control',
                'placeholder': 'Buscar cliente'
            }
        )
    )
