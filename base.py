from dotenv import load_dotenv
load_dotenv()
from pymongo import MongoClient
from flask import *
from flask import Blueprint
from flask_cors import CORS
from bson import ObjectId
import jwt
import os
from datetime import datetime
from functools import wraps
from PIL import Image
import pytesseract
import easyocr
import numpy as np
import cv2
import base64

import common.mongo_operations as cmo
import common.utils as cutils




# Authentication decorator
def token_auth_check(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # ensure the jwt-token is passed with the headers
        print(os.environ.get("SECRET"),'os.environ.get("SECRET")')
        if 'Access-Token' in request.headers:
            token = request.headers['Access-Token']
            
        print(token,"tokentokentoken")
        if not token: # throw error if no token provided
            print("A valid token is missing")
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)
        try:
           
            data = jwt.decode(token, os.environ.get("SECRET"), algorithms=["HS256"])
            print(data,"datadatadatadata")
            current_user = data
        except:
            print("Invalid token")
            return make_response(jsonify({"message": "Invalid token!"}), 401)
         # Return the user information attached to the token
        return f(current_user, *args, **kwargs)
    return decorator
