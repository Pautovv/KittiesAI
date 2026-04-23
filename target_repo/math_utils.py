def fibonacci(n: int) -> list[int]:
    """Возвращает последовательность Фибоначчи до n элементов."""
    if n <= 0: return []
    if n == 1: return [0]
    res = [0, 1]
    for _ in range(2, n):
        res.append(res[-1] + res[-2])
    return res

def calculate_factorial(n: int) -> int:
    """Вычисляет факториал числа n."""
    if n == 0: return 1
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result