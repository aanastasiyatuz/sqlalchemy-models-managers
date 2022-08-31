from core.models import Model

class Test(Model):
    def __init__(self, id, title, price):
        self.id = id
        self.title = title
        self.price = price
    
    def __repr__(self):
        return f"<Product({self.id}) title='{self.title}' price={self.price}>"


print(Test.objects.all())