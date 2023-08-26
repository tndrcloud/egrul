import json
import os
from zipfile import ZipFile
from log import logger
from database import Operations
from settings import settings


def files_partition(length, n):
    for i in range(0, len(length), n):
        yield length[i:i + n]


def archive_unpacker(part_length):
    with ZipFile(f"../{settings.archive}", mode="r") as archive:
        list_filenames = [filename for filename in archive.namelist()]
        new_list = list(files_partition(list_filenames, part_length))

        for part in new_list:
            archive.extractall(members=part)
            for filename in part:
                with open(filename, encoding='utf-8') as file_json:
                    logger.info(f"file {filename} open")
                    file_data = json.load(file_json)
                    yield file_data
                os.remove(filename)
                logger.info(f"file {filename} removed")


def address_handler(address):
    region = address['Регион']['НаимРегион']
    type_region = address['Регион']['ТипРегион']
    type_city = address['Город']['ТипГород']
    city = address['Город']['НаимГород']
    type_street = address['Улица']['ТипУлица']
    street = address['Улица']['НаимУлица']
    apartment = address['Дом']
    index = address['Индекс']

    without_block = False
    if address.get('Корпус'):
        block = address['Корпус']
    elif address.get('Кварт'):
        block = address['Кварт']
    else:
        without_block = True

    if without_block:
        result = f"{region} {type_region}, {type_city} {city}, {type_street} {street}, {apartment}, {index}"
        return result
    result = f"{region} {type_region}, {type_city} {city}, {type_street} {street}, {apartment}, {block}, {index}"
    return result


def analytics(file_data):
    for unit in file_data:
        code = None
        data = unit["data"]
        target_city = settings.city

        if data.get("СвОКВЭД") and data["СвОКВЭД"].get("СвОКВЭДОсн"):
            if data["СвОКВЭД"]["СвОКВЭДОсн"]["КодОКВЭД"] == "62.01":
                code = data["СвОКВЭД"]["СвОКВЭДОсн"]["КодОКВЭД"]

        if code and data["СвАдресЮЛ"].get("АдресРФ") and data["СвАдресЮЛ"]["АдресРФ"].get("Город"):
            if data["СвАдресЮЛ"]["АдресРФ"]["Город"]["НаимГород"] == target_city:
                city = data["СвАдресЮЛ"]["АдресРФ"]
                correct_address = address_handler(city)
                result = {
                    "name": unit["full_name"],
                    "code": code,
                    "inn": int(unit["inn"]),
                    "kpp": int(unit["kpp"]),
                    "address": correct_address
                }
                Operations.add_company(result)
                logger.info(f"company: {unit['full_name']} added to db")


def core():
    result = []
    au = archive_unpacker(settings.unpack_files)

    try:
        while True:
            json_data = next(au)
            analyst = analytics(json_data)
            if analyst:
                result.extend(analyst)
    except StopIteration:
        return result


if __name__ == '__main__':
    logger.info("app is running...")
    core()
    logger.info("app is finished!")
