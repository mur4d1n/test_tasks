import time
from random import randint

# Задание 3. Самый быстрый алгоритм сортировки

# Для выполнения задания я решил использовать сортировку подсчётом.  Хоть она и не поддерживает работу с отрицательными
# числами, она всё ещё остаётся одной из самых быстрых, да и в условии наличие или отстутсвие в массиве отрицательных
# чисел не указано :)


def counting_sort(input_array):
    # Для начала найдём максимальный элемент в массиве
    max_element = max(input_array)

    # Рассчитаем длину массива, в который мы будем записывать подсчёты
    count_array_length = max_element + 1

    # Создадим этот массив и заполним его нулями
    count_array = [0] * count_array_length

    # Пройдём по входному массиву и запишем в count_array
    # количество каждых чисел в массиве
    for el in input_array:
        count_array[el] += 1

    # Пройдёмся по count_array и просуммируем значение каждого
    # элемента, начиная с первого, со значением предыдущего
    for i in range(1, count_array_length):
        count_array[i] += count_array[i-1]

    # Рассчитаем позицию элементов на основе того,
    # что имеем в count_array
    output_array = [0] * len(input_array)
    i = len(input_array) - 1
    while i >= 0:
        current_el = input_array[i]
        count_array[current_el] -= 1
        new_position = count_array[current_el]
        output_array[new_position] = current_el
        i -= 1

    return output_array

# Сложность данного алгоритма в худшем случае составляет O(n + k), аналогично в среднем, а в лучшем - O(n).
# Такие данные обходят многие другие алгоритмы, например, Radix или Quick sort.
#
# Сортировка подсчётом работает быстрее приведённых выше алгоритмов, иногда демонстрируя кратную разницу. В моём случае
# на Quick sort сотни массивов с 1000000 элементов ушла почти минута, когда на такую же сортировку подсчётом
# было затрачено всего 16 секунд - разница почти в 4 раза!
#
# Впрочем, есть и минусы.  Сортировка подсчётом не может работать с отрицательными числами, т.к. это приводит к
# IndexError при попытке обратиться к элементу с отрицательным индексом.


if __name__ == '__main__':
    elems = 100

    while elems <= 1000000:
        tries_count = 100
        tries = list()

        for i in range(tries_count):
            test_arr = [randint(0, 1000) for j in range(elems)]

            start_time = time.time()

            sorted_arr = counting_sort(test_arr)

            tries.append(time.time() - start_time)

        print(f'100 arrays with {elems} elems in it were sorted in {sum(tries)} seconds, approximately {sum(tries) / len(tries)} for each')

        elems *= 10
