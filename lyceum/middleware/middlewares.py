import re

import lyceum.settings


class ContentReverseMiddleware:
    """Simple middleware that reverses every 10th get response.
    To disable set enviroment variable REVERSE='0'"""

    enable = lyceum.settings.REVERSE_EVERY_10

    def __init__(self, get_response):
        self.get_response = get_response
        self.response_count = 0

    def reverse_russian_text(self, text: str):
        changed_text = []
        is_word = False
        start_ind = 0
        for ind, letter in enumerate(text):
            if re.match(r'[а-яА-ЯёЁ]', letter):
                is_word = True
            if not re.match(r'[а-яА-ЯёЁ]', letter) and not is_word:
                start_ind = ind + 1
                changed_text.append(letter)
            if not re.match(r'[а-яА-ЯёЁ]', letter) and is_word:
                changed_text += list(text[start_ind:ind][::-1] + letter)
                is_word = False
                start_ind = ind + 1
        changed_text = ''.join(changed_text)
        if len(changed_text) != text:
            changed_text += text[start_ind:][::-1]
        return changed_text

    def __call__(self, request):
        response = self.get_response(request)
        self.response_count += 1
        if ContentReverseMiddleware.enable:
            if self.response_count % 10 == 0:
                str_response_content = response.content.decode('utf-8')
                response.content = self.reverse_russian_text(
                    str_response_content
                )
        return response
