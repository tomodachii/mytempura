from nlp.models import (
    NLPBot,
    TrainingPhrase,
    Intent,
    Response,
    Entity,
    ResponseEntityCategory,
    EntityCategory,
)
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
import string
from sklearn.feature_extraction.text import CountVectorizer
import os
import pickle
from nlp.exceptions import NLPServiceException
import random
import re
from django.db.models import Count
from underthesea import ner


LIST_DEFAULT_INTENT = [
    {"target": "positive", "data": "Đúng rồi"},
    {"target": "positive", "data": "Đúng rồi nhé"},
    {"target": "positive", "data": "Đúng rồi nha"},
    {"target": "positive", "data": "Đúng"},
    {"target": "positive", "data": "Phải rồi"},
    {"target": "positive", "data": "Oke"},
    {"target": "positive", "data": "Ok"},
    {"target": "positive", "data": "Chuẩn"},
    {"target": "positive", "data": "Được"},
    {"target": "positive", "data": "Được nha"},
    {"target": "positive", "data": "Được nhé"},
    {"target": "positive", "data": "đc"},
    {"target": "positive", "data": "đc nha"},
    {"target": "positive", "data": "đc nhé"},
    {"target": "positive", "data": "tốt"},
    {"target": "positive", "data": "chính xác"},
    {"target": "positive", "data": "chuẩn nha"},
    {"target": "positive", "data": "good"},
    {"target": "positive", "data": "yea"},
    {"target": "positive", "data": "yes"},
    {"target": "stop", "data": "thôi"},
    {"target": "stop", "data": "Không"},
    {"target": "stop", "data": "Không nhé"},
    {"target": "stop", "data": "Không nha"},
    {"target": "stop", "data": "Thôi"},
    {"target": "stop", "data": "Dừng"},
    {"target": "stop", "data": "Dừng lại"},
    {"target": "stop", "data": "Dừng lại đi"},
    {"target": "stop", "data": "stop"},
    {"target": "negative", "data": "Sai"},
    {"target": "negative", "data": "Nhầm rồi"},
    {"target": "negative", "data": "sai rồi"},
    {"target": "negative", "data": "sai rồi kìa"},
    {"target": "negative", "data": "đợi đã"},
    {"target": "negative", "data": "đợi chút"},
    {"target": "negative", "data": "sửa lại tí"},
    {"target": "negative", "data": "thay đổi chút"},
    {"target": "negative", "data": "sửa chút"},
    {"target": "what_about", "data": "Thế còn thì sao"},
    {"target": "what_about", "data": "thế thì thế nào"},
    {"target": "what_about", "data": "còn thì sao"},
    {"target": "what_about", "data": "thì thế nào"},
]

LIST_FALLBACK = [
    "Xin lỗi bot không hiểu ý của bạn, bạn có thế diễn đạt rõ hơn được không",
    "Xin lỗi nha bot không hiểu ý bạn, bạn có thế nói rõ hơn được không :(",
    "bot không hiểu ý bạn :( bạn chat rõ hơn được không, bot xin lỗi nhé :(",
]

LIST_DEFAULT_CATEGORY = ["Họ Tên", "Địa chỉ", "Email", "SĐT"]


class NLPService:
    def __init__(self, bot: NLPBot, context: dict):
        self.bot = bot
        self.context = context
        self.data = []
        self.target = []
        self.entities = []
        self.model = None

    def build_data_and_target_list(self):
        # Get all TrainingPhrase objects associated with the given bot
        training_phrases = TrainingPhrase.objects.filter(intent__bot=self.bot)

        # Create lists to store the training data and target intent objects
        data_list = []
        target_list = []

        for training_phrase in training_phrases:
            # Add the training phrase to the data_list
            data_list.append(training_phrase.phrase)

            # Get the associated intent and add it to the target_list
            target_list.append(training_phrase.intent.intent_name)

        return data_list, target_list

    def text_preprocess(self, text: str):
        translator = str.maketrans("", "", string.punctuation)
        text = text.translate(translator)

        # Convert text to lowercase
        text = text.lower()

        # Remove redundant spaces
        text = " ".join(text.split())

        return text

    def save_model(self):
        if self.bot.id is None:
            raise NLPServiceException(
                "Bot must be saved to the database before saving the model."
            )

        # Create the data directory if it doesn't exist
        data_dir = "nlp/data"
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

        # Define the filename based on the bot's id and name
        filename = f"{self.bot.id}_{self.bot.name}.pkl"
        model_path = os.path.join(data_dir, filename)

        # Save the model using pickle
        with open(model_path, "wb") as file:
            pickle.dump(self.model, file)

        return model_path

    def train_model(self):
        default_data_list = [entry["data"] for entry in LIST_DEFAULT_INTENT]
        default_target_list = [entry["target"] for entry in LIST_DEFAULT_INTENT]
        for i, data in enumerate(default_data_list):
            intent, _ = Intent.objects.get_or_create(
                bot=self.bot, intent_name=default_target_list[i]
            )
            TrainingPhrase.objects.get_or_create(intent=intent, phrase=data)
        raw_train_data, train_target = self.build_data_and_target_list()
        raw_train_data = raw_train_data + default_data_list
        train_target = train_target + default_target_list
        train_data = [self.text_preprocess(data) for data in raw_train_data]
        # Create a TF-IDF vectorizer
        vectorizer = CountVectorizer()

        X_train_vector = vectorizer.fit_transform(train_data)

        model = None

        if self.bot.intent_set.count() <= 2:
            model = MultinomialNB()
        else:
            model = SVC()

        model.fit(X_train_vector, train_target)
        self.model = model
        self.save_model()

    def load_model(self):
        if self.bot.id is None:
            raise NLPServiceException(
                "Bot must be saved to the database before loading the model."
            )

        # Define the filename based on the bot's id and name
        filename = f"{self.bot.id}_{self.bot.name}.pkl"
        model_path = os.path.join("nlp/data", filename)

        if os.path.exists(model_path):
            # Load the model using pickle
            with open(model_path, "rb") as file:
                model = pickle.load(file)
            return model
        else:
            # If the model doesn't exist, train a new one and save it
            model = self.train_model()
            return model

    def predict(self, input_text: str):
        # Load the model or train a new one if it doesn't exist
        if not hasattr(self, "model") or self.model is None:
            self.model = self.load_model()

        # Preprocess the input text
        preprocessed_text = self.text_preprocess(input_text)

        # Transform the input text using the vectorizer
        raw_train_data, train_target = self.build_data_and_target_list()
        train_data = [self.text_preprocess(data) for data in raw_train_data]
        # Create a TF-IDF vectorizer
        vectorizer = CountVectorizer()

        vectorizer.fit_transform(train_data)
        input_vector = vectorizer.transform([preprocessed_text])

        # Use the trained model to make predictions
        prediction = self.model.predict(input_vector)

        return prediction[0]

    def reset_context(self):
        self.context = {
            "current_intent": "",
            "extracted_entities": [],
            "need_confirmation": False,
            "required_entity_categories": [],
            "template_response_id": 0,
            "is_intent_interupt": False,
            "Email": None,
            "SĐT": None,
            "Địa chỉ": None,
            "Họ Tên": None,
        }
        return self.context

    def lists_are_equal(self, A, B):
        sorted_list_A = sorted(A, key=lambda x: (x, A.index(x)))
        sorted_list_B = sorted(B, key=lambda x: (x, B.index(x)))
        if len(sorted_list_A) == len(sorted_list_B):
            return all(a == b for a, b in zip(sorted_list_A, sorted_list_B))
        else:
            return False

    def extract_entity_category(self, input_text: str):
        entity_categories = EntityCategory.objects.filter(bot=self.bot)
        extracted_entity_category = []
        for entity_category in entity_categories:
            pattern = entity_category.category_name
            if entity_category.synonym:
                pattern = "{}|{}".format(
                    entity_category.category_name,
                    entity_category.synonym.lower().replace(",", "|").replace(" ", ""),
                )
            pattern = re.compile(pattern)
            if len(re.findall(pattern, input_text.lower().replace(" ", ""))) > 0:
                extracted_entity_category.append(entity_category)

        return extracted_entity_category

    def extract_entity(self, input_text: str):
        entities = Entity.objects.filter(bot=self.bot)
        extracted_entities = []
        for entity in entities:
            pattern = entity.entity_name
            if entity.synonym:
                pattern = "{}|{}".format(
                    entity.entity_name,
                    entity.synonym.lower().replace(",", "|").replace(" ", ""),
                )
            pattern = re.compile(pattern)
            if len(re.findall(pattern, input_text.lower().replace(" ", ""))) > 0:
                extracted_entities.append(entity)

        return extracted_entities

    def extract_email(self, input_text: str):
        mail = re.compile(r"[\w\-\.]+\@[\w\-\.]+")
        res = re.findall(mail, input_text)
        if res:
            self.context["Email"] = res
            return True
        return False

    def extract_phone(self, input_text):
        phone_regex = re.compile(r"\b\d{10}\b")
        phone_numbers = phone_regex.findall(input_text)
        if phone_numbers:
            self.context["SĐT"] = phone_numbers[0]
            return True
        return False

    def extract_location(self, user_text):
        list_location = []
        location = []
        for list_ner in ner(user_text):
            if "LOC" in list_ner[-1]:
                location.append(list_ner[0])
            else:
                if len(location) > 0:
                    list_location.append(" ".join(location))
                    location = []
        if len(location) > 0:
            list_location.append(" ".join(location))
            location = []
        if len(list_location) > 0:
            self.context["Địa chỉ"] = list_location
            return True
        return False

    def extract_name(self, input_text):
        list_name = []
        name = []
        for list_ner in ner(input_text):
            if "PER" in list_ner[-1]:
                name.append(list_ner[0])
            else:
                if len(name) > 0:
                    list_name.append(" ".join(name))
                    name = []
        if len(name) > 0:
            list_name.append(" ".join(name))
            name = []
        if len(list_name) > 0:
            self.context["Họ Tên"].extend(list_name)
            return True
        return False

    # idx = self.context["required_entity_categories"].index(
    #                 entity.entity_category.category_name
    #             )
    #             self.context["required_entity_categories"].pop(idx)
    #             self.context["extracted_entities"].append(entity.entity_name)

    def extract_non_defined_entities(self, input_text: str):
        extracted_data = []
        # removed_required_entity_category = []
        if self.context["required_entity_categories"]:
            for category_name in self.context["required_entity_categories"]:
                if category_name in LIST_DEFAULT_CATEGORY:
                    if category_name == "Email" and self.extract_email(input_text):
                        extracted_data.append(self.context["Email"])
                        # removed_required_entity_category.append("Email")
                    if category_name == "SĐT" and self.extract_phone(input_text):
                        extracted_data.append(self.context["SĐT"])
                        # removed_required_entity_category.append("SĐT")
                    if category_name == "Địa chỉ" and self.extract_location(input_text):
                        extracted_data.append(self.context["Địa chỉ"])
                        # removed_required_entity_category.append("Địa chỉ")
                    if category_name == "Họ Tên" and self.extract_name(input_text):
                        extracted_data.append(self.context["Họ Tên"])
                        # removed_required_entity_category.append("Họ Tên")
            # for entity_category in removed_required_entity_category:
            #     idx = self.context["required_entity_categories"].index(entity_category)
            #     self.context["required_entity_categories"].pop(idx)
        return extracted_data

    def match_non_defined_category(self):
        for entity_category in ["SĐT", "Email", "Địa chỉ", "Họ Tên"]:
            if self.context[entity_category]:
                idx = self.context["required_entity_categories"].index(entity_category)
                self.context["required_entity_categories"].pop(idx)

    def match_entities(self, entities: list):
        for entity in entities:
            if (
                entity.entity_category.category_name
                in self.context["required_entity_categories"]
                and entity.entity_name not in self.context["extracted_entities"]
            ):
                idx = self.context["required_entity_categories"].index(
                    entity.entity_category.category_name
                )
                self.context["required_entity_categories"].pop(idx)
                self.context["extracted_entities"].append(entity.entity_name)

    def matching_provide_response(self, intent, template_response, responses):
        if not self.context["required_entity_categories"]:
            for response in responses:
                response_entity_set = response.responseentity_set.all()
                entity_list = []

                for response_entity in response_entity_set:
                    entity_list.append(response_entity.entity.entity_name)
                # if set(self.context["extracted_entities"]) == set(entity_list):
                if self.lists_are_equal(
                    self.context["extracted_entities"], entity_list
                ):
                    if response.message_type == Response.PROVIDE_CONFIRM:
                        self.context["current_intent"] = intent.intent_name
                        self.context["need_confirmation"] = True
                    else:
                        self.reset_context()
                    return response.response
        else:
            self.context["current_intent"] = intent.intent_name
            self.context["template_response_id"] = template_response.id
            # get collect response
            responses = Response.objects.filter(
                intent=intent, message_type=Response.COLLECT
            )
            for response in responses:
                response_required_category_set = (
                    response.responseentitycategory_set.all()
                )
                required_category_list = []

                for required_category in response_required_category_set:
                    required_category_list.append(
                        required_category.required_category.category_name
                    )
                # if set(self.context["required_entity_categories"]) == set(
                #     required_category_list
                # ):
                if self.lists_are_equal(
                    self.context["required_entity_categories"], required_category_list
                ):
                    return response.response

            if self.context["is_intent_interupt"]:
                return "Mình thấy bạn đang muốn hỏi cái khác, bạn có còn muốn hỏi về {} nữa không? Nếu có, bạn vui lòng bổ sung những thông tin sau: {}".format(
                    intent.intent_name,
                    ", ".join(self.context["required_entity_categories"]),
                )
            return "Để {}, bạn vui lòng bổ sung những thông tin sau: {}".format(
                intent.intent_name,
                ", ".join(self.context["required_entity_categories"]),
            )

    def generate_provide_response(
        self, template_response: Response, extracted_entities: list
    ) -> (str, dict):
        intent = template_response.intent
        responses = Response.objects.filter(intent=intent)
        required_entity_categories = ResponseEntityCategory.objects.filter(
            response=template_response
        )
        if required_entity_categories.exists():
            for required_entity_category in required_entity_categories:
                self.context["required_entity_categories"].append(
                    required_entity_category.required_category.category_name
                )
            # extracted_entities = self.extract_entity(
            #     input_text=input_text, response_type=Response.PROVIDE
            # )
            self.match_entities(entities=extracted_entities)
            return self.matching_provide_response(
                intent=intent,
                template_response=template_response,
                responses=responses,
            )
        else:
            raise NLPServiceException("Required Category does not exist")

    def generate_addition_info_collect_response(self, extracted_entities: list):
        intent = Intent.objects.get(
            bot=self.bot, intent_name=self.context["current_intent"]
        )
        responses = Response.objects.filter(intent=intent)
        template_response = Response.objects.get(
            id=self.context["template_response_id"]
        )
        # extracted_entities = self.extract_entity(
        #     input_text=input_text, response_type=Response.PROVIDE
        # )
        self.match_entities(extracted_entities)

        return self.matching_provide_response(
            intent=intent,
            template_response=template_response,
            responses=responses,
        )

    # def match_provide_template_response(
    #     self,
    #     intent: Intent,
    #     extracted_entities: list,
    #     extracted_entity_categories: list,
    # ):
    #     responses_filter_by_intent = Response.objects.filter(intent=intent, message_type__in=[Response.PROVIDE, Response.PROVIDE_CONFIRM])
    #     for response in responses_filter_by_intent:
    #         if extracted_entities:
    #             response_entity_set = (
    #                 responses_filter_by_intent.responseentity_set.all()
    #             )
    #             entity_list = []
    #             for response_entity in response_entity_set:
    #                 entity_list.append(response_entity.entity.entity_name)
    #             if set(extracted_entities) == set(entity_list):
    #                 return response
    #     return None

    from django.db.models import Count

    def get_response_with_biggest_entity_category(responses):
        if not responses:
            return None

        annotated_responses = responses.annotate(
            entity_category_count=Count("responseentitycategory")
        )

        # Order the responses based on the entity_category_count in descending order
        ordered_responses = annotated_responses.order_by("-entity_category_count")

        # Get the response with the biggest entity_category_count (the first one after ordering)
        response_with_biggest_category = ordered_responses.first()

        return response_with_biggest_category

    def matching_confirm_response(self, intent, template_response, responses):
        if not self.context["required_entity_categories"]:
            self.reset_context()
            return template_response.response
        else:
            self.context["current_intent"] = intent.intent_name
            self.context["template_response_id"] = template_response.id
            if self.context["is_intent_interupt"]:
                return "Mình thấy bạn đang muốn hỏi cái khác, bạn có còn muốn hỏi về {} nữa không? Nếu có, bạn vui lòng bổ sung những thông tin sau: {}".format(
                    intent.intent_name,
                    ", ".join(self.context["required_entity_categories"]),
                )
            # get collect response
            responses = Response.objects.filter(
                intent=intent, message_type=Response.CONFIRM_POSITIVE_COLLECT
            )
            for response in responses:
                response_required_category_set = (
                    response.responseentitycategory_set.all()
                )
                required_category_list = []

                for required_category in response_required_category_set:
                    required_category_list.append(
                        required_category.required_category.category_name
                    )
                # if set(self.context["required_entity_categories"]) == set(
                #     required_category_list
                # ):
                if self.lists_are_equal(
                    self.context["required_entity_categories"], required_category_list
                ):
                    return response.response

            return "Để {}, bạn vui lòng bổ sung những thông tin sau: {}".format(
                intent.intent_name,
                ", ".join(self.context["required_entity_categories"]),
            )

    def generate_positive_confirmation_response(self):
        intent = Intent.objects.get(intent_name=self.context["current_intent"])
        template_responses = Response.objects.filter(
            intent=intent, message_type=Response.CONFIRM_POSITIVE
        )
        if template_responses:
            template_response = random.choice(template_responses)
            required_entity_categories = ResponseEntityCategory.objects.filter(
                response=template_response
            )
            if (
                required_entity_categories.exists()
                and not self.context["required_entity_categories"]
            ):
                for required_entity_category in required_entity_categories:
                    self.context["required_entity_categories"].append(
                        required_entity_category.required_category.category_name
                    )
            self.match_non_defined_category()
            # extract entities
            return self.matching_confirm_response(
                intent=intent,
                template_response=template_response,
                responses=template_responses,
            )

    def generate_response(self, input_text: str) -> (str, dict):
        intent = None
        try:
            current_intent_name = self.context["current_intent"]
            pred_intent_name = self.predict(input_text=input_text)
            extracted_entities = self.extract_entity(input_text=input_text)
            # extracted_entity_categories = self.extract_entity_category(
            #     input_text=input_text
            # )
            if current_intent_name:
                if self.context["need_confirmation"]:
                    flag = self.extract_non_defined_entities(input_text=input_text)
                    if (
                        current_intent_name == pred_intent_name
                        or pred_intent_name == "positive"
                    ):
                        return (
                            self.generate_positive_confirmation_response(),
                            self.context,
                        )
                    if pred_intent_name in ["negative", "stop"]:
                        self.reset_context()
                        return "Vậy mời bạn hỏi tiếp cái khác ạ ^^", self.context
                    else:
                        if flag:
                            return (
                                self.generate_positive_confirmation_response(
                                    add_context=True
                                ),
                                self.context,
                            )
                        self.context["is_intent_interupt"] = True

                if self.context["is_intent_interupt"]:
                    if pred_intent_name == "positive":
                        self.context["is_intent_interupt"] = False
                        return (
                            self.generate_addition_info_collect_response(
                                extracted_entities=extracted_entities
                            ),
                            self.context,
                        )
                    elif pred_intent_name in ["negative", "stop"]:
                        self.reset_context()
                        return "Vậy mời bạn hỏi tiếp cái khác ạ ^^", self.context
                    else:
                        self.reset_context()
                else:
                    self.match_entities(entities=extracted_entities)
                    if (
                        pred_intent_name != current_intent_name
                        and self.context["required_entity_categories"]
                    ):
                        self.context["is_intent_interupt"] = True
                    return (
                        self.generate_addition_info_collect_response(
                            extracted_entities=extracted_entities
                        ),
                        self.context,
                    )
            intent = Intent.objects.get(bot=self.bot, intent_name=pred_intent_name)
            # TODO: match response function -> match response base on intent, entities, required_categoriese
            responses = Response.objects.filter(
                intent=intent,
                message_type__in=[
                    Response.PROVIDE,
                    Response.PROVIDE_CONFIRM,
                    Response.INSTANT,
                ],
            )
            if responses.exists():
                template_response = random.choice(responses)
                response = None
                if template_response.message_type == Response.INSTANT:
                    response = template_response.response
                    self.reset_context()
                if template_response.message_type in [
                    Response.PROVIDE,
                    Response.PROVIDE_CONFIRM,
                ]:
                    response = self.generate_provide_response(
                        template_response=template_response,
                        extracted_entities=extracted_entities,
                    )
                if not response:
                    self.reset_context()
                    return random.choice(LIST_FALLBACK), self.context
                return response, self.context
            else:
                self.reset_context()
                return random.choice(LIST_FALLBACK), self.context
        except Intent.DoesNotExist:
            self.reset_context()
            raise NLPServiceException("Intent does not exist")
