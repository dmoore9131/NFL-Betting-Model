<img>![futuristic-football-soccer-player-with-glowing-lights](https://github.com/user-attachments/assets/958a9409-57a9-45eb-bd3f-d3817ef4345b)<img>


# NFL Betting Model Project

## Overview

The NFL Betting Model Project aims to analyze and provide insights into NFL games, focusing on player performance, injury reports, and fantasy football decisions. The project utilizes historical game data, player statistics, and injury reports to offer recommendations on fantasy starts/sits and predict key player performance.

## Features

- **Historical Game Data**: Provides historical game scores and stats.
- **Live Game Scores**: Displays current scores of ongoing games.
- **Player Statistics**: Includes detailed statistics for players, such as yards, touchdowns, and PFF grades.
- **Injury Reports**: Lists player injuries and their statuses.
- **Fantasy Draft Decisions**: Offers recommendations on which players to start or sit based on their injury status and performance.
- **Most Targets Analysis**: Identifies players likely to receive the most targets based on their team’s offensive strategies and current injuries.
  <img>![download](https://github.com/user-attachments/assets/25887ef8-c4b5-4148-8b8d-b84e7edeb4ad)
<img>
![download (1)](https://github.com/user-attachments/assets/af69571f-cb3c-44be-8173-8466b01bd9da) <img> 


## Data Sources

- **Historical Game Data**: Simulated for demonstration purposes.
- **Player Statistics**: Includes example data with player performance metrics and PFF grades.
- **Injury Reports**: Contains simulated injury data for players.
- <img width="716" alt="Screenshot 2024-09-06 173141" src="https://github.com/user-attachments/assets/ec86338c-6f39-4f04-8f29-00b9377089de"img>


## Setup

1. **Install Dependencies**:
   Ensure you have Python and the required libraries installed. You can install the necessary packages using pip:

   ```bash
   pip install pandas requests
   ```

2. **Code Integration**:
   The main code file includes functions to fetch and process game data. You can extend the data fetching functions to include real-time data from APIs if available.

3. **Running the Code**:
   Use the following code to fetch and display game data:

   ```python
   game_data = fetch_game_data(1)
   print(game_data['Historical'])
   print(game_data['Live'])
   print(game_data['Player Stats'])
   print(game_data['Injury Reports'])
   print("Fantasy Draft Decisions:")
   print(game_data['Fantasy Draft Decisions'])
   print("Most Targets Packers:", game_data['Most Targets Packers'])
   print("Most Targets Eagles:", game_data['Most Targets Eagles'])
   ```

## Features in Development

- **Live Injury Updates**: Integration with live injury update APIs.
- **Advanced Fantasy Recommendations**: Incorporate more advanced algorithms for fantasy football recommendations.
- **Enhanced Player Target Analysis**: Refine logic for predicting player targets based on defensive strategies and player matchups.

## Contribution

Contributions are welcome! If you have suggestions or improvements, please create a pull request or open an issue.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, please contact [dominiquetucker994@gmail.com].

---

Feel free to adjust any sections to better fit the specifics of your project or your personal preferences.
