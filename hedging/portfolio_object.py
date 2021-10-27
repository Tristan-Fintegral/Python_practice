import datetime

class Portfolio:

    def __init__(self):
        self.deals = {}
        self.deal_counter = 0

    def __repr__(self):
        return '\n'.join([f'{key}: {val}' for key, val in self.deals.items()])

    def create_deal(self, instrument, quantity, counterparty=None, creation_time=None):
        deal = Deal(
            instrument=instrument,
            quantity=quantity,
            counterparty=counterparty,
            creation_time=creation_time
        )
        self.add_deal(deal=deal)

        if deal.quantity == 0:
            self.remove_deal(deal=deal)

    def add_deal(self, deal):
        self.deals[self.deal_counter] = deal
        self.deal_counter += 1

    def price(self, market_data_object):
        total_pv = 0
        for instrument, quantity in self.instrs.items():
            instr_npv = instrument.price(market_data_object)
            position_npv = instr_npv * quantity
            total_pv += position_npv

        return total_pv

    def deals_with_counterparty(self):
        pass

    def deals_on_instrument(self):
        pass


class Deal:

    def __init__(self, instrument, quantity, counterparty='Unknown', creation_time=None):
        self.instrument = instrument
        self.quantity = quantity
        self.creation_time = creation_time or datetime.datetime.now()
        self.counterparty = counterparty

    def __repr__(self):
        return f'Deal(instrument={self.instrument}, ' \
               f'quantity={self.quantity}, ' \
               f'counterparty={self.counterparty}, ' \
               f'creation_time={self.creation_time})'


def main():
    portfolio_A = Portfolio()
    portfolio_A.create_deal(instrument='option', quantity=10)
    portfolio_A.create_deal(instrument='option', quantity=20)
    print(portfolio_A.deals)


if __name__ == '__main__':
    main()
