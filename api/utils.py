import requests
from .models import Clothes

invalidToken = {
    "detail": "Token is invalid or expired",
    "code": "token_not_valid"
}

testResponse = [{"source":"https://www.lamoda.ru/p/to030emlrlr0/clothes-topman-mayka-spo..","clothesType":"body","imageLinks":["https://a.lmcdn.ru/product /T/O/TO030EMLRLR0_12928724_1_v1_2x.jpg","https://a.lmcdn.ru/product/T/O/TO030EMLRLR0_12928725_2_v1_2x...","https://a.lmcdn.ru/product/T/O/TO030EMLRLR0_12928726_3_v1_2x...","https://a.lmcdn.ru/product/T/O/TO030EMLRLR0_12928727_4_v1_2x..."],"sizes":["44/46 RUS (XS INT)","46/48 RUS (S INT)","48/50 RUS (M INT)","50/52 RUS (L INT)","52/54 RUS (XL INT)","54/56 RUS (XXL INT)"],"price":"1290","name":"Topman Майка спортивная ","description":[" Состав: Полиэстер - 100% ","Артикул TO030EMLRLR0"]},{"source":"https://www.lamoda.ru/p/mp002xm1hb15/clothes-ostin-dzhinsy/","clothesType":"legs","imageLinks":["https://a.lmcdn.ru/product /M/P/MP002XM1HB15_13645520_1_v1_2x.jpg","https://a.lmcdn.ru/product/M/P/MP002XM1HB15_13645521_2_v1_2x...","https://a.lmcdn.ru/product/M/P/MP002XM1HB15_13645522_3_v1_2x...","https://a.lmcdn.ru/product/M/P/MP002XM1HB15_13645523_4_v1_2x..."],"sizes":["28/L32 RUS (28/32 JEANS)","29/L32 RUS (29/32 JEANS)","30/L32 RUS (30/32 JEANS)","31/L32 RUS (31/32 JEANS)","32/L32 RUS (32/32 JEANS)","33/L32 RUS (33/32 JEANS)","34/L32 RUS (34/32 JEANS)"],"price":"1999","name":"O'stin Джинсы ","description":[" Состав: Хлопок - 98%, Эластан - 2% "," Размер товара на модели: 32/32 JEANS "," Параметры модели: 94-74-90 ","Артикул MP002XM1HB15"]},{"source":"https://www.lamoda.ru/p/mp002xm1k6tp/shoes-ecco-botinki/","clothesType":"shoes","imageLinks":["https://a.lmcdn.ru/product /M/P/MP002XM1K6TP_11050868_1_v1.jpg","https://a.lmcdn.ru/product/M/P/MP002XM1K6TP_11050869_2_v1.jpg","https://a.lmcdn.ru/product/M/P/MP002XM1K6TP_11050870_3_v1.jpg","https://a.lmcdn.ru/product/M/P/MP002XM1K6TP_11050871_4_v1.jpg","https://a.lmcdn.ru/product/M/P/MP002XM1K6TP_11050872_5_v1.jpg"],"sizes":["39 RUS (39 EUR)","40 RUS (40 EUR)","41 RUS (41 EUR)","42 RUS (42 EUR)","43 RUS (43 EUR)","44 RUS (44 EUR)","45 RUS (45 EUR)","46 RUS (46 EUR)","47 RUS (47 EUR)","48 RUS (48 EUR)","49 RUS (49 EUR)","50 RUS (50 EUR)"],"price":"7999","name":"Ecco Ботинки ECCO IRVING ","description":["Артикул MP002XM1K6TP"]}]

def existClothes(request):
    for i in range(2, len(request.data)):
        if (request.data[i]["nameClothes"] != ""
                and request.data[i]["typeClothes"] != ""
                and request.data[i]["description"] != ""
                and request.data[i]["price"] != ""
                and request.data[i]["linkImage"] != ""
                and request.data[i]["linkSource"] != ""):

            if not request.data[i]["price"].isdigit():
                return False

            response = requests.get(request.data[i]["linkImage"])
            if not response:
                return False

            response = requests.get(request.data[i]["linkSource"])
            if not response:
                return False

            return True
        return False

def existCloneSetOfClothes(request):
    coincidences = 0
    for i in range(2, len(request.data) - 1):
        clothes = Clothes.objects.filter(link_Source=request.data[i]["linkSource"]).first()
        if clothes is None:
            break

        if request.data[i]["linkSource"] == clothes.link_Source:
            coincidences += 1
            continue
        break

    return coincidences == len(request.data) - 1

def countclothes(request):
    pass
    # coincidences = 0
    # for i in range(1, len(request.data)):
    #     if request.data[i]["linkSource"] == Clothes.objects.filter(link_Source=request.data[i]["linkSource"]).first().link_Source:
    #         coincidences += 1
    #
    # return str(coincidences)

        # SetOfClothes.objects.filter(id=request.data["setOfClothes"])

# def existClothes(request):
#     if (request.data[id]["nameClothes"] != ""
#             and request.data["typeClothes"] != ""
#             and request.data["description"] != ""
#             and request.data["price"] != ""
#             and request.data["linkImage"] != ""
#             and request.data["linkSource"] != ""):
#
#         if not request.data["price"].isdigit():
#             return False
#
#         response = requests.get(request.data["linkImage"])
#         if not response:
#             return False
#
#         response = requests.get(request.data["linkSource"])
#         if not response:
#             return False
#
#         return True
#

