# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class FoodConfig(AppConfig):
    name = 'food'

    def ready(self):
    	import food.signals
