import json
import os
import re
from django.core.management.base import BaseCommand
from django.db import transaction
from home.models import Category, Question, Answer


LETTERS = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4}
JSON_PATH = os.path.join(os.path.dirname(__file__), *[os.pardir] * 3, "all_questions.json")

PDF_CATEGORIES = {
    "NSDA Level-4 Python with Django Advanced MCQ.pdf": {
        "name": "Python & Django (Advanced MCQ)",
        "description": "100 English MCQ questions covering Python basics, Django Models, ORM, Forms, Serializers, and advanced topics from NSDA Level-4.",
        "time": 60,
    },
    "NSDA Level-4 Python with Django (Advanced MCQ).pdf": {
        "name": "Python & Django (Advanced MCQ - BN)",
        "description": "50 Bengali MCQ questions covering Python and Django fundamentals from NSDA Level-4.",
        "time": 30,
    },
    "Python with Django MCQ (100+).pdf": {
        "name": "Python & Django (MCQ 100+)",
        "description": "105 MCQ questions in Bengali covering Python basics, operators, functions, OOP, Django, SQL, HTML, and deployment.",
        "time": 60,
    },
    "NSDA Level-4 Python with Django Written Questions with Answers.pdf": {
        "name": "Python & Django (Written)",
        "description": "120 written/theory questions with detailed answers covering Python advanced topics, OOP, Django MVT, ORM, Forms, DRF, signals, caching, security, and error handling.",
        "time": 120,
    },
}


def clean_option(text):
    return re.sub(r"^[A-Ea-e][.．)\s]*", "", text).strip()


def parse_mcq(q):
    options_raw = q.get("options")
    answer_text = (q.get("answer") or "").strip()

    if options_raw:
        correct_letter = answer_text.upper()
        correct_idx = LETTERS.get(correct_letter, -1)

        answers = []
        for i, opt in enumerate(options_raw):
            text = clean_option(opt)
            if text:
                answers.append({"answer": text, "is_correct": i == correct_idx})

        if answers:
            return {
                "question": q["question"],
                "mark": 5,
                "answers": answers,
            }

    if answer_text:
        return {
            "question": q["question"],
            "mark": 5,
            "answers": [{"answer": answer_text, "is_correct": True}],
        }

    return None


def parse_written(q):
    answer_text = q.get("answer", "").strip()
    if not answer_text or answer_text == "See PDF for detailed answer":
        answer_text = "See answer in PDF"
    return {
        "question": q["question"],
        "mark": 5,
        "answers": [{"answer": answer_text[:500], "is_correct": True}],
    }


class Command(BaseCommand):
    help = "Seed ALL Python & Django questions from extracted PDF data into separate categories"

    def add_arguments(self, parser):
        parser.add_argument("--clear", action="store_true", help="Clear all Python & Django categories before seeding")

    def handle(self, *args, **options):
        if not os.path.exists(JSON_PATH):
            self.stdout.write(self.style.ERROR(f"JSON file not found: {JSON_PATH}"))
            return

        with open(JSON_PATH, encoding="utf-8") as f:
            data = json.load(f)

        if options["clear"]:
            for name in [info["name"] for info in PDF_CATEGORIES.values()] + ["Python & Django"]:
                cat = Category.objects.filter(name=name).first()
                if cat:
                    cat.questions.all().delete()
                    cat.delete()
            self.stdout.write(self.style.WARNING("Cleared all Python & Django categories."))

        self.seed(data)

    @transaction.atomic
    def seed(self, data):
        total_created = 0
        total_skipped = 0

        for pdf_entry in data["pdfs"]:
            filename = pdf_entry["file"]
            info = PDF_CATEGORIES.get(filename)
            if not info:
                continue

            category, created = Category.objects.get_or_create(
                name=info["name"],
                defaults={
                    "description": info["description"],
                    "total_time": info["time"],
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {category.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"Category '{category.name}' already exists, adding questions."))

            created_count = 0
            skipped_count = 0

            for q in pdf_entry["questions"]:
                if pdf_entry["type"] == "mcq":
                    parsed = parse_mcq(q)
                else:
                    parsed = parse_written(q)

                if not parsed:
                    skipped_count += 1
                    continue

                question, q_created = Question.objects.get_or_create(
                    category=category,
                    question=parsed["question"],
                    defaults={"mark": parsed["mark"]},
                )
                if q_created:
                    created_count += 1
                    for a_data in parsed["answers"]:
                        Answer.objects.create(
                            question=question,
                            answer=a_data["answer"],
                            is_correct=a_data["is_correct"],
                        )
                else:
                    skipped_count += 1

            category.get_total()
            category.save()

            total_created += created_count
            total_skipped += skipped_count

            self.stdout.write(f"  -> {category.name}: {created_count} created, {skipped_count} skipped")

        self.stdout.write(self.style.SUCCESS(
            f"\nDone! Total: {total_created} created, {total_skipped} skipped across {len(PDF_CATEGORIES)} categories."
        ))
