
class A(object):

    def __init__(self,var):

        self.reset(var)

    def reset(self,var):

        self.vars = {'c':'hahah'}
        self.a = ''
        self.b = None

    def __getattr__(self,name):

        return self.vars[name]
a = A('var')

print a.a
print a.b
print a.c
