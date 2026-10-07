def my_map(func, lst):
    if not lst:
        return []
    head = lst[0]
    tail = lst[1:]
    return [func(head)] + my_map(func, tail)


def my_filter(func, lst):
    if not lst:
        return []
    head = lst[0]
    tail = lst[1:]
    if func(head):
        return [head] + my_filter(func, tail)
    return my_filter(func, tail)


def my_reduce(func, lst, initializer=None):
    if not lst:
        if initializer is None:
            raise TypeError("reduce() of empty sequence with no initial value")
        return initializer
    if initializer is None:
        head = lst[0]
        tail = lst[1:]
        return my_reduce(func, tail, head)
    head = lst[0]
    tail = lst[1:]
    return my_reduce(func, tail, func(initializer, head))


def _bubble_pass(arr, index=0):
    if index >= len(arr) - 1:
        return arr
    if arr[index] > arr[index + 1]:
        new_arr = list(arr)
        new_arr[index], new_arr[index + 1] = new_arr[index + 1], new_arr[index]
        return _bubble_pass(new_arr, index + 1)
    return _bubble_pass(arr, index + 1)


def bubble_sort(arr):
    data = list(arr)
    n = len(data)

    def _sort(lst, count):
        if count <= 1:
            return lst
        lst_after_pass = _bubble_pass(lst)
        return _sort(lst_after_pass, count - 1)

    return _sort(data, n)


if __name__ == '__main__':
    test = [5, 3, 8, 4, 1]
    print("Original:", test)
    print("Bubble sort:", bubble_sort(test))

    nums = [1, 2, 3, 4, 5, 6]
    print("Map (*2):", my_map(lambda x: x * 2, nums))
    print("Filter (even):", my_filter(lambda x: x % 2 == 0, nums))
    print("Reduce (sum):", my_reduce(lambda a, b: a + b, nums))
    print("Reduce (*):", my_reduce(lambda a, b: a * b, [1, 2, 3, 4]))
