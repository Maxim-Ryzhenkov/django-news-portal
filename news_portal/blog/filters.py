import django_filters
from .models import Post, Category
import django.forms

"""
    Фильтр создается при помощи сторонней бибилиотеки Django-Filter
    Фильтр может возвращать QuerySet с объектами модели, которые удовлетворяют
    переданным в поля формы условиям.
    Фильтр передается через дополнительную переменную контекста в 'views'. 
"""


class PostFilter(django_filters.FilterSet):
    """ Набор фильтров для модели Post. """

    title = django_filters.CharFilter(
        field_name='title', label='Заголовок содержит', lookup_expr='icontains',
        widget=django.forms.TextInput(
            attrs={'type': 'text', 'class': "form-control", 'placeholder': "Ведите текст..."}))

    category = django_filters.ModelMultipleChoiceFilter(
        field_name='category', label='Искать в категориях', lookup_expr='exact', queryset=Category.objects.all(),
        widget=django.forms.CheckboxSelectMultiple(
            attrs={'type': 'checkbox', 'class': "form-check-inline"}))

    date_time__gt = django_filters.DateFilter(
        field_name="date_time", label="От даты", lookup_expr='gt',
        widget=django.forms.DateInput(
            attrs={'type': 'date', 'class': "form-control"}))

    date_time__lt = django_filters.DateFilter(
        field_name="date_time", label="До даты", lookup_expr='lt',
        widget=django.forms.DateInput(
            attrs={'type': 'date', 'class': "form-control"}))

    class Meta:
        model = Post
        # Порядок в словаре определяет порядок вывода полей в HTML
        fields = ['title', 'category', 'date_time__gt', 'date_time__lt']

