from nlp.models import NLPBot, TrainingPhrase


class NLPService:
    def __init__(self, bot: NLPBot):
        self.bot = bot
        self.data = []
        self.target = []
        self.entities = []

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

    def text_preprocess():
        pass

    def train_model():
        pass

    def predict():
        pass

    def entity_extraction():
        pass

    def generate_response() -> str:
        pass
