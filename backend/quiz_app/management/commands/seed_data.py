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

        # --- 3. ΔΗΜΙΟΥΡΓΙΑ ΕΡΩΤΗΣΕΩΝ ---
        questions_data = [
            # === Variables & Data Types ===
            {
                "concept": c_vars, "type": "MC", "diff": "easy", 
                "text": "Ποιος είναι ο σωστός τρόπος να ορίσεις μια μεταβλητή;", "code": "x = 5", "a": "int x = 5;", "b": "x = 5", "c": "dim x = 5", "d": "var x = 5", "correct": "B", 
                "explanation": "Στην Python δεν χρειάζεται να δηλώσουμε τον τύπο της μεταβλητής (π.χ. int ή var). Απλά γράφουμε το όνομα και την τιμή.",
                "remedial_resource": "https://www.w3schools.com/python/python_variables.asp",
                "video_resource": "https://www.youtube.com/watch?v=khKv-8q7YmY"
            },
            {
                "concept": c_vars, "type": "TF", "diff": "easy", 
                "text": "Στην Python, δεν χρειάζεται να δηλώσεις τον τύπο της μεταβλητής.", "code": None, "a": "Σωστό", "b": "Λάθος", "correct": "A", 
                "explanation": "Η Python είναι dynamically typed γλώσσα, οπότε καταλαβαίνει αυτόματα τον τύπο από την τιμή που της δίνεις.",
                "remedial_resource": "https://www.w3schools.com/python/python_variables.asp",
                "video_resource": "https://www.youtube.com/watch?v=khKv-8q7YmY"
            },
            {
                "concept": c_vars, "type": "MC", "diff": "easy", 
                "text": "Ποιο από τα παρακάτω είναι έγκυρο όνομα μεταβλητής;", "code": None, "a": "2myvar", "b": "my-var", "c": "my_var", "d": "my var", "correct": "C", 
                "explanation": "Τα ονόματα μεταβλητών δεν μπορούν να ξεκινούν με αριθμό, ούτε να περιέχουν κενά ή παύλες. Το underscore (_) επιτρέπεται.",
                "remedial_resource": "https://www.w3schools.com/python/python_variables_names.asp",
                "video_resource": "https://www.youtube.com/watch?v=khKv-8q7YmY"
            },
            {
                "concept": c_vars, "type": "MC", "diff": "medium", 
                "text": "Τι θα τυπώσει η εντολή;", "code": "x = '5'\ny = 2\nprint(x * y)", "a": "10", "b": "7", "c": "55", "d": "Error", "correct": "C", 
                "explanation": "Ο πολλαπλασιασμός ενός string ('5') με έναν ακέραιο (2) απλά επαναλαμβάνει το string 2 φορές.",
                "remedial_resource": "https://www.w3schools.com/python/python_datatypes.asp",
                "video_resource": "https://www.youtube.com/watch?v=k9TUPpGqYTo"
            },
            {
                "concept": c_vars, "type": "TF", "diff": "medium", 
                "text": "Η εντολή int('3.14') θα επιστρέψει το ακέραιο 3.", "code": None, "a": "Σωστό", "b": "Λάθος", "correct": "B", 
                "explanation": "Λάθος. Η μετατροπή ενός string που περιέχει δεκαδικό σε int πετάει ValueError. Θα έπρεπε πρώτα να γίνει float('3.14').",
                "remedial_resource": "https://www.w3schools.com/python/python_casting.asp",
                "video_resource": "https://www.youtube.com/watch?v=gCCVsvgR2KU"
            },
            {
                "concept": c_vars, "type": "MC", "diff": "easy", 
                "text": "Πώς ελέγχουμε τον τύπο μιας μεταβλητής x;", "code": None, "a": "type(x)", "b": "typeof(x)", "c": "x.type()", "d": "check(x)", "correct": "A", 
                "explanation": "Η ενσωματωμένη συνάρτηση type() επιστρέφει τον τύπο δεδομένων οποιουδήποτε αντικειμένου στην Python.",
                "remedial_resource": "https://www.w3schools.com/python/python_datatypes.asp",
                "video_resource": "https://www.youtube.com/watch?v=k9TUPpGqYTo"
            },
            {
                "concept": c_vars, "type": "MC", "diff": "hard", 
                "text": "Ποιο είναι το αποτέλεσμα της διαίρεσης 5 // 2;", "code": None, "a": "2.5", "b": "2", "c": "3", "d": "1", "correct": "B", 
                "explanation": "Ο τελεστής // κάνει 'ακέραια διαίρεση' (floor division), κόβοντας το δεκαδικό μέρος.",
                "remedial_resource": "https://www.w3schools.com/python/python_operators.asp",
                "video_resource": "https://www.youtube.com/watch?v=v5MR5JnKcZI"
            },
            {
                "concept": c_vars, "type": "TF", "diff": "medium", 
                "text": "Η Python διαχωρίζει τα πεζά από τα κεφαλαία γράμματα (case-sensitive).", "code": None, "a": "Σωστό", "b": "Λάθος", "correct": "A", 
                "explanation": "Σωστό! Η μεταβλητή 'Age' είναι διαφορετική από τη μεταβλητή 'age'.",
                "remedial_resource": "https://www.w3schools.com/python/python_variables_names.asp",
                "video_resource": "https://www.youtube.com/watch?v=khKv-8q7YmY"
            },

            # === Conditionals ===
            {
                "concept": c_cond, "type": "MC", "diff": "easy", 
                "text": "Ποια λέξη κλειδί χρησιμοποιείται για το 'αλλιώς αν';", "code": None, "a": "else if", "b": "elseif", "c": "elif", "d": "if else", "correct": "C", 
                "explanation": "Στην Python, συντομεύουμε το 'else if' γράφοντας 'elif'.",
                "remedial_resource": "https://www.w3schools.com/python/python_conditions.asp",
                "video_resource": "https://www.youtube.com/watch?v=Zp5MuPOtsME"
            },
            {
                "concept": c_cond, "type": "MC", "diff": "medium", 
                "text": "Τι θα τυπωθεί;", "code": "a = 10\nb = 20\nif a > 5 and b < 15:\n  print('Yes')\nelse:\n  print('No')", "a": "Yes", "b": "No", "c": "Error", "d": "None", "correct": "B", 
                "explanation": "Η συνθήκη b < 15 είναι ψευδής (20 < 15). Επειδή έχουμε 'and', πρέπει ΚΑΙ οι δύο να ισχύουν, οπότε πάμε στο else.",
                "remedial_resource": "https://www.w3schools.com/python/python_conditions.asp",
                "video_resource": "https://www.youtube.com/watch?v=DZwmZ8Usvnk"
            },
            {
                "concept": c_cond, "type": "TF", "diff": "easy", 
                "text": "Η εσοχή (indentation) είναι υποχρεωτική στην Python μετά από if.", "code": None, "a": "Σωστό", "b": "Λάθος", "correct": "A", 
                "explanation": "Η Python χρησιμοποιεί τα κενά (εσοχές) για να καταλάβει πού αρχίζει και πού τελειώνει ένα block κώδικα.",
                "remedial_resource": "https://www.w3schools.com/python/python_syntax.asp",
                "video_resource": "https://www.youtube.com/watch?v=Zp5MuPOtsME"
            },
            {
                "concept": c_cond, "type": "MC", "diff": "medium", 
                "text": "Ποιο σύμβολο σημαίνει 'Δεν είναι ίσο';", "code": None, "a": "<>", "b": "!=", "c": "=/=", "d": "not =", "correct": "B", 
                "explanation": "Το θαυμαστικό με το ίσον (!=) χρησιμοποιείται για να ελέγξουμε αν δύο τιμές είναι άνισες.",
                "remedial_resource": "https://www.w3schools.com/python/python_operators.asp",
                "video_resource": "https://www.youtube.com/watch?v=v5MR5JnKcZI"
            },
            {
                "concept": c_cond, "type": "MC", "diff": "hard", 
                "text": "Τι θα τυπωθεί;", "code": "x = 0\nif x:\n  print('True')\nelse:\n  print('False')", "a": "True", "b": "False", "c": "Error", "d": "Τίποτα", "correct": "B", 
                "explanation": "Στην Python, το 0 θεωρείται 'Falsy' (ψευδές) σε συνθήκες if, οπότε εκτελείται το else.",
                "remedial_resource": "https://www.freecodecamp.org/news/truthy-and-falsy-values-in-python/",
                "video_resource": "https://www.youtube.com/watch?v=Zp5MuPOtsME"
            },
            {
                "concept": c_cond, "type": "MC", "diff": "medium", 
                "text": "Ποιος λογικός τελεστής επιστρέφει True αν τουλάχιστον μία συνθήκη είναι True;", "code": None, "a": "and", "b": "or", "c": "not", "d": "xor", "correct": "B", 
                "explanation": "Ο τελεστής 'or' αρκεί να βρει έστω μία αληθή συνθήκη για να επιστρέψει True.",
                "remedial_resource": "https://www.w3schools.com/python/python_operators.asp",
                "video_resource": "https://www.youtube.com/watch?v=DZwmZ8Usvnk"
            },
            {
                "concept": c_cond, "type": "TF", "diff": "medium", 
                "text": "Μπορούμε να έχουμε μόνο ένα 'elif' μέσα σε μια δομή if.", "code": None, "a": "Σωστό", "b": "Λάθος", "correct": "B", 
                "explanation": "Λάθος! Μπορούμε να έχουμε όσα 'elif' θέλουμε για να ελέγξουμε πολλαπλές περιπτώσεις.",
                "remedial_resource": "https://www.w3schools.com/python/python_conditions.asp",
                "video_resource": "https://www.youtube.com/watch?v=Zp5MuPOtsME"
            },

            # === Loops ===
            {
                "concept": c_loops, "type": "MC", "diff": "medium", 
                "text": "Τι θα τυπώσει ο κώδικας;", "code": "for x in range(3):\n  print(x)", "a": "1, 2, 3", "b": "0, 1, 2", "c": "0, 1, 2, 3", "d": "1, 2", "correct": "B", 
                "explanation": "Η range(3) ξεκινάει πάντα από το 0 και σταματάει ΠΡΙΝ το 3.",
                "remedial_resource": "https://www.w3schools.com/python/python_for_loops.asp",
                "video_resource": "https://www.youtube.com/watch?v=OnDr4J2UXSA"
            },
            {
                "concept": c_loops, "type": "TF", "diff": "easy", 
                "text": "Η εντολή 'break' σταματάει αμέσως την εκτέλεση του Loop.", "code": None, "a": "Σωστό", "b": "Λάθος", "correct": "A", 
                "explanation": "Σωστό. Μόλις το πρόγραμμα συναντήσει το 'break', βγαίνει αμέσως έξω από τον βρόχο.",
                "remedial_resource": "https://www.w3schools.com/python/python_while_loops.asp",
                "video_resource": "https://www.youtube.com/watch?v=yCZBnjF4_tU"
            },
            {
                "concept": c_loops, "type": "MC", "diff": "hard", 
                "text": "Τι θα τυπώσει;", "code": "i = 1\nwhile i < 6:\n  i += 1\nprint(i)", "a": "5", "b": "6", "c": "1", "d": "Άπειρο Loop", "correct": "B", 
                "explanation": "Όταν το i γίνει 5, το loop εκτελείται ξανά. Το i γίνεται 6 και ΜΕΤΑ τελειώνει το loop. Το print(i) είναι έξω από το loop και τυπώνει 6.",
                "remedial_resource": "https://www.w3schools.com/python/python_while_loops.asp",
                "video_resource": "https://www.youtube.com/watch?v=HZARImviDxg"
            },
            {
                "concept": c_loops, "type": "MC", "diff": "medium", 
                "text": "Τι κάνει η range(2, 6);", "code": None, "a": "Παράγει: 2, 3, 4, 5, 6", "b": "Παράγει: 2, 3, 4, 5", "c": "Παράγει: 3, 4, 5", "d": "Παράγει: 2, 4, 6", "correct": "B", 
                "explanation": "Ξεκινάει από το 2 (συμπεριλαμβάνεται) και σταματάει στο 6 (ΔΕΝ συμπεριλαμβάνεται).",
                "remedial_resource": "https://www.w3schools.com/python/python_for_loops.asp",
                "video_resource": "https://www.youtube.com/watch?v=OnDr4J2UXSA"
            },
            {
                "concept": c_loops, "type": "MC", "diff": "medium", 
                "text": "Τι κάνει η εντολή 'continue' μέσα σε ένα loop;", "code": None, "a": "Σταματάει το loop", "b": "Πάει στην επόμενη επανάληψη", "c": "Τυπώνει ένα μήνυμα", "d": "Κλείνει το πρόγραμμα", "correct": "B", 
                "explanation": "Το continue αγνοεί τον υπόλοιπο κώδικα της τρέχουσας επανάληψης και πηγαίνει κατευθείαν στην επόμενη.",
                "remedial_resource": "https://www.w3schools.com/python/python_while_loops.asp",
                "video_resource": "https://www.youtube.com/watch?v=yCZBnjF4_tU"
            },
            {
                "concept": c_loops, "type": "MC", "diff": "hard", 
                "text": "Πόσες φορές θα εκτελεστεί το loop;", "code": "for i in range(1, 10, 2):\n  print(i)", "a": "10", "b": "9", "c": "5", "d": "4", "correct": "C", 
                "explanation": "Η range(1, 10, 2) με βήμα 2 παράγει τους αριθμούς: 1, 3, 5, 7, 9. Άρα 5 φορές.",
                "remedial_resource": "https://www.w3schools.com/python/python_for_loops.asp",
                "video_resource": "https://www.youtube.com/watch?v=OnDr4J2UXSA"
            },
            {
                "concept": c_loops, "type": "TF", "diff": "easy", 
                "text": "Το while loop εκτελείται όσο η συνθήκη του είναι Ψευδής (False).", "code": None, "a": "Σωστό", "b": "Λάθος", "correct": "B", 
                "explanation": "Αντίθετα, εκτελείται μόνο όσο η συνθήκη είναι Αληθής (True).",
                "remedial_resource": "https://www.w3schools.com/python/python_while_loops.asp",
                "video_resource": "https://www.youtube.com/watch?v=HZARImviDxg"
            },

            # === Lists ===
            {
                "concept": c_lists, "type": "MC", "diff": "medium", 
                "text": "Ποιο είναι το αποτέλεσμα;", "code": "mylist = ['apple', 'banana', 'cherry']\nprint(mylist[-1])", "a": "apple", "b": "banana", "c": "cherry", "d": "Error", "correct": "C", 
                "explanation": "Τα αρνητικά indexes μετράνε από το τέλος προς την αρχή. Το -1 είναι το τελευταίο στοιχείο.",
                "remedial_resource": "https://www.w3schools.com/python/python_lists_access.asp",
                "video_resource": "https://www.youtube.com/watch?v=W8KRzm-HUcc"
            },
            {
                "concept": c_lists, "type": "MC", "diff": "easy", 
                "text": "Πώς προσθέτεις στοιχείο στο τέλος λίστας;", "code": None, "a": "add()", "b": "insert()", "c": "append()", "d": "push()", "correct": "C", 
                "explanation": "Η μέθοδος append() προσθέτει ένα στοιχείο στο τέλος της λίστας.",
                "remedial_resource": "https://www.w3schools.com/python/python_lists_add.asp",
                "video_resource": "https://www.youtube.com/watch?v=W8KRzm-HUcc"
            },
            {
                "concept": c_lists, "type": "MC", "diff": "hard", 
                "text": "Τι θα δώσει το slicing;", "code": "nums = [10, 20, 30, 40, 50]\nprint(nums[1:3])", "a": "[20, 30]", "b": "[10, 20, 30]", "c": "[20, 30, 40]", "d": "[30, 40]", "correct": "A", 
                "explanation": "Το slicing [1:3] ξεκινάει από το index 1 (το 20) και σταματάει ΠΡΙΝ το index 3 (το 40).",
                "remedial_resource": "https://www.w3schools.com/python/python_lists_access.asp",
                "video_resource": "https://www.youtube.com/watch?v=ajrtAuOA3cg"
            },
            {
                "concept": c_lists, "type": "TF", "diff": "medium", 
                "text": "Οι λίστες στην Python μπορούν να περιέχουν στοιχεία διαφορετικού τύπου.", "code": "my_list = [1, 'hello', 3.14]", "a": "Σωστό", "b": "Λάθος", "correct": "A", 
                "explanation": "Σωστό. Οι λίστες είναι ευέλικτες και δεν περιορίζονται σε έναν τύπο δεδομένων.",
                "remedial_resource": "https://www.w3schools.com/python/python_lists.asp",
                "video_resource": "https://www.youtube.com/watch?v=W8KRzm-HUcc"
            },
            {
                "concept": c_lists, "type": "MC", "diff": "easy", 
                "text": "Με ποια μέθοδο αφαιρούμε και επιστρέφουμε το τελευταίο στοιχείο;", "code": None, "a": "remove()", "b": "delete()", "c": "pop()", "d": "pull()", "correct": "C", 
                "explanation": "Η μέθοδος pop() βγάζει το τελευταίο στοιχείο από τη λίστα (ή όποιο index της δώσουμε).",
                "remedial_resource": "https://www.w3schools.com/python/python_lists_remove.asp",
                "video_resource": "https://www.youtube.com/watch?v=W8KRzm-HUcc"
            },
            {
                "concept": c_lists, "type": "MC", "diff": "medium", 
                "text": "Πώς βρίσκουμε το μήκος μιας λίστας my_list;", "code": None, "a": "my_list.length", "b": "length(my_list)", "c": "my_list.size()", "d": "len(my_list)", "correct": "D", 
                "explanation": "Η συνάρτηση len() επιστρέφει το πλήθος των στοιχείων μιας λίστας.",
                "remedial_resource": "https://www.w3schools.com/python/python_lists.asp",
                "video_resource": "https://www.youtube.com/watch?v=W8KRzm-HUcc"
            },
            {
                "concept": c_lists, "type": "MC", "diff": "hard", 
                "text": "Τι θα τυπώσει η εντολή;", "code": "nums = [1, 2, 3]\nprint(nums[::-1])", "a": "[1, 2, 3]", "b": "Error", "c": "[3, 2, 1]", "d": "[3]", "correct": "C", 
                "explanation": "Το slicing [::-1] είναι ένα κόλπο στην Python για να αντιστρέψουμε (reverse) μια λίστα.",
                "remedial_resource": "https://www.w3schools.com/python/python_lists_access.asp",
                "video_resource": "https://www.youtube.com/watch?v=ajrtAuOA3cg"
            },

            # === Functions ===
            {
                "concept": c_funcs, "type": "MC", "diff": "easy", 
                "text": "Ποια λέξη κλειδί ορίζει συνάρτηση;", "code": None, "a": "func", "b": "def", "c": "function", "d": "define", "correct": "B", 
                "explanation": "Στην Python χρησιμοποιούμε το 'def' (από το define) για να ξεκινήσουμε μια συνάρτηση.",
                "remedial_resource": "https://www.w3schools.com/python/python_functions.asp",
                "video_resource": "https://www.youtube.com/watch?v=9Os0o3wzS_I"
            },
            {
                "concept": c_funcs, "type": "MC", "diff": "medium", 
                "text": "Τι θα επιστρέψει;", "code": "def add(a, b=5):\n  return a + b\nprint(add(3))", "a": "8", "b": "3", "c": "Error", "d": "53", "correct": "A", 
                "explanation": "Το b έχει προεπιλεγμένη τιμή 5. Αφού δεν δώσαμε δεύτερο όρισμα, η συνάρτηση κάνει 3 + 5.",
                "remedial_resource": "https://www.w3schools.com/python/python_functions.asp",
                "video_resource": "https://www.youtube.com/watch?v=9Os0o3wzS_I"
            },
            {
                "concept": c_funcs, "type": "TF", "diff": "hard", 
                "text": "Μια συνάρτηση μπορεί να επιστρέψει πολλές τιμές ταυτόχρονα.", "code": "return x, y", "a": "Σωστό", "b": "Λάθος", "correct": "A", 
                "explanation": "Σωστό! Αν επιστρέψεις πολλές τιμές, η Python τις πακετάρει αυτόματα σε ένα Tuple.",
                "remedial_resource": "https://www.w3schools.com/python/python_tuples.asp",
                "video_resource": "https://www.youtube.com/watch?v=9Os0o3wzS_I"
            },
            {
                "concept": c_funcs, "type": "MC", "diff": "hard", 
                "text": "Τι θα τυπωθεί; (Προσοχή στο Scope)", "code": "x = 5\ndef myFunc():\n  x = 10\nmyFunc()\nprint(x)", "a": "10", "b": "5", "c": "Error", "d": "None", "correct": "B", 
                "explanation": "Το x = 10 μέσα στη συνάρτηση είναι 'Τοπική' (Local) μεταβλητή. Η 'Παγκόσμια' (Global) x παραμένει 5.",
                "remedial_resource": "https://www.w3schools.com/python/python_scope.asp",
                "video_resource": "https://www.youtube.com/watch?v=QVdf0LgmICw"
            },
            {
                "concept": c_funcs, "type": "TF", "diff": "easy", 
                "text": "Είναι υποχρεωτικό μια συνάρτηση να έχει την εντολή 'return'.", "code": None, "a": "Σωστό", "b": "Λάθος", "correct": "B", 
                "explanation": "Όχι, αν λείπει το return, η συνάρτηση απλά εκτελεί τον κώδικά της και επιστρέφει αυτόματα 'None'.",
                "remedial_resource": "https://www.w3schools.com/python/python_functions.asp",
                "video_resource": "https://www.youtube.com/watch?v=9Os0o3wzS_I"
            },
            {
                "concept": c_funcs, "type": "MC", "diff": "medium", 
                "text": "Πώς καλούμε μια συνάρτηση με όνομα 'greet';", "code": None, "a": "call greet", "b": "greet", "c": "greet()", "d": "run greet", "correct": "C", 
                "explanation": "Για να εκτελεστεί (κληθεί) μια συνάρτηση, πρέπει πάντα να βάλουμε παρενθέσεις στο τέλος του ονόματός της.",
                "remedial_resource": "https://www.w3schools.com/python/python_functions.asp",
                "video_resource": "https://www.youtube.com/watch?v=9Os0o3wzS_I"
            },
        ]

        # Εισαγωγή στη βάση
        for q in questions_data:
            Question.objects.update_or_create(
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
                    "correct_option": q["correct"],
                    "explanation": q.get("explanation", ""),
                    "remedial_resource": q.get("remedial_resource", ""),
                    "video_resource": q.get("video_resource", "")
                }
            )

        self.stdout.write(self.style.SUCCESS(f'ΕΠΙΤΥΧΙΑ! Προστέθηκαν {len(questions_data)} ερωτήσεις στη βάση.'))