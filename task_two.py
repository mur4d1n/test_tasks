import time
from collections import deque

# Задание 2. Циклический буфер FIFO.
#
# Ниже приведены два класса, реализующих циклический буфер FIFO. Класс FIFOCycleBuffer не использует никаких
# дополнительных структур данных, класс FIFOCycleBufferWithDeque использует для работы встроенную в Python структуру
# deque - двунаправленную очередь.

# Я посчитал необходимым реализовать класс исключения для приведённых буферов, так как его наличие позволит лучше понять
# причину возникновения ошибки

class FIFOCycleBufferError(Exception):
    __error_msg: str = 'Error: FIFOCycleBuffer is {msg}'

    def __init__(self, msg: str):
        super().__init__(self.__error_msg.format(msg=msg))


# Вариант 1. Всё делаем вручную

class FIFOCycleBuffer:
    def __init__(self, max_size: int):
        """
        Инициализация циклического буфера FIFO

        :param max_size: int - максимальный размер буфера
        """
        self.__max_size: int = max_size             # Задаём маскимальный размер буфера из переданного аргумента
        self.__queue: list = [None] * max_size      # Определяем пустой список, который будем использовать как буфер
        self.__tail: int = 0                        # Задаём нулевой tail, т.к. именно с нуля начинаем заполнять буфер
        self.__head: int = -1                       # head = -1, т.к. при первом pop инкрементируем до 0
        self.__size = 0                             # Задаём size, при ините буфер пустой, поэтому 0

    def put(self, elem: object) -> None:
        """
        Помещение элемента в циклический буфер FIFO.  При переполнении буфера будет вызвано FIFOCycleBufferError.

        :param elem: object - объект, помещаемый в буфер
        :return: None
        """
        if self.__size == self.__max_size:                  # Падаем с ошибкой, если буфер полон
            raise FIFOCycleBufferError('full')

        self.__queue[self.__tail] = elem                    # Помещаем elem в хвост буфера
        self.__tail = (self.__tail + 1) % self.__max_size   # Обновляем индекс хвоста
        self.__size += 1                                    # Инкрементируем текущий объём буфера

    def pop(self) -> object:
        """
        Удаление самого старого элемента из циклического буфера FIFO. Удалённый элемент будет возвращён методом.
        После выполнения метода самым старым элементом будет считаться тот, что был помещён в буфер после удалённого.
        Если буфер пуст, будет вызвано FIFOCycleBufferError.

        :return: object - самое старое значение в буфере
        """
        if self.__size == 0:                    # Падаем с ошибкой, если текущий размер - нулевой (массив пуст)
            raise FIFOCycleBufferError('empty')

        self.__head = (self.__head + 1) % self.__max_size   # Обновляем индекс головы буфера
        elem = self.__queue[self.__head]                    # Забираем из массива самый старый элемент
        self.__queue[self.__head] = None                    # Опустошаем ячейку, из которой взяли значение
        self.__size -= 1                                    # Декрементируем текущй размер

        return elem                                         # Возвращаем самое старое значение

    @property
    def size(self) -> int:
        """
        Текущий размер (объём) циклического буфера FIFO.

        :return: int - размер буфера
        """
        return self.__size

    @property
    def buffer(self) -> list:
        """
        Массив, используемый в качестве хранилища данных циклического буфера FIFO

        :return: list - массив с данными, хранящимися в буфере
        """
        return self.__queue

# Вариант 2. Используем встроенный deque


class FIFOCycleBufferWithDeque:
    def __init__(self, max_size: int):
        """
        Инициализация циклического буфера FIFO

        :param max_size: int - максимальный размер буфера
        """
        self.__max_size = max_size                  # Задаём max_size из переданного параметра
        self.__deque = deque([], maxlen=max_size)   # Заводим deque длины max_size

    def put(self, elem: object) -> None:
        """
        Помещение элемента в циклический буфер FIFO.  При переполнении буфера будет вызвано FIFOCycleBufferError.

        :param elem: object - объект, помещаемый в буфер
        :return: None
        """
        if len(self.__deque) == self.__max_size:    # Падаем с ошибкой, если буфер полон
            raise FIFOCycleBufferError('full')

        self.__deque.append(elem)                   # Добавляем в deque переданный в метод элемент

    def pop(self) -> object:
        """
        Удаление самого старого элемента из циклического буфера FIFO. Удалённый элемент будет возвращён методом.
        После выполнения метода самым старым элементом будет считаться тот, что был помещён в буфер после удалённого.
        Если буфер пуст, будет вызвано FIFOCycleBufferError.

        :return: object - самое старое значение в буфере
        """
        if len(self.__deque) == 0:                  # Падаем с ошибкой, если буфер пуст
            raise FIFOCycleBufferError('empty')

        return self.__deque.popleft()               # Удаляем и возвращаем самый старый элемент дека

    @property
    def size(self) -> int:
        """
        Текущий размер (объём) циклического буфера FIFO.

        :return: int - размер буфера
        """
        return len(self.__deque)

    @property
    def buffer(self) -> deque:
        """
        Двунаправленная очередь, используемая в качестве хранилища данных циклического буфера FIFO

        :return: list - очередь с данными, хранящимися в буфере
        """
        return self.__deque

# Теперь перейдём к сравнению.
#
# Самое очевидное - в первом варианте мы не используем никаких дополнительных структур
# и потому процесс написания такого класса является более сложным и чреватым ошибками и непредусмотренными кейсами.
#
# Второй же вариант является более простым по причине использования уже встроенной в язык структуры двунаправленной
# очереди - нам не нужно следить за головой и хвостом буфера, также не нужно заводить счётчик для отметки длины буфера.
#
# Тесты времени выполнения показывают, что для n-го количества операций (от 100 до 1000000) лучшие результаты по времени
# выполнения показывает класс FIFOCycleBufferWithDeque. Я, признаться честно, ожидал противоположного результата, так
# как было ощущение, что в встроенном деке реализованы лишние действия, ненужные нашему классу, но вышло в итоге так.
#
# Предполагаю, что причиной такого поведения служит тот факт, что deque написан более оптимальным образом. Если
# мы обратимся к документации, то узнаем, что используемые нами методы взаимодействия с deque выполняются за
# константное время, а используемые методы взаимодействия с list - за O(n).


# Здесь приведён код тестирования времени выполнения
if __name__ == '__main__':
    from random import randint

    buffer = FIFOCycleBuffer(1000)
    buffer_deque = FIFOCycleBufferWithDeque(1000)

    ops_count = 100

    while ops_count < 10000000:
        buffer_ops_start_time = time.time()

        for i in range(1000000):
            op = randint(0, 1)

            if op == 0:
                try:
                    buffer.put(i)
                except FIFOCycleBufferError:
                    pass
            else:
                try:
                    buffer.pop()
                except FIFOCycleBufferError:
                    pass

        print(f'FIFOCycleBuffer ops time: {time.time() - buffer_ops_start_time} for {ops_count} ops')

        ops_count *= 10

    ops_count = 100

    while ops_count < 10000000:
        buffer_deque_ops_start_time = time.time()

        for i in range(1000000):
            op = randint(0, 1)

            if op == 0:
                try:
                    buffer_deque.put(i)
                except FIFOCycleBufferError:
                    pass
            else:
                try:
                    buffer_deque.pop()
                except FIFOCycleBufferError:
                    pass

        print(f'FIFOCycleBufferWithDeque ops time: {time.time() - buffer_deque_ops_start_time} for {ops_count} ops')

        ops_count *= 10

