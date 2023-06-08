from keywordrecognition.models import ElizaBot
from keywordrecognition.services import ElizaService

elizabot = ElizaBot.objects.get(id=7)
eliza_service = ElizaService(bot=elizabot)
response = eliza_service.response("bạn là búp măng lon")
print(response)
