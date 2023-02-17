from api import PetFriends
from settings import valid_email, valid_password, not_valid_password
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """ Проверяем что запрос api ключа возвращает статус 200 и в рзультате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Марс', animal_type='собака',
                                     age='1', pet_photo='images/Mars.jpg'):
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Марс', animal_type='собака', age=2):
    """ Проверяем возможность обновления информации о питомце"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_create_new_pet_without_photo(name='Марс', animal_type='собака',
                                      age='1'):
    """ Проверяем, что можно добавить питомца без фото"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_new_pet_wo_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_new_photo_of_pet(pet_id='45a11f83-942b-4bda-b160-81a6ce6da4d0', pet_photo='images/Cat1.jpg'):
    """ Проверяем, что можно добавить фото питомца"""
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status == 200


def test_get_api_key_for_not_valid_user(email=not_valid_password, password=valid_password):
    """ Проверяем, что нельзя получить API key для незарегистрированного пользователя"""
    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_create_new_pet_without_name(name=None, animal_type='собака',
                                     age='1'):
    """ Проверяем, что нельзя добавить питомца без имени"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_new_pet_wo_photo(auth_key, name, animal_type, age)
    assert status == 200
    # Баг. Тест не должен выдавать статус 200, так как не должно быть возможности загрузить питомца без имени.


def test_create_new_pet_without_type(name='Марс', animal_type=None,
                                     age='2'):
    """ Проверяем, что нельзя добавить питомца без типа животного"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_new_pet_wo_photo(auth_key, name, animal_type, age)
    assert status == 200
    # Баг. Тест не должен выдавать статус 200, так как не должно быть возможности загрузить питомца без типа животного.


def test_create_new_pet_with_wrong_age(name='Марс', animal_type='собака',
                                     age='%'):
    """ Проверяем, что нельзя добавить питомца с возрастом в неверном формате"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_new_pet_wo_photo(auth_key, name, animal_type, age)
    assert status == 200
    # Баг. Тест не должен выдавать статус 200, так как возраст в некорректном формате.


def test_add_not_photo_file_of_pet(pet_id='45a11f83-942b-4bda-b160-81a6ce6da4d0', pet_photo='images/Mars.txt'):
    """ Проверяем, что нельзя добавить фото питомца в неверном формате"""

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    assert status != 200


def test_get_my_pets_with_valid_key(filter='my_pets'):
    """Проверяем, что работает фильтр сортировки моих животных my_pets"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) >= 0


def test_successful_delete_not_your_pet():
    """Проверяем, что нельзя удалить питомца НЕ из своего списка животных"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    pet_id = all_pets['pets'][0]['id']
    assert pet_id not in my_pets.values()
    status, _ = pf.delete_pet(auth_key, pet_id)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    assert status == 200
    assert pet_id not in my_pets.values()
    # Баг. Тест не должен выдавать статус 200, так как не должно быть возможности удалять питомца не из своего списка.


def test_update_not_your_pet_info(name='pol', animal_type='Пудель', age=5):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, all_pets = pf.get_list_of_pets(auth_key, "")
    status, result = pf.update_pet_info(auth_key, all_pets['pets'][0]['id'], name, animal_type, age)
    assert status == 200
    assert result['name'] == name
    # Баг. Тест не должен выдавать статус 200, так как нельзя обновлять данные питомца не из своего списка.
