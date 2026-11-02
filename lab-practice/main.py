import sys
from coffee_maker import CoffeeMaker

 # Passes a prompt to the user and returns the user specified string.
def input_output(message):
    print(message)
    try:
        return_value = int(input())
        return return_value
    except ValueError:
        print("Error reading in integer value")
        main_menu()
    except Exception:
        print("Error reading in value")
        main_menu()

# Add inventory user interface that processes input.
def add_ingredients():
    coffee = input_output("\nPlease enter the units of coffee to add: ")
    milk = input_output("\nPlease enter the units of milk to add: ")

    try:
        coffee_maker.add_ingredients(coffee, milk)
        print("Ingredients successfully added")
    except Exception:
        print("Inventory was not added")
    finally:
        main_menu()

# Check ingredients user interface that processes input.
def check_ingredients():
    print(coffee_maker.check_ingredients())
    main_menu()

 # Make coffee user interface the processes input.
def make_coffee():
    print("1. Espresso")
    print("2. Latte")

    item = input_output("Please enter the item you wish to purchase")
    amt_paid = input_output("Please enter the amount you are paying")

    if 1 <= item <= 2:
        change = 0
        if item == 1:
            change = coffee_maker.make_espresso(amt_paid)
        elif item == 2:
            change = coffee_maker.make_latte(amt_paid)

        if change == amt_paid:
            print("Insufficient funds to purchase.")
        else:
            print("Thanks for purchasing")
        print(f"Your change is: {change}\n")
        main_menu()
    else:
        print("Please enter a number from 1 - 2")
        main_menu()

# Prints the main menu and handles user input for main menu commands.
def cleanup():
    coffee_maker.cleanup()
    print("Thanks for cleaning up the machine")
    main_menu()

# Prints the main menu and handles user input for main menu commands.
def main_menu():
    print("1. Make Coffee")
    print("2. Cleanup")
    print("3. Add ingredients")
    print("4. Display ingredients")
    print("0. Exit\n")

    user_input = input_output("Please press the number that corresponds to what you would like the coffee maker to do.")

    if 0 <= user_input <= 4:
        if user_input == 1:
            make_coffee()
        elif user_input == 2:
            cleanup()
        elif user_input == 3:
            add_ingredients()
        elif user_input == 4:
            check_ingredients()
        elif user_input == 0:
            sys.exit(0)
    else:
        print("Please enter a number from 0 - 4")
        main_menu()

def main():
    print("Welcome to the CoffeeMaker!\n")
    main_menu()

if __name__ == "__main__":
    coffee_maker = CoffeeMaker()
    main()


#this is test