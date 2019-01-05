
class Annons_ref:
    def __init__(self, id, link, price):
        self.id = id
        self.link = link
        self.price = price

class Car_Add:
    def __init__(self, id, regnr, price, brand, model, model_year, make_year, gear, fuel, milage, type, hp, geo, add_date, first_seen, last_seen):
        self.id = id
        self.regnr = regnr
        self.price = price
        self.brand = brand
        self.model = model
        self.model_year = model_year
        self.make_year = make_year
        self.gear = gear
        self.fuel = fuel
        self.milage = milage
        self.type = type
        self.hp = hp
        self.geo = geo
        self.add_date = add_date
        self.first_seen = first_seen
        self.last_seen = last_seen