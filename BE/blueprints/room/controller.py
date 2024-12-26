from blueprints.room.model import RoomModel

# def get_all_classes():
#     classes = RoomModel.get_all_records()
#     result = []

#     for clas in classes:
#         result.append(clas.convert_json())

#     return result


def get_all_room_by_filter(page,perPage,name):
    rooms = RoomModel.find_all_by_filter(page = page, perPage = perPage, room_name = name)
    result = []

    for room in rooms:
        result.append(room.convert_json())

    return result

def get_record_by_name(name):
    record = RoomModel.find_by_name(room_name=name)
    return record.convert_json()

def get_by_id(id):
    room_object = RoomModel.find_by_id(id)
    return room_object.convert_json()
