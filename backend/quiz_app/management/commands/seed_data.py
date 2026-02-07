from django.core.management.base import BaseCommand
from quiz_app.models import Concept, Question

class Command(BaseCommand):
    help = 'Γεμίζει τη βάση δεδομένων με πλούσιο υλικό για Python'

    def handle(self, *args, **kwargs):
        self.stdout.write('Ξεκινάει η εισαγωγή δεδομένων...')

        # --- 1. ΔΗΜΙΟΥΡΓΙΑ ΕΝΝΟΙΩΝ (CONCEPTS) ---
        c_vars, _ = Concept.objects.get_or_create(
            name="Variables & Data Types", 
            defaults={"description": "Μεταβλητές, Strings, Integers, Floats και Type Casting.", "remedial_resource": "https://www.w3schools.com/python/python_variables.asp"}
        )

        c_cond, _ = Concept.objects.get_or_create(
            name="Conditionals (If/Else)", 
            defaults={"description": "Έλεγχος ροής με if, elif, else και λογικούς τελεστές.", "remedial_resource": "https://www.w3schools.com/python/python_conditions.asp"}
        )

        c_loops, _ = Concept.objects.get_or_create(
            name="Loops (For & While)", 
            defaults={"description": "Επαναληπτικοί βρόχοι for, while και range().", "remedial_resource": "https://www.w3schools.com/python/python_for_loops.asp"}
        )

        c_lists, _ = Concept.objects.get_or_create(
            name="Lists", 
            defaults={"description": "Δημιουργία, προσπέλαση, μέθοδοι λιστών και slicing.", "remedial_resource": "https://www.w3schools.com/python/python_lists.asp"}
        )

        c_funcs, _ = Concept.objects.get_or_create(
            name="Functions", 
            defaults={"description": "Ορισμός, ορίσματα, return values και scope.", "remedial_resource": "https://www.w3schools.com/python/python_functions.asp"}
        )

        # --- 2. ΟΡΙΣΜΟΣ ΣΧΕΣΕΩΝ ---
        c_cond.prerequisites.add(c_vars)
        c_loops.prerequisites.add(c_cond)
        c_lists.prerequisites.add(c_vars)
        c_funcs.prerequisites.add(c_loops, c_lists)

        self.stdout.write('Ενημερώθηκαν οι έννοιες και οι σχέσεις.')

        # --- 3. ΔΗΜΙΟΥΡΓΙΑ ΕΡΩΤΗΣΕΩΝ (ΣΥΝΟΛΟ 20+) ---
        questions_data = [
            # === Variables & Data Types ===
            {"concept": c_vars, "type": "MC", "diff": "easy", "text": "Ποιος είναι ο σωστός τρόπος να ορίσεις μια μεταβλητή;", "code": "x = 5", "a": "int x = 5;", "b": "x = 5", "c": "dim x = 5", "d": "var x = 5", "correct": "B"},
            {"concept": c_vars, "type": "TF", "diff": "easy", "text": "Στην Python, δεν χρειάζεται να δηλώσεις τον τύπο της μεταβλητής.", "code": None, "a": "Σωστό", "b": "Λάθος", "correct": "A"},
            {"concept": c_vars, "type": "MC", "diff": "easy", "text": "Ποιο από τα παρακάτω είναι έγκυρο όνομα μεταβλητής;", "code": None, "a": "2myvar", "b": "my-var", "c": "my_var", "d": "my var", "correct": "C"},
            {"concept": c_vars, "type": "MC", "diff": "medium", "text": "Τι θα τυπώσει η εντολή;", "code": "x = '5'\ny = 2\nprint(x * y)", "a": "10", "b": "7", "c": "55", "d": "Error", "correct": "C"},
            {"concept": c_vars, "type": "TF", "diff": "medium", "text": "Η εντολή int('3.14') θα επιστρέψει το ακέραιο 3.", "code": None, "a": "Σωστό", "b": "Λάθος", "correct": "B"}, # Θα βγάλει error αν το string έχει τελεία

            # === Conditionals ===
            {"concept": c_cond, "type": "MC", "diff": "easy", "text": "Ποια λέξη κλειδί χρησιμοποιείται για το 'αλλιώς αν';", "code": None, "a": "else if", "b": "elseif", "c": "elif", "d": "if else", "correct": "C"},
            {"concept": c_cond, "type": "MC", "diff": "medium", "text": "Τι θα τυπωθεί;", "code": "a = 10\nb = 20\nif a > 5 and b < 15:\n  print('Yes')\nelse:\n  print('No')", "a": "Yes", "b": "No", "c": "Error", "d": "None", "correct": "B"},
            {"concept": c_cond, "type": "TF", "diff": "easy", "text": "Η indentarion (εσοχή) είναι υποχρεωτική στην Python μετά από if.", "code": None, "a": "Σωστό", "b": "Λάθος", "correct": "A"},
            {"concept": c_cond, "type": "MC", "diff": "medium", "text": "Ποιο σύμβολο σημαίνει 'Δεν είναι ίσο';", "code": None, "a": "<>", "b": "!=", "c": "=/=", "d": "not =", "correct": "B"},

            # === Loops ===
            {"concept": c_loops, "type": "MC", "diff": "medium", "text": "Τι θα τυπώσει ο κώδικας;", "code": "for x in range(3):\n  print(x)", "a": "1, 2, 3", "b": "0, 1, 2", "c": "0, 1, 2, 3", "d": "1, 2", "correct": "B"},
            {"concept": c_loops, "type": "TF", "diff": "easy", "text": "Η εντολή 'break' σταματάει αμέσως την εκτέλεση του Loop.", "code": None, "a": "Σωστό", "b": "Λάθος", "correct": "A"},
            {"concept": c_loops, "type": "MC", "diff": "hard", "text": "Τι θα τυπώσει;", "code": "i = 1\nwhile i < 6:\n  i += 1\nprint(i)", "a": "5", "b": "6", "c": "1", "d": "Infinite Loop", "correct": "B"},
            {"concept": c_loops, "type": "MC", "diff": "medium", "text": "Τι κάνει η range(2, 6);", "code": None, "a": "Παράγει: 2, 3, 4, 5, 6", "b": "Παράγει: 2, 3, 4, 5", "c": "Παράγει: 3, 4, 5", "d": "Παράγει: 2, 4, 6", "correct": "B"},

            # === Lists ===
            {"concept": c_lists, "type": "MC", "diff": "medium", "text": "Ποιο είναι το αποτέλεσμα;", "code": "mylist = ['apple', 'banana', 'cherry']\nprint(mylist[-1])", "a": "apple", "b": "banana", "c": "cherry", "d": "Error", "correct": "C"},
            {"concept": c_lists, "type": "MC", "diff": "easy", "text": "Πώς προσθέτεις στοιχείο στο τέλος λίστας;", "code": None, "a": "add()", "b": "insert()", "c": "append()", "d": "push()", "correct": "C"},
            {"concept": c_lists, "type": "MC", "diff": "hard", "text": "Τι θα δώσει το slicing;", "code": "nums = [10, 20, 30, 40, 50]\nprint(nums[1:3])", "a": "[20, 30]", "b": "[10, 20, 30]", "c": "[20, 30, 40]", "d": "[30, 40]", "correct": "A"},
            {"concept": c_lists, "type": "TF", "diff": "medium", "text": "Οι λίστες στην Python μπορούν να περιέχουν στοιχεία διαφορετικού τύπου.", "code": "my_list = [1, 'hello', 3.14]", "a": "Σωστό", "b": "Λάθος", "correct": "A"},

            # === Functions ===
            {"concept": c_funcs, "type": "MC", "diff": "easy", "text": "Ποια λέξη κλειδί ορίζει συνάρτηση;", "code": None, "a": "func", "b": "def", "c": "function", "d": "define", "correct": "B"},
            {"concept": c_funcs, "type": "MC", "diff": "medium", "text": "Τι θα επιστρέψει;", "code": "def add(a, b=5):\n  return a + b\nprint(add(3))", "a": "8", "b": "3", "c": "Error", "d": "53", "correct": "A"},
            {"concept": c_funcs, "type": "TF", "diff": "hard", "text": "Μια συνάρτηση μπορεί να επιστρέψει πολλές τιμές ταυτόχρονα.", "code": "return x, y", "a": "Σωστό", "b": "Λάθος", "correct": "A"}, # Επιστρέφει tuple
            {"concept": c_funcs, "type": "MC", "diff": "medium", "text": "Ποιο είναι το scope της μεταβλητής x;", "code": "def myFunc():\n  x = 10\nprint(x)", "a": "Global", "b": "Local", "c": "Universal", "d": "Error (undefined)", "correct": "D"}
        ]

        # Εισαγωγή στη βάση (χωρίς διπλότυπα)
        for q in questions_data:
            Question.objects.get_or_create(
                text=q["text"],
                defaults={
                    "concept": q["concept"],
                    "question_type": q["type"],
                    "code_snippet": q["code"],
                    "difficulty": q["diff"],
                    "option_a": q.get("a"),
                    "option_b": q.get("b"),
                    "option_c": q.get("c"),
                    "option_d": q.get("d"),
                    "correct_option": q["correct"]
                }
            )

        self.stdout.write(self.style.SUCCESS(f'ΕΠΙΤΥΧΙΑ! Προστέθηκαν {len(questions_data)} ερωτήσεις στη βάση.'))