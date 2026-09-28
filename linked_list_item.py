class LinkedListItem:
    """
    Класс для хранения элементов двусвязного кольцевого списка.
    Атрибуты:
        data (str) - адрес музыкальной композиции
        _next (LinkedListItem | None): Указатель на следующий элемент списка.
        _prev (LinkedListItem | None): Указатель на предыдущий элемент списка.
    Методы:
        next_item -> (LinkedListItem | None): Возвращает следующий элемент.
        previous_item -> (LinkedListItem | None): Возвращает предыдущий элемент.
    """

    def __init__(self, composition):
        """
        Инициализирует новый элемент списка с указанной музыкальной композицией.
        :param composition:
        """
        self.data = composition
        self._next = None
        self._prev = None

    @property
    def next_item(self) -> 'LinkedListItem':
        return self._next

    @property
    def previous_item(self) -> 'LinkedListItem':
        return self._prev

    @next_item.setter
    def next_item(self, value) -> None:
        """
        Устанавливает следующий элемент списка.
        :param value:
        """
        self._next = value
        if value is not None:
            value.previous_item = self

    @previous_item.setter
    def previous_item(self, value) -> None:
        """
        Устанавливает предыдущий элемент списка.
        :param value:
        """
        self._prev = value
        if value is not None:
            value._next = self

