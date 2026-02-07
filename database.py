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
            # ───────────── General Fresher Queries ─────────────
            (
                "Is VIT Vellore a good university for freshers?",
                "VIT Vellore is considered a good university for freshers due to its structured academic system, large campus, diverse student population, and exposure to multiple opportunities. However, student experience may vary depending on discipline, adaptability, and personal expectations.",
                "vit vellore good university fresher opinion",
            ),
            (
                "Is life at VIT Vellore stressful for freshers?",
                "Life at VIT Vellore can feel demanding initially due to academic workload and rules, especially for freshers. With proper time management and involvement in activities, most students adapt and find a balanced routine over time.",
                "vit vellore stress fresher life",
            ),
            (
                "What should freshers know before joining VIT Vellore?",
                "Freshers should be prepared for a structured academic environment, continuous assessments, and strict adherence to rules. Being proactive, disciplined, and open to learning helps in adjusting smoothly.",
                "vit vellore fresher tips before joining",
            ),
            (
                "Is VIT Vellore very strict?",
                "VIT Vellore follows a rule-based system focusing on discipline and academic integrity. While some students find it strict, others view it as structured and predictable. Experiences vary by hostel, department, and year.",
                "vit vellore strict rules opinion",
            ),
            # ───────────── Academics ─────────────
            (
                "How is the academic workload for freshers?",
                "Freshers at VIT Vellore experience regular assignments, quizzes, and exams. The workload is manageable with consistency, but procrastination can make it overwhelming.",
                "academic workload fresher vit vellore",
            ),
            (
                "Is the grading system tough at VIT Vellore?",
                "The grading system at VIT Vellore is competitive due to relative grading in some courses. Consistent performance throughout the semester is more important than last-minute preparation.",
                "grading system tough vit vellore",
            ),
            (
                "Are professors supportive to freshers?",
                "Many faculty members at VIT Vellore are approachable and supportive, especially when students seek help proactively. Teaching style and engagement can vary across departments and individuals.",
                "faculty support fresher vit vellore",
            ),
            (
                "Is attendance very important at VIT Vellore?",
                "Attendance is an important academic requirement at VIT Vellore. Falling short of the mandated attendance percentage can affect exam eligibility, so regular class participation is essential.",
                "attendance importance vit vellore",
            ),
            # ───────────── Hostels & Campus Life ─────────────
            (
                "How is hostel life for freshers?",
                "Hostel life at VIT Vellore helps freshers adapt to independence and campus culture. While rules are strict, hostels provide safety, community interaction, and convenience.",
                "hostel life fresher vit vellore",
            ),
            (
                "Is hostel food good at VIT Vellore?",
                "Hostel mess food quality at VIT Vellore varies by mess and personal taste. While some students find it satisfactory, others prefer adjusting expectations or choosing alternative mess options when available.",
                "hostel food vit vellore opinion",
            ),
            (
                "Can freshers go out of campus?",
                "Freshers are generally required to follow university and hostel outing rules. Permissions and conditions may apply based on hostel regulations and university policies.",
                "campus outing fresher vit vellore",
            ),
            (
                "Is campus life boring?",
                "Campus life at VIT Vellore depends on student involvement. With clubs, chapters, events, and peer interaction, many students find campus life engaging, while passive participation may feel monotonous.",
                "campus life boring vit vellore opinion",
            ),
            # ───────────── Friends & Social Life ─────────────
            (
                "Is it easy to make friends at VIT Vellore?",
                "With students from diverse backgrounds, it is generally easy to make friends at VIT Vellore. Participation in classes, hostels, and clubs helps build connections.",
                "friends social life vit vellore",
            ),
            (
                "Are seniors helpful to freshers?",
                "Many seniors at VIT Vellore guide freshers academically and socially. However, interactions depend on individual initiative and involvement in student communities.",
                "seniors helpful fresher vit vellore",
            ),
            # ───────────── Clubs & Activities ─────────────
            (
                "Are clubs important for freshers?",
                "Clubs and chapters help freshers develop skills, socialize, and explore interests beyond academics. Participation is optional but highly beneficial for overall development.",
                "clubs importance fresher vit vellore",
            ),
            (
                "Can freshers join technical clubs?",
                "Yes, freshers are encouraged to apply to technical and non-technical clubs. Selection processes vary and may include interviews or basic screening tasks.",
                "technical clubs fresher vit vellore",
            ),
            # ───────────── Pros & Cons ─────────────
            (
                "What are the pros of studying at VIT Vellore?",
                "Pros include a large and diverse campus, structured academics, good infrastructure, exposure to competitions and clubs, and strong peer learning opportunities.",
                "vit vellore pros advantages",
            ),
            (
                "What are the cons of studying at VIT Vellore?",
                "Cons may include strict rules, competition due to large student intake, and the need for self-discipline to stand out academically and professionally.",
                "vit vellore cons disadvantages",
            ),
            (
                "Is VIT Vellore worth the fees?",
                "Whether VIT Vellore is worth the fees depends on how students utilize academic resources, clubs, and placement opportunities. Outcomes vary based on effort and engagement.",
                "vit vellore fees worth opinion",
            ),
            # ───────────── Placements & Future ─────────────
            (
                "Should freshers worry about placements?",
                "Freshers do not need to worry immediately about placements but should focus on building strong fundamentals, skills, and consistent academic performance from the beginning.",
                "placements worry fresher vit vellore",
            ),
            (
                "Does CGPA matter a lot?",
                "CGPA plays an important role in internships, placements, and higher studies. Maintaining a good CGPA gives students more options and flexibility in the future.",
                "cgpa importance vit vellore",
            ),
            # ───────────── Opinion & Comparison ─────────────
            (
                "Is VIT Vellore better than other private universities?",
                "VIT Vellore is often compared favorably with other private universities due to its scale and opportunities. However, the best choice depends on individual priorities and branch of study.",
                "vit vellore comparison private universities",
            ),
            (
                "Is VIT Vellore overrated?",
                "Some students feel VIT Vellore is overrated due to high intake, while others value the opportunities it offers. Experiences differ based on expectations and personal effort.",
                "vit vellore overrated opinion",
            ),
            # ───────────── Adjustment & Survival ─────────────
            (
                "How can freshers survive the first semester?",
                "Freshers can adapt by attending classes regularly, managing time effectively, seeking help early, and maintaining a healthy balance between academics and rest.",
                "fresher survival first semester vit vellore",
            ),
            (
                "What mistakes should freshers avoid?",
                "Freshers should avoid neglecting attendance, procrastinating academics, isolating themselves socially, and ignoring official university communications.",
                "mistakes freshers vit vellore",
            ),
            # ───────────── Final Freshers Questions ─────────────
            (
                "Is VIT Vellore safe for freshers?",
                "VIT Vellore maintains campus security, monitored hostels, and regulated access points. Overall, the campus is considered safe for freshers.",
                "safety fresher vit vellore",
            ),
            (
                "Will freshers get free time?",
                "Freshers do get free time outside classes. How this time is used depends on academic planning, club involvement, and personal habits.",
                "free time fresher vit vellore",
            ),
            (
                "Is joining VIT Vellore a good decision?",
                "Joining VIT Vellore can be a good decision for students willing to adapt, work consistently, and actively explore opportunities provided by the university.",
                "joining vit vellore good decision opinion",
            ),
            # ───────────── Expectations vs Reality ─────────────
            (
                "What is the biggest reality shock for freshers at VIT Vellore?",
                "Many freshers are surprised by the level of academic competition and the need for self-discipline. Managing time effectively and staying consistent are more important than relying on last-minute preparation.",
                "reality shock fresher vit vellore",
            ),
            (
                "Is VIT Vellore like school or college?",
                "Academically, VIT Vellore is more structured than many colleges, which can feel school-like initially. However, students have more responsibility for managing their own academics and activities.",
                "vit vellore school or college opinion",
            ),
            (
                "Do freshers feel homesick at VIT Vellore?",
                "Homesickness is common among freshers, especially during the first few weeks. Most students gradually adjust as they form friendships and settle into campus life.",
                "homesick fresher vit vellore",
            ),
            # ───────────── Academics Deep Dive ─────────────
            (
                "Are first-year subjects difficult?",
                "First-year subjects at VIT Vellore focus on fundamentals. While concepts may not be extremely difficult, consistent study is required due to continuous assessments.",
                "first year subjects difficulty vit vellore",
            ),
            (
                "Is rote learning enough to score well?",
                "Rote learning alone is usually insufficient. Understanding concepts and applying them in quizzes, assignments, and exams leads to better performance.",
                "rote learning vit vellore opinion",
            ),
            (
                "Do freshers need to study every day?",
                "Daily study is not mandatory, but regular revision and timely completion of assignments help avoid stress before assessments.",
                "daily study fresher vit vellore",
            ),
            # ───────────── Competition & Pressure ─────────────
            (
                "Is competition very high among students?",
                "Due to the large and diverse student population, competition at VIT Vellore can be high. However, students who focus on personal growth rather than comparison tend to perform better.",
                "competition students vit vellore",
            ),
            (
                "Do freshers feel academic pressure?",
                "Some freshers experience academic pressure initially, especially during assessment-heavy periods. Proper planning and seeking help early can reduce this pressure.",
                "academic pressure fresher vit vellore",
            ),
            (
                "Is it hard to stand out at VIT Vellore?",
                "Standing out requires consistent effort, skill development, and participation in academics or extracurricular activities. The large campus offers many platforms, but initiative is essential.",
                "stand out vit vellore opinion",
            ),
            # ───────────── Campus Culture ─────────────
            (
                "How diverse is the student population?",
                "VIT Vellore has students from different states, cultures, and educational backgrounds. This diversity provides exposure to varied perspectives and experiences.",
                "diversity campus vit vellore",
            ),
            (
                "Is English necessary to survive at VIT Vellore?",
                "English is commonly used in academics and communication, but students gradually improve their proficiency through regular interaction and coursework.",
                "english language vit vellore",
            ),
            (
                "Is there a strong campus culture?",
                "Campus culture at VIT Vellore is shaped largely by student clubs, events, and peer groups. Active participation enhances the overall experience.",
                "campus culture vit vellore",
            ),
            # ───────────── Rules & Discipline ─────────────
            (
                "Are rules strictly enforced?",
                "University rules are enforced to maintain discipline and safety. Enforcement intensity may vary, but students are expected to follow official guidelines.",
                "rules enforcement vit vellore",
            ),
            (
                "Do rules become relaxed after first year?",
                "Some academic and hostel rules may feel less restrictive as students progress, but core regulations remain applicable throughout the program.",
                "rules after first year vit vellore",
            ),
            # ───────────── Time & Balance ─────────────
            (
                "Is it possible to manage academics and clubs?",
                "Yes, many students successfully balance academics and club activities through proper planning and prioritization.",
                "academics clubs balance vit vellore",
            ),
            (
                "Do freshers get weekends free?",
                "Free time on weekends depends on academic workload, assignments, and personal planning. Some weekends may be busier than others.",
                "weekends fresher vit vellore",
            ),
            # ───────────── Mental & Personal Growth ─────────────
            (
                "Does VIT Vellore help in personality development?",
                "VIT Vellore provides opportunities through presentations, teamwork, clubs, and events that contribute to personality and communication skill development.",
                "personality development vit vellore",
            ),
            (
                "Can introverts survive at VIT Vellore?",
                "Introverted students can thrive by choosing activities and peer groups that align with their comfort levels. The campus environment supports different personalities.",
                "introverts vit vellore opinion",
            ),
            (
                "Does college life improve confidence?",
                "College life at VIT Vellore can improve confidence as students face academic challenges, presentations, and collaborative projects.",
                "confidence college life vit vellore",
            ),
            # ───────────── Opinions & Reflections ─────────────
            (
                "Is VIT Vellore more about discipline or freedom?",
                "VIT Vellore emphasizes discipline within a structured framework while offering freedom in academics, learning paths, and extracurricular choices.",
                "discipline freedom vit vellore opinion",
            ),
            (
                "Do students enjoy their first year?",
                "First-year experiences vary. While some students enjoy the learning curve and social exposure, others take time to adjust to the academic structure.",
                "first year experience vit vellore",
            ),
            (
                "Is VIT Vellore suitable for average students?",
                "Average students can perform well at VIT Vellore through consistency, effort, and effective use of available resources.",
                "average students vit vellore",
            ),
            # ───────────── Long-Term Perspective ─────────────
            (
                "Does the first year decide everything?",
                "The first year builds a foundation, but long-term outcomes depend on sustained effort across all semesters.",
                "first year importance vit vellore",
            ),
            (
                "Will fresher mistakes affect the future?",
                "Minor mistakes in the first year are common and usually do not define long-term success if students learn and improve.",
                "mistakes fresher future vit vellore",
            ),
            # ───────────── Final Opinion-Based ─────────────
            (
                "Is VIT Vellore more opportunity-driven or pressure-driven?",
                "VIT Vellore offers many opportunities, but students may feel pressure if they do not manage time and expectations effectively. The experience depends on individual approach.",
                "opportunities pressure vit vellore",
            ),
            (
                "Is self-learning important at VIT Vellore?",
                "Self-learning is very important, as classroom teaching is complemented by independent study, practice, and exploration.",
                "self learning vit vellore",
            ),
            (
                "Will joining VIT Vellore change a student?",
                "Many students experience academic, personal, and social growth at VIT Vellore. The extent of change depends on engagement and mindset.",
                "student change vit vellore opinion",
            ),
            (
                "Is VIT Vellore really worth joining or is it overrated?",
                "Experiences shared online vary widely — some students highlight good facilities, regular opportunities, and placements, while others emphasize that satisfaction depends on personal effort, expectations, and goals. It’s normal for opinions to differ. Make a decision based on your priorities and long-term plans rather than just online commentary.",
                "vit worth it overrated reddit opinion",
            ),
            (
                "What do students say about VIT Vellore’s opportunities?",
                "Many students report that VIT provides a steady flow of internship, club, and project opportunities, with frequent event notifications and chances to participate in activities. However, making the most of these requires initiative and active participation.",
                "reddit opportunities vit vellore",
            ),
            (
                "Is the first day of arrival hectic or what happens for freshers?",
                "On the first day at VIT Vellore, freshers usually complete admission verification, room allocation, and receive keys from hostel wardens before they bring in their luggage and settle into their rooms. This helps ensure proper identity checks and accommodation assignments.",
                "first day arrival vit vellore reddit",
            ),
            (
                "Do students say there is a gym booking issue on campus?",
                "Some students have mentioned that gym slots can fill up quickly when booking through the official system, so booking early is helpful. Outside equipment (like dumbbells) may be used personally in hostels but official gym access follows booking rules.",
                "gym booking reddit vit vellore",
            ),
            (
                "Is there ragging or should freshers worry about it?",
                "According to student discussions, ragging is officially prohibited at VIT Vellore and seniors generally do not engage in sanctioned ragging. If any inappropriate conduct occurs, reporting to hostel or university authorities is recommended.",
                "ragging reddit vit vellore",
            ),
            (
                "Do Reddit users complain about being overwhelmed by events?",
                "Some freshers online have mentioned getting many event invites and messages, which can feel overwhelming at first. Participation is optional, and students often recommend choosing events that match personal interests to avoid overload.",
                "events overwhelm reddit vit vellore",
            ),
            (
                "Are there discussions on Reddit about choosing branches or future paths?",
                "Yes — students sometimes ask about how to go abroad, how to build coding experience from first semester, and which clubs are worth joining. These reflect common concerns about future readiness and skills building.",
                "future abroad clubs reddit vit vellore",
            ),
            (
                "Do students online compare VIT Vellore with other campuses like VIT Chennai?",
                "Some Reddit discussions compare VIT Vellore and VIT Chennai in terms of placements, campus vibe, and city surroundings. Views are subjective, with some preferring Vellore’s placement opportunities and others preferring Chennai’s urban environment.",
                "vit vellore vs vit chennai reddit",
            ),
            (
                "Have students shared honest negative experiences from their first year?",
                "There are posts where some students have shared difficulty adjusting academically or socially. These personal anecdotes highlight that experiences differ from person to person and are not universally representative.",
                "negative experience reddit vit vellore",
            ),
            (
                "What advice do seniors on Reddit give to freshers?",
                "Online, seniors often advise freshers to stay consistent with academics, manage time well, actively seek internships or projects, and use campus resources. They also emphasize maintaining a healthy balance between work and relaxation.",
                "seniors advice reddit vit vellore",
            ),
            # ───────────── Arrival & Orientation ─────────────
            (
                "What happens on the first day for freshers?",
                "The first day usually involves reporting formalities, identity verification, hostel allocation, and initial instructions. Freshers are guided through the process by university staff and volunteers.",
                "first day fresher vit vellore",
            ),
            (
                "Is orientation important for freshers?",
                "Orientation helps freshers understand academic rules, campus facilities, and expectations. Attending orientation makes it easier to adapt during the first few weeks.",
                "orientation fresher vit vellore",
            ),
            (
                "Will classes start immediately after reporting?",
                "Classes generally begin after orientation and administrative processes are completed. The exact start date is communicated through official channels.",
                "classes start fresher vit vellore",
            ),
            # ───────────── Academics ─────────────
            (
                "Are first-year classes common for all branches?",
                "Many first-year courses focus on core fundamentals and may be common across branches, though some branch-specific subjects may also be included.",
                "first year common subjects vit vellore",
            ),
            (
                "How often do freshers have assessments?",
                "Freshers usually have regular assessments such as quizzes, assignments, and exams spread throughout the semester to encourage continuous learning.",
                "assessments fresher vit vellore",
            ),
            (
                "Are internal marks important?",
                "Internal assessments contribute significantly to the final grade, so consistent performance throughout the semester is important.",
                "internal marks importance vit vellore",
            ),
            (
                "Do professors explain from basics?",
                "Most professors cover foundational concepts, but students are expected to do self-study to fully understand topics.",
                "teaching style vit vellore",
            ),
            # ───────────── Attendance & Exams ─────────────
            (
                "How strictly is attendance monitored?",
                "Attendance is monitored regularly and plays a key role in exam eligibility. Students should attend classes consistently to avoid issues.",
                "attendance strict vit vellore",
            ),
            (
                "Are exams very difficult for freshers?",
                "Exams test both understanding and application of concepts. They may feel challenging initially but become manageable with regular preparation.",
                "exam difficulty fresher vit vellore",
            ),
            (
                "Is it possible to recover after a bad exam?",
                "Yes, continuous assessments allow students to improve performance over time if they identify mistakes and work consistently.",
                "bad exam recovery vit vellore",
            ),
            # ───────────── Hostels ─────────────
            (
                "Are hostels compulsory for freshers?",
                "Hostel accommodation is generally recommended for freshers, especially those from outside Vellore, but policies may vary.",
                "hostel compulsory fresher vit vellore",
            ),
            (
                "Is adjusting to hostel life difficult?",
                "Initial adjustment can be challenging, but most students adapt within a few weeks as they form routines and friendships.",
                "hostel adjustment vit vellore",
            ),
            (
                "Are hostel rules very strict?",
                "Hostel rules are designed for safety and discipline. While they may feel strict initially, students usually adjust over time.",
                "hostel rules strict vit vellore",
            ),
            # ───────────── Food & Daily Life ─────────────
            (
                "Do freshers struggle with food initially?",
                "Some freshers take time to adjust to mess food, but most adapt gradually or choose from available options.",
                "food adjustment vit vellore",
            ),
            (
                "Is outside food allowed?",
                "Outside food policies depend on hostel regulations and may change, so students should follow official guidelines.",
                "outside food vit vellore",
            ),
            # ───────────── Social Life ─────────────
            (
                "Is it easy to make friends in the first year?",
                "Yes, first year is one of the easiest times to make friends due to shared classes, hostels, and activities.",
                "friends fresher vit vellore",
            ),
            (
                "Do freshers interact with seniors?",
                "Interaction with seniors happens through clubs, hostels, and academic activities, and is usually helpful and positive.",
                "seniors interaction vit vellore",
            ),
            # ───────────── Clubs & Activities ─────────────
            (
                "Should freshers join clubs in the first semester?",
                "Joining clubs can help freshers explore interests and build skills, but balancing academics should be a priority.",
                "clubs first semester vit vellore",
            ),
            (
                "Are club selections competitive?",
                "Some clubs have selection processes, while others are open. Selection criteria vary by club.",
                "club selection vit vellore",
            ),
            # ───────────── Pressure & Mental Health ─────────────
            (
                "Do freshers feel academic pressure?",
                "Some pressure is common due to a new environment and competition, but it becomes manageable with planning and support.",
                "academic pressure fresher vit vellore",
            ),
            (
                "Is it okay to feel lost initially?",
                "Feeling confused at the beginning is normal. Most students gain clarity as they settle into routines.",
                "feeling lost fresher vit vellore",
            ),
            # ───────────── Opinions & Reality ─────────────
            (
                "Is VIT Vellore only about studies?",
                "While academics are important, students also have opportunities for clubs, events, and personal development.",
                "vit vellore studies only opinion",
            ),
            (
                "Is college life enjoyable at VIT Vellore?",
                "Enjoyment depends on involvement and mindset. Active participation generally leads to a better experience.",
                "college life enjoyable vit vellore",
            ),
            (
                "Is VIT Vellore overrated or underrated?",
                "Opinions vary widely. Outcomes depend more on how students use available opportunities than on reputation alone.",
                "vit vellore overrated underrated",
            ),
            # ───────────── Future Focus ─────────────
            (
                "Should freshers think about internships early?",
                "Freshers should focus on fundamentals first, while gradually exploring skills needed for internships in later years.",
                "internships early fresher vit vellore",
            ),
            (
                "Does first-year CGPA matter?",
                "First-year CGPA forms the foundation for future semesters and can influence opportunities later on.",
                "first year cgpa vit vellore",
            ),
            # ───────────── Safety & Discipline ─────────────
            (
                "Is the campus safe for freshers?",
                "The campus has security measures and monitored hostels, making it generally safe for students.",
                "campus safety fresher vit vellore",
            ),
            (
                "Are rules enforced equally?",
                "Rules are meant to be applied uniformly, though experiences may vary slightly based on situation.",
                "rules enforcement vit vellore",
            ),
            # ───────────── Adjustment & Growth ─────────────
            (
                "How long does it take to feel settled?",
                "Most freshers start feeling comfortable within the first one to two months.",
                "settle time fresher vit vellore",
            ),
            (
                "Does college life change students?",
                "College life often leads to personal growth, independence, and improved self-management skills.",
                "college life change vit vellore",
            ),
            (
                "Is joining VIT Vellore a good choice for freshers?",
                "For students willing to adapt and put in consistent effort, VIT Vellore can provide valuable academic and personal growth opportunities.",
                "joining vit vellore good choice",
            ),
            (
                "Where can I get my hair cut (for both men and women)?",
                "Haircut and grooming services are available inside the VIT Vellore campus through designated salons for men and women. These facilities operate as per university-approved schedules, and students can also choose to visit salons outside the campus if permitted by hostel and outing rules.",
                "hair cut salon grooming vit vellore",
            ),
            (
                "Where can I get decent meal-like food to eat and not just junk?",
                "VIT Vellore campus has multiple food courts and dining outlets offering regular meals in addition to snacks. Students can choose options that serve rice, chapati, curries, and other balanced meals depending on availability and preference.",
                "healthy food meals campus vit vellore",
            ),
            (
                "Where can I buy hygiene products?",
                "Hygiene and personal care products such as soap, shampoo, toothpaste, and sanitary items are available at campus convenience stores and supermarkets. Availability may vary, but essential items are generally stocked.",
                "hygiene products buy campus vit vellore",
            ),
            (
                "If I fail in any subject, how do I retake the exam?",
                "If a student fails a course, VIT Vellore provides options such as re-registration or arrear examinations as per academic regulations. The exact procedure, eligibility, and timelines are communicated through official academic notifications and the student portal.",
                "fail subject retake exam vit vellore",
            ),
            (
                "Why are there so many politicians coming to the college?",
                "Visits by public figures, including politicians, are usually part of formal events, conferences, or official programs organized by the university. These visits are institutional activities and do not typically affect academic schedules.",
                "politicians visit vit vellore campus",
            ),
            (
                "What kind of events can we look forward to?",
                "Students at VIT Vellore can look forward to technical fests, cultural festivals, workshops, guest lectures, sports events, and club-organized activities conducted throughout the academic year.",
                "events fests workshops vit vellore",
            ),
            (
                "How do I get a gym membership?",
                "Gym access at VIT Vellore is provided through a registration or booking process as defined by the university. Students must follow the official procedure announced by the sports or facilities department.",
                "gym membership vit vellore",
            ),
            (
                "Are there any free gyms available?",
                "Some fitness facilities may be accessible as part of hostel or campus amenities, while others may require registration. Availability and access rules are communicated by the university.",
                "free gym campus vit vellore",
            ),
            (
                "Are there going to be trainers in the gym?",
                "Gym facilities may have trainers or instructors available during specific hours or programs. This depends on university arrangements and is subject to change.",
                "gym trainers vit vellore",
            ),
            (
                "How do we give our clothes to the laundry?",
                "Laundry services at VIT Vellore operate through designated campus facilities or vendors. Students follow the prescribed process for handing over clothes, tracking items, and collecting them as informed by hostel administration.",
                "laundry process vit vellore",
            ),
            (
                "How do I change my room?",
                "Room change requests are handled through the hostel administration. Students must apply using the official process, and approvals depend on availability and valid reasons.",
                "room change hostel vit vellore",
            ),
            (
                "What is the procedure for room allotment from the second year?",
                "From the second year onward, room allotment is generally conducted through an online or administrative process based on availability, eligibility, and university guidelines announced before the academic year.",
                "second year room allotment vit vellore",
            ),
            (
                "How do I get a cycle?",
                "Students can bring personal bicycles to campus or purchase one from vendors near the university. Registration or tagging procedures may be required as per campus security rules.",
                "cycle buy campus vit vellore",
            ),
            (
                "What do I do if my cycle gets stolen?",
                "In case of cycle theft, students should report the incident immediately to campus security or the designated authority and follow the prescribed complaint procedure.",
                "cycle stolen report vit vellore",
            ),
            (
                "How do I meet a counsellor?",
                "Students can meet a counsellor by booking an appointment or visiting the university counselling services as per the process communicated by the administration. Counselling services are confidential and meant to support student well-being.",
                "counsellor appointment vit vellore",
            ),
            (
                "How do I find my lost stuff?",
                "Lost items can be reported to campus security, hostel offices, or designated lost-and-found services. Students are advised to check these points and report missing belongings promptly.",
                "lost and found vit vellore",
            ),
            (
                "Where can I buy sports apparel?",
                "Sports apparel such as jerseys, track pants, and sports shoes may be available at campus stores or nearby shops outside the university. Availability depends on stock and demand.",
                "sports apparel buy vit vellore",
            ),
            (
                "How do I join clubs?",
                "Students can join clubs by applying during recruitment drives or responding to official announcements made by clubs and chapters. Selection procedures vary depending on the club.",
                "join clubs vit vellore",
            ),
            (
                "How do I get night slips?",
                "Night slips, where applicable, must be requested through the official hostel or wardens’ approval process. Students must follow the current hostel guidelines.",
                "night slip hostel vit vellore",
            ),
            (
                "How do I get in contact with seniors?",
                "Freshers can interact with seniors through clubs, hostels, academic activities, and official mentoring programs if available. Interactions are generally supportive and informal.",
                "contact seniors vit vellore",
            ),
            (
                "Where can I go to report bullying?",
                "Bullying or harassment incidents should be reported immediately to hostel authorities, faculty advisors, or designated university grievance and anti-ragging committees.",
                "report bullying vit vellore",
            ),
            (
                "How do I get my clothes pressed or ironed?",
                "Clothes pressing or ironing services are available through laundry facilities or local vendors associated with the campus. Students should follow the instructions provided by hostel administration.",
                "clothes ironing vit vellore",
            ),
            (
                "Where can I buy clothes?",
                "Clothing items can be purchased from shops inside the campus or from stores located outside the university, subject to outing permissions.",
                "buy clothes vit vellore",
            ),
            (
                "How do I report something suspicious or unsafe?",
                "Suspicious or unsafe activities should be reported immediately to campus security, hostel authorities, or appropriate university officials to ensure safety.",
                "report suspicious activity vit vellore",
            ),
            (
                "How do I collect my parcels?",
                "Parcels from online shopping websites or private senders are usually received at designated collection points on campus. Students must follow the notified procedure to collect their parcels using valid identification.",
                "parcel collection vit vellore",
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
