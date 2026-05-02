"""Generate RSMT college info PDF from scraped website content."""
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_LEFT

OUT = Path("data/rsmt_college_info.pdf")
OUT.parent.mkdir(exist_ok=True)

styles = getSampleStyleSheet()
h1 = ParagraphStyle("h1", parent=styles["Heading1"], fontSize=16, spaceAfter=10)
h2 = ParagraphStyle("h2", parent=styles["Heading2"], fontSize=13, spaceAfter=6, spaceBefore=12)
body = ParagraphStyle("body", parent=styles["BodyText"], fontSize=10, leading=14, spaceAfter=6, alignment=TA_LEFT)

story = []

def H1(t): story.append(Paragraph(t, h1))
def H2(t): story.append(Paragraph(t, h2))
def P(t): story.append(Paragraph(t, body))
def SP(): story.append(Spacer(1, 0.2*cm))

# ---- About ----
H1("Rajarshi School of Management & Technology (RSMT), Varanasi")
P("Source: https://www.rsmt.ac.in/")
P("Rajarshi School of Management & Technology (RSMT) is a leading institute offering "
  "under-graduate and post-graduate programmes in Computer Application and Management. "
  "RSMT is one of the units of Udai Pratap College, Varanasi. The campus is strategically "
  "located in Varanasi (Kashi) - the cultural and educational hub of India. RSMT integrates "
  "modern management and technology education with the eternal brilliance of the city of light.")

H2("Our Inspiration")
P("RSMT is one of the units of Udai Pratap College, Varanasi, founded in 1909. The institution "
  "was established due to the philanthropy of Late Rajarshi Udai Pratap Singh Ju Deo, Raja of "
  "Bhinaga (District Baharaich, U.P.), born 3 September 1850, died 1913. He laid the foundation "
  "of Hewett Kshatriya High School in Varanasi on 25 November 1909, which has grown into Udai "
  "Pratap Autonomous College, Varanasi.")

H2("Vision")
P("To be a world-class institution that nurtures talent and catalytically transforms the lives "
  "of its students through excellence in teaching, research, service and community development. "
  "To uphold a commitment to shaping lives through scholarly teaching and learning that "
  "contributes to an equitable and holistic transformation of society at large.")

H2("Mission")
P("To create and sustain a community of lifelong learners in an environment that emphasizes "
  "literacy, critical thinking, humanistic and scientific inquiry. The institute provides a "
  "dynamic, challenging and ethical environment for high quality teaching, research, learning "
  "and service. Goals include: pursue excellence in teaching and scholarship; prepare students "
  "for leadership; support world-class research; develop mastery of disciplines; channelize "
  "talent for service to society; promote academic freedom, diversity, equality and justice.")

# ---- Programs ----
H1("Programmes Offered")
H2("MCA (Master of Computer Application)")
P("Duration: 2 years (full-time post-graduate). "
  "Affiliation: Dr. A.P.J. Abdul Kalam Technical University (AKTU), Lucknow. "
  "Approval: All India Council for Technical Education (AICTE), Ministry of HRD, Government of India.")
P("Eligibility: Graduation Degree with Mathematics as one of the subjects at 10+2 or Graduation level. "
  "Candidates appearing for the qualifying examination are also eligible (subject to clearing it).")
P("Selection Process: (1) State level combined entrance examination; (2) Direct admission under "
  "management quota / lapse seat.")

H2("MBA (Master of Business Administration)")
P("Duration: 2 years (full-time post-graduate). "
  "Affiliation: Dr. A.P.J. Abdul Kalam Technical University (AKTU), Lucknow. "
  "Approval: AICTE, Ministry of HRD, Government of India.")
P("Eligibility: Graduation Degree (any discipline). Candidates appearing for qualifying exam also eligible.")
P("Selection Process: (1) State level combined entrance examination; (2) Direct admission under "
  "management quota / lapse seat.")
P("MBA Course Structure (AKTU):")
P("Semester 1: Managing Organization, Managerial Economics, Business Accounting, Business Environment, "
  "Business Statistics, Marketing Management, Communication for Management, Fundamentals of Computer & "
  "Information System.")
P("Semester 2: Managing Human Resources, Business Laws, Customer Relationship Management, Financial "
  "Management, Operation Research, Cost & Management Accounting, Operations Management, Research "
  "Methodology, Comprehensive Viva.")
P("Semester 3: Entrepreneurship Development, International Business Management, Rural Development, "
  "Specialization Group-1 Electives 1 & 2, Specialization Group-2 Electives 1 & 2, Summer Training "
  "Project Report.")
P("Semester 4: Strategic Management, Insurance & Risk Management, Hospitality & Tourism Management, "
  "Behavioural Finance, Specialization Group-1 Elective 3, Specialization Group-2 Elective 3, "
  "Research Project Report, Comprehensive Viva.")
P("MBA Specializations: Human Resource, Marketing, Financial Management, Rural Development, "
  "Information Technology, International Business.")

H2("BCA (Bachelor of Computer Application)")
P("Duration: 3 years (full-time under-graduate). "
  "Affiliation: Mahatma Gandhi Kashi Vidyapith (MGKVP), Varanasi.")
P("Eligibility: 10+2 in any discipline. Candidates appearing in final 10+2 exam may also apply.")
P("Selection: Online registration on www.rsmt.ac.in followed by direct admission (no entrance test).")
P("BCA Course Structure (selected highlights):")
P("Semester 1: Computer Fundamentals & Office Automation, Programming Principle & Algorithm, "
  "Principles of Management, Business Communication, Mathematics-I, Office Automation Lab, "
  "Programming Lab.")
P("Semester 2: C Programming, Digital Electronics & Computer Organization, Organization Behavior, "
  "Financial Accounting and Management, Mathematics-II, C Programming Lab.")
P("Semester 3: OOP using C++, Data Structures (C/C++), Computer Architecture & Assembly Language, "
  "Business Economics, Elements of Statistics, OOPS Lab, DS Lab.")
P("Semester 4: Computer Graphics & Multimedia, Operating System, Software Engineering, "
  "Optimization Techniques, Mathematics-III, Computer Graphics Lab.")
P("Semester 5: Introduction to DBMS, Java Programming & Dynamic Web Page Design, Computer Network, "
  "Numerical Methods, Minor Project, Summer Training Viva, DBMS Lab, Java Lab.")
P("Semester 6: Computer Network Security, Information System Analysis Design & Implementation, "
  "E-Commerce, Knowledge Management, Major Project, Project Presentation/Seminar.")

H2("BBA (Bachelor of Business Administration)")
P("Duration: 3 years (full-time under-graduate). "
  "Affiliation: Mahatma Gandhi Kashi Vidyapith (MGKVP), Varanasi.")
P("Eligibility: 10+2 in any discipline. Candidates appearing in 10+2 final exam also eligible "
  "(subject to clearing the entrance test conducted by RSMT).")
P("BBA Course Structure (selected highlights):")
P("Semester 1: Business Economics, Basic Accounting, Business Statistics, Principles of Management, "
  "Business Ethics & Governance, Computer Applications.")
P("Semester 2: Organisational Behavior, Business Finance, HRD, Marketing Theory & Practices, "
  "Business Mathematics, Advertising Management.")
P("Semester 3: Management & Cost Accounting, Business Law, Production Management, Business Policy, "
  "Business Communication, Business Environment.")
P("Semester 4: Supply Chain Management, Research Methodology, Specialised Accounting, Consumer "
  "Behaviour, Investment Analysis & Portfolio Management, Company Law.")
P("Semester 5: Income Tax, Marketing Communication, Entrepreneurship & Small Business Management, "
  "Sales Management, Industrial Relations & Labour Laws, Company Accounts.")
P("Semester 6: Project Management, Goods & Service Tax, Auditing, International Trade, "
  "Strategic Management, Training and Development.")

# ---- Fees ----
H1("Fee Structure 2026-27")
P("(All fees in INR per year)")
P("BBA: 1st Year - 42,000 | 2nd Year - 39,000 | 3rd Year - 36,100")
P("BCA: 1st Year - 52,000 | 2nd Year - 49,000 | 3rd Year - 47,100")
P("MBA: 1st Year - 90,000 | 2nd Year - 70,000")
P("MCA: 1st Year - 90,000 | 2nd Year - 70,000")

# ---- Admission ----
H1("Admission Procedure")
H2("BBA & BCA (Affiliated to MGKVP, Varanasi)")
P("Eligibility: Intermediate or 10+2 in any discipline. Candidates appearing for 10+2 final examination may apply.")
P("Procedure: Direct admission.")
P("How to Apply: Online via www.rsmt.ac.in, or obtain physical application from campus/city office on payment of Rs. 500.")

H2("MCA & MBA (Affiliated to AKTU, Lucknow)")
P("Eligibility (MCA): Graduation with Mathematics at 10+2 or Graduation level.")
P("Eligibility (MBA): Graduation Degree.")
P("Selection: (1) State-level combined entrance examination; (2) Direct admission under management quota/lapse seat.")

H2("Admission Helpline")
P("BBA: Dr. Preeti Singh - 8808050200")
P("BCA: Dr. C.P. Singh - 9415812094")
P("MBA: Mr. P.N. Singh - 7007723301")
P("MCA: Dr. S.K. Singh - 7905278092")
P("Online Admission Form: https://admission.rsmt.ac.in/")

H2("Learning Outcomes")
P("Knowledge and curiosity in academic domains; employability skills; positive attitude; rational "
  "thinking and decision making; team management and leadership; ethical and moral values; ICT "
  "skills; sensitivity towards humanity, society and environment; traits of a responsible citizen.")

# ---- Scholarship ----
H1("Scholarship & Bank Finance")
P("Scholarships are available for students from weaker sections of society to finance or reduce "
  "the burden of professional education. Scholarships are provided by the Ministry of Social "
  "Welfare, Government of India.")

# ---- Hostel ----
H1("Hostel & Transportation")
P("RSMT provides comfortable, well-furnished hostel accommodation for girl students only.")
P("Hostel Rent: Rs. 15,000 per year + Rs. 8,000 refundable caution money = Rs. 23,000 per year per "
  "student on triple sharing basis (exclusive of meals). The hostel caters all three meals plus "
  "evening tea on all days of the week.")
P("Allotment: Limited seats, first come first served basis on advance deposit of one year hostel fee.")
P("Facilities: Triple-occupancy rooms with beds, study tables, chairs, partitioned almirah, fan, "
  "fluorescent tubes, balcony; RO drinking water; mess; high-capacity generator power backup and "
  "inverter; located within walking distance of RSMT.")
P("Rules: Night stay for visitors strictly prohibited; visitors not allowed in rooms; rooms must be "
  "kept locked; no unauthorised electric appliances; students arrange their own bedsheets, "
  "mattresses, pillows, locks, etc.")

# ---- Infrastructure ----
H1("Infrastructure")
H2("Computer Lab")
P("Wi-Fi powered campus with sophisticated, well-equipped, fully air-conditioned, state-of-the-art "
  "computer laboratories. More than 150 HP Intel Core i5-based PCs, spacious server room, 4 large "
  "labs. Programming languages taught: C++, Java, .NET. LED projectors for presentations and group "
  "discussions.")
P("Branded PCs/Laptops with SUN, IBM, DELL and HP servers connected via Ethernet LAN. Internet via "
  "100 MBPS dedicated leased line on fibre optics. Printing through high-speed Mono Laser Jet "
  "Network printers and scanners. Software: IBM SPSS, MS-Project, Oracle, SQL Server, Visual Studio.")
P("Network protected with Antivirus, Anti-Spam, Bandwidth Management and multiple gateways with "
  "Auto Fail-over. Entire campus has 50+ Smart Wi-Fi Access Points. Each student/faculty/staff "
  "gets an @rsmt.ac.in mail-id. Online UPS, multimedia computing, Windows XP/7 multi-OS.")

H2("Library")
P("Well-stocked library with 20,000+ books on management and computers. Separate reading room. "
  "Subscriptions to leading management/computer journals, business newspapers and current-affairs "
  "magazines. Fully computerised, centrally air-conditioned, 100+ reader seating capacity. "
  "Separate section for multimedia and digital resources. Rich source of Books, E-books, CDs, "
  "Project Reports, Case Studies, Reference Books, Journals and Periodicals. Online catalog "
  "search; members can suggest book purchases.")

H2("Other Facilities")
P("Seminar Hall, Health Care, Cafeteria, Hostel (girls), Sports complex, Guest House, on-campus "
  "Bank and Post Office. Wi-Fi enabled campus.")

# ---- Placement ----
H1("Training & Placement")
P("RSMT's Training and Placement Cell finds appropriate jobs for graduates and summer internships "
  "for students. The Center for Corporate Relations (CCR) acts as a nodal center for industry-"
  "academia interaction, organising MDPs, Consultancy, Research, In-company Training, industry "
  "visits, guest lectures, CEO Forums, quizzes, and alumni interactions.")
P("Skill Development: Communication, personality, business etiquette, decision making.")
P("Grooming & Etiquette: Personal grooming, business dressing & dining etiquette, telephonic and "
  "mailing etiquette.")
P("Personality Development Programs and Mock Interviews & Group Discussions are conducted regularly.")
P("Summer Training: MBA students undergo 6-8 week summer internships. MCA students undertake "
  "6-month technical internships in their specialisation.")

H2("Placement Contacts")
P("Email: placement@rsmt.ac.in, placementrsmt@gmail.com")
P("Placement Head: Dr. Garima Anand - +91 9695154222")

H2("Recent Placement Highlights")
P("MBA placements at: Bajaj Allianz, Aisshpra Gems, Learning Routes Ltd., PinClick Ltd., Flipkart, "
  "MindSeekers Technologies, SLMG Beverage, Rinex Technology, Prodesk IT Solutions, Utkarsh Bank.")

H2("List of Recruiters (selected)")
P("Finance: Power Finance Corp., Shriram Transport Finance, Bajaj Finance, Mahindra & Mahindra "
  "Financial Services, Muthoot Finance, HDB Finance, Cholamandalam, Tata Capital, L&T Finance, "
  "Aditya Birla Finance.")
P("International Business: Airports Authority of India, Bhartia International, C&S Electric, "
  "Cryobank International, DSS Communications, GO-AIR, Indian Airlines, Indorama, Ispat Industries, "
  "Jet Airways, Panacea Biotec, TCI.")
P("Human Resource: Apollo Hospitals, Bajaj Corp, Everest Industries, Hotel Sun & Sand, Indian "
  "Airlines, Infopro, Jet Airways, Tata Chemicals, Tata Indicom.")
P("Marketing: Vodafone, Bharti Airtel, Hindustan Unilever, Cadbury, Coca Cola India, Pepsico, ITC, "
  "Sony India, Tata Motors, Samsung, Nokia, Idea Cellular, P&G, Maruti Udyog, Colgate Palmolive, "
  "Tata Teleservices, Hero Motocorp, Nestle, LIC, Mahindra & Mahindra, LG Electronic, Hyundai, "
  "L'Oreal India, Volkswagen, Johnson & Johnson.")
P("Operations: Airtel, Samsung, Wipro, Amazon, P&G, Colgate-Palmolive, Johnson & Johnson, Uber, "
  "Flipkart, Cummins.")
P("IT Companies: TCS, Infosys, Wipro, HCL Technologies, Tech Mahindra, Oracle Financial Services, "
  "L&T Infotech, Mphasis, Mindtree, Hexaware, 3i Infotech, Cognizant, Collabera, CSC, Cybage, "
  "Cyient, Datamatics, Eclerx, Firstsource, Honeywell, HSBC GLT India, IGATE, KPIT Technologies, "
  "Mastek, Microland, Microsoft, NIIT Technologies, Nucleus Software, Persistent Systems, Polaris, "
  "Pramati, Quest Global, Ramco Systems, Rediff, Samsung India Software, Sasken, Sonata, "
  "Tata Interactive Systems, CMC Limited.")

# ---- Contact ----
H1("Contact Information")
P("Director's Office / Chairman's Office:")
P("Administrative Building, RSMT, Udai Pratap College Campus, Varanasi - 221003, Uttar Pradesh, India.")
P("Phone: +91-542-2280674, +91-542-2280641")
P("Email: rsmtvaranasi1999upes@gmail.com")
P("Website: https://www.rsmt.ac.in/")
P("Online Admission: https://admission.rsmt.ac.in/")

P("Social: Facebook (rsmt123), Twitter (rsmtvns1), LinkedIn (rsmt-varanasi-52b580102), YouTube (rsmtvns)")

# ---- Build ----
doc = SimpleDocTemplate(str(OUT), pagesize=A4,
                        leftMargin=2*cm, rightMargin=2*cm,
                        topMargin=2*cm, bottomMargin=2*cm,
                        title="RSMT College Information")
doc.build(story)
import os
print(f"Wrote {OUT} ({os.path.getsize(OUT)/1024:.1f} KB)")
