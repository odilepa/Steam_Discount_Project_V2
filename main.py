from Game_items import Game, TYPE_DISCOUNT, TYPE_SAVED_DISCOUNT, TYPE_HYBRID_PRICE

COMMAND_LIST_SHOWCASE = """
The commands are as followed:
- 'help': Show this list of commands
- 'add': Add a new game to the list
- 'remove': Remove a game from the list
- 'show': List all the games in the list
- 'list': Generate the list of games based on discount and budget
- 'clear': Clear the current list of games
- 'save': Save the current list of games (if the program exits naturaly this should be done automatically, this exists as a safeguard)
- 'quit': Exit the program
Some extra inputs may be required for some commands, these will be prompted when needed.
"""

game_list = []

# TEST & DEBUG FUNCTION
def return_game_list():
    return game_list

# Attempts to read and generate a list based on the given list of games
def read_game_list(filename = "game_list.txt"):
    try:
        with open(filename, "r") as file:
            # Read and seperate the file into a list of games as their string forms
            raw_list = file.read().strip("###------###\n").split("###------###\n###------###\n")
            # If list is empty, return an empty list
            if raw_list == ['']:
                print("Empty game list found. Starting with an empty list.")
                return
            # Iterate trough the list of game strings, and add each one to the game list as a Game object
            for raw_item in raw_list:
                lines = raw_item.strip().split("\n")
                # print(lines)
                title = lines[0].split(": ")[1].strip(",")
                original_price = lines[1].split(": ")[1].strip("$,")
                discount = lines[2].split(": ")[1].strip("%")
                game = Game(title, float(original_price), float(discount))
                game_list.append(game)
    # If the file is not found, print the message and start with an empty list
    except FileNotFoundError:
        print("No previous game list found. Starting with an empty list.")
    # If an unknown error occurs, print the message and start with an empty list
    except Exception:
        print("An unknown error occurred while reading the game list. Starting with an empty list.")

# Saves the current list of games based on a name
def save_game_list(filename = "game_list.txt"):
    with open(filename, "w") as file:
        for game in game_list:
            file.write(str(game) + "\n")

# Booting up sequence
def booting():
    print("Booting up system...\nReading previous list of games...\n")
    read_game_list()
    print(f"""
Welcome to the Steam Discount Calculator v2!
In this program, you can calculate the optimal amount of games to buy based on your budget, with multiple types of list calculation available.
This version still requires to manually input the games, their original price and the discount amount, further versions will automate this process.
{COMMAND_LIST_SHOWCASE}
""")

# Adds an Item to the list of games
def add_item():
    title = input("Enter the title of the game: ")
    original_price = float(input("Enter the original price of the game: "))
    discount = float(input("Enter the discount (as a decimal or percentage): "))
    
    game = Game(title, original_price, discount)
    print(game)
    
    game_list.append(game)

# Organizes the list by price, from highest to lowest
def order_list_by_price():
    return sorted(game_list, key=lambda game: game.return_discounted_price(), reverse=True)

# Organizes the list by score, from highest to lowest
def order_list_by_score(type_score):
    if type_score == TYPE_SAVED_DISCOUNT:
        return sorted(game_list, key=lambda game: game.return_saved_discount(), reverse=True)
    elif type_score == TYPE_HYBRID_PRICE:
        return sorted(game_list, key=lambda game: game.return_hybrid_price(), reverse=True)
    else:
        return sorted(game_list, key=lambda game: game.return_discount(), reverse=True)

# Iterates through the list of games, and selects the nex item based on the remaining budget an type of score, until the end where it return the full list and score
def list_iteration_v1(remaining_budget, ordered_list, dna_list, iteration_index, current_score, type_list):
    
    # if reached end of list, return curent dna and score
    if iteration_index >= len(ordered_list):
        final_dna = dna_list.copy()
        return final_dna, current_score
    
    # Check if there is budget fot this game
    if remaining_budget >= ordered_list[iteration_index].return_discounted_price():
        # Assume yes
        new_remaining_budget = remaining_budget - ordered_list[iteration_index].return_discounted_price()
        dna_list[iteration_index] = 1
        new_current_score = current_score + ordered_list[iteration_index].score_self(type_list)
        accepted_dna, accepted_score = list_iteration_v1(new_remaining_budget, ordered_list, dna_list, iteration_index + 1, new_current_score, type_list)
        
        # Assume no
        dna_list[iteration_index] = 0
        rejected_dna, rejected_score = list_iteration_v1(remaining_budget, ordered_list, dna_list, iteration_index + 1, current_score, type_list)
    
        # Compare the two scores and return the better one
        if accepted_score > rejected_score:
            return accepted_dna, accepted_score
        else:
            return rejected_dna, rejected_score
        
    else:
        # Cannot afford this game, move to the next one
        dna_list[iteration_index] = 0
        return list_iteration_v1(remaining_budget, ordered_list, dna_list, iteration_index + 1, current_score, type_list)
    
# Creates the list of games based on the iteration function
def create_list(budget, type_list):
    generated_list = []
    total_cost = 0
    
    # Generate a new ordered list based on the type of evaluation
    ordered_list = order_list_by_score(type_list)
    dna_list = [0 for _ in range(len(ordered_list))]  # Initialize a DNA list to track selected games
    
    # Iterate through the ordered list and add games to the generated list until the budget is reached
    final_dna, total_score = list_iteration_v1(budget, ordered_list, dna_list, 0, 0, type_list)
    
    # Generate the final list of games based on the selected DNA
    for i in range(len(final_dna)):
        if final_dna[i] == 1:
            game = ordered_list[i]
            generated_list.append(game)
            total_cost += game.return_discounted_price()
    
    # Return the ordered list of games and total score based on the type of evaluation
    return generated_list, total_cost, total_score

def game_list_clear():
    game_list.clear()
    print("Game list cleared.")

def main_loop():
    booting()
    quiting = False
    
    while not quiting:
        user_input = input("Enter a command (type 'quit' to exit): ").lower()
        
        ### Help ###
        # Ask for help with the commands
        if user_input == 'help':
            print(COMMAND_LIST_SHOWCASE)
        
        ### Add ###
        # Add a new game to the list
        elif user_input == 'add':
            add_item()
        
        ### Remove ###
        # Remove a game from the list
        elif user_input == 'remove':
            title_to_remove = input("Enter the title of the game to remove: ")
            game_to_remove = next((game for game in game_list if game.return_title() == title_to_remove), None)
            if game_to_remove:
                game_list.remove(game_to_remove)
                print(f"Removed {title_to_remove} from the list.")
            else:
                print(f"No game found with the title: {title_to_remove}")
        
        ### Show ###
        # Show the list of games
        elif user_input == 'show':
            if not game_list:
                print("No games in the list.")
            else:
                for game in game_list:
                    print(game)
        
        ### List ###
        # Generate the list of games based on discount and budget
        elif user_input == 'list':
            
            # Get budget from user
            budget_str = ""
            while not budget_str.isnumeric():
                budget_str = input("Enter your budget: ")
            budget = float(budget_str)
            
            # Get type of list from user
            type_list_str = ""
            type_list = 0
            while not type_list_str.isdecimal() and type_list not in [1, 2, 3]:
                type_list_str = input("Enter the type of evaluation to apply (1 for pure discount, 2 for discounted price, 3 for a hybrid approach): ")
                if type_list_str.isdecimal():
                    type_list = float(type_list_str)
            
            # Generating list based on budget and type
            print(f"Generating list based on budget of {budget}$ and type {type_list}...")
            generated_list, total_cost, total_score = create_list(budget, type_list)
            print(f"Generated list with total cost of {total_cost}$ and total score of {total_score}.")
            for game in generated_list:
                print(game)
            if generated_list:
                print(f"Total cost of selected games: {total_cost:.2f}$")
                if input("Do you want to save this generated list to a file? (y/n): ").lower().find('y') != -1:
                    filename = input("Enter the filename to save the generated list (default is 'generated_list.txt'): ")
                    if not filename:
                        filename = "generated_list.txt"
                    save_game_list(filename)
                    print(f"Generated list saved to {filename}.")
        
        ### Clear ###
        # Clear the current list of games
        elif user_input == 'clear':
            if input("The following command cannot be undone, do you wish to proceed? (any input containing 'y' for yes, anything else for no): ").lower().find('y') != -1:
                game_list_clear()
            else:
                print("Clear command aborted.")
        
        ### Save ###
        # Save the current list of games to a file
        elif user_input == 'save':
            save_game_list()
            print("Game list saved successfully.")
        
        ### Quit ###
        # Save the list of games to a file and quit the program
        elif user_input == 'quit':
            save_game_list()
            quiting = True
            print("Exiting the program. Goodbye!")
        
        ### Invalid command ###
        else:
            print(f"invalid command: {user_input}\nInput 'help' for the list of valid commands.")

if __name__ == "__main__":
    main_loop()