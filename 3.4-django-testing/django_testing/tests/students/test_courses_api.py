import pytest
from model_bakery import baker
from rest_framework import status
from students.models import Course, Student


@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(**kwargs):
        return baker.make('students.Course', **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(**kwargs):
        return baker.make('students.Student', **kwargs)
    return factory


# 1. Тест получения курса
@pytest.mark.django_db
def test_retrieve_course(api_client, course_factory):
    course = course_factory(name='Test Course')
    url = f'/api/v1/courses/{course.id}/'
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == course.id
    assert response.data['name'] == 'Test Course'


# 2. Тест получения списка курсов
@pytest.mark.django_db
def test_list_courses(api_client, course_factory):
    courses = course_factory(_quantity=3)
    url = '/api/v1/courses/'
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3


# 3. Тест фильтрации по id
@pytest.mark.django_db
def test_filter_courses_by_id(api_client, course_factory):
    courses = course_factory(_quantity=3)
    target_course = courses[1]
    url = f'/api/v1/courses/?id={target_course.id}'
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['id'] == target_course.id


# 4. Тест фильтрации по name
@pytest.mark.django_db
def test_filter_courses_by_name(api_client, course_factory):
    course1 = course_factory(name='Python Course')
    course2 = course_factory(name='Django Course')
    url = '/api/v1/courses/?name=Python Course'
    response = api_client.get(url)
    
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'Python Course'


# 5. Тест создания курса
@pytest.mark.django_db
def test_create_course(api_client):
    url = '/api/v1/courses/'
    course_data = {'name': 'New Course'}
    response = api_client.post(url, data=course_data, format='json')
    
    assert response.status_code == status.HTTP_201_CREATED
    assert Course.objects.count() == 1
    assert Course.objects.get().name == 'New Course'


# 6. Тест обновления курса
@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    course = course_factory(name='Old Name')
    url = f'/api/v1/courses/{course.id}/'
    update_data = {'name': 'Updated Name'}
    response = api_client.put(url, data=update_data, format='json')
    
    assert response.status_code == status.HTTP_200_OK
    course.refresh_from_db()
    assert course.name == 'Updated Name'


# 7. Тест удаления курса
@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    course = course_factory()
    url = f'/api/v1/courses/{course.id}/'
    response = api_client.delete(url)
    
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Course.objects.count() == 0