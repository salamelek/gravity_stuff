my_list = []


class Test:
    def __init__(self, i):
        self.a = i

    def print_list(self):
        for i in my_list:
            if i is not self:
                print(i.a)


for i in range(2):
    my_list.append(Test(i))


for obj in my_list:
    obj.print_list()
