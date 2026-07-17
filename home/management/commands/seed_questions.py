from django.core.management.base import BaseCommand
from django.db import transaction
from home.models import Category, Question, Answer

import random

category_data = [
    {
        "name": "General Knowledge",
        "description": "Test your general knowledge with questions from various domains including geography, culture, and famous personalities.",
        "total_time": 30,
        "questions": [
            {
                "question": "What is the capital of France?",
                "mark": 5,
                "answers": [
                    {"answer": "Paris", "is_correct": True},
                    {"answer": "London", "is_correct": False},
                    {"answer": "Berlin", "is_correct": False},
                    {"answer": "Madrid", "is_correct": False},
                ],
            },
            {
                "question": "Which planet is known as the Red Planet?",
                "mark": 5,
                "answers": [
                    {"answer": "Mars", "is_correct": True},
                    {"answer": "Venus", "is_correct": False},
                    {"answer": "Jupiter", "is_correct": False},
                    {"answer": "Saturn", "is_correct": False},
                ],
            },
            {
                "question": "Who wrote 'Romeo and Juliet'?",
                "mark": 5,
                "answers": [
                    {"answer": "William Shakespeare", "is_correct": True},
                    {"answer": "Charles Dickens", "is_correct": False},
                    {"answer": "Jane Austen", "is_correct": False},
                    {"answer": "Mark Twain", "is_correct": False},
                ],
            },
            {
                "question": "What is the largest ocean in the world?",
                "mark": 5,
                "answers": [
                    {"answer": "Pacific Ocean", "is_correct": True},
                    {"answer": "Atlantic Ocean", "is_correct": False},
                    {"answer": "Indian Ocean", "is_correct": False},
                    {"answer": "Arctic Ocean", "is_correct": False},
                ],
            },
            {
                "question": "In which year did World War II end?",
                "mark": 5,
                "answers": [
                    {"answer": "1945", "is_correct": True},
                    {"answer": "1944", "is_correct": False},
                    {"answer": "1946", "is_correct": False},
                    {"answer": "1943", "is_correct": False},
                ],
            },
            {
                "question": "What is the chemical symbol for gold?",
                "mark": 5,
                "answers": [
                    {"answer": "Au", "is_correct": True},
                    {"answer": "Ag", "is_correct": False},
                    {"answer": "Fe", "is_correct": False},
                    {"answer": "Cu", "is_correct": False},
                ],
            },
            {
                "question": "Which country has the largest population in the world?",
                "mark": 5,
                "answers": [
                    {"answer": "India", "is_correct": True},
                    {"answer": "China", "is_correct": False},
                    {"answer": "USA", "is_correct": False},
                    {"answer": "Indonesia", "is_correct": False},
                ],
            },
            {
                "question": "What is the tallest mountain in the world?",
                "mark": 5,
                "answers": [
                    {"answer": "Mount Everest", "is_correct": True},
                    {"answer": "K2", "is_correct": False},
                    {"answer": "Kangchenjunga", "is_correct": False},
                    {"answer": "Lhotse", "is_correct": False},
                ],
            },
            {
                "question": "Which gas do plants absorb from the atmosphere?",
                "mark": 5,
                "answers": [
                    {"answer": "Carbon Dioxide", "is_correct": True},
                    {"answer": "Oxygen", "is_correct": False},
                    {"answer": "Nitrogen", "is_correct": False},
                    {"answer": "Hydrogen", "is_correct": False},
                ],
            },
            {
                "question": "What is the smallest country in the world by area?",
                "mark": 5,
                "answers": [
                    {"answer": "Vatican City", "is_correct": True},
                    {"answer": "Monaco", "is_correct": False},
                    {"answer": "San Marino", "is_correct": False},
                    {"answer": "Liechtenstein", "is_correct": False},
                ],
            },
        ],
    },
    {
        "name": "Science & Technology",
        "description": "Challenge yourself with questions about scientific discoveries, inventions, and technological advancements.",
        "total_time": 25,
        "questions": [
            {
                "question": "What is the chemical formula of water?",
                "mark": 5,
                "answers": [
                    {"answer": "H2O", "is_correct": True},
                    {"answer": "CO2", "is_correct": False},
                    {"answer": "NaCl", "is_correct": False},
                    {"answer": "HCl", "is_correct": False},
                ],
            },
            {
                "question": "Who invented the light bulb?",
                "mark": 5,
                "answers": [
                    {"answer": "Thomas Edison", "is_correct": True},
                    {"answer": "Nikola Tesla", "is_correct": False},
                    {"answer": "Alexander Graham Bell", "is_correct": False},
                    {"answer": "Albert Einstein", "is_correct": False},
                ],
            },
            {
                "question": "What is the powerhouse of the cell?",
                "mark": 5,
                "answers": [
                    {"answer": "Mitochondria", "is_correct": True},
                    {"answer": "Nucleus", "is_correct": False},
                    {"answer": "Ribosome", "is_correct": False},
                    {"answer": "Golgi apparatus", "is_correct": False},
                ],
            },
            {
                "question": "What is the speed of light in vacuum?",
                "mark": 5,
                "answers": [
                    {"answer": "299,792,458 m/s", "is_correct": True},
                    {"answer": "150,000,000 m/s", "is_correct": False},
                    {"answer": "199,792,458 m/s", "is_correct": False},
                    {"answer": "399,792,458 m/s", "is_correct": False},
                ],
            },
            {
                "question": "Which element has the atomic number 1?",
                "mark": 5,
                "answers": [
                    {"answer": "Hydrogen", "is_correct": True},
                    {"answer": "Helium", "is_correct": False},
                    {"answer": "Lithium", "is_correct": False},
                    {"answer": "Carbon", "is_correct": False},
                ],
            },
            {
                "question": "What does CPU stand for?",
                "mark": 5,
                "answers": [
                    {"answer": "Central Processing Unit", "is_correct": True},
                    {"answer": "Computer Personal Unit", "is_correct": False},
                    {"answer": "Central Process Unit", "is_correct": False},
                    {"answer": "Core Processing Unit", "is_correct": False},
                ],
            },
            {
                "question": "Which planet has the most moons?",
                "mark": 5,
                "answers": [
                    {"answer": "Saturn", "is_correct": True},
                    {"answer": "Jupiter", "is_correct": False},
                    {"answer": "Uranus", "is_correct": False},
                    {"answer": "Neptune", "is_correct": False},
                ],
            },
            {
                "question": "What is the main gas in Earth's atmosphere?",
                "mark": 5,
                "answers": [
                    {"answer": "Nitrogen", "is_correct": True},
                    {"answer": "Oxygen", "is_correct": False},
                    {"answer": "Carbon Dioxide", "is_correct": False},
                    {"answer": "Argon", "is_correct": False},
                ],
            },
            {
                "question": "Who developed the theory of relativity?",
                "mark": 5,
                "answers": [
                    {"answer": "Albert Einstein", "is_correct": True},
                    {"answer": "Isaac Newton", "is_correct": False},
                    {"answer": "Galileo Galilei", "is_correct": False},
                    {"answer": "Stephen Hawking", "is_correct": False},
                ],
            },
            {
                "question": "What is the largest organ in the human body?",
                "mark": 5,
                "answers": [
                    {"answer": "Skin", "is_correct": True},
                    {"answer": "Liver", "is_correct": False},
                    {"answer": "Brain", "is_correct": False},
                    {"answer": "Heart", "is_correct": False},
                ],
            },
        ],
    },
    {
        "name": "Mathematics",
        "description": "Sharpen your math skills with questions covering arithmetic, geometry, algebra, and number theory.",
        "total_time": 20,
        "questions": [
            {
                "question": "What is the value of Pi (π) to two decimal places?",
                "mark": 5,
                "answers": [
                    {"answer": "3.14", "is_correct": True},
                    {"answer": "3.16", "is_correct": False},
                    {"answer": "3.12", "is_correct": False},
                    {"answer": "3.18", "is_correct": False},
                ],
            },
            {
                "question": "What is the square root of 144?",
                "mark": 5,
                "answers": [
                    {"answer": "12", "is_correct": True},
                    {"answer": "14", "is_correct": False},
                    {"answer": "10", "is_correct": False},
                    {"answer": "16", "is_correct": False},
                ],
            },
            {
                "question": "How many sides does a hexagon have?",
                "mark": 5,
                "answers": [
                    {"answer": "6", "is_correct": True},
                    {"answer": "5", "is_correct": False},
                    {"answer": "7", "is_correct": False},
                    {"answer": "8", "is_correct": False},
                ],
            },
            {
                "question": "What is 15% of 200?",
                "mark": 5,
                "answers": [
                    {"answer": "30", "is_correct": True},
                    {"answer": "25", "is_correct": False},
                    {"answer": "35", "is_correct": False},
                    {"answer": "20", "is_correct": False},
                ],
            },
            {
                "question": "What is the next prime number after 7?",
                "mark": 5,
                "answers": [
                    {"answer": "11", "is_correct": True},
                    {"answer": "9", "is_correct": False},
                    {"answer": "13", "is_correct": False},
                    {"answer": "10", "is_correct": False},
                ],
            },
            {
                "question": "What is the area of a rectangle with length 8 and width 5?",
                "mark": 5,
                "answers": [
                    {"answer": "40", "is_correct": True},
                    {"answer": "13", "is_correct": False},
                    {"answer": "45", "is_correct": False},
                    {"answer": "35", "is_correct": False},
                ],
            },
            {
                "question": "What is 2 raised to the power of 10?",
                "mark": 5,
                "answers": [
                    {"answer": "1024", "is_correct": True},
                    {"answer": "512", "is_correct": False},
                    {"answer": "2048", "is_correct": False},
                    {"answer": "256", "is_correct": False},
                ],
            },
            {
                "question": "How many degrees are in a right angle?",
                "mark": 5,
                "answers": [
                    {"answer": "90", "is_correct": True},
                    {"answer": "45", "is_correct": False},
                    {"answer": "180", "is_correct": False},
                    {"answer": "360", "is_correct": False},
                ],
            },
            {
                "question": "What is the LCM of 6 and 8?",
                "mark": 5,
                "answers": [
                    {"answer": "24", "is_correct": True},
                    {"answer": "48", "is_correct": False},
                    {"answer": "12", "is_correct": False},
                    {"answer": "36", "is_correct": False},
                ],
            },
            {
                "question": "What is the sum of angles in a triangle?",
                "mark": 5,
                "answers": [
                    {"answer": "180 degrees", "is_correct": True},
                    {"answer": "90 degrees", "is_correct": False},
                    {"answer": "360 degrees", "is_correct": False},
                    {"answer": "270 degrees", "is_correct": False},
                ],
            },
        ],
    },
    {
        "name": "History",
        "description": "Travel back in time with questions about ancient civilizations, world wars, and historical figures.",
        "total_time": 25,
        "questions": [
            {
                "question": "Who was the first President of the United States?",
                "mark": 5,
                "answers": [
                    {"answer": "George Washington", "is_correct": True},
                    {"answer": "Thomas Jefferson", "is_correct": False},
                    {"answer": "Abraham Lincoln", "is_correct": False},
                    {"answer": "John Adams", "is_correct": False},
                ],
            },
            {
                "question": "In which year did the Titanic sink?",
                "mark": 5,
                "answers": [
                    {"answer": "1912", "is_correct": True},
                    {"answer": "1911", "is_correct": False},
                    {"answer": "1913", "is_correct": False},
                    {"answer": "1910", "is_correct": False},
                ],
            },
            {
                "question": "Which ancient civilization built the pyramids?",
                "mark": 5,
                "answers": [
                    {"answer": "Egyptian", "is_correct": True},
                    {"answer": "Roman", "is_correct": False},
                    {"answer": "Greek", "is_correct": False},
                    {"answer": "Mesopotamian", "is_correct": False},
                ],
            },
            {
                "question": "Who discovered America in 1492?",
                "mark": 5,
                "answers": [
                    {"answer": "Christopher Columbus", "is_correct": True},
                    {"answer": "Vasco da Gama", "is_correct": False},
                    {"answer": "Ferdinand Magellan", "is_correct": False},
                    {"answer": "Amerigo Vespucci", "is_correct": False},
                ],
            },
            {
                "question": "The French Revolution began in which year?",
                "mark": 5,
                "answers": [
                    {"answer": "1789", "is_correct": True},
                    {"answer": "1776", "is_correct": False},
                    {"answer": "1799", "is_correct": False},
                    {"answer": "1765", "is_correct": False},
                ],
            },
            {
                "question": "Who was the first woman to fly solo across the Atlantic?",
                "mark": 5,
                "answers": [
                    {"answer": "Amelia Earhart", "is_correct": True},
                    {"answer": "Harriet Quimby", "is_correct": False},
                    {"answer": "Bessie Coleman", "is_correct": False},
                    {"answer": "Jacqueline Cochran", "is_correct": False},
                ],
            },
            {
                "question": "Which empire was ruled by Genghis Khan?",
                "mark": 5,
                "answers": [
                    {"answer": "Mongol Empire", "is_correct": True},
                    {"answer": "Ottoman Empire", "is_correct": False},
                    {"answer": "Roman Empire", "is_correct": False},
                    {"answer": "Persian Empire", "is_correct": False},
                ],
            },
            {
                "question": "What was the name of the ship that brought the Pilgrims to America?",
                "mark": 5,
                "answers": [
                    {"answer": "Mayflower", "is_correct": True},
                    {"answer": "Santa Maria", "is_correct": False},
                    {"answer": "Beagle", "is_correct": False},
                    {"answer": "Endeavour", "is_correct": False},
                ],
            },
            {
                "question": "Who was the last Pharaoh of Egypt?",
                "mark": 5,
                "answers": [
                    {"answer": "Cleopatra VII", "is_correct": True},
                    {"answer": "Nefertiti", "is_correct": False},
                    {"answer": "Hatshepsut", "is_correct": False},
                    {"answer": "Ramesses II", "is_correct": False},
                ],
            },
            {
                "question": "The Berlin Wall fell in which year?",
                "mark": 5,
                "answers": [
                    {"answer": "1989", "is_correct": True},
                    {"answer": "1991", "is_correct": False},
                    {"answer": "1987", "is_correct": False},
                    {"answer": "1990", "is_correct": False},
                ],
            },
        ],
    },
    {
        "name": "Geography",
        "description": "Explore the world with questions about countries, capitals, rivers, mountains, and natural wonders.",
        "total_time": 20,
        "questions": [
            {
                "question": "What is the longest river in the world?",
                "mark": 5,
                "answers": [
                    {"answer": "Nile", "is_correct": True},
                    {"answer": "Amazon", "is_correct": False},
                    {"answer": "Mississippi", "is_correct": False},
                    {"answer": "Yangtze", "is_correct": False},
                ],
            },
            {
                "question": "Which country has the most number of islands?",
                "mark": 5,
                "answers": [
                    {"answer": "Sweden", "is_correct": True},
                    {"answer": "Indonesia", "is_correct": False},
                    {"answer": "Philippines", "is_correct": False},
                    {"answer": "Japan", "is_correct": False},
                ],
            },
            {
                "question": "What is the capital of Japan?",
                "mark": 5,
                "answers": [
                    {"answer": "Tokyo", "is_correct": True},
                    {"answer": "Seoul", "is_correct": False},
                    {"answer": "Beijing", "is_correct": False},
                    {"answer": "Bangkok", "is_correct": False},
                ],
            },
            {
                "question": "Which desert is the largest hot desert in the world?",
                "mark": 5,
                "answers": [
                    {"answer": "Sahara", "is_correct": True},
                    {"answer": "Gobi", "is_correct": False},
                    {"answer": "Kalahari", "is_correct": False},
                    {"answer": "Arabian", "is_correct": False},
                ],
            },
            {
                "question": "What is the deepest point in the ocean?",
                "mark": 5,
                "answers": [
                    {"answer": "Mariana Trench", "is_correct": True},
                    {"answer": "Tonga Trench", "is_correct": False},
                    {"answer": "Philippine Trench", "is_correct": False},
                    {"answer": "Java Trench", "is_correct": False},
                ],
            },
            {
                "question": "Which country is known as the 'Land of the Rising Sun'?",
                "mark": 5,
                "answers": [
                    {"answer": "Japan", "is_correct": True},
                    {"answer": "China", "is_correct": False},
                    {"answer": "South Korea", "is_correct": False},
                    {"answer": "Thailand", "is_correct": False},
                ],
            },
            {
                "question": "What is the capital of Australia?",
                "mark": 5,
                "answers": [
                    {"answer": "Canberra", "is_correct": True},
                    {"answer": "Sydney", "is_correct": False},
                    {"answer": "Melbourne", "is_correct": False},
                    {"answer": "Perth", "is_correct": False},
                ],
            },
            {
                "question": "Which river flows through London?",
                "mark": 5,
                "answers": [
                    {"answer": "Thames", "is_correct": True},
                    {"answer": "Seine", "is_correct": False},
                    {"answer": "Danube", "is_correct": False},
                    {"answer": "Rhine", "is_correct": False},
                ],
            },
            {
                "question": "What is the largest lake in Africa?",
                "mark": 5,
                "answers": [
                    {"answer": "Lake Victoria", "is_correct": True},
                    {"answer": "Lake Tanganyika", "is_correct": False},
                    {"answer": "Lake Malawi", "is_correct": False},
                    {"answer": "Lake Chad", "is_correct": False},
                ],
            },
            {
                "question": "Which country has the longest coastline?",
                "mark": 5,
                "answers": [
                    {"answer": "Canada", "is_correct": True},
                    {"answer": "Australia", "is_correct": False},
                    {"answer": "Russia", "is_correct": False},
                    {"answer": "Indonesia", "is_correct": False},
                ],
            },
        ],
    },
    {
        "name": "Sports",
        "description": "Test your sports knowledge from football to cricket, tennis to basketball, and everything in between.",
        "total_time": 20,
        "questions": [
            {
                "question": "In which sport is the term 'love' used?",
                "mark": 5,
                "answers": [
                    {"answer": "Tennis", "is_correct": True},
                    {"answer": "Badminton", "is_correct": False},
                    {"answer": "Table Tennis", "is_correct": False},
                    {"answer": "Squash", "is_correct": False},
                ],
            },
            {
                "question": "How many players are on a basketball team on the court?",
                "mark": 5,
                "answers": [
                    {"answer": "5", "is_correct": True},
                    {"answer": "6", "is_correct": False},
                    {"answer": "7", "is_correct": False},
                    {"answer": "4", "is_correct": False},
                ],
            },
            {
                "question": "Which country has won the most FIFA World Cups?",
                "mark": 5,
                "answers": [
                    {"answer": "Brazil", "is_correct": True},
                    {"answer": "Germany", "is_correct": False},
                    {"answer": "Italy", "is_correct": False},
                    {"answer": "Argentina", "is_correct": False},
                ],
            },
            {
                "question": "What is the maximum score in a single frame of bowling?",
                "mark": 5,
                "answers": [
                    {"answer": "30", "is_correct": True},
                    {"answer": "10", "is_correct": False},
                    {"answer": "20", "is_correct": False},
                    {"answer": "50", "is_correct": False},
                ],
            },
            {
                "question": "In which sport would you perform a 'slam dunk'?",
                "mark": 5,
                "answers": [
                    {"answer": "Basketball", "is_correct": True},
                    {"answer": "Volleyball", "is_correct": False},
                    {"answer": "Handball", "is_correct": False},
                    {"answer": "Netball", "is_correct": False},
                ],
            },
            {
                "question": "How long is a marathon in miles?",
                "mark": 5,
                "answers": [
                    {"answer": "26.2 miles", "is_correct": True},
                    {"answer": "26 miles", "is_correct": False},
                    {"answer": "25 miles", "is_correct": False},
                    {"answer": "27 miles", "is_correct": False},
                ],
            },
            {
                "question": "Which sport uses a shuttlecock?",
                "mark": 5,
                "answers": [
                    {"answer": "Badminton", "is_correct": True},
                    {"answer": "Tennis", "is_correct": False},
                    {"answer": "Cricket", "is_correct": False},
                    {"answer": "Hockey", "is_correct": False},
                ],
            },
            {
                "question": "What is the diameter of a basketball hoop in inches?",
                "mark": 5,
                "answers": [
                    {"answer": "18 inches", "is_correct": True},
                    {"answer": "16 inches", "is_correct": False},
                    {"answer": "20 inches", "is_correct": False},
                    {"answer": "15 inches", "is_correct": False},
                ],
            },
            {
                "question": "In cricket, how many players are in a team?",
                "mark": 5,
                "answers": [
                    {"answer": "11", "is_correct": True},
                    {"answer": "9", "is_correct": False},
                    {"answer": "10", "is_correct": False},
                    {"answer": "12", "is_correct": False},
                ],
            },
            {
                "question": "Which country hosted the first modern Olympic Games?",
                "mark": 5,
                "answers": [
                    {"answer": "Greece", "is_correct": True},
                    {"answer": "France", "is_correct": False},
                    {"answer": "USA", "is_correct": False},
                    {"answer": "UK", "is_correct": False},
                ],
            },
        ],
    },
]


class Command(BaseCommand):
    help = "Seed the database with categories, questions, and answers"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Clear existing data before seeding",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            self.stdout.write(self.style.WARNING("Clearing existing data..."))
            Answer.objects.all().delete()
            Question.objects.all().delete()
            Category.objects.all().delete()
            self.stdout.write(self.style.WARNING("Existing data cleared."))

        self.seed()

    @transaction.atomic
    def seed(self):
        created_count = 0
        skipped_count = 0

        for cat_data in category_data:
            category, created = Category.objects.get_or_create(
                name=cat_data["name"],
                defaults={
                    "description": cat_data["description"],
                    "total_time": cat_data["total_time"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {category.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Category '{category.name}' already exists, skipping."))

            for q_data in cat_data["questions"]:
                question, q_created = Question.objects.get_or_create(
                    category=category,
                    question=q_data["question"],
                    defaults={"mark": q_data["mark"]},
                )
                if q_created:
                    created_count += 1
                    self.stdout.write(f"  Created question: {question.question[:50]}...")
                    for a_data in q_data["answers"]:
                        Answer.objects.create(
                            question=question,
                            answer=a_data["answer"],
                            is_correct=a_data["is_correct"],
                        )
                else:
                    skipped_count += 1

            category.get_total()
            category.save()

        self.stdout.write(self.style.SUCCESS(
            f"\nSeeding complete! Created {created_count} new questions, skipped {skipped_count} existing."
        ))
