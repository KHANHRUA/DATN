from blueprints.user_subject.model import UserSubjectModel

def get_all_subjects():
    subjects = UserSubjectModel.get_all_records()
    result = []

    for subject in subjects:
        result.append(subject.convert_json())

    return result


def get_all_relative_by_filter(page,perPage,name):
    relative_objects = UserSubjectModel.find_all_by_filter(page = page, perPage = perPage, name = name)
    result = []

    for relative_object in relative_objects:
        result.append(relative_object.convert_json())

    return result

def get_by_user_id(id):
    result = []
    relative_objects = UserSubjectModel.find_by_user_id(id)
    for relative_object in relative_objects:
        result.append(relative_object.convert_json())
    return result

def get_model_by_user_id(id):
    return UserSubjectModel.find_by_user_id(id)

def get_by_subject_id(id):
    result = []
    relative_objects = UserSubjectModel.find_by_subject_id(id)
    for relative_object in relative_objects:
        result.append(relative_object.convert_json())
    return result