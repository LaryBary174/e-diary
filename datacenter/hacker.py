import random

from .models import *


def fix_marks(schoolkid):
    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid)


        child_bad_marks = Mark.objects.filter(schoolkid=child, points__in=[2, 3])
        for mark in child_bad_marks:
            mark.points = 5
            mark.save()
        print(f'Все плохие оценки ученика {child} исправлены, можно показывать дневник маме')
    except Schoolkid.MultipleObjectsReturned:
        print('Несколько имен, уточните')
    except Schoolkid.DoesNotExist:
        print('Нет такого ученика')

def delete_chastisement(schoolkid):
    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid)
        chastisement = Chastisement.objects.filter(schoolkid=child)
        for chast in chastisement:
            chast.delete()
        print(f'Все замечания ученика {child} удалены')
    except Schoolkid.MultipleObjectsReturned:
        print('Несколько имен, уточните')
    except Schoolkid.DoesNotExist:
        print('Нет такого ученика')


def create_commendation(schoolkid, subject_title):
    commendation_list = [
        'Молодец', 'Отлично', 'Очень хороший ответ!', 'Уже существенно лучше!', 'Потрясающе!', 'Так держать!',
        'Это как раз то, что нужно!'
    ]
    best_commendation = random.choice(commendation_list)
    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid)
        subject = Subject.objects.get(title=subject_title,year_of_study=child.year_of_study)
        lesson = Lesson.objects.filter(
            subject=subject,
            year_of_study=child.year_of_study,
            group_letter=child.group_letter,
        ).order_by('date').first()
        teacher = lesson.teacher
        lesson_date = lesson.date
        commendation = Commendation.objects.create(
            text=best_commendation,
            created=lesson_date,
            schoolkid=child,
            subject=subject,
            teacher=teacher,
        )
        commendation.save()
        print(f'Похвала ученику {child} по предмету {subject} записана')
    except Schoolkid.MultipleObjectsReturned:
        print('Несколько имен, уточните')
    except Schoolkid.DoesNotExist:
        print('Нет такого ученика')







