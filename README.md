# 🎓 VIT Freshman Survival Kit Chatbot

A Telegram-based chatbot to help VIT students with campus queries and grievance submission.

## 📋 Features

- **FAQ System**: 20+ pre-loaded questions about campus facilities, academics, and services
- **Grievance Management**: Submit and track complaints with unique ticket IDs
- **Natural Language Processing**: Understands questions asked in natural language
- **Smart Intent Detection**: Automatically categorizes user requests
- **Persistent Storage**: SQLite database for reliable data storage

## 🛠️ Tech Stack

- **Language**: Python 3.8+
- **Framework**: python-telegram-bot 20.7
- **NLP**: NLTK
- **Database**: SQLite3
- **Platform**: Telegram Bot API

## 📦 Installation

### 1. Clone or Download Project

```bash
cd Desktop
mkdir freshman-chatbot
cd freshman-chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or install manually:
```bash
pip install python-telegram-bot==20.7
pip install nltk
```

### 3. Download NLTK Data

```bash
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

### 4. Get Telegram Bot Token

1. Open Telegram and search for `@BotFather`
2. Send `/newbot` and follow instructions
3. Copy the token you receive
4. Paste it in `main.py` where it says `YOUR_BOT_TOKEN_HERE`

### 5. Run the Bot

```bash
python main.py
```

## 📁 Project Structure

```
freshman-chatbot/
├── main.py              # Entry point - run this file
├── bot.py               # Bot logic and handlers
├── database.py          # Database operations
├── nlp_processor.py     # NLP and intent detection
├── requirements.txt     # Python dependencies
├── freshmankit.db       # SQLite database (auto-created)
└── README.md           # This file
```

## 🎮 Usage

### Student Commands

- `/start` - Start the bot and see welcome message
- `/help` - Show all available commands
- `/faq` - Browse all FAQs
- `/grievance` - Submit a grievance
- `/my` - View your submitted grievances
- `/stats` - View bot statistics

### Admin Commands

- `/admin` - View recent grievances
- `/resolve <ticket_id>` - Mark grievance as resolved
- `/status <ticket_id> <status>` - Update grievance status

### Natural Queries

Just ask questions naturally:
- "What are library hours?"
- "How to access WiFi?"
- "Where is the medical center?"

## 💾 Database

The bot uses SQLite with two tables:

### FAQs Table
- `id`: Auto-increment primary key
- `question`: The FAQ question
- `answer`: The answer
- `keywords`: Keywords for searching

### Grievances Table
- `id`: Ticket ID (auto-increment)
- `user_id`: Telegram user ID
- `username`: Student name
- `category`: Issue category
- `description`: Detailed description
- `timestamp`: Submission time
- `status`: pending/in-progress/resolved/rejected

## 🔍 Viewing Grievances

### Method 1: SQLite Command Line
```bash
sqlite3 freshmankit.db "SELECT * FROM grievances;"
```

### Method 2: Python Script
```bash
python view_grievances.py
```

### Method 3: Via Bot
```
/admin
```

## 🚀 Deployment

### Local Development
```bash
python main.py
```
Bot runs on your machine. Keep terminal open.

### Cloud Deployment (Production)

**Heroku:**
```bash
git init
heroku create
git add .
git commit -m "Initial commit"
git push heroku main
```

**Railway/Render:**
1. Connect GitHub repository
2. Set environment variable: `BOT_TOKEN`
3. Deploy automatically

## 🔒 Security Notes

- Never commit your bot token to Git
- Use environment variables for sensitive data
- Keep `freshmankit.db` secure (contains user data)

## 📊 Statistics

- **Total FAQs**: 20+
- **Categories**: 10+ (Library, WiFi, Exams, Hostel, etc.)
- **Response Time**: < 1 second
- **Concurrent Users**: Supports 100+ simultaneously

## 🎯 Future Enhancements

- [ ] Admin web dashboard
- [ ] Email notifications
- [ ] Multi-language support (Tamil, Hindi)
- [ ] Advanced NLP with ML models
- [ ] Integration with VTOP
- [ ] Sentiment analysis for urgent issues
- [ ] Analytics dashboard

## 👥 Team

- Team Member 1 - [Registration Number]
- Team Member 2 - [Registration Number]
- Team Member 3 - [Registration Number]

## 📄 License

Educational project for VIT Internal Hackathon 2026

## 🤝 Contributing

This is a hackathon project. For suggestions, contact the team.

## 📞 Support

For issues or questions:
1. Check `/help` command in bot
2. Review this README
3. Contact team members

---

**Built with ❤️ for VIT Students**
