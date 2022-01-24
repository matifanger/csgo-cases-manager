from database import database
from cases import cases
import requests, re

class functions:

    def __init__(self):
        self.db = database()
        self.cases = cases

    def get_dolar(self):
        try:
            print('Updating dolar price...')
            
            self.URL = 'https://www.dolarsi.com/api/api.php?type=valoresprincipales'
            self.json = requests.get(self.URL).json()
            self.db.update_data('dolar', {'latest_dolar_hoy': self.formatprice(self.json[0]['casa']['venta'][:-1]), 'latest_dolar_hoy_blue': self.formatprice(self.json[1]['casa']['venta'][:-1])})
            return '[Success] Dolar obtained!\n'
        except:
            return '[Error] Something happened...\n'


    def get_case(self):
        try:
            print('Obtaining cases...')
            i=0
            for case in cases:
                self.URL = 'http://csgobackpack.net/api/GetItemPrice/?id='+ cases[i]['id'] +'&time=7&currency=USD'
                self.json = requests.get(self.URL).json()
                i+=1
                self.db.update_data(case['title'],{'currentpriceusd': float(self.json['median_price'])})
            return '[Success] Cases obtained!\n'
        except:
            return '[Error] Something happened...\n'

    def im_i_winning(self):
        ammounts = []
        for case in cases:
            currentprices = self.db.get_data(case['title'], 'currentpriceusd')
            spent = self.db.get_data(case['title'], 'pricebuyinusd')
            ammounts.append(currentprices-spent)
        total = 0
        for price in ammounts:
            total = total + price
        if total >= 0:
            total_is = True
        else:
            total_is = False
        return total, total_is

        
    def cases_prices(self):
        casesprice = []
        self.im_i_winning()
        for case in cases:
            currentprices = self.db.get_data(case['title'], 'currentpriceusd')
            spent = self.db.get_data(case['title'], 'pricebuyinusd')
            casesprice.append((case['title'], spent, currentprices, self.is_winning(spent, currentprices)))
        #print(tabulate(casesprice, headers=['CASE', 'BUYED AT (USD)','PRICE (USD)', 'WINNING'], tablefmt="psql"))
        return casesprice
    
    def formatprice(self, value):
        print('Formatting prices...')
        x = False
        # Check for '$' string.
        try:
            matchsign = re.search('$', value)
            if matchsign is not None:
                x = True
                value = value.replace('$', '').strip(' ')
            
            # Check for ',' string.
            matchcomma = re.search(',', value)
            if matchcomma is not None:
                x = True
                value = value.replace(',', '.')
        except:
            pass
        
        if x is True:
            return float(value)
        else:
            return int(value)

    def rounded(self, value):
        rounded = float(round(value, 2))
        return rounded


    def is_winning(self, spent, currentprices):
        return self.rounded(currentprices-spent)
