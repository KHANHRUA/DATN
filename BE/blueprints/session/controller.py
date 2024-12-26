from blueprints.session.model import SessionModel

def get_all_sessions_by_filter(class_id, date_from, date_to):
    sessions = SessionModel.find_all_by_filter(class_id = class_id)
    result = []

    for session in sessions:
        if date_from is not None and session.start_at < int(date_from):
            continue

        # Check date_to filter
        if date_to is not None and session.start_at > int(date_to):
            continue
        result.append(session.convert_json())

    return result

def get_current_session(room_id, current_time):
    sessions = SessionModel.find_all_by_filter(room_id = room_id)
    for session in sessions:
        # if session.start_at - 10*60*1000 > int(current_time*1000):
        #     continue

        # # Check date_to filter
        # if session.end_at + 10*60*1000 < int(current_time*1000):
        #     continue
        return session.convert_json()
    return False


def get_by_id(id):
    subject_object = SessionModel.find_by_id(id)
    return subject_object.convert_json()
