import re
from django import template
from pathlib import Path

register = template.Library()


@register.filter()
def censor(post_text):
    """ Замена нецензурных слов на символ '*'.

        Замена выполнена при помощи регулярки и цикла.
        Это не оптимальное решение для больших, текстов.
        Для больших текстов лучше взять одну из готовых библиотек.
    """
    key_words = Path(__file__).resolve().parent.joinpath('censored_words.txt').read_text(encoding='utf-8')
    key_words = [word.strip() for word in key_words.split()]
    for word in key_words:
        pattern = f'\\b{word}\\b'
        post_text = re.sub(pattern, f"{word[0]}{(len(word)-2) * '*'}{word[-1]}", post_text, flags=re.I)
    return post_text
