
class SpotRate:
    def __init__(self, interest_rate, n_periods):
        self.interest_rate = interest_rate
        self.n_periods = n_periods
    def discountRate(self):
        return 1./(1.+self.interest_rate)**self.n_periods


def discountRate(spot_rate, n_periods):
    return 1./(1.+spot_rate)**n_periods

def forwardPrice(asset_price, spot_rate):
    return asset_price / spot_rate.discountRate()

def forwardValue(F_0, F_t, spot_rate):
    return (F_t - F_0) * spot_rate.discountRate()

def forwardRate(spot_1, spot_2):
    return (((1+spot_2.interest_rate)**spot_2.n_periods /
             (1+spot_1.interest_rate)**spot_1.n_periods)
            ** (1/(spot_2.n_periods - spot_1.n_periods))) - 1.
