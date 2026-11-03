class CoffeeMaker:
    def __init__(self):
        self.coffee = 0
        self.milk = 0

    # Returns the current number of coffee units in the coffee maker.
    def get_coffee(self):
        return self.coffee

    # Returns the current number of milk units in the coffee maker.
    def get_milk(self):
        return self.milk

    # Returns a string describing the current contents of the inventory.
    def check_ingredients(self):
        # TODO: code this method
        return "Not yet implemented\n"

    # Cleanup coffee maker emptying all its content.
    def cleanup(self):
        # TODO: code this method
        pass

    # Adds ingredients to the coffee maker
    def add_ingredients(self, amt_coffee, amt_milk):
        # TODO: code this method
        pass

    # Make an espresso and return the change, or the user's money if the espresso cannot be made.
    # An espresso uses one unit of coffee and costs one pound.
    def make_espresso(self, amt_paid):
        # TODO: code this method
        return -1

    # Make a latte and return the change, or  the user's money if the latte cannot be made.
    # A latte uses two units of coffee and one unit of milk.
    def make_latte(self, amt_paid):
        # TODO: code this method
        return -1