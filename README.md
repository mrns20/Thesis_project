# MyPython

## Οδηγίες Εγκατάστασης & Λειτουργίας

### 1. Backend

1.Μεταβείτε στον κατάλογο του backend:

cd backend

2.Virtual Environment,
ΓΙΑ WINDOWS :

python -m venv venv
venv\Scripts\activate

ΓΙΑ macOS KAI LINUX :

python3 -m venv venv
source venv/bin/activate

3. Εγκατάσταση εξαρτήσεων,

pip install -r requirements.txt

4. Migrations, τρέξιμο του σερβερ,

python manage.py migrate
python manage.py runserver

### 2. Frontend

Πάμε σε νέο τερματικό, ενώ τρέχει κανονικα το backend στο άλλο τερματικό

1.  Μεταβένουμε στον κατάλογο του frontend, κατεβάζουμε τα απαραίτητα πακέτα και εκκινούμε την εφαρμογή

cd frontend
npm install
npm start

---

Διπλωματική Εργασία
Πανεπιστήμιο Δυτικής Αττικής
Αθήνα 2026
