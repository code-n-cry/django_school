<h1>ER-диаграмма:</h1>

<img src="https://github.com/code-n-cry/django_school/blob/main/image.png">

<h1>Статус пайплайна:</h1>

[![Python linting](https://github.com/code-n-cry/django_school/actions/workflows/python-linting.yml/badge.svg)](https://github.com/code-n-cry/django_school/actions/workflows/python-linting.yml)

[![Python testing](https://github.com/code-n-cry/django_school/actions/workflows/python-testing.yml/badge.svg)](https://github.com/code-n-cry/django_school/actions/workflows/python-testing.yml)

<h1>Руководство по запуску</h1>
Для включения в dev-режиме:
<ul>
<li>Клонировать репозиторий с помощью git.<br>Для этого в консоль вводим команду:<br><blockquote>git clone https://github.com/code-n-cry/django_school.git</blockquote>Которая <b>скопирует папку с кодом</b> из Github</li>
<li>Перейти в папку django-school</li>
<li>Создать venv(код в консоли для этого):
<table>
<tr>
<th>Linux/MacOS</th>
<th>Windows</th>
</tr>
<tr>
<td>python3 -m venv /ваше_имя_папки</td>
<td>python -m venv \ваше_имя_папки</td>
</tr>
</table>
Команда создаст вирутальное окружение(venv) Python, которое позволит устанавливать версии библиотек без конфликтов с уже установленными.</li>
<li>Активировать venv
<table>
<tr>
<th>Linux/MacOS</th>
<th>Windows</th>
</tr>
<tr>
<td>source имя_папки_с_venv/bin/activate</td>
<td>имя_папки_с_venv\Scripts\activate.bat</td>
</tr>
</table>
Немного левее текущей строки <b>в скобках</b> должно появиться имя папки c venv - это говорит о том, что команда сработала и вы вошли в окружение.
</li>
<li>Установить зависимости(библиотеки, необходимые для работы проекта)
<table>
<tr>
<th>Linux/MacOS</th>
<th>Windows</th>
</tr>
<tr>
<td>pip3 install basic-requirements.txt</td>
<td>pip install basic-requirements.txt</td>
</tr>
<tr>
<td>pip3 install dev-requirements.txt</td>
<td>pip install dev-requirements.txt</td>
</tr>
<tr>
<td>pip3 install test-requirements.txt</td>
<td>pip install test-requirements.txt</td>
</tr>
</table>
Зачем нужен каждый из файлов:
<ul>
<li><b>basic-requirements.txt</b> - здесь находятся библиотеки, без которых проект в принципе не сможеть работать(на самом деле, оно не сможет работать без установки всех трёх файлов - разделение условное), корневые.</li>
<li><b>dev-requirements.txt</b> - здесь находятся библиотеки, которые помогают разработке проекта</li>
<li><b>test-requirements.txt</b> - библиотеки, которые нужны для тестирования</li>
</ul>
<li>Запустить сервер:
<table>
<tr>
<th>Linux/MacOS</th>
<th>Windows</th>
</tr>
<tr>
<td>python3 manage.py runserver</td>
<td>python manage.py runserver</td>
</tr>
</table>
Для этого необходимо находиться в одной директории с файлом manage.py(в консоли)</li>
<li>Критичные для безопасности проекта и конфигурационные переменные находятся в файле <b>example.env</b>. Скопируйте его с помощью консольной команды<br>
<code>cp .env.example .env</code><br>
и, при необходимости, отредактируйте.
</ul>
<h2>Данные администратора:</h2><br>
Пользователь: <b>admin</b><br>
Пароль: <b>admin1234</b>
<h2>Запуск БД</h2>
<ol>
<li>Начальная миграция
<table>
<tr>
<th>Linux/MacOS</th>
<th>Windows</th>
</tr>
<tr>
<td>python3 manage.py migrate</td>
<td>python manage.py migrate</td>
</tr>
</table>
<li>Создание админа(superuser):
<table>
<tr>
<th>Linux/MacOS</th>
<th>Windows</th>
</tr>
<tr>
<td>python3 manage.py createsuperuser</td>
<td>python manage.py createsuperuser</td>
</tr>
</table>
Далее следовать указаниям консоли
</li>
<li>Добавление в миграцию данных catalog
<table>
<tr>
<th>Linux/MacOS</th>
<th>Windows</th>
</tr>
<tr>
<td>python3 manage.py makemigrations</td>
<td>python manage.py makemigrations</td>
</tr>
</table>
</li>
<li>Добавление моделей catalog в БД
<table>
<tr>
<th>Linux/MacOS</th>
<th>Windows</th>
</tr>
<tr>
<td>python3 manage.py migrate catalog</td>
<td>python manage.py migrate catalog</td>
</tr>
</table>
<li>Загрузка фикстур(начальных данных) приложения каталог
<table>
<tr>
<th>Linux/MacOS</th>
<th>Windows</th>
</tr>
<tr>
<td>python manage.py loaddata fixture.json --app catalog</td>
<td>python3 manage.py loaddata fixture.json --app catalog</td>
</tr>
</table>
