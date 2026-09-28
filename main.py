from PyQt5.QtGui import QIcon

from playlist import *
from linked_list import *
from PyQt5.QtWidgets import QApplication
import sys


if __name__ == "__main__":
    """
    Главный модуль приложения PlayList.

    Создаёт экземпляр графического пользовательского интерфейса на основе PyQt5 и инициализирует 
    двусвязный список для хранения аудиокомпозиций.

    Создаётся объект QApplication, который управляет основным циклом событий приложения.
    Инициализируется двусвязный список для хранения музыкальных композиций.
    Создаётся главное окно плеера.
    Запускается приложение.
    """
    app = QApplication(sys.argv)
    app.setApplicationName("PlayList")

    linked_list = LinkedList()

    window = PlayList(linked_list)
    window.setWindowIcon(QIcon("icon.png"))
    window.resize(300, 200)
    window.show()

    sys.exit(app.exec_())
