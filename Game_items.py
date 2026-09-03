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

    def __eq__(self, other):
        if isinstance(other, Game):
            return self.title == other.title and self.original_price == other.original_price and self.discount == other.discount
        return False
    
    # Discount
    def return_discount(self):
        return self.discount
    
    # Original Price
    def return_original_price(self):
        return self.original_price
    
    # Saved Amount
    def return_saved_discount(self):
        return self.original_price * self.discount
    
    # Discounted Price
    def return_discounted_price(self):
        return self.original_price - self.return_saved_discount()
    
    # Hybrid System
    def return_hybrid_price(self):
        return self.return_saved_discount() * self.discount
    
    # Title
    def return_title(self):
        return self.title

    # Score based on type of score
    def score_self(self, type_score):
        self_score = 0
        if type_score == 2:
            self_score = self.return_saved_discount()
        elif type_score == 3:
            self_score = self.return_hybrid_price()
        else:
            self_score = self.return_discount()
        if self_score <= 0:
            self_score = 0.01
        return self_score
