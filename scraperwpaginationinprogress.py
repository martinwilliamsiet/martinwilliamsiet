import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Initialize the Selenium WebDriver
driver = webdriver.Chrome()  # or any other browser driver
# Wait and click the dropdown to select the season
dropdown_button = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "dropdown__toggle"))
)
dropdown_button.click()

# Wait and select the 22/23 season
season_22_23 = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located((By.XPATH, "//div[contains(text(), '22/23')]"))
)
season_22_23.click()

# Now the page is on the 22/23 NHL season, you can continue with the scraping logic

for week in range(1, 26):  # Loop through the first 25 weeks
    # Load the page content into BeautifulSoup
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Call your existing scraping function here
    scraped_data = process_NHL_html(soup)

    # Check if there is a "next" button and if it is active
    next_button = driver.find_element_by_class_name("ml-pagination__btn--next")
    if not next_button or 'inactive-class-name' in next_button.get_attribute('class'):
        break  # Exit the loop if no "next" button or if it is inactive

    # Click the next button to go to the next page
    next_button.click()

# Close the WebDriver after scraping
driver.quit()

def process_NHL_html(file_path): 
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
    with open('NHL_season_output.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        #old writer.writerow(['AwayTeam', 'HomeTeam', 'AwayQ1', 'HomeQ1', 'AwayQ2', 'HomeQ2', 'AwayQ3', 'HomeQ3', 'AwayQ4', 'HomeQ4', 'AwayTotal', 'HomeTotal'])
        #new column header writing below to try to fix alternating corresponding column name issue
        writer.writerow(['HomeTeam', 'AwayTeam', 'HomeQ1', 'AwayQ1', 'HomeQ2', 'AwayQ2', 'HomeQ3', 'AwayQ3', 'HomeQ4', 'AwayQ4', 'HomeTotal', 'AwayTotal'])
        writer.writerows(games)
    
    print("Data saved to NHL_season_output.csv!")
    # Open the CSV file automatically if on Windows (requires os module)
    import os
    os.startfile('NHL_season_output.csv')

# Call the function to process the file
process_NHL_html('TEMP.txt')
