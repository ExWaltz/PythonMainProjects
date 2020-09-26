

class Recipe:
    """ title: Title of recipe
        ingredients: Must be LIST; ingredients of recipe
        time: Must be LIST; format:[0,1,30]; (1 minute and 30 seconds)
            * wiil override hour,minute and second
        hour: hours to finish the recipe
        minute: minutes to finish the recipe
        second: seconds to finish the recipe
        temperature: celcius; temperature recommended for the recipe
        instructions: str; instructions for recipe
                    * list; ["step 1", "step 2", "step 3", "instructions", "ect"]
        utensils: Must be List; ["Pot", "frying pan", "timer", "ladle", "ect"]
        serving: Int; recommended amout of people for eating"""

    def __init__(self, title, ingredients=None, time=None, hour=0, minute=0, second=0, temperature=100, instructions=None, utensils=None, serving=1):
        self.title = str(title)
        self.ingredients = ingredients
        self.time = time
        self.hour = int(hour)
        self.minute = int(minute)
        self.second = int(second)
        self.temperature = str(temperature)
        self.instructions = instructions
        self.utensils = utensils
        self.serving = int(serving)

        self.updateMutableParam()

    def updateMutableParam(self):
        if self.ingredients is None:
            self.ingredients = ["", ]
        if self.time is None:
            self.time = [self.hour, self.minute, self.second]
        if self.instructions is None:
            self.instructions = ["", ]
        if self.utensils is None:
            self.utensils = ["", ]

        if self.time is not None:
            self.hour, self.minute, self.second = [int(tm) for tm in self.time]
            self.day = 0
            while self.hour > 24 or self.minute >= 60 or self.second >= 60:
                if self.hour > 24:
                    self.day += 1
                    self.hour -= 24
                if self.minute >= 60:
                    self.hour += 1
                    self.minute -= 60
                if self.second >= 60:
                    self.minute += 1
                    self.second -= 60

        if isinstance(self.instructions, str):
            self.instructions = [self.instructions, ]
        if isinstance(self.ingredients, str):
            self.ingredients = [self.ingredients, ]
        if isinstance(self.utensils, str):
            self.utensils = [self.utensils, ]

    @staticmethod
    def ScrambledEgg():
        return Recipe("Scrambled Egg", ["Egg", "Oil"], time=[0, 5, 0], temperature=110, serving=1, utensils=["Frying pan", "bowl", "fork or whisk"], instructions=["Put oil on frying pan", "Break the egg into a bowl and scramble it with a fork or whisk", "Add Salt to the egg", "Pour the egg into the frying pan", "Cook for 5 mins"])

    @staticmethod
    def BoiledEgg():
        return Recipe("Boiled Egg", ["Egg", "Water"], time=[0, 15, 0], temperature=97, serving=1, utensils=["Pot"], instructions=["Put 3 cups of water in pot", "Put egg into pot", "Let it boil for 15 mins"])

    def getTime(self):
        self.updateMutableParam()
        rTime = ""
        if self.hour != 0:
            rTime += f"{self.hour:02d}:"
        if self.minute != 0:
            rTime += f"{self.minute:02d}:"
        if self.second != 0:
            rTime += f"{self.second:02d}"
        return rTime

    def __str__(self):
        instruct = '\n\t* ' + '\n\t* '.join(self.instructions)
        recipeStr = f"Title:\t\t\t{self.title}\nIngredients:\t{', '.join(self.ingredients)}\nTime:\t\t\t{self.getTime()}\nServing:\t\t{self.serving}\nTemperature:\t{self.temperature}C\nUtensils:\t\t{''.join(self.utensils)}\nInstructions:\t{instruct}"
        return recipeStr

    def __repr__(self):
        return 'Recipe("Fried Fish", ["Fish", "Oil", "Salt"], time=[0,45,0], temperature=103, serving=2, utensils=["Frying pan", "Spatula"], instructions=["Cut fish in half", "Remove fish bones", "Cut into bite size pieces", "Sprinkle salt into fish", "Put oil in frying pan", "Put fish piece into the frying pan"])'


f = Recipe.ScrambledEgg()
print(f)
