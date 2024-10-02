# Discord to Telegram Message Forwarder

## Introduction

This project is a **Discord to Telegram message forwarder**. It allows forwarding messages sent by specific users or all users from a Discord channel to a Telegram chat. It is highly configurable and utilizes a MySQL database to manage message forwarding configurations.

## Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Slash Commands](#slash-commands)
- [Troubleshooting](#troubleshooting)

## Installation

To set up this message forwarder, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/johnmalek312/DiscordToTelegram.git
   cd DiscordToTelegram

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up a MySQL database, following the schema provided in the [Database Setup](#database-setup) section.

4. Set up the configuration by filling out the `.env` file (details below).

## Configuration

Create a `.env` file in the project root directory with the following environment variables:

```
DISCORD_TOKEN=your_discord_bot_token
TELEGRAM_TOKEN=your_telegram_bot_token
MYSQL_HOST=your_mysql_host
MYSQL_USER=your_mysql_user
MYSQL_PASSWORD=your_mysql_password
MYSQL_DATABASE=your_database_name
```

- `DISCORD_TOKEN`: Your Discord bot token.
- `TELEGRAM_TOKEN`: Your Telegram bot token.
- `MYSQL_HOST`: The hostname of your MySQL server.
- `MYSQL_USER`: The username for MySQL access.
- `MYSQL_PASSWORD`: The password for the MySQL user.
- `MYSQL_DATABASE`: The name of your MySQL database.

## Database Setup

You need to set up a MySQL database and create the following table to store the forwarding configuration:

```sql
CREATE TABLE forwarder (
    id INT NOT NULL PRIMARY KEY,  
    discord BIGINT NOT NULL,      
    telegram BIGINT NOT NULL,     
    header VARCHAR(255) NOT NULL, 
    whitelist INT DEFAULT NULL    
);
```

- `id`: Unique identifier for each forwarding configuration.
- `discord`: Discord user/channel ID.
- `telegram`: Telegram chat ID.
- `header`: A message header to include in forwarded messages.
- `whitelist`: Optional user whitelist for restricting forwarding.

## Usage

1. Start the bot by running the following command:

   ```bash
   python main.py
   ```

2. The bot will listen to messages in Discord and forward them to the specified Telegram chats based on the configuration stored in the MySQL database.

3. You can customize which users' messages are forwarded by modifying the `whitelist` column in the `forwarder` table.

## Features

- Forward messages from Discord to Telegram.
- Optionally forward messages only from specific users.
- Flexible configuration using a MySQL database.
- Automatically reconnects to the database if the connection is lost.
- Manage channel forwarding from Discord to Telegram effortlessly using simple discord bot commands.
## Slash Commands

Once the bot is running, you need to sync the slash commands in your Discord server. Follow these steps:

1. In your Discord server, with admin permissions, type:

   ```
   .sync
   ```

2. This will enable slash commands such as `/add`, `/list`, and others, which will be described in Discord once synced.

These commands allow you to manage the bot more easily, providing more control over what and how messages are forwarded.

## Dependencies

- Python 3.8+
- [discord.py](https://discordpy.readthedocs.io/en/stable/)
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/)
- [MySQL Connector](https://dev.mysql.com/doc/connector-python/en/)

To install dependencies, simply run:

```bash
pip install -r requirements.txt
```

## Troubleshooting

- **MySQL Connection Issues**: Ensure that the MySQL credentials in the `.env` file are correct and that your database server is running.
- **Discord Bot Not Responding**: Make sure the bot has the necessary permissions in the Discord server, and that the `DISCORD_TOKEN` is valid.
- **Telegram Messages Not Forwarding**: Verify that the Telegram bot has access to the target chat, and the `TELEGRAM_TOKEN` is correctly set in the `.env` file.

