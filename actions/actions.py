# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

# from underthesea import ner
from pprint import pprint


class ActionGraduationCondition(Action):
    def name(self) -> Text:
        return "action_graduation_condition"
    
    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        entities = (tracker.latest_message)['entities']
        
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
        dispatcher.utter_message(text=message)
        return []


