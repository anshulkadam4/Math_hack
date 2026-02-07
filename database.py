import sqlite3
from datetime import datetime


class Database:
    def __init__(self):
        self.conn = sqlite3.connect("freshmankit.db", check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Table for grievances
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS grievances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                username TEXT,
                category TEXT,
                description TEXT,
                timestamp TEXT,
                status TEXT DEFAULT 'pending'
            )
        """)

        # Table for FAQs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS faqs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT,
                answer TEXT,
                keywords TEXT
            )
        """)

        self.conn.commit()
        self.populate_faqs()

    def populate_faqs(self):
        """Add sample FAQs"""
        cursor = self.conn.cursor()

        # Check if FAQs already exist
        cursor.execute("SELECT COUNT(*) FROM faqs")
        if cursor.fetchone()[0] > 0:
            return

        faqs = [
            (
                "What are the library hours?",
                "Library is open Monday-Friday: 8 AM - 10 PM, Saturday-Sunday: 9 AM - 6 PM",
                "library hours timing schedule open close",
            ),
            (
                "How do I access WiFi?",
                "Connect to 'VIT-Student' network. Username: your registration number, Password: your date of birth (DDMMYYYY)",
                "wifi internet connection network password login access",
            ),
            (
                "Where is the examination cell?",
                "Examination Cell is located in the Main Building, 2nd floor, Room 201",
                "exam examination cell location office where find",
            ),
            (
                "What is the attendance requirement?",
                "Minimum 75% attendance is required in each course to be eligible for exams",
                "attendance percentage requirement minimum needed eligibility",
            ),
            (
                "How do I apply for leave?",
                "Login to VTOP > Student Login > Apply for Leave. Approval takes 24-48 hours",
                "leave application absence apply request",
            ),
            (
                "Where can I get my ID card?",
                "Visit Academic Section in Main Building with 2 passport photos and fee receipt",
                "id card identity student card get obtain",
            ),
            (
                "What are mess timings?",
                "Breakfast: 7-9 AM, Lunch: 12-2 PM, Snacks: 4-5 PM, Dinner: 7-9 PM",
                "mess food timing canteen dining hall breakfast lunch dinner",
            ),
            (
                "How to contact placement cell?",
                "Email: placements@vit.ac.in, Phone: +91-xxx-xxxx, Office: 3rd Floor, Admin Block",
                "placement cell contact job internship career email phone",
            ),
            (
                "What is the hostel curfew time?",
                "Hostel gates close at 10 PM on weekdays and 11 PM on weekends",
                "hostel curfew timing gate close entry time",
            ),
            (
                "How do I register for courses?",
                "Course registration opens before each semester on VTOP. Check academic calendar for dates",
                "course registration subject enroll add drop",
            ),
            (
                "Where is the medical center?",
                "Medical Center is located near Boys Hostel, open 24/7 for emergencies",
                "medical center hospital health clinic doctor emergency",
            ),
            (
                "How do I get a bonafide certificate?",
                "Apply through VTOP > Request for Certificate. Collect from Academic Section after 3 working days",
                "bonafide certificate document proof request",
            ),
            (
                "What is the fee payment deadline?",
                "Fee payment deadline is mentioned in academic calendar. Usually 2 weeks before semester starts. Late fee applies after deadline",
                "fee payment deadline date pay tuition semester",
            ),
            (
                "Where can I print documents?",
                "Xerox shops are available near Library and Academic Block. Cost: ₹1 per page for B&W, ₹5 for color",
                "print xerox photocopy document scan shop",
            ),
            (
                "How do I access VTOP?",
                "Visit vtop.vit.ac.in, login with registration number and password. Reset password option available if forgotten",
                "vtop login access portal student website password",
            ),
            (
                "What are sports facilities available?",
                "Cricket ground, Basketball court, Badminton court, Gym, Swimming pool, Tennis court. Timing: 5 AM - 9 PM",
                "sports facilities gym cricket basketball badminton swimming",
            ),
            (
                "Where is the ATM?",
                "ATMs are located near Main Gate, Boys Hostel, and Girls Hostel. SBI, ICICI, and HDFC available",
                "atm cash money bank withdraw location",
            ),
            (
                "How do I report a lost item?",
                "Report to Security Office near Main Gate with details. Check Lost & Found section daily",
                "lost found item report missing security",
            ),
            (
                "What is the grievance redressal process?",
                "Submit grievance through this bot or email: grievance@vit.ac.in. Response within 48 hours",
                "grievance complaint redressal process issue problem",
            ),
            (
                "Where can I buy stationery?",
                "Stationery shops available near Academic Block and Hostel. Open 9 AM - 8 PM",
                "stationery shop books pen paper notebook buy",
            ),
        ]

        cursor.executemany(
            "INSERT INTO faqs (question, answer, keywords) VALUES (?, ?, ?)", faqs
        )
        self.conn.commit()
        print("✅ Database initialized with 20 FAQs")

    def add_grievance(self, user_id, username, category, description):
        cursor = self.conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            """
            INSERT INTO grievances (user_id, username, category, description, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """,
            (user_id, username, category, description, timestamp),
        )
        self.conn.commit()
        return cursor.lastrowid

    def search_faq(self, query):
        """Search FAQ using keywords"""
        cursor = self.conn.cursor()
        query_lower = query.lower()

        cursor.execute("SELECT question, answer, keywords FROM faqs")
        faqs = cursor.fetchall()

        # Score each FAQ based on keyword matches
        matches = []
        for q, a, k in faqs:
            score = 0
            query_words = query_lower.split()

            for word in query_words:
                if len(word) > 2:  # Skip very short words
                    if word in q.lower():
                        score += 3
                    if word in a.lower():
                        score += 2
                    if word in k.lower():
                        score += 1

            if score > 0:
                matches.append((score, q, a))

        # Sort by score (highest first) and return top 3
        matches.sort(reverse=True, key=lambda x: x[0])
        return [(q, a) for score, q, a in matches[:3]]

    def get_all_faqs(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT question, answer FROM faqs")
        return cursor.fetchall()

    def get_grievance_count(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM grievances")
        return cursor.fetchone()[0]
