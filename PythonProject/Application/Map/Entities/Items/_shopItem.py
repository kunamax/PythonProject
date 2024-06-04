from ._item import Item
class ShopItem():
    def __init__(self,item:Item,price:int,img=None):
        self.item=item
        self.price=price
        self.img=img #mozetak moze nie?