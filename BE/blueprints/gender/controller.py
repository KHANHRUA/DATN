from blueprints.gender.model import GenderModel

def get_all_genders():
    genders = GenderModel.get_all_records()
    result = []

    for gender in genders:
        result.append(gender.convert_json())

    return result

def get_by_id(id):
    gender_object = GenderModel.find_by_id(id)
    return gender_object.convert_json()