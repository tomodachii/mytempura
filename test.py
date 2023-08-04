from nlp.models import NLPBot
from nlp.services import NLPService

bot = NLPBot.objects.get(id=8)
nlp_service = NLPService(bot=bot, context={})
nlp_service.train_model()
print(nlp_service.generate_response("đúng rồi nha"))
