import random


def read_sudoku(filename):
    """ Прочитать Судоку из указанного файла """
    digits = [c for c in open(filename).read() if c in '123456789.']
    grid = group(digits, 9)
    return grid


def display(values):
    """Вывод Судоку """
    width = 2
    line = '+'.join(['-' * (width * 3)] * 3)
    for row in range(9):
        print(''.join(values[row][col].center(width) + ('|' if str(col) in '25' else '') for col in range(9)))
        if str(row) in '25':
            print(line)
    print()


def group(values, n):
    a_list = []
    i = 0
    while i < n:
        a_list.append(values[slice(i * n, n * (i + 1))])
        i += 1
    return a_list


def get_row(values, pos):
    return values[pos[0]]


def get_col(values, pos):
    t = []
    a = pos[1]
    for i in range(0, 9):
        t += values[i][a]
    return t


def get_block(values, pos):
    b = []
    if 9 / (pos[0] + 1) >= 3:
        r = 0
    elif 9 / (pos[0] + 1) >= 1.5:
        r = 3
    else:
        r = 6

    if 9 / (pos[1] + 1) >= 3:
        c = 0
    elif 9 / (pos[1] + 1) >= 1.5:
        c = 3
    else:
        c = 6
    for i in range(0, 3):
        for j in range(0, 3):
            b += values[r + i][c + j]
    return b


def find_empty_positions(grid):
    for row in range(0, 9):
        for col in range(0, 9):
            if grid[row][col] == '.':
                pos = row, col
                return pos
    return False


def find_possible_values(grid, pos):

    b = get_block(grid, pos)
    c = get_col(grid, pos)
    r = get_row(grid, pos)
    m = []
    for i in range(1, 10):
        if not str(i) in b and not str(i) in c and not str(i) in r:
            m += str(i)
    return m


def solve(grid):

    pos = find_empty_positions(grid)
    if find_empty_positions(grid) == False:
        display(grid)
        print(check_solution(grid))
    else:
        for a in range(1, 10):
            if str(a) in find_possible_values(grid, pos):
                grid[pos[0]][pos[1]] = str(a)
                if solve(grid):
                    return True
                grid[pos[0]][pos[1]] = '.'
    return False


def check_solution(solution):
    m = 'True'
    for row in range(0, 9):
        for col in range(0, 9):
            pos = row, col
            b = get_block(solution, pos)
            c = get_col(solution, pos)
            r = get_row(solution, pos)
            for i in range(1, 10):
                if not (str(i) in b and str(i) in c and str(i) in r):
                    m = 'False'

    # Если решение solution верно, то вернуть True, в противном случае False
    return m

grid = read_sudoku('C:\ Users\Talantseva Ekaterina\Desktop\ University\Python\Lab\lab2\puzzle1.txt')
display(grid)
solve(grid)


def generate_sudoku(N):    # единственное решение
    grid = read_sudoku('C\ Users\Talantseva Ekaterina\Desktop\ University\Python\Lab\lab2\sample.txt')
    print(grid)
    j = random.randint(3, 6)
    for i in range(0, j):
        a = random.randint(0, 2)
        area = a * 3
        line1 = random.randint(area, area + 2)
        line2 = random.randint(area, area + 2)
        while line2 == line1:
            line2 = random.randint(area, area + 2)
        grid[line1], grid[line2] = grid[line2], grid[line1]

    j = random.randint(5, 8)
    for i in range(0, j):
        a = random.randint(6, 9)
        area = a * 3
        line1 = random.randint(area, area + 2)
        line2 = random.randint(area, area + 2)
        while line2 == line1:
            line2 = random.randint(area, area + 2)
        for k in range(0, 9):
            grid[k][line1], grid[k][line2] = grid[k][line2], grid[k][line1]

    for i in range(0, 81 - N):     # расставляем точки
        row = (random.randint(0, 8))
        col = (random.randint(0, 8))
        while grid[row][col] == ".":
            row = (random.randint(0, 8))
            col = (random.randint(0, 8))
        grid[row][col] = "."
    display(grid)
    solve(grid)

generate_sudoku(40)