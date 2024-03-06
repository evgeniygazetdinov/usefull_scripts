import requests
from cities.models import AlternativeName
from cities.models import City
from cities.models import Country
from django.contrib.gis.geos import Point
from django.core.management.base import BaseCommand


ALL_COUNTRIES = [
    {
        "Russia": [
            {"Novosibirsk": "Новосибирск"},
            {"Ekaterinburg": "Екатеринбург"},
            {"Nizhny Novgorod": "Нижний Новгород"},
            {"Samara": "Самара"},
            {"Omsk": "Омск"},
            {"Kazan": "Казань"},
            {"Chelyabinsk": "Челябинск"},
            {"Rostov-on-Don": "Ростов-на-Дону"},
            {"Ufa": "Уфа"},
            {"Volgograd": "Волгоград"},
            {"Perm": "Пермь"},
            {"Krasnoyarsk": "Красноярск"},
            {"Voronezh": "Воронеж"},
            {"Saratov": "Саратов"},
            {"Krasnodar": "Краснодар"},
            {"Tolyatti": "Тольятти"},
            {"Izhevsk": "Ижевск"},
            {"Ulyanovsk": "Ульяновск"},
            {"Barnaul": "Барнаул"},
            {"Vladivostok": "Владивосток"},
            {"Yaroslavl": "Ярославль"},
            {"Irkutsk": "Иркутск"},
            {"Tyumen": "Тюмень"},
            {"Makhachkala": "Махачкала"},
            {"Khabarovsk": "Хабаровск"},
            {"Novokuznetsk": "Новокузнецк"},
            {"Orenburg": "Оренбург"},
            {"Kemerovo": "Кемерово"},
            {"Ryazan": "Рязань"},
            {"Tomsk": "Томск"},
            {"Astrakhan": "Астрахань"},
            {"Penza": "Пенза"},
            {"Naberezhnye Chelny": "Набережные Челны"},
            {"Lipetsk": "Липецк"},
            {"Tula": "Тула"},
            {"Kirov": "Киров"},
            {"Cheboksary": "Чебоксары"},
            {"Kaliningrad": "Калининград"},
            {"Bryansk": "Брянск"},
            {"Kursk": "Курск"},
            {"Ivanovo": "Иваново"},
            {"Magnitogorsk": "Магнитогорск"},
            {"Ulan-Ude": "Улан-Удэ"},
            {"Tver": "Тверь"},
            {"Stavropol": "Ставрополь"},
            {"Nizhny Tagil": "Нижний Тагил"},
            {"Belgorod": "Белгород"},
            {"Arkhangelsk": "Архангельск"},
            {"Vladimir": "Владимир"},
            {"Sochi": "Сочи"},
            {"Kurgan": "Курган"},
            {"Smolensk": "Смоленск"},
            {"Kaluga": "Калуга"},
            {"Chita": "Чита"},
            {"Orel": "Орел"},
            {"Volzhsky": "Волжский"},
            {"Cherepovets": "Череповец"},
            {"Vladikavkaz": "Владикавказ"},
            {"Murmansk": "Мурманск"},
            {"Surgut": "Сургут"},
            {"Vologda": "Вологда"},
            {"Saransk": "Саранск"},
            {"Tambov": "Тамбов"},
            {"Sterlitamak": "Стерлитамак"},
            {"Grozniy": "Грозный"},
            {"Yakutsk": "Якутск"},
            {"Kostroma": "Кострома"},
            {"Komsomolsk-on-Amur": "Комсомольск-на-Амуре"},
            {"Petrozavodsk": "Петрозаводск"},
            {"Taganrog": "Таганрог"},
            {"Nizhnevartovsk": "Нижневартовск"},
            {"Yugra": "Югра"},
            {"Yoshkar-Ola": "Йошкар-Ола"},
            {"Bratsk": "Братск"},
            {"Novorossiysk": "Новороссийск"},
            {"Dzerzhinsk": "Дзержинск"},
            {"Mines": "Шахты"},
            {"Nalchik": "Нальчик"},
            {"Orsk": "Орск"},
            {"Syktyvkar": "Сыктывкар"},
            {"Nizhnekamsk": "Нижнекамск"},
            {"Angarsk": "Ангарск"},
            {"Stary Oskol": "Старый Оскол"},
            {"Veliky Novgorod": "Великий Новгород"},
            {"Balashikha": "Балашиха"},
            {"Blagoveshchensk": "Благовещенск"},
            {"Prokopyevsk": "Прокопьевск"},
            {"Biysk": "Бийск"},
            {"Khimki": "Химки"},
            {"Pskov": "Псков"},
            {"Engels": "Энгельс"},
            {"Rybinsk": "Рыбинск"},
            {"Balakovo": "Балаково"},
            {"Severodvinsk": "Северодвинск"},
            {"Armavir": "Армавир"},
            {"Podolsk": "Подольск"},
            {"Yuzhno-Sakhalinsk": "Южно-Сахалинск"},
            {"Petropavlovsk-Kamchatsky": "Петропавловск-Камчатский"},
            {"Syzran": "Сызрань"},
            {"Norilsk": "Норильск"},
            {"Zlatoust": "Златоуст"},
            {"Kamensk-Uralsky": "Каменск-Уральский"},
            {"Mytishchi": "Мытищи"},
            {"Lyubertsy": "Люберцы"},
            {"Volgodonsk": "Волгодонск"},
            {"Novocherkassk": "Новочеркасск"},
            {"Abakan": "Абакан"},
            {"Nahodka": "Находка"},
            {"Ussuriysk": "Уссурийск"},
            {"Berezniki": "Березники"},
            {"Electostal": "Электросталь"},
            {"Rubtsovsk": "Рубцовск"},
            {"Almetyevsk": "Альметьевск"},
            {"Carpets": "Ковров"},
            {"Kolomna": "Коломна"},
            {"Maykop": "Майкоп"},
            {"Pyatigorsk": "Пятигорск"},
            {"Odintsovo": "Одинцово"},
            {"Kopeysk": "Копейск"},
            {"Cherkessk": "Черкесск"},
            {"Khasavyurt": "Хасавюрт"},
            {"Railway": "Железнодорожный"},
            {"Novomoskovsk": "Новомосковск"},
            {"Kislovodsk": "Кисловодск"},
            {"Serpukhov": "Серпухов"},
            {"Pervouralsk": "Первоуральск"},
            {"Novocheboksarsk": "Новочебоксарск"},
            {"Nefteyugansk": "Нефтеюганск"},
            {"Dimitrovgrad": "Димитровград"},
            {"Neftekamsk": "Нефтекамск"},
            {"Orekhovo-Zuyevo": "Орехово-Зуево"},
            {"Derbent": "Дербент"},
            {"Kamyshin": "Камышин"},
            {"Nevinnomyssk": "Невинномысск"},
            {"Krasnogorsk": "Красногорск"},
            {"Moore": "Моор"},
            {"Bataysk": "Батайск"},
            {"Novoshakhtinsk": "Новошахтинск"},
            {"Sergiev Posad": "Сергиев Посад"},
            {"November": "Ноябрь"},
            {"Shchelkovo": "Щелково"},
            {"Kyzyl": "Кызыл"},
            {"October": "Октябрь"},
            {"Achinsk": "Ачинск"},
            {"Seversk": "Северск"},
            {"Novokuibyshevsk": "Новокуйбышевск"},
            {"Yelets": "Елец"},
            {"Arzamas": "Арзамас"},
            {"Obninsk": "Обнинск"},
            {"Novy Urengoy": "Новый Уренгой"},
            {"Kaspiysk": "Каспийск"},
            {"Elista": "Элиста"},
            {"Pushkino": "Пушкино"},
            {"Zhukovsky": "Жуковский"},
            {"Artem": "Артем"},
            {"Mezhdurechensk": "Междуреченск"},
            {"Leninsk-Kuznetsky": "Ленинск-Кузнецкий"},
            {"Sarapul": "Сарапул"},
            {"Essentuki": "Ессентуки"},
            {"Votkinsk": "Воткинск"},
            {"Tobol'sk": "Тобольск"},
            {"Velikiy Novgorod": "Новгород"},
            {"Nizhny Novgorod": "Нижний"},
            {"Vladimir": "Владимир"},
            {"Rostov-na-Dony": "Ростов"},
            {"Sychevka": "Сычевка"},
            {"Vjazma": "Вязьма"},
        ]
    },
    {"Belarus": [{"Minsk": "Минск"}]},
    {"Kazakhstan": [{"Nur-sultan": "Астана"}, {"Аlamti": "Алматы"}]},
    {"Ukraine": [{"Kiev": "Киев"}]},
]


class Command(BaseCommand):
    def check_longitude_and_population(self, name):
        coordinate, population = Point(0, 0), 15000
        api_url = "https://public.opendatasoft.com/api/explore/v2.1/catalog/datasets/geonames-all-cities-with-a-population-500/records?select=population%2C%20latitude%2C%20longitude&where=name%3D%22{}%22&limit=20".format(
            name
        )
        response = requests.get(api_url, headers={"X-Api-Key": "1RyEqnm8ueMC24CKjd5wOqxbkhazHNBoE8sabRkz"})
        if response.status_code == requests.codes.ok and len(response.json().get("results")) > 0:
            result = response.json().get("results")[0]
            coordinate = Point(float(result["latitude"]), float(result["longitude"]))
            population = result["population"]
        return coordinate, population

    def handle(self, *args, **options):
        import django
        django.setup()

        from django.contrib.auth.models import User
        User = django.contrib.auth.get_user_model()
        u = User(username='admin2')
        u.set_password('admin2')
        u.is_superuser = True
        u.is_staff = True
        u.save()


        # for country in ALL_COUNTRIES:
        #     for country_name, cities in country.items():
        #         for city in cities:
        #             for key, value in city.items():
        #                 has_alternative_name = AlternativeName.objects.filter(name=value).first()
        #                 city_exist_in_db = City.objects.filter(name_std=key).first()
        #                 country = Country.objects.filter(name=country_name).first()
        #                 slug = "" if city_exist_in_db is None else f"{city_exist_in_db.id}-{city_exist_in_db.name_std}"
        #                 location, population = self.check_longitude_and_population(key)
        #                 has_location = (
        #                     hasattr(city_exist_in_db, "location")
        #                     and city_exist_in_db.__dict__.get("location") < location
        #                     and location.area != 0.0
        #                 )
        #                 has_population = (
        #                     hasattr(city_exist_in_db, "population")
        #                     and city_exist_in_db.__dict__.get("population") < population
        #                     and population != 15000
        #                 )
        #                 if has_alternative_name and city_exist_in_db and has_location and has_population:
        #                     pass
        #                 else:
        #                     if not has_alternative_name and not city_exist_in_db:
        #                         AlternativeName.objects.create(
        #                             name=value, is_preferred=True, city=city, kind="name", slug=slug
        #                         )
        #
        #                     elif not has_alternative_name and city_exist_in_db:
        #                         city = City.objects.filter(name_std=key).first()
        #                         alt_name = AlternativeName.objects.create(
        #                             name=value, is_preferred=True, city=city, kind="name", slug=slug
        #                         )
        #                         city.alt_names.add(alt_name)
        #                         city.save()
        #
        #                     elif has_alternative_name and not city_exist_in_db:
        #                         alt_name = AlternativeName.objects.filter(name=value).first()
        #                         city = City.objects.create(
        #                             name_std=key, population=population, location=location, country=country
        #                         )
        #                         city.alt_names.add(alt_name)
        #                         city.save()
        #
        #                     if not has_location and city_exist_in_db:
        #                         city_exist_in_db.location = location
        #                         city_exist_in_db.save()
        #
        #                     if not has_population and city_exist_in_db:
        #                         city_exist_in_db.population = population
        #                         city_exist_in_db.save()
