# -*- coding: utf-8 -*-

import os
from dotenv import load_dotenv
load_dotenv()

REDDIT_KEY = os.getenv('reddit_secret_token')