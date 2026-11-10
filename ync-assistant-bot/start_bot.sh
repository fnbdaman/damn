#!/bin/bash
# YNC Assistant - Bot Startup Script
# This script starts the YNC Telegram bot with all configurations

echo "=========================================="
echo "  YNC Assistant Bot - Startup Script"
echo "=========================================="
echo ""

# Change to project directory
cd "$(dirname "$0")"

echo "Step 1: Checking Environment Configuration..."
if [ -f ".env" ]; then
    echo "✓ .env file found"
    source .env
else
    echo "✗ .env file not found"
    exit 1
fi

echo ""
echo "Step 2: Verifying Dependencies..."
python3 -c "import telegram, anthropic, dotenv; print('✓ All required modules installed')"

echo ""
echo "Step 3: Starting YNC Bot..."
echo "Bot will connect to Telegram and start monitoring messages..."

# Start the bot
python3 bot.py

echo ""
echo "=========================================="
echo "  Bot is now running!"
echo "=========================================="
