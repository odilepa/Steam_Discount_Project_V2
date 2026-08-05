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

def read_game_list():
    try:
        with open("game_list.txt", "r") as file:
            raw_list = file.read().strip("###------###\n").split("###------###\n###------###\n")
            # print(raw_list)
            if raw_list == ['']:
                print("Empty game list found. Starting with an empty list.")
                return
            for raw_item in raw_list:
                lines = raw_item.strip().split("\n")
                # print(lines)
                title = lines[0].split(": ")[1].strip(",")
                original_price = lines[1].split(": ")[1].strip("$,")
                discount = lines[2].split(": ")[1].strip("%")
                game = Game(title, float(original_price), float(discount))
                game_list.append(game)
    except FileNotFoundError:
        print("No previous game list found. Starting with an empty list.")
    except Exception:
        print("An error occurred while reading the game list. Starting with an empty list.")

def save_game_list():
    with open("game_list.txt", "w") as file:
        for game in game_list:
            file.write(str(game) + "\n")

def booting():
    print("Booting up system...\nReading previous list of games...\n")
    read_game_list()
    print(f"""
Welcome to the Steam Discount Calculator v2!
In this program, you can calculate the optimal amount of games to buy based on your budget, with multiple types of list calculation available.
This version still requires to manually input the games, their original price and the discount amount, further versions will automate this process.
{COMMAND_LIST_SHOWCASE}
""")


def add_item():
    title = input("Enter the title of the game: ")
    original_price = float(input("Enter the original price of the game: "))
    discount = float(input("Enter the discount (as a decimal or percentage): "))
    
    game = Game(title, original_price, discount)
    print(game)
    
    game_list.append(game)

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
            print("This feature is not yet implemented")
        
        ### Clear ###
        # Clear the current list of games
        elif user_input == 'clear':
            if input("The following command cannot be undone, do you wish to proceed? (any input containing 'y' for yes, anything else for no): ").lower().find('y') != -1:
                game_list.clear()
                print("Game list cleared.")
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