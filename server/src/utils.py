import random
import string


def generate_random_string(length):
    """
    Note: random.sample prevents character reuse, multiplying the size of the character
    set makes multiple repetitions possible, but they are still less likely then they
    are in a pure random choice. If we go for a string of length 6, and we pick 'X'
    as the first character, in the choice example, the odds of getting 'X'
    for the second character are the same as the odds of getting 'X' as the first character.
    """
    char_set = string.ascii_letters + string.ascii_uppercase

    return "".join(random.choice(char_set) for _ in range(length))
