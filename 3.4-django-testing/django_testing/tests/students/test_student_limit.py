import pytest
from django.core.exceptions import ValidationError
from django.conf import settings


def validate_student_limit(students):
    """
    Валидатор для проверки максимального количества студентов
    """
    if len(students) > settings.MAX_STUDENTS_PER_COURSE:
        raise ValidationError(
            f'Количество студентов на курсе не может превышать {settings.MAX_STUDENTS_PER_COURSE}'
        )


@pytest.mark.parametrize('student_count,should_raise_error', [
    (20, False),  
    (21, True),   
])
def test_student_limit_with_settings(settings, student_count, should_raise_error):
    """Тестируем ограничение студентов используя parametrize и settings"""
    
    settings.MAX_STUDENTS_PER_COURSE = 20
    
    # Создаем mock список студентов
    students_list = list(range(student_count))
    
    if should_raise_error:
       
        with pytest.raises(ValidationError) as exc_info:
            validate_student_limit(students_list)
        assert 'не может превышать 20' in str(exc_info.value)
    else:
       
        validate_student_limit(students_list)  