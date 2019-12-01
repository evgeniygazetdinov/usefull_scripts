#my undestanding yield



class Bank():
    crisis = False
    def create_atm(self):
        #and he (create_atm)return constantly 100$ with .next()
        while not self.crisis:
            yield '$100'



#and crisis very useful for stop generator
