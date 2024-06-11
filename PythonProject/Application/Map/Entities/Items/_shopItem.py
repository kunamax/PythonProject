from ._item import Item
class ShopItem():
    def __init__(self,item:Item,price:int):
        self.item=item
        self.price=price