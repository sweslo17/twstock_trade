import enum

class EventType(enum.Enum):
    BUY_STOCK = 1
    SELL_STOCK = 2
    GET_INTEREST = 3

class TradeLogger:
    def __init__(self):
        self.log = []
        
    def __repr__(self):
        return "\n".join([f"{log[1]}: {log[0]} shares:{log[2]:d} price:{log[3]:f} money_in_pocket:{log[4]:f}" for log in self.log])
    
    def buy_stock(self, datetime, shares, price, money_in_pocket):
        self.log.append((EventType.BUY_STOCK, datetime, shares, price, money_in_pocket))
        
    def sell_stock(self, datetime, shares, price, money_in_pocket):
        self.log.append((EventType.SELL_STOCK, datetime, shares, price, money_in_pocket))
        
    def get_interest(self, datetime, shares, price, money_in_pocket):
        self.log.append((EventType.GET_INTEREST, datetime, shares, price, money_in_pocket))