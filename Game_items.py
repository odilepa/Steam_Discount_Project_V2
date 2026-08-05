TYPE_DISCOUNT = 1
TYPE_SAVED_DISCOUNT = 2
TYPE_HYBRID_PRICE = 3

class Game():
    def __init__(self, title, original_price, discount):
        self.title = title
        self.original_price = original_price
        if discount < 0:
            discount = 0
        elif discount > 1:
            discount = discount / 100
        self.discount = discount
    
    def __str__(self):
        return f"""###------###
Item: {self.title},
Original Price: {self.original_price:.2f}$,
Discount Amount: {self.discount * 100}%
###------###"""
    
    def return_discount(self):
        return self.discount
    
    def return_original_price(self):
        return self.original_price
    
    def return_discount_amount(self):
        return self.original_price * self.discount
    
    def return_saved_discount(self):
        return self.original_price - self.return_discount_amount()
    
    def return_hibrid_price(self):
        return self.return_saved_discount() * self.discount
    
    def return_title(self):
        return self.title

    def score_self(self, type_score):
        if type_score == 2:
            return self.return_saved_discount()
        elif type_score == 3:
            return self.return_hibrid_price()
        return self.return_discount()
