# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions
import re
from typing import Any, Text, Dict, List
import psql as db
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from underthesea import pos_tag
import difflib


def diff_check(orig_word: str, target_word: str) -> float:
    return difflib.SequenceMatcher(None, orig_word, target_word).ratio()

class ActionGraduationCondition(Action):
    def name(self) -> Text:
        return "action_graduation_condition"

    def response_message(self, entities):
        text = """
                        - Cho đến thời điểm xét tốt nghiệp không bị truy cứu trách nhiệm hình sự hoặc
                       không đang trong thời gian bị kỷ luật ở mức đình chỉ học tập;\n
                       - Tích lũy đủ số học phần, số tín chỉ theo đúng quy định cho từng chương trình đào
                       tạo của trường;\n
                       - Điểm trung bình chung tích lũy của toàn khóa học đạt từ 2,00 trở lên;\n
                       - Thỏa mãn một số yêu cầu về kết quả học tập đối với nhóm học phần thuộc ngành
                       đào tạo chính và các điều kiện khác do Hiệu trưởng quy định;\n
                       - Có chứng chỉ Giáo dục quốc phòng - an ninh đối với các ngành đào tạo không
                       chuyên về quân sự và hoàn thành học phần Giáo dục thể chất đối với các ngành đào tạo
                       không chuyên về thể dục - thể thao, ngoại ngữ không chuyên.\n
                       - Có đơn gửi Phòng Đào tạo Đại học đề nghị được xét tốt nghiệp trong trường hợp
                       đủ điều kiện tốt nghiệp sớm hoặc muộn so với thời gian thiết kế của khóa học.
                       """
        if entities == []:
            message = text
        elif entities[0]['value'] != 'classification':
            message = """
                    Hạng tốt nghiệp được xác định theo điểm trung bình chung tích lũy của
                    toàn khóa học, như sau:\n
                        a) Loại xuất sắc: Điểm trung bình chung tích lũy từ 3,60 đến 4,00;\n
                        b) Loại giỏi: Điểm trung bình chung tích lũy từ 3,20 đến 3,59;\n
                        c) Loại khá: Điểm trung bình chung tích lũy từ 2,50 đến 3,19;\n
                        d) Loại trung bình: Điểm trung bình chung tích lũy từ 2,00 đến 2,49.\n
                    """
        elif entities[0]['value'] != 'mức điểm':
            message = "Điểm trung bình chung tích lũy của toàn khóa học đạt từ 2,00 trở lên;\n"
        else:
            message = text
        return message

    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = (tracker.latest_message)['entities']

        message = self.response_message(entities)

        dispatcher.utter_message(text=message)
        return []


class GetInfoTeacher(Action):
    def name(self) -> Text:
        return "action_ask_info_teacher"

    def get_subject_from_text(self, pos_tag_text):
        list_noun_text = [pos_tag_text[i][0] for i in range(len(pos_tag_text)) if pos_tag_text[i][1] == 'N']
        list_subjects_from_db = db.get_list_subject()
        arr = []
        text = ''
        for item in list_noun_text:
            for i in range(len(list_subjects_from_db)):
                if diff_check(list_subjects_from_db[i][0], item) > 0.65:
                    arr.append(list_subjects_from_db[i][0]) 
        if len(arr) > 1:
            text = list(set(arr))[0]
        elif len(arr) == 1:
            text = arr[0]
        else:
            text = '0'
        return text

    def response_message(self, latest_message):
        list_pos_tag_text = pos_tag(latest_message)
        subjects = self.get_subject_from_text(list_pos_tag_text)
        record = db.get_info_gv_from_mon_hoc(subjects)
        if subjects == '0' or len(record) == 0:
            message = 'Chưa có thông tin giáo viên cho môn học này bạn nhé !'
            return message
        teacher =  ', '.join([', '.join(i) for i in record])
        message = "Môn học " + subjects + ' có thầy/cô ' + teacher + 'dạy nhé. Bạn có thể lên trang tín chỉ để đăng kí những thầy,cô này .'
        return message

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = (tracker.latest_message)['text']
        message = self.response_message(latest_message)

        dispatcher.utter_message(text=message)
        return []

class GetInfoStudent(Action):
    def name(self) -> Text:
        return "action_ask_info_student"

    def get_student_code(self, latest_message):
        split_text = latest_message.split(' ')
        arr_msv = []
        for text in split_text:
            if re.match('[1-9]{2}[a-zA-Z]{1}[0-9]{7}', text):
                arr_msv.append(text)
        if len(arr_msv) > 0:
            return arr_msv[0]
        else:
            return '0'

    def get_D_chu(self, score):
        if score == 4:
            return 'A'
        elif score == 3:
            return 'B'
        elif score == 2:
            return 'C'
        else:
            return 'D'

    def format_text(self,list_subject_score):
        str = ''
        for item in list_subject_score:
            str += item[0] +' - ' +self.get_D_chu(item[1]) +'\n'
        return str

    def response_message(self, latest_message):
        student_code = self.get_student_code(latest_message)
        list_subject_score = db.get_info_student(student_code)
        if student_code == '0' or len(list_subject_score) == 0:
            return "Không tìm thấy tên học phần và mã sinh viên tương ứng !."
        else:
            str_list_subject_score = self.format_text(list_subject_score)
            message = "Tên học phần và điểm số của " + student_code + ' ' + str_list_subject_score
            return message

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        latest_message = (tracker.latest_message)['text']
        message = self.response_message(latest_message)

        dispatcher.utter_message(text=message)
        return []


