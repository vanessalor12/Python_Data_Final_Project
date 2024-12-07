# ui.py
# Author: Vanessa Lor
# Date: 5/15/2024

# Import necessary modules
import sqlite3
import db
from business import Player

# Define functions to display UI elements and handle user inputs
def display_separator():
    print("=" * 90)

def display_title():
    title = "WEEKLY BOWLING SCORES"
    spaces = (80 - len(title)) // 2
    print(" " * spaces + title)

def display_menu():
    print("1. View scores")
    print("2. Add a player")
    print("3. Add score to a player")
    print("4. Edit a player's score")
    print("5. Delete a player")
    print("6. Exit")
    print()

# Define functions to interact with the database
def view_scores():
    conn = sqlite3.connect('bowling_scores.db')
    c = conn.cursor()
    c.execute('''SELECT id, first_name, last_name, score1, score2, score3, score4, avg_score
                 FROM scores''')
    rows = c.fetchall()
    
    if not rows:
        print("There are currently no players in the lineup.")
    else:
        print(f"{'Player ID':<10}{'First Name':<15}{'Last Name':<15}"
              f"{'Score1':<10}{'Score2':<10}{'Score3':<10}{'Score4':<10}{'Avg Score':<10}")
        print("-" * 90)
        for row in rows:
            player_id, first_name, last_name, score1, score2, score3, score4, avg_score = row
            score1 = "" if score1 is None else score1
            score2 = "" if score2 is None else score2
            score3 = "" if score3 is None else score3
            score4 = "" if score4 is None else score4
            avg_score = "" if avg_score is None else round(avg_score, 1)
            print(f"{player_id:<10}{first_name:<15}{last_name:<15}"
                  f"{score1:<10}{score2:<10}{score3:<10}{score4:<10}{avg_score:<10}")
    
    conn.close()
    print()

def add_player():
    first_name = input("Enter First Name: ")
    last_name = input("Enter Last Name: ")
    db.insert_player(first_name, last_name)
    print("Player added successfully.")
    print()

def add_score():
    while True:
        player_id = int(input("Enter Player ID: "))
        # Check if the Player ID exists
        conn = sqlite3.connect('bowling_scores.db')
        c = conn.cursor()
        c.execute('''SELECT id FROM scores WHERE id = ?''', (player_id,))
        if c.fetchone():
            break
        else:
            print("Invalid input. Player ID does not exist. Please try again.")
            conn.close()

    valid_columns = ['score1', 'score2', 'score3', 'score4']
    while True:
        column = input("Enter score column (score1, score2, score3, or score4): ")
        if column in valid_columns:
            break
        else:
            print("Invalid input. Please enter one of the following options: score1, score2, score3, or score4.")
    
    # Check if the column already has a score
    c.execute(f'''SELECT {column} FROM scores WHERE id = ?''', (player_id,))
    existing_score = c.fetchone()[0]
    if existing_score is not None:
        print(f"Score already exists in {column}. Please enter menu option 4 to update the score.")
        conn.close()
        return
    
    new_score = int(input("Enter new score: "))
    db.update_score(player_id, column, new_score)
    print("Score updated successfully.")

    # Calculate average score
    c.execute('''SELECT score1, score2, score3, score4 FROM scores WHERE id = ?''', (player_id,))
    scores = c.fetchone()
    num_scores = sum(1 for score in scores if score is not None)
    total_score = sum(score for score in scores if score is not None)
    
    # Calculate average score based on available scores
    avg_score = total_score / num_scores if num_scores > 0 else None
    
    c.execute('''UPDATE scores SET avg_score = ? WHERE id = ?''', (avg_score, player_id))
    conn.commit()  # Commit changes to the database
    conn.close()
    print("Average score updated successfully.")
    print()

def edit_player():
    # Fetch available Player IDs
    conn = sqlite3.connect('bowling_scores.db')
    c = conn.cursor()
    c.execute('''SELECT id FROM scores''')
    available_player_ids = [str(row[0]) for row in c.fetchall()]
    conn.close()

    # Ensure valid Player ID is chosen
    while True:
        player_id = input("Enter Player ID to edit: ")
        if player_id in available_player_ids:
            player_id = int(player_id)
            break
        else:
            print("Invalid input. Player ID does not exist. Please try again.")

    valid_columns = ['score1', 'score2', 'score3', 'score4']
    while True:
        column = input("Enter score column to edit (score1, score2, score3, or score4): ")
        if column in valid_columns:
            break
        else:
            print("Invalid input. Please enter one of the following options: score1, score2, score3, or score4.")
    
    # Check if the column already has a score
    conn = sqlite3.connect('bowling_scores.db')
    c = conn.cursor()
    c.execute(f'''SELECT {column} FROM scores WHERE id = ?''', (player_id,))
    existing_score = c.fetchone()[0]
    conn.close()
    
    if existing_score is None:
        print(f"There is no data to edit in {column}. Please use menu option 3 to add a score to the player.")
        return

    new_score = int(input("Enter new score: "))
    db.update_score(player_id, column, new_score)
    print("Score updated successfully.")

    # Calculate average score
    conn = sqlite3.connect('bowling_scores.db')
    c = conn.cursor()
    c.execute('''SELECT score1, score2, score3, score4 FROM scores WHERE id = ?''', (player_id,))
    scores = c.fetchone()
    num_scores = sum(1 for score in scores if score is not None)
    total_score = sum(score for score in scores if score is not None)
    
    # Calculate average score based on available scores
    avg_score = total_score / num_scores if num_scores > 0 else None
    
    c.execute('''UPDATE scores SET avg_score = ? WHERE id = ?''', (avg_score, player_id))
    conn.commit()  
    conn.close()
    print("Average score updated successfully.")
    print()

def delete_player():
    # Fetch available Player IDs
    conn = sqlite3.connect('bowling_scores.db')
    c = conn.cursor()
    c.execute('''SELECT id FROM scores''')
    available_player_ids = [str(row[0]) for row in c.fetchall()]
    conn.close()

    # Ensure valid Player ID is chosen
    while True:
        player_id = input("Enter Player ID to delete: ")
        if player_id in available_player_ids:
            player_id = int(player_id)
            break
        else:
            print("Invalid input. Player ID does not exist. Please try again.")

    # Delete player
    db.delete_player(player_id)
    print("Player deleted successfully.")
    print()

# Define other functions for adding scores, editing players, deleting players, etc.
def main():
    display_separator()
    display_title()
    while True:
        display_separator()
        print()
        display_menu()
        choice = input("Enter your choice: ")
        
        if choice == '1':
            print()
            view_scores()
        elif choice == '2':
            print()
            add_player()
        elif choice == '3':
            print()
            add_score()
        elif choice == '4':
            print()
            edit_player()
        elif choice == '5':
            print()
            delete_player()
        elif choice == '6':
            print()
            print("Exiting program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
