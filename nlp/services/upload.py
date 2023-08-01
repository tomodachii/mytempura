from nlp.models import (
    NLPBot,
    Intent,
    Entity,
    # Response,
    EntityCategory,
    # ResponseEntity,
    TrainingPhrase,
)
import csv


class UploadService:
    def __init__(self, bot: NLPBot):
        self.bot = bot

    def upload_entities_from_csv(self, file):
        # Open the CSV file
        with open(file, "r", encoding="utf-8") as csvfile:
            # Create a CSV reader
            csvreader = csv.reader(csvfile, delimiter="\t")

            for row in csvreader:
                entity_category_name, entity_name, synonym = row

                # Check if the EntityCategory with the given name exists, if not create a new one
                entity_category, _ = EntityCategory.objects.get_or_create(
                    bot=self.bot, category_name=entity_category_name
                )

                # Check if the Entity with the given name and EntityCategory exists, if not create a new one
                entity, _ = Entity.objects.get_or_create(
                    bot=self.bot,
                    entity_name=entity_name,
                    entity_category=entity_category,
                    synonym=synonym,
                )

    def upload_intents_from_csv(self, file):
        # Open the CSV file
        with open(file, "r", encoding="utf-8") as csvfile:
            # Create a CSV reader
            csvreader = csv.reader(csvfile, delimiter="\t")

            for row in csvreader:
                intent_name, phrase = row

                # Check if the Intent with the given name exists, if not create a new one
                intent, _ = Intent.objects.get_or_create(
                    bot=self.bot, intent_name=intent_name
                )

                # Check if the TrainingPhrase with the given phrase and Intent exists, if not create a new one
                training_phrase, _ = TrainingPhrase.objects.get_or_create(
                    intent=intent, phrase=phrase
                )
