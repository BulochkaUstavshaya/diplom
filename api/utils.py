from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import requests

def ExistClothes(request):
    if (request.data["nameClothes"] != ""
            and request.data["typeClothes"] != ""
            and request.data["description"] != ""
            and request.data["price"] != ""
            and request.data["linkImage"] != ""
            and request.data["linkSource"] != ""):

        if not request.data["price"].isdigit():
            return False

        response = requests.get(request.data["linkImage"])
        if not response:
            return False

        response = requests.get(request.data["linkSource"])
        if not response:
            return False

        return True
