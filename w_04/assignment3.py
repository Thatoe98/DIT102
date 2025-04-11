class Adventurer:
    def __init__ (self, name, race, level):
        self.name = name
        self.race= race
        self.level = level
    
    def get_info (self):
        return f"The adventurer {self.name} is of {self.race} race and level {self.level}\n"

class Mage (Adventurer):
    def __init__ (self,name, race, level, role, spell):
        super().__init__(name,race,level)
        self.role = role
        self.spell = spell

    def favorite_spell (self):
        return f"{self.name}'s favorite spell is {self.spell}\n"
    
    def get_info(self):
        return f"{self.name} of {self.race} race is serving as {self.role} role. The level is {self.level}\n"
    
class Warrior (Adventurer):
    def __init__(self, name, race, level, weapon, Armor):
        super().__init__(name, race, level)
        self.hp = weapon
        self.armor = Armor

    def get_info (self):
        return f"The warrior '{self.name}' of {self.race} race got {self.hp} weapon and wearing {self.armor} armor\n"
    
person1 = Adventurer("Edith" , "Human", 10)
person2 = Mage("Alexa", "Elf" , 22, "Damage" ,"Explosion" )

person3 = Warrior("David", "Minotaur", 35, "Hammer", "Mithril")

print (person1.get_info())
print (person2.get_info())
print (person2.favorite_spell())
print (person3.get_info())