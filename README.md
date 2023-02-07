# <b>Руководство по запуску</b>
Для включения в dev-режиме:
<ul>
<li>Клонировать репозиторий с помощью git.<br>Для этого в консоль вводим команды:<br><blockquote><b>git init</b></blockquote>Которая инициализирует git-репозиторий в открытой папке<br><blockquote>git clone https://github.com/code-n-cry/django_school.git</blockquote>Которая <b>скопирует папку с кодом</b> из Github</li>
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
Для этого необходимо находиться в одной директории с файлом manage.py(в консоли)
<li>И не забудьте в файле .env поменять значение <b>DEBUG</b> на <b>False</b>, если не хотите запускать проект в DEBUG-режиме.</li>
</ul>