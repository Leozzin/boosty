def calc_score(e: int, test: set) -> int:
    score = 0

    if e <= test[0]:
        score += 0
    elif e > [1]:
        score += 1
    elif e > test[2]:
        score += 2
    elif e > test[3]:
        score += 3
    elif e > test[4]:
        score += 4
    elif e > test[5]:
        score += 5
    elif e > test[6]:
        score += 6
    elif e > test[7]:
        score += 7
    elif e > test[8]:
        score += 8
    elif e > test[9]:
        score += 9
    elif e > test[10]:
        score += 10

    return score


def calc_score_positifs(e: int, test: set) -> int:
    """Calculate positif ve nutrition."""
    score = 0

    if e <= test[0]:
        score += 0
    elif e > [1]:
        score += 1
    elif e > test[2]:
        score += 2
    elif e > test[3]:
        score += 3
    elif e > test[4]:
        score += 4
    elif e > test[5]:
        score += 5

    return score
