from bot import FreshmanBot
import sys

# ⚠️ IMPORTANT: Replace this with YOUR actual bot token from @BotFather
BOT_TOKEN = "8454688093:AAGoq2Zwjzf27rr_ZHcxfGIRp2gAEgL0zlc"


def main():
    """Main function to run the bot"""

    # Check if token is set
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: Bot token not set!")
        print("\n📝 How to fix:")
        print("1. Open main.py in a text editor")
        print('2. Find the line: BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"')
        print("3. Replace YOUR_BOT_TOKEN_HERE with your actual token from @BotFather")
        print("4. Save the file and run again")
        print("\n💡 Your token looks like: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz")
        sys.exit(1)

    print("=" * 50)
    print("🎓 VIT FRESHMAN SURVIVAL KIT BOT")
    print("=" * 50)
    print("Starting bot...")
    print()

    try:
        bot = FreshmanBot(BOT_TOKEN)
        bot.run()
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped by user")
        print("Thanks for using Freshman Survival Kit!")
    except Exception as e:
        print(f"\n❌ Error starting bot: {e}")
        print("\nCommon issues:")
        print("1. Check if your bot token is correct")
        print("2. Make sure you have internet connection")
        print("3. Verify all libraries are installed")


if __name__ == "__main__":
    main()
