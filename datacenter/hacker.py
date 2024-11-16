import random

from .models import Schoolkid, Subject, Lesson, Chastisement, Commendation, Mark


def get_schoolkid(schoolkid):
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid)
    except Schoolkid.MultipleObjectsReturned:
        print('Несколько имен, уточните')
    except Schoolkid.DoesNotExist:
        print('Нет такого ученика')
    return None


def fix_marks(schoolkid):
    child = get_schoolkid(schoolkid)

    Mark.objects.filter(schoolkid=child, points__in=[2, 3]).update(points=5)

    print(f'Все плохие оценки ученика {child} исправлены, можно показывать дневник маме')


def delete_chastisement(schoolkid):
    child = get_schoolkid(schoolkid)
    Chastisement.objects.filter(schoolkid=child).delete()

    print(f'Все замечания ученика {child} удалены')


def create_commendation(schoolkid, subject_title, lesson_date):
    commendations = [
        'Молодец', 'Отлично', 'Очень хороший ответ!', 'Уже существенно лучше!', 'Потрясающе!', 'Так держать!',
        'Это как раз то, что нужно!'
    ]
    best_commendation = random.choice(commendations)

    child = get_schoolkid(schoolkid)
    subject = Subject.objects.filter(title=subject_title, year_of_study=child.year_of_study).first()
    if not subject:
        print(f'Предмет с названием "{subject_title}" для указанного класса не найден.')
    lesson = Lesson.objects.filter(
        subject=subject,
        year_of_study=child.year_of_study,
        group_letter=child.group_letter,
        date=lesson_date
    ).first()
    if not lesson:
        print(f'Не найден урок для создания похвалы на указанную дату {lesson_date}.')
    teacher = lesson.teacher

    Commendation.objects.create(
        text=best_commendation,
        created=lesson_date,
        schoolkid=child,
        subject=subject,
        teacher=teacher,
    )

    print(f'Похвала ученику {child} по предмету {subject} записана')
