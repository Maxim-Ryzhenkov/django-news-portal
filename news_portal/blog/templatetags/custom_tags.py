from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    """ Метод принимает URL с параметрами GET запроса. Парсит их в словарь 'request_data'.
        Подставляет/добавляет значения из **kwargs в 'request_data' и возвращает обновленную строку.
        Применяется для пагинации на странице.
    """
    request_data = context['request'].GET.copy()
    for param, value in kwargs.items():
        request_data[param] = value
    return request_data.urlencode()
