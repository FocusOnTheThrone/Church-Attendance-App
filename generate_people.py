#!/usr/bin/env python
"""
Script to generate 60 realistic people for the church register.
Run with: python generate_people.py
"""
import os
import sys
import django

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from attendance.models import Person
from datetime import date, timedelta
import random

# Sample data
FIRST_NAMES = [
    "David", "Sarah", "James", "Grace", "Michael", "Rebecca", "John", "Mary",
    "Peter", "Elizabeth", "Paul", "Ruth", "Andrew", "Deborah", "Thomas", "Hannah",
    "Philip", "Esther", "Nathaniel", "Martha", "Simon", "Priscilla", "Matthew", "Lydia",
    "Mark", "Abigail", "Luke", "Naomi", "Stephen", "Judith", "Timothy", "Anna",
    "Titus", "Susanna", "Philemon", "Joanna", "Silas", "Bethany", "Barnabas", "Magdalene",
    "Joseph", "Miriam", "Zacharias", "Salome", "Theophilus", "Candace", "Cornelius", "Eunice",
    "Sergius", "Dorcas", "Gaius", "Tabitha", "Erastus", "Phoebe", "Aquila", "Priscilla"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
    "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
    "Ayokunle", "Okafor", "Adeyemi", "Mensah", "Kofi", "Nkosi", "Adebayo", "Okonkwo",
    "Anane", "Mwangi", "Kipchoge", "Kimani", "Nyambura", "Owusu", "Eze", "Okoro"
]

OCCUPATIONS = [
    "Teacher", "Nurse", "Engineer", "Accountant", "Doctor", "Lawyer", "Manager",
    "Electrician", "Plumber", "Chef", "Carpenter", "Mechanic", "Farmer", "Trader",
    "Hairdresser", "Tailor", "Driver", "Clerk", "Student", "Retiree", "Shopkeeper",
    "Painter", "Builder", "Welder", "Pastor", "Administrator", "Receptionist",
    "Sales Associate", "Technician", "Consultant", "Freelancer"
]

RESIDENCES = [
    "Central District", "North Avenue", "East End", "West Side", "Downtown",
    "Suburb A", "Suburb B", "Suburb C", "Village Heights", "Riverside",
    "Hillside", "Lakeside", "Riverside Park", "Oak Street", "Maple Avenue",
    "Pine Road", "Elm Street", "Cedar Lane", "Birch Way", "Spruce Court"
]

TITLES = [
    (Person.BROTHER, 15),
    (Person.SISTER, 15),
    (Person.PASTOR, 3),
    (Person.SENIOR_PASTOR, 1),
    (Person.BISHOP, 1),
    (Person.VISITOR, 10),
    (Person.EMPLOYEE, 5),
    (Person.OVERSEER, 2),
]

FELLOWSHIPS = [
    (Person.YOUTH_FELLOWSHIP, 20),
    (Person.MENS_FELLOWSHIP, 12),
    (Person.WOMENS_FELLOWSHIP, 12),
    (Person.CHOIR, 8),
    (Person.PRAYER, 6),
    (Person.USHERING, 2),
    (Person.NONE, 0),
]

GENDERS = [Person.MALE, Person.FEMALE, Person.OTHER]

def generate_birthdate():
    """Generate a random birthdate for ages 12 to 80."""
    age = random.randint(12, 80)
    days_back = age * 365 + random.randint(0, 365)
    return date.today() - timedelta(days=days_back)

def choose_weighted(items):
    """Choose from a list of (item, weight) tuples."""
    items_list, weights = zip(*items)
    return random.choices(items_list, weights=weights, k=1)[0]

def generate_people(count=60):
    """Generate and save count people to the database."""
    people = []
    
    for i in range(count):
        first = random.choice(FIRST_NAMES)
        last = random.choice(LAST_NAMES)
        full_name = f"{first} {last}"
        
        gender = random.choice(GENDERS)
        title = choose_weighted(TITLES)
        
        # Visitors are more likely to be recent
        if title == Person.VISITOR:
            first_visit = date.today() - timedelta(days=random.randint(0, 90))
        else:
            first_visit = date.today() - timedelta(days=random.randint(0, 730))
        
        person = Person(
            full_name=full_name,
            gender=gender,
            date_of_birth=generate_birthdate(),
            phone=f"+1{random.randint(2000000000, 9999999999)}",
            email=f"{first.lower()}.{last.lower()}{random.randint(1, 999)}@email.com",
            title=title,
            first_visit_date=first_visit,
            occupation=random.choice(OCCUPATIONS) if random.random() > 0.3 else "",
            fellowship=choose_weighted(FELLOWSHIPS),
            residence=random.choice(RESIDENCES) if random.random() > 0.2 else "",
            notes="Auto-generated test record" if random.random() > 0.8 else "",
        )
        people.append(person)
    
    # Bulk create for efficiency
    Person.objects.bulk_create(people)
    return len(people)

if __name__ == "__main__":
    print("Generating 60 people for the church register...")
    count = generate_people(60)
    print(f"✅ Successfully created {count} people!")
    total = Person.objects.count()
    print(f"📊 Total people in register: {total}")
