

class Navigate:
    '''status: 'c'- continue,'''

    def __init__(self, page):
        self.len_page = len(page)
        self.status = None
        self.keyword_list = {
            'qqq': 'qqq',
            'ins': 'ins',
            'see': 'see',
            'name': 'name',
            'next': 'next',
            'back': 'back'}

    def allocation(self):
        key = input()
        try:
            key = int(key)
        except:
            return self.str_navigate(key)
        else:
            return self.int_navigate(key)

    def int_navigate(self, key):
        if key <= self.len_page:
            self.status = 'c'
            return key, self.status, None
        else:
            key = 1
            self.status = 'c'
            return key, self.status, None

    def str_navigate(self, key):
        if key.lower() in self.keyword_list:
            self.status = 'c'
            return 1, self.status, self.keyword_list[key]
        else:
            key = 1
            self.status = 'c'
            return 1, self.status, None


while True:
    navigate = Navigate([1, 2, 3, 4, 5, 1, 2, 3, 4, 1, 3,])
    b = navigate.allocation()
    print(b)
