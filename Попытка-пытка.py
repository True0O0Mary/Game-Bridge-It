def ind(x, y, char):  # дает номер 0 или +
    if char == '0': return x // 2 + 4 * (y // 2)
    if char == '+': return x // 2 + 5 * (y // 2)

#connection
def m_connect():                       #соединяет вершины визуально
    global m, x1, y1, x2, y2
    if x1 == x2:
        y1, y2 = min(y1, y2), max(y1, y2)
        m[y1+1][x1] = '|'
    if y1 == y2:
        x1, x2 = min(x1, x2), max(x1, x2)
        m[y1][x1+1] = '—'

def m_01_connect(char):              #типа декоратора на m_0_connect и m_1_connect()
    if char == '0':
        m_0_connect()
    if char == '+':
        m_1_connect()
def m_0_connect():                      #соединяет 0 в их списке
    global m_0, x1, y1, x2, y2
    m_0[ind(x1, y1, '0' )] += [ind(x2, y2, '0')]
    m_0[ind(x2, y2, '0' )] += [ind(x1, y1, '0')]
    #m_0.sort()
def m_1_connect():                      #соединяет + в их списке
    global x1, y1, x2, y2, m_1
    m_1[ind(x1, y1, '+' )].append(ind(x2, y2, '+'))
    m_1[ind( x2, y2, '+' )].append( ind( x1, y1, '+' ) )
    #m_1.sort()

#красивый вывод
def pprint():                        #красивый вывод игральной доски
    global m
    print(' '*4, *(range(9)), 'X', sep = ' ')
    print(' '*4, '—'*18)
    for i in range(height):
        print(i, ' |', *m[i])
    print('Y')

#проверяет правильность ввода
def check_ade(char):                 # проверяет правильность ввода пользователя
    global x1, x2, y1, y2
    x_b, y_b = (x1+x2)//2, (y1+y2) // 2
    che = all(i in [j for j in range(0, 9)] for i in (x1, x2, y1, y2)) and ((abs(y1-y2) == 2) and (x1 == x2)) or ((abs(x1 - x2) == 2) and (y1 == y2))
    empty = not(m[y_b][x_b] == '|' or m[y_b][x_b] == '—')
    if char == '0':
        return che and all(i%2 == 1 for i in (x1, x2)) and all(i%2 == 0 for i in (y1, y2)) and empty
    if char == '+':
        return che and all(i%2 == 0 for i in (x1, x2)) and all(i%2 == 1 for i in (y1, y2)) and empty

def check_inp(c):
    c = c.split()
    if len(c) == 2:
        if c[0] in '012345678' and c[1] in '012345678':
            return int(c[0]), int(c[1])
    return -1, -1
#проверяет победу

def dfs(v, m):
    global component, visited, num_components
    component[v] = num_components
    visited[v] = True
    for w in m[v]:
        if visited[w] == False:
            dfs(w, m)

#проверяет возможность хода
def capability(char):
    if char == '0':
        return m_0_capability()
    if char == '+':
        return m_1_capability()
def m_0_capability():
    global m
    for i in range(len(m)):
        if not((i % 2 == 0 and m[i].count('—')+m[i].count('|') >= 3) or (i % 2 == 1 and m[i].count('—')+m[i].count('|') >= 4)):
            break
    else:
        return False
    return True
def m_1_capability():
    global m
    for i in range(1, len(m)-1):
        if not ((i % 2 == 1 and m[i].count( '—' ) + m[i].count( '|' ) == 4) or (
                i % 2 == 0 and m[i].count( '—' ) + m[i].count( '|' ) == 5)):
            break
    else:
        return False
    return True

#создание поля
width, height = 4, 9
m = list()
for i in range(height):
    a = list()
    if i % 2 == 0:
        char = '0'
        k = 0
    if i % 2 == 1:
        char = '+'
        k = 1
    for j in range(height):
        if k == 0:
            a.append(' ')
            k = 1
        else:
            a.append(char)
            k = 0
    m.append(a)

#процесс игры
m_0 = [[] for i in range(20)]
m_1 = [[] for i in range(20)]
print(m_0[4])
pprint()

char = '0'
i = 0
winner = 0
n = 20

while True:
    if char == '0':
        print('Ходите, мистер 0, ┌( ಠ_ಠ)┘')
    elif char == '+':
        print('Отвечайте, мистер +, ᕦ(ò_óˇ)ᕤ' )
    a = input()
    b = input()
    x1, y1 = check_inp(a)
    x2, y2 = check_inp(b)
    if not(check_ade(char)):
        print('Неправильный ввод ¯\_(ツ)_/¯')
        continue

    visited = [False] * 20
    m_connect()
    if char == '0':
        m_0_connect()
    if char == '+':
        m_1_connect()

    pprint()

    if char == '0':
        visited = [False] * n
        component = [-1] * n  # для каждой вершины храним номер её компоненты
        num_components = 0

        for v in range(n):
            if not visited[v]:
                dfs(v, m_0)
                num_components += 1

        if any(component[i] == component[j] for i in range(4) for j in range(16, 20)):
            print('Выиграли 0')
            winner = 1
        char = '+'
    elif char == '+':
        visited = [False] * n
        component = [-1] * n  # для каждой вершины храним номер её компоненты
        num_components = 0

        for v in range(n):
            if not visited[v]:
                dfs(v, m_1)
                num_components += 1

        if any(component[i] == component[j] for i in range(0, 16, 5) for j in range(4, 20, 5)):
            print('Выиграли +')
            winner = 1

        char = '0'
    if winner == 1:
        break
