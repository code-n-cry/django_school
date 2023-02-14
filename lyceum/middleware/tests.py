from django.http import HttpResponse
from django.test import Client, TestCase

from lyceum.middleware.middlewares import ContentReverseMiddleware


class StaticUrlTests(TestCase):
    def test_middleware_reversing_text(self):
        my_middleware = ContentReverseMiddleware(HttpResponse)
        with self.subTest('Test of reversing different strings'):
            strings = [
                '?12Список.элементов раз,два:три!(четыре)',
                'Павел-лучший,ментор!и!ревьювер',
                'Данила...не пишет_мне**ишьюс:(',
                'Мамаmylaрамуramuмылаmama',
            ]
            changed_strings = [
                '?12косипС.вотнемелэ зар,авд:ирт!(ерытеч)',
                'леваП-йишчул,ротнем!и!ревюьвер',
                'алинаД...ен тешип_енм**сюьши:(',
                'амаМmylaумарramuалымmama'
            ]
            for ind, string in enumerate(strings):
                self.assertEqual(
                    my_middleware.reverse_russian_text(string),
                    changed_strings[ind],
                    msg=string,
                )

    def test_middleware_turned_on(self):
        ContentReverseMiddleware.enable = True
        client = Client()
        urls = [
            '/about/',
            '/catalog/',
            '/',
        ]
        with self.subTest('Middleware is turned on, works on all endpoints'):
            changed_contents = [
                '<body>бО мотэ еткеорп ьтировог ёще огечен (</body>',
                '<body>косипС вотнемелэ</body>',
                '<body>яанвалГ ацинартс O_o</body>',
            ]
            for ind, url in enumerate(urls):
                for _ in range(10):
                    response = client.get(url)
                self.assertEqual(
                    response.content.decode('utf-8'),
                    changed_contents[ind],
                    msg=url
                )

    def test_middleware_turned_off(self):
        ContentReverseMiddleware.enable = False
        client = Client()
        urls = [
            '/about/',
            '/catalog/',
            '/',
        ]
        with self.subTest('Middleware is turned off and doesnt work'):
            unchanged_contents = [
                '<body>Об этом проекте говорить ещё нечего (</body>',
                '<body>Список элементов</body>',
                '<body>Главная страница O_o</body>',
            ]
            for ind, url in enumerate(urls):
                for _ in range(10):
                    response = client.get(url)
                self.assertEqual(
                    response.content.decode('utf-8'),
                    unchanged_contents[ind],
                    msg=url
                )
