from blueprints.gender.model import GenderModel

def get_all_genders():
    genders = GenderModel.get_all_records()
    result = []

    for gender in genders:
        result.append(gender.convert_json())

    return result