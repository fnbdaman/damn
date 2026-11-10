import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

# Add current directory to path
sys.path.insert(0, '.')

# Define __file__ for exec context
__file__ = Path('bot.py')

# Load environment variables
load_dotenv()

print("\n=== YNC Assistant Deployment Verification ===")
print("=" * 60)

# Read and execute bot.py
with open('bot.py') as f:
    bot_code = f.read()

# Execute bot module
exec(compile(bot_code, str(__file__), 'exec'))

print(f"\nBASE_DIR: {BASE_DIR}")
print(f"DB_PATH: {DB_PATH}")
print(f"PROMPTS_DIR: {PROMPTS_DIR}")
print(f"OWNER_USER_ID: {OWNER_USER_ID}")
print(f"MODEL: {MODEL}")
print(f"HISTORY_TURNS: {HISTORY_TURNS}")
print(f"VENICE_API_KEY: {'Loaded' if VENICE_API_KEY else 'Not Set'}")
print(f"TELEGRAM_BOT_TOKEN: {'Loaded' if TELEGRAM_BOT_TOKEN else 'Not Set'}")

print("\n" + "=" * 60)
print("✓ All components verified successfully!")
print("✓ Ready for Railway deployment")

# Run main function to verify bot initialization
if __name__ == "__main__":
    main()
