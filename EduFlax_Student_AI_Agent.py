#!/usr/bin/env python3
"""
EduFlax - Your Personal AI Student Helper Agent
Built by Flax. Your personal AI study companion.
A fun, helpful CLI-based AI agent to assist students with studying.

Run it with: python EduFlax_Student_AI_Agent.py

This is the MVP version (demo AI):
- Rule-based + smart templates for reliable help
- SymPy for real math solving
- Expandable knowledge base
- In a full version, plug in any LLM (GPT, Groq, Claude, local models, etc.) for unlimited smart answers.
  See comments at the bottom for how to upgrade it easily.

Features:
1. Smart Q&A and General Help
2. Personalized Study Plan Generator
3. Interactive Quiz Creator & Grader
4. Concept Explainer (with analogies)
5. Math Problem Solver (powered by SymPy)
6. Quick Study Tips & Motivation
7. Student News Digest (EduNews mode - simulated for now)
8. Exit

Let's help students crush their goals! 🚀
"""

import sys
import random
from datetime import datetime, timedelta

# Try to import SymPy for math superpower
try:
    import sympy as sp
    from sympy import symbols, solve, simplify, diff, integrate, Symbol
    HAS_SYMPY = True
except ImportError:
    HAS_SYMPY = False
    print("Note: SymPy not available. Math solver will be limited. (pip install sympy to enable)")

# ============== KNOWLEDGE BASE & TEMPLATES ==============

CONCEPT_EXPLANATIONS = {
    "photosynthesis": {
        "simple": "Photosynthesis is how plants make their own food using sunlight, water, and carbon dioxide. It's like a solar-powered kitchen inside the plant's leaves!",
        "detailed": "In photosynthesis, plants convert light energy into chemical energy. The overall equation is: 6CO₂ + 6H₂O + light → C₆H₁₂O₆ + 6O₂. It happens in chloroplasts using chlorophyll. Light-dependent reactions make ATP and NADPH, then Calvin cycle fixes CO2 into glucose. This process produces the oxygen we breathe and is the base of most food chains.",
        "analogy": "Think of it like a solar panel (chlorophyll) charging a battery (glucose) while releasing oxygen as exhaust. Without it, no plants, no oxygen, no us!",
        "example": "Example: A tree in your backyard is doing this right now, turning sunlight into sugar for growth and releasing oxygen for you to breathe."
    },
    "derivative": {
        "simple": "A derivative tells you the 'rate of change' or slope of a function at any point. It's how fast something is changing.",
        "detailed": "In calculus, the derivative of f(x) is the limit as h→0 of [f(x+h) - f(x)] / h. It gives the instantaneous rate of change. Rules: power rule (x^n → n*x^{n-1}), product rule, chain rule. Used everywhere: physics (velocity = derivative of position), economics, machine learning (gradients).",
        "analogy": "Imagine driving a car. Your speedometer shows the derivative of your position over time – how fast your distance is changing right now.",
        "example": "For f(x) = x², the derivative f'(x) = 2x. So at x=3, the slope is 6 (steep upward)."
    },
    "ww2 causes": {
        "simple": "World War II was caused by a mix of unresolved anger from WWI, economic crisis (Great Depression), rise of aggressive dictators like Hitler, and failed diplomacy.",
        "detailed": "Main causes: 1) Treaty of Versailles humiliated Germany (reparations, land loss). 2) Great Depression caused instability and extremism. 3) Rise of fascism: Hitler (Germany), Mussolini (Italy), militarism in Japan. 4) Expansionism: Japan invaded China, Italy Ethiopia, Germany Austria/Czechoslovakia. 5) Appeasement policy by Britain/France failed. 6) Invasion of Poland by Germany on Sept 1, 1939 triggered declarations of war.",
        "analogy": "Like a pressure cooker: WWI treaty + economic crash built up steam, dictators turned up the heat, and invasion of Poland blew the lid off.",
        "example": "Hitler's invasion of Poland was the spark, but the fuel was built over 20 years of resentment and bad decisions after WWI."
    },
    "what is ai": {
        "simple": "AI (Artificial Intelligence) is when computers are programmed to do tasks that normally require human intelligence, like learning, reasoning, understanding language, or recognizing patterns.",
        "detailed": "AI includes machine learning (systems improve from data), deep learning (neural networks inspired by brain), NLP (understanding human language), computer vision, and generative AI (like me, EduFlax!). Modern AI like large language models are trained on massive text data to predict and generate human-like responses. It's used in recommendation systems (Netflix), self-driving cars, medical diagnosis, and now education tools!",
        "analogy": "AI is like teaching a very fast, very patient student (the computer) millions of examples so it can guess the right answer or create new things, without being explicitly told every rule.",
        "example": "When you ask ChatGPT or EduFlax a question, the AI has 'read' billions of pages of text and learned patterns to give helpful answers."
    },
    "supply and demand": {
        "simple": "Supply and demand is the basic rule of markets: when something is wanted more (high demand) and there's not enough (low supply), the price goes up. When there's too much supply or low demand, price goes down.",
        "detailed": "The law of demand: higher price → lower quantity demanded (downward curve). Law of supply: higher price → higher quantity supplied (upward curve). Equilibrium is where supply = demand. Shifts: increase in demand (right shift) raises both price and quantity. Used to understand everything from housing prices to why iPhones cost what they do.",
        "analogy": "Think of concert tickets. If a popular artist announces a show in a small venue (low supply, high demand), scalpers charge crazy prices. If it's a huge stadium with many tickets (high supply), prices are lower.",
        "example": "During COVID, demand for masks and sanitizers skyrocketed while supply was limited → prices rose sharply until production caught up."
    }
}

# Sample quizzes (expandable)
QUIZZES = {
    "python basics": [
        {"q": "What does 'print(\"Hello\")' do in Python?", "options": ["A) Adds two numbers", "B) Displays text on screen", "C) Creates a variable", "D) Ends the program"], "answer": "B", "explanation": "print() is a built-in function that outputs text to the console."},
        {"q": "Which symbol is used for comments in Python?", "options": ["A) //", "B) #", "C) /* */", "D) --"], "answer": "B", "explanation": "# starts a single-line comment. Everything after it on that line is ignored."},
        {"q": "What is the output of: len([1, 2, 3]) ?", "options": ["A) 1", "B) 2", "C) 3", "D) Error"], "answer": "C", "explanation": "len() returns the number of items in a list. Here there are 3 items."},
        {"q": "How do you create a function in Python?", "options": ["A) function myFunc()", "B) def myFunc():", "C) create myFunc()", "D) func myFunc()"], "answer": "B", "explanation": "Use the 'def' keyword followed by the function name and colon."}
    ],
    "algebra basics": [
        {"q": "Solve for x: 2x + 5 = 13", "options": ["A) x=3", "B) x=4", "C) x=9", "D) x=18"], "answer": "B", "explanation": "Subtract 5: 2x=8. Divide by 2: x=4."},
        {"q": "What is the slope of the line y = 3x - 7?", "options": ["A) -7", "B) 3", "C) 0", "D) 1/3"], "answer": "B", "explanation": "In y = mx + b form, m is the slope. Here m=3."},
        {"q": "Factor: x² - 9", "options": ["A) (x-3)(x+3)", "B) (x-9)(x+1)", "C) (x-3)^2", "D) x(x-9)"], "answer": "A", "explanation": "Difference of squares: a² - b² = (a-b)(a+b). Here a=x, b=3."},
        {"q": "If f(x) = x², what is f(5)?", "options": ["A) 10", "B) 25", "C) 52", "D) 7"], "answer": "B", "explanation": "5 squared = 25."}
    ],
    "biology basics": [
        {"q": "What is the powerhouse of the cell?", "options": ["A) Nucleus", "B) Mitochondria", "C) Ribosome", "D) Cell membrane"], "answer": "B", "explanation": "Mitochondria produce ATP (energy) through cellular respiration."},
        {"q": "What molecule carries genetic information?", "options": ["A) Protein", "B) Carbohydrate", "C) DNA", "D) Lipid"], "answer": "C", "explanation": "DNA (deoxyribonucleic acid) stores the genetic blueprint."},
        {"q": "Which process do plants use to make food?", "options": ["A) Respiration", "B) Photosynthesis", "C) Digestion", "D) Fermentation"], "answer": "B", "explanation": "Photosynthesis converts light, CO2 and water into glucose and oxygen."},
        {"q": "What is the basic unit of life?", "options": ["A) Atom", "B) Molecule", "C) Cell", "D) Organ"], "answer": "C", "explanation": "The cell is the smallest structural and functional unit of living organisms."}
    ]
}

# Simulated Student News (EduNews) - plausible for June 2026
STUDENT_NEWS = [
    {
        "headline": "New AI Tutors Personalized for Every Learning Style Launch in Schools Worldwide",
        "summary": "Major edtech companies rolled out adaptive AI tutors that analyze how each student learns best (visual, auditory, kinesthetic) and adjust explanations in real-time. Early results show 30% improvement in test scores for math and science.",
        "why_it_matters": "This is huge for students who struggle with one-size-fits-all teaching. The future of education is becoming truly personal."
    },
    {
        "headline": "Climate Science Kits + Student Data Projects Win Big at 2026 Global Youth Innovation Fair",
        "summary": "Teen teams from 45 countries presented projects using real satellite data and low-cost sensors to track local climate impacts. Winners received funding and mentorship from NASA and leading universities.",
        "why_it_matters": "Students aren't just learning about climate change — they're actively contributing real research. Hands-on science at its best."
    },
    {
        "headline": "Mental Health Breaks Now Mandatory in School Schedules Across Several Countries",
        "summary": "Following strong student advocacy and new research on focus/ burnout, many education systems are building in 10-15 minute 'reset blocks' with mindfulness, movement, or just quiet time. Teachers report better engagement in afternoon classes.",
        "why_it_matters": "Your brain needs recovery time to learn effectively. This validates what many students have been saying for years."
    }
]

def print_header():
    print("\033[96m" + "="*60)
    print("   🎓  EduFlax - Your Personal AI Student Helper Agent  🎓")
    print("   Powered by Flax AI  |  v0.1 MVP")
    print("="*60 + "\033[0m")
    print("Hey there! I'm here to help you study smarter, not harder.")
    print("Ask me anything academic, plan your week, test yourself, or get motivated.\n")

def print_menu():
    print("\033[93m" + "-"*50)
    print("What would you like to do today?")
    print("-"*50 + "\033[0m")
    print("  1. 💬  Ask a question / General Q&A")
    print("  2. 📅  Generate a personalized Study Plan")
    print("  3. 📝  Take or Create a Quiz (test yourself)")
    print("  4. 🧠  Explain a tough Concept (with analogies)")
    print("  5. 🔢  Math Problem Solver (real SymPy power)")
    print("  6. 💪  Quick Study Tips & Motivation Boost")
    print("  7. 📰  Student News Digest (EduNews mode)")
    print("  8. ❌  Exit EduFlax")
    print("\033[93m" + "-"*50 + "\033[0m")

def get_input(prompt):
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        print("\nThanks for studying with me! Keep crushing it. 👋")
        sys.exit(0)

# ============== FEATURE FUNCTIONS ==============

def qa_session():
    print("\n\033[92m[ Q&A Mode ]\033[0m Ask me anything about your studies!")
    print("Examples: 'Explain mitosis', 'How do I remember formulas?', 'What's the best way to study history?'")
    print("Type 'menu' to go back or 'exit' to quit.\n")
    
    while True:
        q = get_input("Your question: ").lower()
        if q in ['menu', 'back', 'exit', 'quit']:
            break
        
        # Simple keyword-based smart routing (demo of intent detection)
        if any(word in q for word in ['study plan', 'schedule', 'plan my', 'how should i study']):
            print("Sounds like you want a study plan! Let's switch to that...")
            generate_study_plan()
            break
        elif any(word in q for word in ['quiz', 'test me', 'practice questions']):
            print("Quiz time! Switching to quiz mode...")
            create_quiz()
            break
        elif any(word in q for word in ['explain', 'what is', 'how does', 'tell me about']):
            # Try to find concept
            for concept in CONCEPT_EXPLANATIONS:
                if concept in q or any(word in q for word in concept.split()):
                    explain_concept(concept)
                    return
            print("Good question! In the full LLM version I'd give a perfect tailored answer.")
            print("For now, try the 'Explain a Concept' menu option for deep dives, or ask something more specific.")
        else:
            # Default helpful response
            print("\n\033[94mEduFlax thinks...\033[0m")
            print("That's a solid question! In a production version with a real LLM (GPT, Groq, Claude, etc.), I'd give you a detailed, personalized explanation with examples and follow-up questions.")
            print("\nQuick tip while we're in demo mode: Break big topics into small chunks, use active recall (test yourself), and teach it to someone (or your pet).")
            print("Want me to explain a specific concept? Use option 4 or rephrase your question.\n")

def generate_study_plan():
    print("\n\033[92m[ Study Plan Generator ]\033[0m Let's build you a realistic plan!")
    name = get_input("What's your name? (or nickname): ") or "Student"
    print(f"\nNice to meet you, {name}! Let's customize this.")

    print("\nWhat are your main subjects right now? (comma separated)")
    print("Examples: Math, Physics, History, English, Biology, Chemistry, CS")
    subjects_input = get_input("Subjects: ") or "Math, Science, History"
    subjects = [s.strip().title() for s in subjects_input.split(",")]

    try:
        hours = float(get_input("How many hours can you realistically study per day? (e.g. 3.5): ") or "3")
    except ValueError:
        hours = 3.0

    goal = get_input("What's your main goal? (e.g. 'Ace final exams in 4 weeks', 'Improve math grade', 'Learn Python for fun'): ") or "Improve overall grades"

    weeks = 2
    try:
        weeks_input = get_input("How many weeks until your main deadline/goal? (default 2): ") or "2"
        weeks = max(1, int(weeks_input))
    except:
        pass

    print(f"\n\033[96m{'='*55}")
    print(f"  📅 PERSONALIZED STUDY PLAN FOR {name.upper()}")
    print(f"{'='*55}\033[0m")
    print(f"Goal: {goal}")
    print(f"Daily study time: {hours} hours")
    print(f"Timeline: {weeks} weeks")
    print(f"Focus subjects: {', '.join(subjects)}")
    print()

    # Simple smart allocation
    daily_subjects = min(len(subjects), 3)
    time_per_subject = round(hours / daily_subjects, 1)

    print("\033[93mRecommended Weekly Structure:\033[0m")
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    
    for i, day in enumerate(days):
        if i < 5:  # Weekdays - focused
            plan = f"  • {day}: "
            for j, subj in enumerate(subjects[:daily_subjects]):
                plan += f"{subj} ({time_per_subject}h) + "
            plan = plan.rstrip(" + ") + " | 25min Pomodoro x 4-6 sessions"
            print(plan)
        elif i == 5:  # Saturday - review + light
            print(f"  • Saturday: Review weak topics from the week ({round(hours*0.7,1)}h) + 1 fun/creative session")
        else:  # Sunday - rest + planning
            print(f"  • Sunday: Light review or practice test ({round(hours*0.5,1)}h) + Plan next week + Rest day (important!)")

    print("\n\033[92mPro Tips for Success:\033[0m")
    print("• Use Pomodoro: 25 min focus + 5 min break. After 4 rounds → longer break.")
    print("• Active recall > passive reading. Close the book and test yourself.")
    print("• Teach the material out loud (even to your mirror or dog).")
    print("• Track progress daily – small wins build momentum.")
    print("• Sleep 7-9 hours. Your brain consolidates memories while you sleep!")
    print(f"\nYou've got this, {name}! Consistency beats cramming every time. 💪")
    print("Want me to adjust this plan or add specific topics? Just say the word.\n")

def create_quiz():
    print("\n\033[92m[ Quiz Master ]\033[0m Time to test your knowledge!")
    print("Available topics:", ", ".join(QUIZZES.keys()).title())
    
    topic = get_input("\nChoose a topic (or type 'random'): ").lower().strip()
    
    if topic == "random" or topic not in QUIZZES:
        topic = random.choice(list(QUIZZES.keys()))
        print(f"Randomly selected: {topic.title()}")
    
    if topic not in QUIZZES:
        print("Sorry, that topic isn't in the demo bank yet. Try one of the available ones.")
        return
    
    questions = QUIZZES[topic]
    print(f"\n--- {topic.upper()} QUIZ ({len(questions)} questions) ---")
    print("Type the letter of your answer (A/B/C/D). No cheating! 😎\n")
    
    score = 0
    for i, q in enumerate(questions, 1):
        print(f"Q{i}. {q['q']}")
        for opt in q['options']:
            print(f"   {opt}")
        
        user_ans = get_input("Your answer (A/B/C/D): ").upper().strip()
        correct = q['answer']
        
        if user_ans == correct:
            print("\033[92m✓ Correct! " + q['explanation'] + "\033[0m\n")
            score += 1
        else:
            print(f"\033[91m✗ Not quite. Correct answer: {correct}. {q['explanation']}\033[0m\n")
    
    percentage = (score / len(questions)) * 100
    print(f"\033[96m{'='*40}")
    print(f"  FINAL SCORE: {score}/{len(questions)} ({percentage:.0f}%) ")
    print(f"{'='*40}\033[0m")
    
    if percentage == 100:
        print("🔥 PERFECT SCORE! You're a legend. Teach me next time!")
    elif percentage >= 75:
        print("💪 Solid work! A few more practice rounds and you'll be unstoppable.")
    elif percentage >= 50:
        print("👍 Good effort! Review the explanations and try again soon.")
    else:
        print("📚 No worries – this is how we learn. Let's go over the concepts together using option 4.")
    
    print("\nWant another quiz or different topic? Choose option 3 again.\n")

def explain_concept(concept_key=None):
    print("\n\033[92m[ Concept Explainer ]\033[0m I break down tough ideas simply + with analogies.")
    
    if not concept_key:
        print("Available demo concepts:", ", ".join(CONCEPT_EXPLANATIONS.keys()))
        concept_input = get_input("\nWhat concept do you want explained? (e.g. photosynthesis, derivative): ").lower().strip()
        
        # Fuzzy match
        concept_key = None
        for key in CONCEPT_EXPLANATIONS:
            if key in concept_input or concept_input in key:
                concept_key = key
                break
        
        if not concept_key:
            print(f"\nI don't have '{concept_input}' in my current demo knowledge base yet.")
            print("But here's general advice: Start with the 'what is it in one sentence', then 'why it matters', then examples.")
            print("Try one of the available concepts or ask me to add more in future versions!")
            return
    
    data = CONCEPT_EXPLANATIONS[concept_key]
    
    print(f"\n\033[96m=== {concept_key.upper().replace('_', ' ')} ===\033[0m")
    print(f"\033[93mSimple version:\033[0m {data['simple']}")
    print(f"\n\033[93mMore detailed:\033[0m {data['detailed']}")
    print(f"\n\033[93mAnalogy:\033[0m {data['analogy']}")
    print(f"\n\033[93mReal-world example:\033[0m {data['example']}")
    print("\nWant me to explain it even simpler, give practice questions, or move to another concept?\n")

def math_solver():
    print("\n\033[92m[ Math Solver ]\033[0m Powered by SymPy (real symbolic math)")
    
    if not HAS_SYMPY:
        print("SymPy is not installed in this environment. Basic calculator mode only.")
        expr = get_input("Enter a simple math expression (e.g. 2 + 2 * 3): ")
        try:
            result = eval(expr)  # Safe-ish for demo
            print(f"Result: {result}")
        except:
            print("Couldn't compute that. Try basic arithmetic.")
        return
    
    print("I can solve equations, simplify expressions, take derivatives, and more!")
    print("Examples:")
    print("  - Solve equation: x**2 - 5*x + 6 = 0")
    print("  - Simplify: (x**2 - 1)/(x - 1)")
    print("  - Derivative: diff(x**3, x)")
    print("  - Integrate: integrate(x**2, x)")
    print("\nType 'menu' to go back.\n")
    
    while True:
        user_input = get_input("Enter math problem or expression: ").strip()
        if user_input.lower() in ['menu', 'back', 'exit']:
            break
        
        x = symbols('x')
        try:
            if '=' in user_input:
                # Solve equation
                left, right = user_input.split('=', 1)
                eq = sp.sympify(left) - sp.sympify(right)
                solutions = solve(eq, x)
                print(f"\033[92mSolutions for {user_input}:\033[0m {solutions}")
            elif user_input.lower().startswith('diff'):
                # e.g. diff(x**2 + 3*x, x)
                expr = sp.sympify(user_input.split('diff(')[1].rstrip(')'))
                result = diff(expr, x)
                print(f"\033[92mDerivative:\033[0m {result}")
            elif user_input.lower().startswith('integrate'):
                expr = sp.sympify(user_input.split('integrate(')[1].rstrip(')'))
                result = integrate(expr, x)
                print(f"\033[92mIntegral:\033[0m {result} + C")
            else:
                # Simplify or evaluate
                expr = sp.sympify(user_input)
                simplified = simplify(expr)
                print(f"\033[92mSimplified / Result:\033[0m {simplified}")
        except Exception as e:
            print(f"\033[91mCouldn't parse or solve that. Error: {e}\033[0m")
            print("Try simpler expressions like 'x**2 - 4' or 'solve x**2 + 2*x - 8 = 0'")
        print()

def study_tips():
    print("\n\033[92m[ Motivation & Study Tips ]\033[0m Let's get you in the zone!")
    
    tips = [
        "The 2-minute rule: If a task takes less than 2 minutes, do it now. Builds momentum.",
        " Feynman Technique: Explain the topic in simple words as if teaching a 10-year-old. Gaps in understanding become obvious.",
        "Spaced repetition beats cramming. Review material after 1 day, 3 days, 1 week, 1 month.",
        "Your environment matters. Same place + same time = brain gets into 'study mode' faster.",
        "Sleep is part of studying. 7-9 hours helps memory consolidation. All-nighters destroy retention.",
        "Exercise before studying can improve focus for 1-2 hours afterward (even a 10-min walk).",
        "Reward yourself after focused sessions. Small dopamine hits keep you going.",
        "Track your 'wins' daily. Even 'I studied 45 focused minutes' counts. Progress compounds."
    ]
    
    print("\nHere's a powerful tip for you today:")
    print(f"  → {random.choice(tips)}")
    
    motivational = [
        "Every expert was once a beginner. You're already ahead by showing up.",
        "The discomfort of learning is temporary. The regret of not trying lasts forever.",
        "Small consistent effort > occasional heroic effort. Show up daily.",
        "Your future self is counting on the work you're doing right now. Make them proud.",
        "It's okay to struggle. That's literally how your brain grows new connections."
    ]
    print(f"\n\033[93mMotivation boost:\033[0m {random.choice(motivational)}")
    print("\nYou've got the tools. Now go use them. I'm rooting for you! 🔥\n")

def student_news_digest():
    print("\n\033[92m[ EduNews Digest ]\033[0m What's happening in education & student world (June 2026)")
    print("Note: This is simulated data for the demo. In a full version, I'd pull real-time relevant news.\n")
    
    for i, news in enumerate(STUDENT_NEWS, 1):
        print(f"\033[96m{i}. {news['headline']}\033[0m")
        print(f"   {news['summary']}")
        print(f"   \033[93mWhy it matters for students:\033[0m {news['why_it_matters']}\n")
    
    print("Want deeper dives on any of these topics or how they connect to what you're studying? Just ask!\n")

# ============== MAIN LOOP ==============

def main():
    print_header()
    
    while True:
        print_menu()
        choice = get_input("\nEnter your choice (1-8): ").strip()
        
        if choice == "1":
            qa_session()
        elif choice == "2":
            generate_study_plan()
        elif choice == "3":
            create_quiz()
        elif choice == "4":
            explain_concept()
        elif choice == "5":
            math_solver()
        elif choice == "6":
            study_tips()
        elif choice == "7":
            student_news_digest()
        elif choice == "8" or choice.lower() in ["exit", "quit", "bye"]:
            print("\n\033[96mThanks for using EduFlax! Remember: consistent small steps lead to big results.")
            print("Come back anytime you need help studying. You've got this! 🚀\033[0m\n")
            break
        else:
            print("\033[91mInvalid choice. Please pick a number from 1 to 8.\033[0m")
        
        input("\nPress Enter to return to the main menu...")

if __name__ == "__main__":
    main()
