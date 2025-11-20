class Reservation:
    def __init__(self, dateResa, nbrPersResa:int, prefClient:str):
        self.__date = dateResa
        self.__nbrPers = nbrPersResa
        self.__pref = prefClient

    @property
    def date(self):
        return self.__date
    
    @date.setter
    def date (self,new_date):
         self.__date = new_date

    @property
    def nbr_pers (self):
        return self.__nbrPers
    
    @nbr_pers.setter
    def nbr_pers(self, new_nbr):
        self.__nbrPers = new_nbr

    @property
    def preferences(self):
        return self.__pref
    
    @preferences.setter
    def preferences(self, new_pref):
        self.__pref = new_pref

    def suppr_resa(self):