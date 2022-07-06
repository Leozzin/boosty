import json
from chatterbot import ChatBot
from django.http import JsonResponse
from django.views.generic import View
from chatterbot.ext.django_chatterbot import settings
from chatterbot.trainers import ChatterBotCorpusTrainer
import os

base_path = os.path.abspath(os.path.dirname(__file__))


filenames = [
    "allergies.yml",
    "ask.yml",
    "constipation.yml",
    "diabetes.yml",
    "goodbye.yml",
    "greeting.yml",
    "nutrition_for_all.yml",
    "nutrition_for_babies.yml",
    "obesity.yml",
    "options.yml",
    "pregnant_women_nutrition.yml",
    "sport_nutrition.yml",
    "thanks.yml",
]


training_filenames = [os.path.join("data/chatbot/", filename) for filename in filenames]


class ChatBotApi(View):
    """
    Provides an API endpoint to interact with the chatbot.
    """

    bot = ChatBot(**settings.CHATTERBOT)
    #trainer = ChatterBotCorpusTrainer(bot)
    #trainer.train(*training_filenames)
    #print("***** Training is Done *****")

    def post(self, request, *args, **kwargs):
        """
        Return a response to the statement in the posted data.

        * The JSON data should contain a 'text' attribute.
        """
        print(request.body)
        input_data = json.loads(request.body.decode("utf-8"))

        if "text" not in input_data:
            return JsonResponse(
                {"text": ['The attribute "text" is required']}, status=400
            )

        response = self.bot.get_response(input_data)
        response_data = response.serialize()

        return JsonResponse(response_data, status=200)

    def get(self, request, *args, **kwargs):
        """
        Return data corresponding to the current conversation.
        """
        return JsonResponse({"name": self.bot.name})
