from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QMessageBox, QFileDialog, QListWidget, \
    QHBoxLayout, QSpinBox
from PyQt5.QtCore import QTimer
import pygame


class PlayList(QWidget):

    """
    Основное окно плеера, позволяющее управлять списком музыкальных композиций.

    Атрибуты:
        list (LinkedList): Связанный список, содержащий музыкальные файлы.
        curr_node (LinkedListItem): Текущий узел в связанном списке, указывающий на воспроизводимую композицию.
        timer (QTimer): Таймер для управления воспроизведением музыки.
        list_widget (QListWidget): Виджет для отображения списка композиций в интерфейсе.
        data (QLabel): Метка, отображающая название текущей воспроизводимой композиции.
        play (QPushButton): Кнопка для воспроизведения выбранной композиции.
        button_play_all (QPushButton): Кнопка для запуска воспроизведения всех композиций начиная с заданной.
        number_of_song (QSpinBox): Поле ввода номера композиции, с которой начать воспроизведение.
        button_back (QPushButton): Кнопка для перехода к предыдущей композиции.
        button_next (QPushButton): Кнопка для перехода к следующей композиции.
        add_song (QPushButton): Кнопка для добавления новой композиции в плейлист.
        del_song (QPushButton): Кнопка для удаления выбранной композиции из плейлиста.
        move_up (QPushButton): Кнопка для сдвига выбранной композиции вверх по плейлисту.
        move_down (QPushButton): Кнопка для сдвига выбранной композиции вниз по плейлисту.

    Методы:
        init_ui(): Создаёт и размещает все элементы интерфейса плеера.
        change_max_value_of_song(): Обновляет диапазон number_of_song в соответствии с длиной списка.
        play_one(): Воспроизводит композицию, выбранную в list_widget.
        move_up_song(): Сдвигает выбранную композицию на одну позицию вверх.
        move_down_song(): Сдвигает выбранную композицию на одну позицию вниз.
        delete(): Удаляет выбранную композицию из плейлиста и списка.
        add(): Открывает диалог выбора файла и добавляет композицию в плейлист.
        play_all_before(): Считывает номер из number_of_song и передаёт его в play_all.
        play_all(item): Начинает воспроизведение всех композиций, начиная с позиции item.
        play_next(): Загружает и воспроизводит текущую композицию, переключает таймер на check_if_done.
        check_if_done(): Проверяет, завершено ли воспроизведение, и переходит к следующей композиции.
        previous_track(): Переход к предыдущей композиции в списке.
        next_track(): Переход к следующей композиции в списке.
        current(): Возвращает название текущей композиции или сообщение об отсутствии элементов.
    """

    def __init__(self, linked_list):

        """
        Инициализация окна плеера.

        Аргумент:
            linked_list (LinkedList): Связанный список, содержащий музыкальные файлы.
        """

        super().__init__()
        self.list = linked_list
        self.curr_node = linked_list.first_item

        pygame.mixer.init()

        self.init_ui()

        self.timer = QTimer()
        self.timer.timeout.connect(self.play_next)

    def init_ui(self):

        """
        Создание пользовательского интерфейса плеера
        """

        layout = QVBoxLayout()

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)

        self.name = QLabel("Pause", self)
        layout.addWidget(self.name)

        self.play = QPushButton("PLAY", self)
        self.play.clicked.connect(self.play_one)
        layout.addWidget(self.play)

        h_layout_play_all = QHBoxLayout()

        self.button_play_all = QPushButton("PLAY ALL", self)
        self.button_play_all.clicked.connect(self.play_all_before)

        self.number_of_song = QSpinBox()
        self.number_of_song.setRange(0, len(self.list))  # границы
        self.number_of_song.setSingleStep(1)

        h_layout_play_all.addWidget(self.button_play_all)
        h_layout_play_all.addWidget(self.number_of_song)

        layout.addLayout(h_layout_play_all)

        h_layout_back_next = QHBoxLayout()

        self.button_back = QPushButton("BACK", self)
        self.button_back.clicked.connect(self.previous_track)
        h_layout_back_next.addWidget(self.button_back)

        self.button_next = QPushButton("NEXT", self)
        self.button_next.clicked.connect(self.next_track)
        h_layout_back_next.addWidget(self.button_next)

        h_layout_add_del = QHBoxLayout()

        self.add_song = QPushButton("ADD SONG", self)
        self.add_song.clicked.connect(self.add)
        h_layout_add_del.addWidget(self.add_song)

        self.del_song = QPushButton("DELETE SONG", self)
        self.del_song.clicked.connect(self.delete)
        h_layout_add_del.addWidget(self.del_song)

        layout.addLayout(h_layout_back_next)
        layout.addLayout(h_layout_add_del)

        self.move_up = QPushButton("MOVE UP", self)
        self.move_up.clicked.connect(self.move_up_song)
        layout.addWidget(self.move_up)

        self.move_down = QPushButton("MOVE DOWN", self)
        self.move_down.clicked.connect(self.move_down_song)
        layout.addWidget(self.move_down)

        self.setLayout(layout)

    def change_max_value_of_song(self) -> None:
        if len(self.list) == 0:
            self.number_of_song.setRange(0, 0)
            return
        self.number_of_song.setRange(1, len(self.list))

    def play_one(self) -> None:
        """
        Воспроизведение выбранной песни из списка.
        Если ни одна песня не выбрана, отображает предупреждение.
        """

        selected_row = self.list_widget.currentRow()
        if selected_row >= 0:
            tmp_node = self.list.first_item
            item_text = self.list_widget.item(selected_row).text()
            while (tmp_node.data != item_text):
                tmp_node = tmp_node.next_item
            self.curr_node = tmp_node
            self.timer.start(100)
            self.play_next()
        else:
            QMessageBox.warning(self, "Warning", "Please select a song to play.")

    def move_up_song(self) -> None:
        """
        Сдвиг песни вверх по плейлисту.
        Если песня уже вверху, ничего не происходит.
        """
        selected_row = self.list_widget.currentRow()
        if selected_row > 0:
            tmp_node = self.list.first_item
            item_text = self.list_widget.item(selected_row).text()
            while (tmp_node.next_item.data != item_text):
                tmp_node = tmp_node.next_item
            self.list.remove(item_text)
            if tmp_node == self.list.first_item:
                self.list.append_left(item_text)
            else:
                self.list.insert(tmp_node.previous_item.data, item_text)
            self.list_widget.insertItem(selected_row - 1, self.list_widget.takeItem(selected_row))
            self.list_widget.setCurrentRow(selected_row - 1)

    def move_down_song(self) -> None:
        """
        Сдвиг песни вниз по плейлисту.
        Если песня уже вверху, ничего не происходит.
        """
        selected_row = self.list_widget.currentRow()
        if selected_row < self.list_widget.count() - 1:
            tmp_node = self.list.last
            item_text = self.list_widget.item(selected_row).text()
            while (tmp_node.previous_item.data != item_text):
                tmp_node = tmp_node.previous_item

            self.list.remove(item_text)
            self.list.insert(tmp_node.data, item_text)

            self.list_widget.insertItem(selected_row + 1, self.list_widget.takeItem(selected_row))
            self.list_widget.setCurrentRow(selected_row + 1)

    def delete(self) -> None:
        """
        Удаление выбранной песни из плейлиста.
        Если песня не выбрана, отображает предупреждение
        """
        selected_row = self.list_widget.currentRow()
        if selected_row >= 0:
            item_text = self.list_widget.takeItem(selected_row).text()
            self.list.remove(item_text)
            QMessageBox.information(self, "Song Deleted", f"Song deleted: {item_text}")
            self.change_max_value_of_song()

            if len(self.list) == 0:
                pygame.mixer.music.stop()
                self.timer.stop()
                self.name.setText("Pause")
                return

            if self.curr_node.data == item_text:
                if self.curr_node.next_item:
                    self.curr_node = self.curr_node.next_item
                else:
                    self.curr_node = self.list.first_item
                self.play_next()

                if self.curr_node:
                    name_of_song = self.current().split("/")[-1]
                    self.name.setText(name_of_song)

        else:
            QMessageBox.warning(self, "Warning", "Please select a song to delete.")

    def add(self) -> None:
        """
        Добавление песни в плейлист.
        """
        file_name, _ = QFileDialog.getOpenFileName(self, "Choose song", "", "(*.mp3)")

        if file_name:
            self.list.append_right(file_name)
            if (self.curr_node == None):
                self.curr_node = self.list.first_item
            self.list_widget.addItem(file_name)
            QMessageBox.information(self, "Song Added", f"Song added: {file_name}")
            self.change_max_value_of_song()

    def play_all_before(self):
        number = self.number_of_song.value()
        self.play_all(number)

    def play_all(self, item= 1) -> None:
        """
        Проигрывание композиций уже находящихся в плейлисте, начиная с первой.
        Если список пуст, отображает предупреждение.
        """
        if self.list.len == 0:
            QMessageBox.warning(self, "Warning", "Elements are missing")
            return

        if self.list.len < item:
            QMessageBox.warning(self, "Warning", "The number of elements in the list is less than the number.")
            return

        self.curr_node = self.list.first_item
        for i in range(0, item - 1):
            self.curr_node = self.curr_node.next_item

        self.timer.start(100)
        self.play_next()

    def play_next(self) -> None:
        """
        Воспроизведение следующей песни в списке.
        """
        if self.curr_node is not None:

            name_of_song = self.current().split("/")[-1]

            self.name.setText(name_of_song)
            pygame.mixer.music.load(self.curr_node.data)
            pygame.mixer.music.play()
            self.timer.timeout.disconnect()
            self.timer.timeout.connect(self.check_if_done)
        else:
            self.timer.stop()
            QMessageBox.warning(self, "Warning", "Elements are missing")

    def check_if_done(self) -> None:
        """
        Проверка, завершено ли воспроизведение текущей песни.
        Если завершено, воспроизводит следующую песню.
        """
        if not pygame.mixer.music.get_busy():
            self.curr_node = self.curr_node.next_item
            self.play_next()

    def previous_track(self) -> None:
        """
        Воспроизведение предыдущей песни в списке.
        """
        if self.curr_node is not None:
            if self.list.len == 1:
                QMessageBox.warning(self, "Warning", "Only one element in list")
            if self.curr_node.previous_item is not None:
                self.curr_node = self.curr_node.previous_item
                self.play_next()
            else:
                QMessageBox.warning(self, "Warning", "Unknown warning")
        else:
            QMessageBox.warning(self, "Warning", "Elements are missing")

    def next_track(self) -> None:
        """
        Воспроизведение следующей песни в списке.
        """
        if self.curr_node is not None:
            if self.list.len == 1:
                QMessageBox.warning(self, "Warning", "Only one element in list")
            if self.curr_node.next_item is not None:
                self.curr_node = self.curr_node.next_item
                self.play_next()
            else:
                QMessageBox.warning(self, "Warning", "Unknown warning")
        else:
            QMessageBox.warning(self, "Warning", "Elements are missing")

    def current(self) -> str:
        """
        Получение названия текущей песни.
        Возвращает название текущей песни или сообщение о том, что элементы отсутствуют.
        """
        return self.curr_node.data if self.curr_node else "Elements are missing"
