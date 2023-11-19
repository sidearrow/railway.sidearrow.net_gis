import re

def convert_company_line_name(company_name: str, line_name: str):
    company_line_name = "{}_{}".format(company_name, line_name)

    # DB に合わせる
    honsen_map = {
        "北海道旅客鉄道_根室線": True,
        "北海道旅客鉄道_日高線": True,
        "北海道旅客鉄道_釧網線": True,
        "北海道旅客鉄道_留萌線": True,
        "北海道旅客鉄道_石北線": True,
        "北海道旅客鉄道_宗谷線": True,
        "北海道旅客鉄道_室蘭線": True,
        "北海道旅客鉄道_函館線": True,
        "東日本旅客鉄道_中央線": True,
        "東日本旅客鉄道_羽越線": True,
        "東日本旅客鉄道_東北線": True,
        "東日本旅客鉄道_奥羽線": True,
        "東日本旅客鉄道_信越線": True,
        "東日本旅客鉄道_総武線": True,
        "東日本旅客鉄道_東海道線": True,
        "東海旅客鉄道_紀勢線": True,
        "東海旅客鉄道_東海道線": True,
        "東海旅客鉄道_関西線": True,
        "東海旅客鉄道_高山線": True,
        "東海旅客鉄道_中央線": True,
        "西日本旅客鉄道_山陽線": True,
        "西日本旅客鉄道_北陸線": True,
        "西日本旅客鉄道_高山線": True,
        "西日本旅客鉄道_山陰線": True,
        "西日本旅客鉄道_関西線": True,
        "西日本旅客鉄道_東海道線": True,
        "西日本旅客鉄道_紀勢線": True,
        "九州旅客鉄道_久大線": True,
        "九州旅客鉄道_日豊線": True,
        "九州旅客鉄道_筑豊線": True,
        "九州旅客鉄道_山陽線": True,
        "九州旅客鉄道_鹿児島線": True,
        "九州旅客鉄道_長崎線": True,
        "九州旅客鉄道_豊肥線": True,
        "阪急電鉄_京都線": True,
        "阪急電鉄_宝塚線": True,
        "阪急電鉄_神戸線": True,
    }

    if company_line_name in honsen_map:
        line_name = re.sub("線$", "本線", line_name)
        return (company_name, line_name)

    line_name = re.sub("[\(\)（）]", "", line_name)
    company_name = company_name.replace("　", " ")

    company_name_map = {
        "アイジーアールいわて銀河鉄道": "IGRいわて銀河鉄道",
        "神戸すまいまちづくり公社": "神戸住環境整備公社",
    }
    if company_name in company_name_map:
        company_name = company_name_map[company_name]

    company_line_name_map = {
        "伊豆箱根鉄道_十国鋼索線": "十国峠_十国鋼索線",
    }
    if company_line_name in company_line_name_map:
        [company_name, line_name] = company_line_name_map[company_line_name].split("_")

    return [company_name, line_name]
