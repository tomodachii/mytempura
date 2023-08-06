from nlp.models import (
    NLPBot,
    Intent,
    Entity,
    Response,
    EntityCategory,
    ResponseEntity,
    TrainingPhrase,
    ResponseEntityCategory,
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

    def upload_responses_from_csv(self, file):
        # Open the CSV file
        with open(file, "r", encoding="utf-8") as csvfile:
            # Create a CSV reader
            csvreader = csv.reader(csvfile, delimiter="\t")

            for row in csvreader:
                (
                    intent_name,
                    message_type,
                    entity_categories_str,
                    entities_str,
                    response_text,
                ) = row

                # Check if the Intent with the given name exists, if not create a new one
                intent, _ = Intent.objects.get_or_create(
                    bot=self.bot, intent_name=intent_name
                )

                # Create or update the Response based on the message_type
                response, _ = Response.objects.get_or_create(
                    intent=intent, message_type=message_type, response=response_text
                )

                # Process the entities
                if entity_categories_str:
                    entity_category_names = entity_categories_str.split(",")
                    entity_categories = []
                    for category_name in entity_category_names:
                        category, _ = EntityCategory.objects.get_or_create(
                            bot=self.bot, category_name=category_name.strip()
                        )
                        entity_categories.append(category)

                    # Update the ResponseEntityCategory mappings for the response
                    response_required_categories = (
                        ResponseEntityCategory.objects.filter(response=response)
                    )
                    response_required_categories.delete()
                    for category in entity_categories:
                        ResponseEntityCategory.objects.create(
                            response=response, required_category=category
                        )
                    if entities_str:
                        entity_names = entities_str.split(",")
                        entities = []
                        if message_type == Response.PROVIDE:
                            for entity_name in entity_names:
                                entity, _ = Entity.objects.get_or_create(
                                    bot=self.bot, entity_name=entity_name.strip()
                                )
                                entities.append(entity)

                            # Update the ResponseEntity mappings for the response
                            response_entities = ResponseEntity.objects.filter(
                                response=response
                            )
                            if response_entities.exists():
                                response_entities.delete()
                            for entity in entities:
                                ResponseEntity.objects.create(
                                    response=response, entity=entity
                                )
