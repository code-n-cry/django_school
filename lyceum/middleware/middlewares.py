import os


class SimpleMiddleware:
    """Simple middleware that reverses every 10th get response.
    To disable set enviroment variable REVERSE='0'"""
    def __init__(self, get_response):
        self.get_response = get_response
        self.response_count = 0

    def __call__(self, request):
        response = self.get_response(request)
        if bool(int(os.environ['REVERSE'])):
            self.response_count += 1
            if self.response_count % 10 == 0:
                str_response_content = response.content.decode('utf-8')
                russian_response_content = str_response_content[
                    6 : len(str_response_content) - 7
                ].split()
                russian_response_content = ' '.join(
                    [word[::-1] for word in russian_response_content]
                )
                new_response_content = (
                    str_response_content[0:6]
                    + russian_response_content
                    + str_response_content[-7:]
                )
                response.content = new_response_content
        return response
