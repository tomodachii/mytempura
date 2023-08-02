from nlp.models import NLPBot, TrainingPhrase, Intent, Response
from sklearn.svm import SVC
from sklearn.naive_bayes import MultinomialNB
import string
from sklearn.feature_extraction.text import CountVectorizer
import os
import pickle
from nlp.exceptions import NLPServiceException
import random


class NLPService:
    def __init__(self, bot: NLPBot):
        self.bot = bot
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
        raw_train_data, train_target = self.build_data_and_target_list()
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

    def generate_response(self, input_text: str) -> str:
        try:
            pre_intent_name = self.predict(input_text=input_text)
            intent = Intent.objects.get(bot=self.bot, intent_name=pre_intent_name)
            responses = Response.objects.filter(intent=intent)
            if responses.exists():
                response = random.choice(responses)
                return response.response
            else:
                return "Fallback"
        except Intent.DoesNotExist:
            raise NLPServiceException("Intent does not exist")
