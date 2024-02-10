from django.forms import ModelForm, CharField, TextInput, DateField, DateInput
from .models import Tag, Author, Quote


class TagForm(ModelForm):
    name = CharField(min_length=3, max_length=25, required=True, widget=TextInput())

    class Meta:
        model = Tag
        fields = ['name']


class AuthorForm(ModelForm):
    fullname = CharField(min_length=5, max_length=200, required=True, widget=TextInput())
    born_date = DateField(required=True, widget=DateInput())
    born_location = CharField(min_length=5, max_length=300, required=True,
                              widget=TextInput())
    description = CharField(max_length=10000, required=False, widget=TextInput())

    class Meta:
        model = Author
        fields = ['fullname', 'born_date', 'born_location', 'description']


class QuoteForm(ModelForm):
    # Change to quote model
    quote = CharField(min_length=5, max_length=500, required=True, widget=TextInput())
    # tags = MultipleChoiceField(choices=Tag.objects.all(), widget=SelectMultiple())

    class Meta:
        model = Quote
        fields = ['quote',]
