
# Discord Leveling and Utility Bot

This Discord bot offers an engaging user experience with features like leveling, rewards, custom roles, and interactive commands. Perfect for communities seeking to gamify their interactions.

## Features
- **Leveling System**: Gain experience points (XP) for participating in chats and level up.
- **Rewards System**:
  - "Ballcoins" as an in-server currency.
  - Random loot drops with scrolls and boosts.
- **Custom Roles and Colors**: 
  - Members can create and manage custom roles.
  - Change role colors using pre-defined palettes.
- **Interactive Commands**:
  - Joke and roast commands for fun interactions.
  - Leaderboards for competitive engagement.
- **Daily Rewards**: Claim daily ballcoins with special bonuses for specific roles.
- **Membership Perks**: Exclusive benefits like additional scrolls, boosts, and role customizations.

## Requirements
- Python 3.7+
- Discord bot token
- SQLite for database management

### Python Libraries
Install the required libraries:
```bash
pip install discord.py aiohttp Pillow
```

## Setup Instructions
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. **Set Up the Bot**:
   - Replace `TOKEN` with your Discord bot token.
   - Replace `guild_id` with your server's ID.
3. **Run the Script**:
   ```bash
   python main.py
   ```

## Commands Overview
| Command           | Description                                                                                          |
|-------------------|------------------------------------------------------------------------------------------------------|
| `-level`          | Check your current level and XP.                                                                    |
| `-balls`          | Claim OG Baller rewards.                                                                            |
| `-ballcoin`       | View, earn, or spend ballcoins. Includes `-bc shop` for store items and `-bc buy <item>` to purchase.|
| `-membership`     | Manage membership perks, such as custom roles and palettes.                                         |
| `-joke`           | Generate a random joke using API.                                                                   |
| `-roast <user>`   | Roast a user with a randomly generated insult.                                                      |
| `-inventory`      | View your collected scrolls and boosts.                                                             |
| `-leaderboard`    | Display top users based on level and XP.                                                            |

## Database Schema
The bot uses an SQLite database (`levels.db`) with the following schema:
- **Table Name**: `levels`
- **Columns**:
  - `user_id`: User's Discord ID.
  - `level`: Current level of the user.
  - `exp`: Experience points.
  - `ballcoin`: User's in-server currency balance.
  - `custom_role_id`: ID of the user's custom role (if any).
  - `membership_date`: Start date of the user's membership.

## Customization
- Modify the leveling formula in `on_message()` for customized XP scaling.
- Update loot rewards and prices in the `-bc shop` and loot drop logic.

## Notes
- Ensure the bot has appropriate permissions (manage roles, send messages, etc.).
- Test the bot in a private server before deploying.

## License
This bot is provided as-is. Feel free to customize and adapt it to your needs.


