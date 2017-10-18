data = [
    (None,'A'),
    ('A','A1'),
    ('A1','A1-1'),
    ('A','A2'),
    ('A1','A1-2'),
    ('A1-1','A1-1-1'),
    ('A','A3'),
    ('A1-1-1','A1-1-1-1'),
    ('A2','A2-1'),
    ('A2','A2-2'),
    ('A2-2','A2-2-1'),
    ('A3','A3-1'),
    (None,'B'),
    ('B','B1'),
    ('B1','B1-1'),
    ('B1','B1-2'),
    ('B','B2'),
    (None,'C'),
    ('C','C1'),
     ]

def a(data):
    data_dic = {}
    for i in data:
        x, y = i[0], i[1]
        if x == None:
            data_dic[y] = {}
        else:
            b(data_dic, x, y)
    print(data_dic)

def b(data_dic, x, y):
    for c, d in data_dic.items():
        if c == x:
            data_dic[c][y] = {}
            return
        else:
            b(data_dic[c], x, y)

if __name__ == '__main__':
    a(data)