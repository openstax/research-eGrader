import csv

from eGrader.core import db
from eGrader.models import Exercise

def get_rows(filename):
    with open(filename, 'r') as csvfile:
        datareader = csv.DictReader(csvfile)
        for row in datareader:
            yield row


def update_exercises_with_book_info(file_name):
    count = 0
    for row in get_rows(file_name):
        count +=1
        print(count)
        if not row['Section'] == 0 and row['Exercise Numbers']:
            chapter = row['Chapter']
            section = row['Section']
            exercise_ids = row['Exercise Numbers'].split(',')
            for exercise_id in exercise_ids:
                exercise = db.session.query(Exercise) \
                    .filter(Exercise.uid.like('{0}@%'.format(exercise_id))) \
                    .first()
                if exercise:
                    exercise.chapter_id = chapter
                    exercise.section_id = section
                    exercise.book_row_id = count
                    db.session.add(exercise)

    db.session.commit()
