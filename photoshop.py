"""
Достаточно простая пародия на Photoshop

by duny-explorer
"""
import random
import sys
from PyQt5 import uic
from PIL import Image, ImageFilter, ImageEnhance
import numpy as np
from PyQt5.QtCore import Qt
from PIL.ImageQt import ImageQt
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QInputDialog, QColorDialog, QWidget


class AboutMyProgram(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel(self)
        self.label.setText(open("about.txt").read())
        self.setGeometry(400, 400, 600, 400)
        self.setWindowTitle('О программе')


class InfoProgram(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.label = QLabel(self)
        self.setGeometry(400, 400, 300, 300)
        self.setWindowTitle('Как пользоваться?')


class Fotopocalipsis(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('interface.ui', self)
        self.foto = QLabel()  # В Qt Designer есть некоторые роблемы с QScrollArea, поэтому здесь добавим место для фото
        self.initUI()

    def initUI(self):

        self.foto_place.setWidget(self.foto)

        self.setWindowTitle("Фотопокалипсис")
        self.setWindowIcon(QIcon('images\\icon.jpg'))

        """
        Верстаем минюшку для открытия, сохранения файла и других tools

        P.S + ещё конечно же шедевральная справка и инфо от автора
        """

        menubar = self.menuBar()
        menu = menubar.addMenu('Меню')
        self.open_activity = menu.addAction("Открыть")
        self.save_activity = menu.addAction("Сохранить")
        self.save_activity.setEnabled(False)
        self.info_activity = menu.addAction("Справка")
        self.about_activity = menu.addAction("О программе")
        self.open_activity.triggered.connect(self.open_file)
        self.save_activity.triggered.connect(self.save_file)
        self.info_activity.triggered.connect(self.info_program)
        self.about_activity.triggered.connect(self.about_program)

        """
        Подключаем фильтры
        """

        self.negative.clicked.connect(self.negative_filter)
        self.grey.clicked.connect(self.grey_filter)
        self.sepia.clicked.connect(self.sepia_filter)
        self.pixel.clicked.connect(self.pixel_filter)
        self.color_glass.clicked.connect(self.color_filter_glass)
        self.color.clicked.connect(self.color_filter)
        self.origin.clicked.connect(self.start_foto)
        self.stereopara.clicked.connect(self.stereopara_filter)
        self.white_black.clicked.connect(self.white_black_filter)

        self.btn_back.clicked.connect(self.back)
        self.result.clicked.connect(self.change_parameters)
        self.resize_btn.clicked.connect(self.resize_foto)
        self.plus_foto.clicked.connect(self.add_foto)

        """
        Сделаем всплывающие подсказки для фильтров. Всё для удобства пользователей.
        """

        self.origin.setToolTip("Без фильтров")
        self.negative.setToolTip("Негатив")
        self.grey.setToolTip("В оттенках одного цвета")
        self.sepia.setToolTip("Сепия")
        self.pixel.setToolTip("Пикселизация")
        self.color.setToolTip("В оттеках одного \nцвета")
        self.color_glass.setToolTip("Прозрачная цветовая \nплёнка")
        self.stereopara.setToolTip("Стереопара")
        self.white_black.setToolTip("Чёрно-белое")

        """
        Так как клавиатурное решение немного заедает, решила на всякий пожарный добавить кнопки.
        """

        self.right.clicked.connect(self.rot_90)
        self.left.clicked.connect(self.rot_90)

        self.first_page.clicked.connect(self.change_page)  # Смена страниц фильтров
        self.second_page.clicked.connect(self.change_page)

        """
        Меняем текст на Labels, чтобы пользователь видел значения, которые выбирает ползунком.
        """

        self.brightness.valueChanged.connect(self.change_value)
        self.contrast.valueChanged.connect(self.change_value)
        self.saturation.valueChanged.connect(self.change_value)
        self.sharpness.valueChanged.connect(self.change_value)
        self.noise.valueChanged.connect(self.change_value)
        self.degradation.valueChanged.connect(self.change_value)

    def keyPressEvent(self, event):

        """
        Осуществляем поворот нашей картинки

        клавиша А - влево на 90 градусов, D - вправо на 90 градусов
        """

        try:
            if event.key() == Qt.Key_A:
                print(2)
                self.pixels = np.rot90(self.pixels)
                self.start_pixels = self.pixels.copy()  # Предосторожность, чтобы до открытия фото всё не вылетело
                self.img = Image.fromarray(np.uint8(self.pixels))
                self.foto_viz()
            elif event.key() == Qt.Key_D:
                self.pixels = np.rot90(self.pixels, 3)
                self.start_pixels = self.pixels.copy()
                self.img = Image.fromarray(np.uint8(self.pixels))
                self.foto_viz()
            elif event.key() == Qt.Key_Backspace:
                self.back()
        except Exception as e:
            print(e)  # Кнопки не всегда работают

    def grey_filter(self):

        """
        Конвентируем в оттеках серого изображение
        """

        self.past_pixels = self.pixels.copy() if (self.past_pixels != self.pixels).all() else self.past_pixels
        size = self.pixels.shape
        k = np.array([[[0.2989, 0.587, 0.114]]])
        self.pixels = np.repeat(np.round(np.sum(self.pixels * k, axis=2)), 3).astype(np.uint8).reshape(*size)
        self.img = Image.fromarray(np.uint8(self.pixels))
        self.foto_viz()

    def negative_filter(self):

        """
        Негатив, почувствуй себя рентгенологом
        """

        self.past_pixels = self.pixels.copy() if (self.past_pixels != self.pixels).all() else self.past_pixels
        self.pixels = np.array([255, 255, 255]) - self.pixels  # NumPy наше всё
        self.img = Image.fromarray(np.uint8(self.pixels))
        self.foto_viz()

    def sepia_filter(self):

        """
        Дивиз сепии - песоным человеком может стать каждый.

        P.S зараза долгий, до алтернативы на NumPy не додумала
        """

        self.past_pixels = self.pixels.copy() if (self.past_pixels != self.pixels).all() else self.past_pixels

        for x in range(self.img.size[0]):
            for y in range(self.img.size[1]):
                r, g, b = self.img.getpixel((x, y))
                red = int(r * 0.393 + g * 0.769 + b * 0.189)
                green = int(r * 0.349 + g * 0.686 + b * 0.168)
                blue = int(r * 0.272 + g * 0.534 + b * 0.131)
                self.img.putpixel((x, y), (red, green, blue))

        self.pixels = np.asarray(self.img)
        self.foto_viz()

    def pixel_filter(self):

        """
        Пикселизация. 8-bit рулят миром.
        """

        self.past_pixels = self.pixels.copy() if (self.past_pixels != self.pixels).all() else self.past_pixels

        i, okBtnPressed = QInputDialog.getInt(
            self, "Размер пикселей", "Размер", 13, 5, 50
        )
        if okBtnPressed:
            self.img = self.img.resize((self.img.size[0] // i, self.img.size[1] // i), Image.NEAREST)
            self.img = self.img.resize((self.img.size[0] * i, self.img.size[1] * i), Image.NEAREST)
            self.pixels = np.asarray(self.img)
            self.foto_viz()

    def color_filter_glass(self):

        """
        Ажурная прозрачная цветовая маска на изображение.
        """

        self.past_pixels = self.pixels.copy() if (self.past_pixels != self.pixels).all() else self.past_pixels
        color = QColorDialog.getColor()
        if color.isValid():
            color = color.name()
            layer = Image.new("RGB", self.img.size, color)
            self.img = Image.blend(self.img, layer, 0.5)

            self.pixels = np.asarray(self.img)
            self.foto_viz()

    def color_filter(self):

        """
        Специально для любителей одного цвета.
        """

        self.past_pixels = self.pixels.copy() if (self.past_pixels != self.pixels).all() else self.past_pixels

        color = QColorDialog.getColor()
        if color.isValid():
            color = color.name()

            size = self.pixels.shape
            k = np.array([[[0.2989, 0.587, 0.114]]])  # Нужно сделать изображение серым, чтобы было все в одно тоне
            self.pixels = np.repeat(np.round(np.sum(self.pixels * k, axis=2)), 3).astype(np.uint8).reshape(*size)

            layer = Image.new("RGB", self.img.size, color)  # Создаем слой нужного нам цвета
            self.img = Image.blend(Image.fromarray(np.uint8(self.pixels)), layer, 0.5)

            self.pixels = np.asarray(self.img)
            self.foto_viz()

    def stereopara_filter(self):

        """
        Пытаемся создать эффект 3D изображения
        """

        self.past_pixels = self.pixels.copy() if (self.past_pixels != self.pixels).all() else self.past_pixels

        delta, okBtnPressed = QInputDialog.getInt(
            self, "Размер сдвига", "Размер", 13, 5, 50
        )

        if okBtnPressed:
            x, y = self.img.size
            newImage = self.img.copy()
            self.pixels_load = self.img.load()
            self.pixels_load2 = newImage.load()

            for i in range(delta, x):
                for n in range(y):
                    r, g, b = self.pixels_load2[i - delta, n]
                    r1, g1, b1 = self.pixels_load2[i, n]
                    self.pixels_load[i, n] = r, g1, b1

            for j in range(delta):
                for m in range(y):
                    self.pixels_load[j, m] = 0, self.pixels_load[j, m][1], self.pixels_load[j, m][2]

        self.pixels = np.asarray(self.img)
        self.foto_viz()

    def degradation_parameter(self):
        p = self.degradation.value()
        self.img = self.img.filter(ImageFilter.GaussianBlur(p))
        self.pixels = np.asarray(self.img)

    def contrast_parameter(self):
        level = self.contrast.value()
        self.img = ImageEnhance.Contrast(self.img).enhance(level)
        self.pixels = np.asarray(self.img)

    def brightness_parameter(self):
        p = self.brightness.value() / 10

        for x in range(self.img.size[0]):
            for y in range(self.img.size[1]):
                r, g, b = self.img.getpixel((x, y))

                red = min(255, max(0, int(r * p)))
                green = min(255, max(0, int(g * p)))
                blue = min(255, max(0, int(b * p)))

                self.img.putpixel((x, y), (red, green, blue))

        self.pixels = np.asarray(self.img)

    def noise_parameter(self):

        for i in range(self.img.size[0]):
            for j in range(self.img.size[1]):
                rand = random.randint(-self.noise.value(), self.noise.value())
                r, g, b = self.img.getpixel((i, j))
                r = min(max(r + rand, 0), 255)
                g = min(max(g + rand, 0), 255)
                b = min(max(b + rand, 0), 255)
                self.img.putpixel((i, j), (r, g, b))

        self.pixels = np.asarray(self.img)

    def saturation_parameter(self):
        self.img = ImageEnhance.Color(self.img).enhance(self.saturation.value() / 10)
        self.pixels = np.asarray(self.img)

    def sharpness_parameter(self):
        self.img = self.img.filter(ImageFilter.UnsharpMask(self.sharpness.value()))
        self.pixels = np.asarray(self.img)

    def white_black_filter(self):

        """
        Только чёрный и белый. Только ХАРДКОР. Тоже медленная.
        Просто уже лень было придумавать способ с помощью маски и NumPy.
        """

        self.past_pixels = self.pixels.copy() if (self.past_pixels != self.pixels).all() else self.past_pixels

        p = 255 / 1 / 2 * 3
        for x in range(self.img.size[0]):
            for y in range(self.img.size[1]):
                r, g, b = self.img.getpixel((x, y))
                total = r + g + b
                if total > p:
                    self.img.putpixel((x, y), (255, 255, 255))
                else:
                    self.img.putpixel((x, y), (0, 0, 0))

        self.pixels = np.asarray(self.img)
        self.foto_viz()

    def start_foto(self):
        self.past_pixels = self.pixels.copy()
        self.pixels = self.start_pixels.copy()
        self.img = Image.fromarray(np.uint8(self.pixels))
        self.foto_viz()

    def open_file(self):

        """
        Открытие файла. Обернула в исключение, а то вылетает, если передумаешь открывать файл (Лень if писать)
        """

        self.save_activity.setEnabled(True)

        try:
            file_name = QFileDialog.getOpenFileName(  # Открывает окно для выбора файла
                self, "Открыть файл", "", "*.jpg *.jpeg *.bmp *.png"
            )

            self.img = Image.open(file_name[0])
            self.start_pixels = np.asarray(self.img)
            self.past_pixels = np.asarray(self.img)
            self.pixels = np.asarray(self.img)
            self.width.setText(str(self.img.size[1]))
            self.height.setText(str(self.img.size[0]))
            self.foto_viz()
        except Exception:
            pass

    def save_file(self):

        """
        Сохранение файла. Аналогично открытию только с некоторыми различиями
        """

        try:
            new_file = QFileDialog.getSaveFileName(
                self, "Сохранить файл", "picture", filter="*.jpg;;*.jpeg;;*.bmp;;*.png"
            )  # Окно для сохранения. Ничем не отличается от открытия, просто кнопка другая
            self.img.save(new_file[0])
        except Exception:
            pass

    def about_program(self):
        self.ex2 = AboutMyProgram()
        self.ex2.show()

    def info_program(self):
        self.ex3 = InfoProgram()
        self.ex3.show()

    def change_page(self):
        if self.sender().text() == ">":
            self.stack.setCurrentIndex(1)
        else:
            self.stack.setCurrentIndex(0)

    def rot_90(self):
        if self.sender().text() == "<--":
            print(2)
            self.pixels = np.rot90(self.pixels)
            self.start_pixels = self.pixels.copy()  # Предосторожность, чтобы до открытия фото всё не вылетело
            self.img = Image.fromarray(np.uint8(self.pixels))
            self.foto_viz()
        else:
            self.pixels = np.rot90(self.pixels, 3)
            self.start_pixels = self.pixels.copy()
            self.img = Image.fromarray(np.uint8(self.pixels))
            self.foto_viz()

    def change_parameters(self):
        self.past_pixels = self.pixels.copy() if (self.past_pixels != self.pixels).all() else self.past_pixels

        if self.brightness.value() != 0:
            self.brightness_parameter()

        if self.sharpness.value() != 0:
            self.sharpness_parameter()

        if self.contrast.value() != 0:
            self.contrast_parameter()

        if self.degradation.value() != 0:
            self.degradation_parameter()

        if self.noise.value() != 0:
            self.noise_parameter()

        if self.saturation.value() != 0:
            self.saturation_parameter()

        self.foto_viz()

        self.brightness.setValue(0)
        self.contrast.setValue(0)
        self.sharpness.setValue(0)
        self.degradation.setValue(0)
        self.noise.setValue(0)
        self.saturation.setValue(0)

    def change_value(self):
        self.count_brightness.setText(str(self.brightness.value()))
        self.count_contrast.setText(str(self.contrast.value()))
        self.count_saturation.setText(str(self.saturation.value()))
        self.count_sharpness.setText(str(self.sharpness.value()))
        self.count_noise.setText(str(self.noise.value()))
        self.count_degradation.setText(str(self.degradation.value()))

    def back(self):
        self.pixels = self.past_pixels.copy()
        self.img = Image.fromarray(np.uint8(self.pixels))
        self.foto_viz()

    def foto_viz(self):
        self.qimage = ImageQt(self.img)
        self.pixmap = QPixmap.fromImage(self.qimage)
        self.pix = QPixmap(self.pixmap)
        self.foto.setPixmap(self.pix)
        self.show()

        if not self.tools.isEnabled():
            self.tools.setEnabled(True)
            self.result.setEnabled(True)

    def add_foto(self):
        self.past_pixels = self.pixels.copy() if (self.past_pixels != self.pixels).all() else self.past_pixels

        try:
            file_name = QFileDialog.getOpenFileName(  # Открывает окно для выбора файла
                self, "Открыть файл", "", "*.jpg *.jpeg *.bmp *.png"
            )

            second_image = Image.open(file_name[0]).resize(self.img.size)
            k = int(self.glass.text()) / 100

            self.img = Image.blend(self.img, second_image, k)
            self.pixels = np.asarray(self.img)
            self.foto_viz()
        except Exception:
            pass

    def resize_foto(self):
        self.past_pixels = self.pixels.copy() if (self.past_pixels != self.pixels).all() else self.past_pixels

        try:
            self.img = self.img.resize((int(self.width.text()), int(self.height.text())))
            self.pixels = np.asarray(self.img)
            self.foto_viz()
        except Exception:
            self.width.setText(str(self.img.size[1]))
            self.height.setText(str(self.img.size[0]))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Fotopocalipsis()
    ex.show()
    sys.exit(app.exec_())
