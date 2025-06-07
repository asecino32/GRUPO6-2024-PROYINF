from django import forms
from .models import Boletin, PlantillaBoletin, Fuente
from django.core.validators import RegexValidator

class PlantillaBoletinForm(forms.ModelForm):
    archivo_html = forms.FileField(required=False, help_text="Solo se permiten archivos .html")
    
    # Aquí se define explícitamente el campo contenido_html con sus validadores
    contenido_html = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 20, 'cols': 100}),
        required=False,
        validators=[
            RegexValidator(
                regex=r'\{\{.*?\}\}',
                message="Debe incluir al menos una variable entre dobles llaves",
                inverse_match=False  # Cambiado a False para que REQUIERA el patrón
            )
        ]
    )
    
    class Meta:
        model = PlantillaBoletin
        fields = ['nombre', 'contenido_html', 'archivo_html']
        # Eliminamos el widget de aquí ya que lo definimos arriba

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ya no es necesario hacer required=False aquí porque lo definimos arriba

    def clean_archivo_html(self):
        archivo = self.cleaned_data.get('archivo_html')
        if archivo:
            if not archivo.name.lower().endswith('.html'):
                raise forms.ValidationError("Solo se permiten archivos con extensión .html")
        return archivo

    def clean(self):
        cleaned_data = super().clean()
        contenido = cleaned_data.get('contenido_html')
        archivo = cleaned_data.get('archivo_html')

        if not contenido and not archivo:
            raise forms.ValidationError(
                "Debe proporcionar contenido HTML directamente o subir un archivo .html."
            )

        return cleaned_data

class CrearBoletinForm(forms.ModelForm):
    plantilla = forms.ModelChoiceField(
        queryset=PlantillaBoletin.objects.all(),
        required=False,
        label="Plantilla disponible"
    )
    contenido_html = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 20, 'cols': 100}),
        label="Contenido HTML editable",
        required=False
    )

    class Meta:
        model = Boletin
        fields = ['titulo', 'ciudad_tratada', 'tematica', 'fuente_boletin']
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['fuente_boletin'].queryset = Fuente.objects.filter(fuente_activa=True)
        self.fields['fuente_boletin'].label_from_instance = lambda obj: obj.titulo
        self.fields['plantilla'].queryset = PlantillaBoletin.objects.all()
        self.fields['plantilla'].label_from_instance = lambda obj: obj.nombre
