
import copy

class CurrencyRate:
    #base
    #quote

    def __init__(self, base, quote):
        self.base = base
        self.quote = quote

    def __imul__(self, val):
        self.base *= val
        self.quote *= val
        return self

    def __deepcopy__(self, memo):
        return CurrencyRate(self.base, self.quote)


def fwd(spot, currency_rate):
    c = currency_rate
    return spot * (1+c.quote/100.) / (1+c.base/100.)

def fwd_timed(spot, currency_rate, day_period, day_count):
    c = currency_rate
    c = copy.deepcopy(c)
    ratio = 1. * day_period / day_count
    c *= ratio
    return fwd(spot, c)


if __name__ == "__main__":
    spot = 0.85
    cr = CurrencyRate(1.257, 1.085)
    print fwd_timed(spot, cr, 92, 360)

    spot = 0.85
    cr = CurrencyRate(1.517, 1.385)
    print fwd_timed(spot, cr, 182, 360)
