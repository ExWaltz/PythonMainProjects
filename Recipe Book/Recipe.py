

class Recipe:
    """ title: Title of recipe
        ingredients: Must be LIST; ingredients of recipe
        time: Must be LIST; format:[00:00:00]
            * wiil override hour,minute and second
        hour: hours to finish the recipe
        minute: minutes to finish the recipe
        second: seconds to finish the recipe
        temperature: celcius; temperature recommended for the recipe"""

    def __init__(self, title, ingredients=None, time=None, hour=0, minute=0, second=0, temperature=100):
        self.title = title
        self.ingredients = ingredients
        self.time = time
        self.hour = int(hour)
        self.minute = int(minute)
        self.second = int(second)
        self.temperature = str(temperature)

        if self.ingredients is None:
            self.ingredients = []
        if self.time is not None:
            self.hour, self.minute, self.second = self.time
