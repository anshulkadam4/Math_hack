from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from database import Database
from nlp_processor import NLPProcessor

# Conversation states
CATEGORY, DESCRIPTION = range(2)

class FreshmanBot:
    def __init__(self, token):
        self.token = token
        self.db = Database()
        self.nlp = NLPProcessor()
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Welcome message"""
        welcome_text = """
🎓 *Welcome to VIT Freshman Survival Kit!*

I'm here to help you with:
📚 Campus & Academic FAQs
📝 Submit Grievances
❓ Answer your queries
💡 Quick assistance 24/7

*Quick Commands:*
/help - See all available commands
/faq - Browse all FAQs
/grievance - Submit a grievance

*Or just ask me anything!*
Example: "What are library hours?" or "Where is the exam cell?"
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help"""
        help_text = """
🤖 *How to Use This Bot:*

*Available Commands:*
/start - Start the bot
/help - Show this help message
/faq - Browse all FAQs
/grievance - Submit a grievance
/stats - View bot statistics
/cancel - Cancel current operation

*Ask Questions Naturally:*
Just type your question! Examples:
• "What are mess timings?"
• "How to access WiFi?"
• "Where is medical center?"

*Submit Grievances:*
Use /grievance to report issues like:
• Broken equipment
• Academic problems
• Hostel issues
• Any complaints

💡 *Tip:* You can ask in your own words, I'll understand!
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def show_all_faqs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Display all FAQs"""
        faqs = self.db.get_all_faqs()
        
        faq_text = "📚 *Frequently Asked Questions:*\n\n"
        for i, (question, answer) in enumerate(faqs, 1):
            faq_text += f"*Q{i}: {question}*\n{answer}\n\n"
            
            # Split into multiple messages if too long
            if len(faq_text) > 3500:
                await update.message.reply_text(faq_text, parse_mode='Markdown')
                faq_text = ""
        
        if faq_text:
            await update.message.reply_text(faq_text, parse_mode='Markdown')
        
        await update.message.reply_text(
            "💡 *Tip:* You can ask any of these questions in your own words!",
            parse_mode='Markdown'
        )
    
    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show bot statistics"""
        grievance_count = self.db.get_grievance_count()
        faq_count = len(self.db.get_all_faqs())
        
        stats_text = f"""
📊 *Bot Statistics:*

📝 Total Grievances Submitted: {grievance_count}
📚 Total FAQs Available: {faq_count}
👥 Active Users: {update.effective_user.first_name} and others

*Most Common Topics:*
• Library & WiFi access
• Hostel & Mess queries
• Examination information
• Course registration
        """
        await update.message.reply_text(stats_text, parse_mode='Markdown')
    
    async def start_grievance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Start grievance submission"""
        reply_keyboard = [
            ['Academic Issue', 'Infrastructure'],
            ['Hostel Issue', 'Faculty Concern'],
            ['Mess/Food', 'Other']
        ]
        
        await update.message.reply_text(
            "📝 *Grievance Submission*\n\n"
            "I'll help you submit your complaint.\n\n"
            "Please select a category for your grievance:",
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True),
            parse_mode='Markdown'
        )
        
        return CATEGORY
    
    async def grievance_category(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Store category and ask for description"""
        context.user_data['category'] = update.message.text
        
        await update.message.reply_text(
            f"✅ Category: *{update.message.text}*\n\n"
            "Now, please describe your grievance in detail.\n"
            "Include:\n"
            "• What's the problem?\n"
            "• Where/when did it occur?\n"
            "• Any specific details\n\n"
            "Type /cancel to cancel this submission.",
            reply_markup=ReplyKeyboardRemove(),
            parse_mode='Markdown'
        )
        
        return DESCRIPTION
    
    async def grievance_description(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Store grievance and confirm"""
        category = context.user_data.get('category', 'Other')
        description = update.message.text
        user_id = str(update.effective_user.id)
        username = update.effective_user.first_name or "Student"
        
        # Save to database
        grievance_id = self.db.add_grievance(user_id, username, category, description)
        
        confirmation_text = f"""
✅ *Grievance Submitted Successfully!*

📋 *Details:*
🎫 Ticket ID: #{grievance_id}
📁 Category: {category}
👤 Submitted by: {username}
⏰ Status: Pending Review

*What happens next?*
• Your grievance will be reviewed by the admin
• You'll be notified of any updates
• Keep your Ticket ID for tracking: #{grievance_id}

*Note:* Expected response time is 24-48 hours.

Thank you for using VIT Freshman Survival Kit! 🎓
        """
        
        await update.message.reply_text(confirmation_text, parse_mode='Markdown')
        
        # Clear user data
        context.user_data.clear()
        
        return ConversationHandler.END
    
    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel operation"""
        await update.message.reply_text(
            "❌ Operation cancelled.\n\n"
            "Type /start to begin again or /help for assistance.",
            reply_markup=ReplyKeyboardRemove()
        )
        context.user_data.clear()
        return ConversationHandler.END
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages"""
        user_message = update.message.text
        intent = self.nlp.detect_intent(user_message)
        
        if intent == 'greeting':
            await update.message.reply_text(
                f"Hello {update.effective_user.first_name}! 👋\n\n"
                "How can I help you today?\n\n"
                "You can:\n"
                "• Ask me questions about VIT\n"
                "• Type /faq to see all questions\n"
                "• Type /grievance to submit a complaint\n\n"
                "Just ask naturally - I'll understand! 😊"
            )
        
        elif intent == 'grievance':
            await update.message.reply_text(
                "It seems you want to submit a grievance.\n\n"
                "Please use the /grievance command to start the submission process."
            )
        
        else:  # FAQ search
            matches = self.db.search_faq(user_message)
            
            if matches:
                response = "🔍 *Here's what I found:*\n\n"
                for i, (question, answer) in enumerate(matches, 1):
                    response += f"*{i}. {question}*\n{answer}\n\n"
                response += "━━━━━━━━━━━━━━━━━━\n"
                response += "💡 Not what you're looking for?\n"
                response += "• Try rephrasing your question\n"
                response += "• Type /faq to see all questions\n"
                response += "• Or type /help for assistance"
            else:
                response = (
                    "🤔 I couldn't find a specific answer to that question.\n\n"
                    "*Here's what you can do:*\n"
                    "• Type /faq to browse all available questions\n"
                    "• Try rephrasing your question\n"
                    "• Submit a grievance using /grievance if it's a specific issue\n\n"
                    "I'm always learning! Your question helps improve the system. 📚"
                )
            
            await update.message.reply_text(response, parse_mode='Markdown')
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle errors"""
        print(f"Error occurred: {context.error}")
        if update and update.effective_message:
            await update.effective_message.reply_text(
                "⚠️ Oops! Something went wrong.\n\n"
                "Please try again or use /start to restart the bot."
            )
    
    def run(self):
        """Start the bot - FIXED VERSION"""
        print("🚀 Initializing Freshman Survival Kit Bot...")
        
        # Create application - This is the correct way for version 20.x
        application = Application.builder().token(self.token).build()
        
        # Add command handlers
        application.add_handler(CommandHandler("start", self.start))
        application.add_handler(CommandHandler("help", self.help_command))
        application.add_handler(CommandHandler("faq", self.show_all_faqs))
        application.add_handler(CommandHandler("stats", self.show_stats))
        
        # Grievance conversation handler
        grievance_handler = ConversationHandler(
            entry_points=[CommandHandler('grievance', self.start_grievance)],
            states={
                CATEGORY: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.grievance_category)],
                DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, self.grievance_description)]
            },
            fallbacks=[CommandHandler('cancel', self.cancel)]
        )
        application.add_handler(grievance_handler)
        
        # Handle regular messages
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Error handler
        application.add_error_handler(self.error_handler)
        
        # Start bot - CRITICAL: Use correct method for version 20.x
        print("✅ Bot is ready!")
        print("🤖 Bot is now running... Press Ctrl+C to stop")
        print("📱 Open Telegram and search for your bot to test!")
        
        # This is the CORRECT way for python-telegram-bot 20.x
        application.run_polling(drop_pending_updates=True)
