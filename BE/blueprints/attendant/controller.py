from blueprints.attendant.model import AttendantModel

def get_all_classes():
    classes = AttendantModel.get_all_records()
    result = []

    for clas in classes:
        result.append(clas.convert_json())

    return result


def get_all_classes_by_filter(page,perPage,user_id):
    attendants = AttendantModel.find_all_by_filter(page = page, perPage = perPage, user_id = user_id)
    result = []

    for attendant in attendants:
        result.append(attendant.convert_json())

    return result

# def get_by_id(id):
#     class_object = ClassModel.find_by_id(id)
#     return class_object.convert_json()
