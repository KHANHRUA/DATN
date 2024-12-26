from blueprints.subject.model import SubjectModel

def get_all_subjects():
    subjects = SubjectModel.get_all_records()
    result = []

    for subject in subjects:
        result.append(subject.convert_json())

    return result


def get_all_classes_by_filter(page,perPage,name):
    subjects = SubjectModel.find_all_by_filter(page = page, perPage = perPage, name = name)
    result = []

    for subject in subjects:
        result.append(subject.convert_json())

    return result

def get_by_id(id):
    subject_object = SubjectModel.find_by_id(id)
    return subject_object.convert_json()