from typing import Any, Generator

from linked_list_item import *


class LinkedList:
    """
        Класс, представляющий двусвязный список.

        Атрибуты:
            first_item (LinkedListItem): Указатель на первый элемент списка.
            last (LinkedListItem): Указатель на последний элемент списка.
            len (int): Текущая длина списка (количество элементов).
            current_iter (LinkedListItem): Указатель для итерации по списку.

        Методы:
            is_empty() -> bool: Проверяет, пуст ли список.
            append_left(composition: str) -> None: Добавляет новый элемент в начало списка.
            append_right(composition: str) -> None: Добавляет новый элемент в конец списка.
            append(composition: str) -> None: Эквивалент метода append_right.
            remove(composition: str) -> None: Удаляет элемент из списка по значению.
            insert(previous: str, composition: str) -> None: Вставляет новый элемент после заданного элемента.
            last() -> LinkedListItem: Возвращает последний элемент списка.
            __getitem__(index: int) -> LinkedListItem: Получает элемент по индексу.
            __contains__(composition: str) -> bool: Проверяет, содержится ли элемент в списке.
            __len__() -> int: Возвращает длину списка.
            __iter__() -> LinkedList: Возвращает итератор для списка.
            __next__() -> str: Возвращает следующий элемент при итерации по списку.
            __reversed__() -> Iterator[str]: Возвращает элементы списка в обратном порядке.
        """

    def __init__(self, head=None):
        """
        Инициализирует новый пустой двусвязный список.
        """
        self.first_item = head
        self.last = head
        self.len = 0

        if head is not None:
            self.len = 1
            current = head
            while current.next_item != head and current.next_item is not None:
                current = current.next_item
                self.len += 1
            self.last = current

            self.current_iter = head


    def is_empty(self) -> bool:
        """
        Проверят пуст ли список.
        """
        return self.first_item is None

    def append_left(self, composition: str) -> None:
        """
        Добавляет новый элемент в начало списка.
        """
        new_node = LinkedListItem(composition)

        if self.is_empty():
            self.first_item = new_node
            self.last = new_node
            self.first_item.next_item = self.last
            self.last.previous_item = self.first_item
        else:
            new_node.next_item = self.first_item
            new_node.previous_item = self.last
            self.first_item.prev = new_node
            self.first_item = new_node
            self.last.next = self.first_item

        self.len += 1

    def append_right(self, composition: str) -> None:
        """
        Добавляет новый элемент в конец списка.
        """
        new_node = LinkedListItem(composition)
        if self.is_empty():
            self.first_item = new_node
            self.last = new_node
            self.first_item.next_item = self.last
            self.last.previous_item = self.first_item
        else:
            self.last.next_item = new_node
            new_node.previous_item = self.last
            new_node.next_item = self.first_item
            self.last = new_node
            self.first_item.previous_item = self.last

        self.len += 1

    append = append_right

    def remove(self, composition: str) -> None:
        """
        Удаляет элемент из списка по значению.
        :param composition:
        """
        if self.is_empty():
            raise ValueError("Empty")

        temp_node = self.first_item
        while True:
            if composition == temp_node.data:
                if temp_node == self.first_item:
                    self.first_item = temp_node.next_item
                if temp_node == self.last:
                    self.last = temp_node.previous_item
                temp_node.previous_item.next_item = temp_node.next_item
                temp_node.next_item.previous_item = temp_node.previous_item
                self.len -= 1
                if self.len == 0:
                    self.first_item = None
                    self.last = None
                return
            temp_node = temp_node.next_item
            if temp_node == self.first_item:
                break

        raise ValueError(f"Composition {composition} not found")

    def insert(self, previous: str, composition: str) -> ValueError | None:
        """
        Вставляет новый элемент после заданного элемента.
        :param previous:
        :param composition:
        """

        if self.is_empty():
            raise ValueError("Empty")

        new_node = LinkedListItem(composition)
        temp_node = self.first_item
        while True:
            if temp_node.data == previous:
                new_node.next_item = temp_node.next_item
                new_node.previous_item = temp_node

                if temp_node == self.last:
                    self.last = new_node

                self.len += 1
                return

            temp_node = temp_node.next_item


    def last(self):
        """
        Возвращает последний элемент списка.
        """
        return self.last

    def __getitem__(self, index) -> 'LinkedListItem':
        """
        Получает элемент по индексу.
        :param index:
        """

        if index < 0:
            index += self.len

        if index < 0 or index >= self.len:
            raise IndexError("Index out of range")

        temp_node = self.first_item
        for _ in range(index):
            temp_node = temp_node.next_item
        return temp_node.data

    def __contains__(self, composition: str) -> bool:
        """
        Проверяет, содержится ли элемент в списке.
        :param composition:
        """
        temp_node = self.first_item
        if temp_node is None:
            return False

        while True:
            if temp_node.data == composition:
                return True
            else:
                temp_node = temp_node.next_item
                if temp_node == self.first_item:
                    break

        return False

    def __len__(self) -> int:
        """
        Возвращает длину списка.
        """
        return self.len

    def __iter__(self) -> 'LinkedList':
        """
        Возвращает итератор для списка.
        """
        self.current_iter = self.first_item
        return self

    def __next__(self) -> str:
        """
        Возвращает следующий элемент при итерации по списку.
        """
        if self.current_iter is None:
            raise StopIteration

        curr_node = self.current_iter
        self.current_iter = self.current_iter.next_item

        if self.current_iter == self.first_item:
            self.current_iter = None

        return curr_node

    def __reversed__(self) -> Generator[Any, Any, None]:
        """
        Возвращает элементы списка в обратном порядке.
        """
        if self.is_empty():
            return

        temp_node = self.last
        stop_node = self.last
        while True:
            yield temp_node.data
            temp_node = temp_node.previous_item
            if temp_node == stop_node:
                break
