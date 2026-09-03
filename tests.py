import pytest
import main as mp
from Game_items import Game, TYPE_DISCOUNT, TYPE_SAVED_DISCOUNT, TYPE_HYBRID_PRICE

TEST_FOLDER = "test_files/"

# Item lists
example_list_1 = [Game("Game 1", 10.0, 0), Game("Game 2", 20.0, 0.5), Game("Game 3", 30.0, 0.25)]
example_list_empty = []

# Tests regarding the main functions
def test_read_game_list():
    test_file = f"{TEST_FOLDER}example_list_1.txt"
    mp.read_game_list(test_file)
    recieved_list = mp.return_game_list()
    assert recieved_list == example_list_1, f"Expected {example_list_1}, but got {recieved_list}"
    mp.game_list_clear()

def test_game_list_clear():
    test_file = f"{TEST_FOLDER}example_list_1.txt"
    mp.read_game_list(test_file)
    mp.game_list_clear()
    recieved_list = mp.return_game_list()
    assert recieved_list == example_list_empty, f"Expected {example_list_empty}, but got {recieved_list}"

def test_read_game_list_empty():
    test_file = f"{TEST_FOLDER}example_list_empty.txt"
    mp.read_game_list(test_file)
    recieved_list = mp.return_game_list()
    assert recieved_list == example_list_empty, f"Expected {example_list_empty}, but got {recieved_list}"
    mp.game_list_clear()

def test_read_game_list_nonexistent():
    test_file = f"{TEST_FOLDER}nonexistent_file.txt"
    mp.read_game_list(test_file)
    recieved_list = mp.return_game_list()
    assert recieved_list == example_list_empty, f"Expected {example_list_empty}, but got {recieved_list}"
    mp.game_list_clear()

def test_save_game_list():
    test_file = f"{TEST_FOLDER}example_list_1.txt"
    mp.read_game_list(test_file)
    original_list = mp.return_game_list()
    mp.save_game_list(f"{TEST_FOLDER}test_save.txt")
    mp.game_list_clear()
    mp.read_game_list(f"{TEST_FOLDER}test_save.txt")
    recieved_list = mp.return_game_list()
    assert recieved_list == original_list, f"Expected {original_list}, but got {recieved_list}"
    mp.game_list_clear()

# Tests regarding the list creations
def test_generation_of_lists():
    base_lists_files = ["example_list_empty.txt", # 1
                        "example_list_single.txt", # 2
                        "example_list_single_discount.txt", # 3
                        "example_list_2.txt", # 4
                        "example_list_3.txt", # 5
                        "example_list_4.txt", # 6
                        "example_list_5.txt"] # 7
    results_list = [[], # 1
                    [Game("Game 1", 10.0, 0)], # 2
                    [Game("Game 1", 10.0, 0.5)], # 3
                    [Game("Game 2", 3.0, 0.1)], # 4
                    [Game("Game 1", 2.0, 0.1), Game("Game 2", 3.0, 0.1)], # 5
                    [Game("Game 2", 6.0, 0.5)], # 6
                    [Game("Game 1", 4.0, 0.5), Game("Game 3", 2.5, 0.2)], # 7
                    [Game("Game 1", 10.0, 0.6)], # 8
                    [Game("Game 2", 3.0, 0.5), Game("Game 3", 3.0, 0.5)], # 9
                    [Game("Game 1", 10.0, 0.9), Game("Game 2", 8.0, 0.8), Game("Game 3", 6.0, 0.5), Game("Game 4", 16.0, 0.3), Game("Game 5", 9.0, 0.0)] # 10
                    ]
    test_list = [{"games_file": 1, "budget": 10, "type": TYPE_DISCOUNT, "expected_results": 1, "expected_budget": 0, "expected_score":0}, # 1
                 {"games_file": 2, "budget": 5, "type": TYPE_DISCOUNT, "expected_results": 1, "expected_budget": 0, "expected_score":0}, # 2
                 {"games_file": 2, "budget": 12, "type": TYPE_DISCOUNT, "expected_results": 2, "expected_budget": 10, "expected_score":0.01}, # 3
                 {"games_file": 3, "budget": 3, "type": TYPE_DISCOUNT, "expected_results": 1, "expected_budget": 0, "expected_score":0}, # 4
                 {"games_file": 3, "budget": 6, "type": TYPE_DISCOUNT, "expected_results": 3, "expected_budget": 5, "expected_score":0.5}, # 5
                 {"games_file": 4, "budget": 4, "type": TYPE_DISCOUNT, "expected_results": 4, "expected_budget": 2.7, "expected_score":0.1}, # 6
                 {"games_file": 4, "budget": 4, "type": TYPE_SAVED_DISCOUNT, "expected_results": 4, "expected_budget": 2.7, "expected_score":0.3}, # 7
                 {"games_file": 4, "budget": 4, "type": TYPE_HYBRID_PRICE, "expected_results": 4, "expected_budget": 2.7, "expected_score":0.03}, # 8
                 {"games_file": 4, "budget": 5, "type": TYPE_DISCOUNT, "expected_results": 5, "expected_budget": 4.5, "expected_score":0.2}, # 9
                 {"games_file": 5, "budget": 4, "type": TYPE_DISCOUNT, "expected_results": 7, "expected_budget": 4.0, "expected_score":0.7}, # 10
                 {"games_file": 5, "budget": 4, "type": TYPE_SAVED_DISCOUNT, "expected_results": 6, "expected_budget": 3.0, "expected_score":3.0}, # 11
                 {"games_file": 5, "budget": 4, "type": TYPE_HYBRID_PRICE, "expected_results": 6, "expected_budget": 3.0, "expected_score":1.5}, # 12
                 {"games_file": 6, "budget": 5, "type": TYPE_DISCOUNT, "expected_results": 9, "expected_budget": 3.0, "expected_score":1.0}, # 13
                 {"games_file": 6, "budget": 5, "type": TYPE_SAVED_DISCOUNT, "expected_results": 8, "expected_budget": 4.0, "expected_score":6.0}, # 14
                 {"games_file": 6, "budget": 5, "type": TYPE_HYBRID_PRICE, "expected_results": 8, "expected_budget": 4.0, "expected_score":3.6}, # 15
                 {"games_file": 7, "budget": 100, "type": TYPE_DISCOUNT, "expected_results": 10, "expected_budget": 25.8, "expected_score":2.51}] # 16
    mp.game_list_clear()
    for test_case in test_list:
        # print(f"Running test case: {test_case}")
        test_file = f"{TEST_FOLDER}{base_lists_files[test_case['games_file'] - 1]}"
        mp.read_game_list(test_file)
        generated_list, total_budget, total_score = mp.create_list(test_case['budget'], test_case['type'])
        # print(f"Generated list: {generated_list}")
        # print(f"Generated list: {results_list[test_case['expected_results'] - 1]}")
        assert generated_list == results_list[test_case['expected_results'] - 1], f"Expected {results_list[test_case['expected_results'] - 1]} games, but got {generated_list}"
        assert total_budget == pytest.approx(test_case['expected_budget'], rel=1e-2), f"Expected budget {test_case['expected_budget']}, but got {total_budget}"
        assert total_score == pytest.approx(test_case['expected_score'], rel=1e-2), f"Expected score {test_case['expected_score']}, but got {total_score}"
        mp.game_list_clear()