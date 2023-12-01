# Код для обхода страниц сайта, получения списка книг и их ссылок
# ...
import os

# Код для перехода на ссылку первой книги и получения названия, описания и картинки
# ...

# Код для сохранения картинки в папку проекта
# ...

# Код для создания интерфейса Kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView

import urllib.request
import re

title = None

class BookApp(App):
    global title

    def build(self):
        layout = BoxLayout(orientation='vertical')

        # Название книги
        self.book_title = Label(text='Название книги')
        layout.add_widget(self.book_title)

        # Картинка книги
        self.book_image = Image(source='temp/картинка.jpg')
        layout.add_widget(self.book_image)

        # Описание книги
        self.book_description = Label(text='Описание книги')
        scroll_view = ScrollView()
        scroll_view.add_widget(self.book_description)
        layout.add_widget(scroll_view)

        # Кнопка сохранения ссылки
        self.save_button = Button(text='Сохранить ссылку')
        layout.add_widget(self.save_button)

        # Кнопка перехода к следующей книге
        self.next_button = Button(text='Следующая книга')
        layout.add_widget(self.next_button)

        self.next_button.bind(on_press=self.on_next_button_press)  # Привязываем событие к кнопке

        return layout



    def on_next_button_press(self, instance):
        global title
        # Обработка события при нажатии кнопки "Следующая книга"
        # Получаем номер страницы, на котором в последний раз остановились
        books()
        self.book_title.text = title
        print('s')



def books():
    global title

    # Получаем номер страницы, на котором в последний раз остановились
    with open(os.getcwd() + '\\current_page.txt', 'r') as file:
        page = file.read()
    # Получаем номер книги, на которой в последний раз остановились
    with open(os.getcwd() + '\\current_book.txt', 'r') as file:
        book = int(file.read())

    # Отправляем запрос на указанный URL и получаем HTML-код страницы
    url = 'https://www.litres.ru/genre/knigi-iskusstvo-5020/?page=' + page
    response = urllib.request.urlopen(url)
    html_code = response.read().decode('utf-8')

    # Используем регулярные выражения для поиска всех элементов на странице с указанным шаблоном
    pattern = r'<div class="ArtV2Default-module__container_3ymrO">.*?</div>'
    book_elements = re.findall(pattern, html_code, re.DOTALL)

    # Извлекаем значение href из каждой ссылки с помощью регулярного выражения
    links = [re.search(r'href="([^"]+)"', book_element).group(1) for book_element in book_elements]


    # Выводим HTML-код страницы и список элементов с указанным шаблоном
    title = links[book]

    book = book + 1
    # Изменяем номер книги, на которой в последний раз остановились
    with open(os.getcwd() + '\\current_book.txt', 'w') as file:
        file.write(str(book))


# Инициализация
def init():
    try:
        with open (os.getcwd() + '\\current_page.txt', 'r') as file:
            pass
    except:
        with open (os.getcwd() + '\\current_page.txt', 'w') as file:
            file.write('1')

    try:
        with open(os.getcwd() + '\\current_book.txt', 'r') as file:
            pass
    except:
        with open(os.getcwd() + '\\current_book.txt', 'w') as file:
            file.write('1')

init()
#books()


if __name__ == '__main__':
    BookApp().run()


