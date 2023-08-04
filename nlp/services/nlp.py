from nlp.models import NLPBot, TrainingPhrase, Intent, Response
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
import string
from sklearn.feature_extraction.text import CountVectorizer
import os
import pickle
from nlp.exceptions import NLPServiceException
import random

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

    def entity_extraction():
        pass

    def generate_response(self, input_text: str) -> (str, dict):
        try:
            pre_intent_name = self.predict(input_text=input_text)
            intent = Intent.objects.get(bot=self.bot, intent_name=pre_intent_name)
            responses = Response.objects.filter(intent=intent)
            if responses.exists():
                response = random.choice(responses)
                if response.message_type == Response.INSTANT:
                    return response.response, self.context
            else:
                return random.choice(LIST_FALLBACK), self.context
        except Intent.DoesNotExist:
            raise NLPServiceException("Intent does not exist")
