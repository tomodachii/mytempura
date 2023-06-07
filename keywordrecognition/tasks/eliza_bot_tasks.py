from celery import shared_task
from keywordrecognition.services import ElizaService
from keywordrecognition.models import ElizaBot


@shared_task(bind=True, name='eliza-load-txt')
def eliza_save_txt_data(self, data: list, bot_id):
    bot = ElizaBot.objects.get(id=bot_id)
    eliza_service = ElizaService(bot=bot)
    eliza_service.load_txt(data=data)

    return
