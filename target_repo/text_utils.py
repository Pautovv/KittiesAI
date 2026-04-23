def count_vowels(text: str) -> int:
    """Считает количество гласных букв (английских и русских) в строке."""
    vowels = set("aeiouAEIOUаеёиоуыэюяАЕЁИОУЫЭЮЯ")
    return sum(1 for char in text if char in vowels)

def is_palindrome(text: str) -> bool:
    """Проверяет, является ли строка палиндромом (читается одинаково слева направо и справа налево)."""
    clean_text = ''.join(char.lower() for char in text if char.isalnum())
    return clean_text == clean_text[::-1]