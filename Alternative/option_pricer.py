import pandas as pd
import numpy as np
from scipy.stats import norm

class OptionPricer:
    def __init__(self, trade_data_path, market_data_path, output_path):
        self.trade_data_path = trade_data_path
        self.market_data_path = market_data_path
        self.output_path = output_path
        
        #rates
        self.rates = {
            'r_usd': 0.05,
            'r_eur': 0.03,
            'r_misc': 0.02
        }

    def load_data(self):
        self.trade_data = pd.read_csv(self.trade_data_path)
        self.market_data = pd.read_csv(self.market_data_path)
        self.data = pd.merge(self.trade_data, self.market_data, on='underlying', how='left')
        #self.data.to_csv("merge.csv", index=False)
        

    @staticmethod
    def d1(S, K, T, r, sigma):
        return (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))

    @staticmethod
    def d2(S, K, T, r, sigma):
        return OptionPricer.d1(S, K, T, r, sigma) - sigma * np.sqrt(T)

    @staticmethod
    def black_scholes_call(S, K, T, r, sigma):
        return S * norm.cdf(OptionPricer.d1(S, K, T, r, sigma)) - K * np.exp(-r * T) * norm.cdf(OptionPricer.d2(S, K, T, r, sigma))

    @staticmethod
    def black_scholes_put(S, K, T, r, sigma):
        return K * np.exp(-r * T) * norm.cdf(-OptionPricer.d2(S, K, T, r, sigma)) - S * norm.cdf(-OptionPricer.d1(S, K, T, r, sigma))

    def calculate_options(self):
        self.data[['PV', 'Equity Delta', 'Equity Vega']] = self.data.apply(self.option_valuation, axis=1)
    
    def get_fx_rate(self, currency):
        # Check if USD is the base currency
        if f"USD/{currency}" in self.market_data['underlying'].values:
            rate =self.market_data.loc[self.market_data['underlying'] == f"USD/{currency}", 'spot_price'].iloc[0]
            return 1 / rate  # Invert the rate because USD is the base currency
        
        # Check if USD is the quote currency
        elif f"{currency}/USD" in self.market_data['underlying'].values:
            return self.market_data.loc[self.market_data['underlying'] == f"{currency}/USD", 'spot_price'].iloc[0]
        
        else:
            raise ValueError(f"FX rate for {currency} not found in the data")
        
        
    def option_valuation(self, row):
        S = row['spot_price']
        K = row['strike']
        T = row['expiry']
        
        """
        #rates
        r_usd=0.05 
        r_eur=0.03
        r_misc=0.02
        """
        r = self.rates['r_usd'] if row['payment_currency'] == 'USD' else self.rates['r_eur'] if row['payment_currency'] == 'EUR' else self.rates['r_misc']
        
        sigma = row['volatility']
        quantity = row['quantity']
        option_type = 'call' if row['call_put'].upper() == 'CALL' else 'put'
        
        price_function = self.black_scholes_call if option_type == 'call' else self.black_scholes_put
        
        pv = price_function(S, K, T, r, sigma) * quantity
        
        
        if row['payment_currency'] == 'USD':
            pv = pv
            delta = norm.cdf(self.d1(S, K, T, r, sigma)) if option_type == 'call' else -norm.cdf(-self.d1(S, K, T, r, sigma))
            vega = S * norm.pdf(self.d1(S, K, T, r, sigma)) * np.sqrt(T)
        else:
            fx_rate = self.get_fx_rate(row['payment_currency'])
            pv = pv * fx_rate
            delta = (norm.cdf(self.d1(S, K, T, r, sigma)) * fx_rate if option_type == 'call' else -norm.cdf(-self.d1(S, K, T, r, sigma))) * fx_rate
            vega = S * norm.pdf(self.d1(S, K, T, r, sigma)) * np.sqrt(T) * fx_rate
        
        delta *= quantity
        vega *= quantity


        return pd.Series([pv, delta, vega], index=['PV', 'Equity Delta', 'Equity Vega'])

    def save_results(self):
        self.data[['trade_id', 'PV', 'Equity Delta', 'Equity Vega']].round(4).to_csv(self.output_path, index=False)

if __name__ == '__main__':
    pricer = OptionPricer('trade_data.csv', 'market_data.csv', 'result.csv')
    pricer.load_data()
    pricer.calculate_options()
    pricer.save_results()
