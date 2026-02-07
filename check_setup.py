"""
Version Checker - Run this to check your setup
"""

print("🔍 Checking your setup...\n")

# Check Python version
import sys

print(f"✅ Python version: {sys.version}")
print()

# Check python-telegram-bot
try:
    import telegram

    print(f"✅ python-telegram-bot installed: version {telegram.__version__}")

    # Check if it's the right version
    version_parts = telegram.__version__.split(".")
    major_version = int(version_parts[0])

    if major_version >= 20:
        print("   ✅ Version is compatible (20.x)")
    elif major_version >= 13:
        print("   ⚠️  You have version 13.x - needs update to 20.x")
        print("   Run: pip install --upgrade python-telegram-bot==20.7")
    else:
        print("   ❌ Version too old - needs update")
        print("   Run: pip install --upgrade python-telegram-bot==20.7")
except ImportError:
    print("❌ python-telegram-bot NOT installed")
    print("   Run: pip install python-telegram-bot==20.7")
print()

# Check NLTK
try:
    import nltk

    print("✅ NLTK installed")

    # Check NLTK data
    try:
        nltk.data.find("tokenizers/punkt")
        print("   ✅ NLTK punkt data available")
    except:
        print("   ⚠️  NLTK punkt data missing")
        print("   Run: python -c \"import nltk; nltk.download('punkt')\"")

    try:
        nltk.data.find("corpora/stopwords")
        print("   ✅ NLTK stopwords data available")
    except:
        print("   ⚠️  NLTK stopwords data missing")
        print("   Run: python -c \"import nltk; nltk.download('stopwords')\"")
except ImportError:
    print("❌ NLTK NOT installed")
    print("   Run: pip install nltk")
print()

# Check SQLite
try:
    import sqlite3

    print(f"✅ SQLite available: version {sqlite3.sqlite_version}")
except ImportError:
    print("❌ SQLite NOT available (should be built-in with Python)")
print()

# Check if files exist
import os

files_to_check = ["main.py", "bot.py", "database.py", "nlp_processor.py"]
print("📁 Checking project files:")
for file in files_to_check:
    if os.path.exists(file):
        print(f"   ✅ {file} exists")
    else:
        print(f"   ❌ {file} missing")
print()

print("=" * 50)
print("🎯 SUMMARY:")
print("=" * 50)

# Give recommendation
try:
    import telegram

    version_parts = telegram.__version__.split(".")
    major_version = int(version_parts[0])

    if major_version >= 20:
        print("✅ Your setup looks good! Try running: python main.py")
    else:
        print("⚠️  Update python-telegram-bot:")
        print("   pip install --upgrade python-telegram-bot==20.7")
        print("   Then run: python main.py")
except:
    print("❌ Install python-telegram-bot first:")
    print("   pip install python-telegram-bot==20.7")
    print("   Then run: python main.py")
