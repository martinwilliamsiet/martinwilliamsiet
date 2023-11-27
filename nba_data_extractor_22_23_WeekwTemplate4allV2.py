import csv
from bs4 import BeautifulSoup

def process_nba_html(file_path):
    # Read the HTML content from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Parse the HTML content
    soup = BeautifulSoup(content, 'lxml')
    
    # Initialize a list to store game data
    games = []
    
    # Extract game details
    for game in soup.find_all("a", class_="match-url match-url--flex"):
        # Extracting team names
        teams = [team.get_text(strip=True) for team in game.find_all("div", class_="match-team__name")]
        
        # Extracting scores
        scores = [int(score.get_text(strip=True)) for score in game.find_all("span", class_="match-score-result__score")]
        
        # Determine if the game went to overtime and adjust scores
        if 'OT' in game.find("div", class_="match-status").get_text():
            # Assuming the last two scores are the total scores, remove them
            total_scores = scores[-2:]
            quarter_scores = scores[:-2]
            
            # Add OT scores to the 4th quarter scores
            quarter_scores[6] += sum(quarter_scores[8:])
            quarter_scores[7] += sum(quarter_scores[9::2])
            
            # Use the adjusted quarter scores and the total scores
            scores = quarter_scores[:8] + total_scores
        
        # Append the extracted data to the games list
        games.append(teams + scores)
    
    # Write data to a CSV file
    with open('nba_season_output.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        #old writer.writerow(['AwayTeam', 'HomeTeam', 'AwayQ1', 'HomeQ1', 'AwayQ2', 'HomeQ2', 'AwayQ3', 'HomeQ3', 'AwayQ4', 'HomeQ4', 'AwayTotal', 'HomeTotal'])
        #new column header writing below to try to fix alternating corresponding column name issue
        writer.writerow(['HomeTeam', 'AwayTeam', 'HomeQ1', 'AwayQ1', 'HomeQ2', 'AwayQ2', 'HomeQ3', 'AwayQ3', 'HomeQ4', 'AwayQ4', 'HomeTotal', 'AwayTotal'])
        writer.writerows(games)
    
    print("Data saved to nba_season_output.csv!")
    # Open the CSV file automatically if on Windows (requires os module)
    import os
    os.startfile('nba_season_output.csv')

# Call the function to process the file
process_nba_html('TEMP.txt')
