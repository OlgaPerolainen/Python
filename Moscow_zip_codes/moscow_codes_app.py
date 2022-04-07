"""
This is a program to find location by ZIP code and ZIP code(s) by location,
as well as to calculate the distance between two ZIP codes.

This module relies on a database
Check column indexes if you change the database

There are four menu items: 1. find address, 2. find Zip code, 3. calculate distance, 4. exit
User chooses the needed one with entering corresponding figure
After choosing, user enters corresponding data: Zip code, location, two Zip codes

Moscow ZIP code is a six-digit integer number.
Location is given by the name of a city area.

Sample Execution in Russian:
-----------------

1. Найти адрес
2. Найти индекс
3. Найти расстояние
4. Выйти
Выберите пункт: 1
Введите почтовый индекс: 101000
Почтовый индекс: 101000
Адрес: Центральный административный округ, Басманный район, Мясницкая улица. дом 26
Координаты: (055°45'49.90"N,037°38'13.80"E)

1. Найти адрес
2. Найти индекс
3. Найти расстояние
4. Выйти
Выберите пункт: 2
Введите район: Басманный
Район: Басманный
Найденные почтовые индексы: 101000, 105005, 105062, 105064, 105066, 105082, 107174, 105175, 107450

1. Найти адрес
2. Найти индекс
3. Найти расстояние
4. Выйти
Выберите пункт: 3
Введите первый индекс: 101000
Введите второй индекс: 109012
Расстояние между 101000 и 109012 в километрах составляет: 1.33

1. Найти адрес
2. Найти индекс
3. Найти расстояние
4. Выйти
Выберите пункт: 4

Всего доброго!
"""

import read_postal_codes
import menu_process_file
import geo_formulas
import logging
import logging.handlers

zip_column_index = 0
county_column_index = 1
area_column_index = 2
street_column_index = 3
lat_column_index = 5
long_column_index = 4


def process_loc(codes):
    """
    This procedure runs on if user is searching for location
    and enters a ZIP code
    
    Parameters
    ----------
    codes: list
        full ZIP codes list
    
    Other functions involved
    ----------
    menu_process_file.location_by_zip(codes, zipcode)
    geo_formulas.format_location(location)
    """
    
    # ZIP code request
    zipcode = input("Введите почтовый индекс: ").replace(" ", "")
    
    # Calling function that gets data behind ZIP code
    location = menu_process_file.location_by_zip(codes, zipcode)
    
    # Checking that data exists
    if len(location) > 0:
        print("Почтовый индекс: {}\nАдрес: {}, {}, {}\nКоординаты: {}".
              format(zipcode, location[county_column_index], location[area_column_index],
              location[street_column_index],
              geo_formulas.format_location((location[lat_column_index], location[long_column_index]))))
    else:
        print("Почтовый индекс не найден")


def process_zip(codes):
    """
    This procedure runs on if user is searching for ZIP code(s)
    and enters location
    
    Parameters
    ----------
    codes: list
        full ZIP codes list
    
    Other functions involved
    ----------
    menu_process_file.zip_by_location(codes, location)
    """
    
    # Location request
    area = input("Введите район: ").replace("район", "").strip()
    
    # Calling function that gets ZIP codes behind given location
    zipcodes = menu_process_file.zip_by_location(codes, area)
    
    # Checking that ZIP codes exist
    if len(zipcodes) > 0:
        print("Район: {}\nНайденные почтовые индексы: {}".
              format(area, ", ".join(zipcodes)))
    else:
        print("Район: {}\nПочтовые индексы не найдены".format(area))

    
def process_dist(codes):
    """
    This procedure runs on if user is searching for distance between two ZIP codes
    
    Parameters
    ----------
    codes: list
        full ZIP codes list
    
    Other functions involved
    ----------
    menu_process_file.location_by_zip(codes, zipcode)
    geo_formulas.calculate_distance(location1, location2)
    """
    
    # First ZIP code request and searching for its coordinates
    zip1 = input("Введите первый индекс: ").replace(" ", "")
    
    logger.info(f"Received the first ZIP {zip1}")
    location1 = menu_process_file.location_by_zip(codes, zip1)
    
    # Second ZIP code request and searching for its coordinates
    zip2 = input("Введите второй индекс: ").replace(" ", "")

    logger.info(f"Received the second ZIP {zip2}")
    location2 = menu_process_file.location_by_zip(codes, zip2)
    
    # Checking that ZIP codes exist
    if len(location1) == 0 or len(location2) == 0:
        print("Расстояние между {} и {} невозможно рассчитать".
              format(zip1, zip2))
    
    # Calling function that calculates the distance between two ZIP codes
    else:
        dist = geo_formulas.calculate_distance((location1[lat_column_index], location1[long_column_index]),
                                                (location2[lat_column_index], location2[long_column_index]))
        print("Расстояние между {} и {} в километрах составляет: {:.2f}".
              format(zip1, zip2, dist))


if __name__ == "__main__":

    rfh = logging.handlers.RotatingFileHandler(
        filename="moscow_codes_app.log",
        mode="a",
        maxBytes=5*1024*1024,
        backupCount=9,
        encoding=None,
        delay=0
    )
    logging.basicConfig(format="%(asctime)s: %(name)s - %(levelname)s - %(message)s",
                        level=logging.INFO, datefmt="%y-%m-%d %H:%M:%S",
                        handlers=[rfh])
    logger = logging.getLogger("main")



    zip_codes = read_postal_codes.read_zip_all()

    command = ""
    while command != "4":
        command_name = "Выйти"
        command = input("1. Найти адрес\n2. Найти индекс\n3. Найти расстояние\n4. Выйти\nВыберите пункт: ")
        if command == "1":
            command_name = "Найти адрес"
            process_loc(zip_codes)              #calling function that looks for an address by given ZIP code
        elif command == "2":
            command_name = "Найти индекс"
            process_zip(zip_codes)              #calling function that looks for ZIP code(s) by given address
        elif command == "3":
            command_name = "Найти расстояние"
            process_dist(zip_codes)             #calling function that calculates distance between two given ZIP codes
        elif command != "4":
            print("Неизвестная команда")
        logger.info(f"Received command {command_name}")
        print()
    print("Всего доброго!")
    logging.shutdown()
