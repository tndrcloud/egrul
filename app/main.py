import json
import os
from zipfile import ZipFile
from log import logger
from database import Operations
from settings import settings


def archive_unpacker(part_length):
    """unpacks the archive and alternately gives the contents of the files to json"""

    with ZipFile(f"../{settings.ARCHIVE}", mode="r") as archive:
        filenames = [filename for filename in archive.namelist()]

        partition = (filenames[i:i + part_length] for i in range(0, len(filenames), part_length))

        for part in list(partition):
            archive.extractall(members=part)
            for filename in part:
                with open(filename, encoding='utf-8') as file_json:
                    logger.info(f"file {filename} unpacked and open")

                    file_data = json.load(file_json)
                    yield file_data

                os.remove(filename)
                logger.info(f"file {filename} removed")


def address_handler(addr):
    """converts address data to a string"""

    if addr.get('Корпус'):
        subaddr = ', ' + addr['Корпус']
    elif addr.get('Кварт'):
        subaddr = ', ' + addr['Кварт']
    else:
        subaddr = ''

    result = f"""{addr['Регион']['НаимРегион']} {addr['Регион']['ТипРегион']}, 
        {addr['Город']['ТипГород']} {addr['Город']['НаимГород']}, {addr['Улица']['ТипУлица']} 
        {addr['Улица']['НаимУлица']}, {addr['Дом'] + subaddr}, {addr['Индекс']}"""
    return result


def analytics(file_data):
    """checks the parameters of the json data for compliance with the search, 
    if successful, adds the data to the database"""
    
    for unit in file_data:
        data = unit["data"]
        code = None

        if data.get("СвОКВЭД") and data["СвОКВЭД"].get("СвОКВЭДОсн"):
            if data["СвОКВЭД"]["СвОКВЭДОсн"]["КодОКВЭД"] == settings.CODE:
                code = data["СвОКВЭД"]["СвОКВЭДОсн"]["КодОКВЭД"]

        if code: 
            if data["СвАдресЮЛ"].get("АдресРФ") and data["СвАдресЮЛ"]["АдресРФ"].get("Город"):
                if data["СвАдресЮЛ"]["АдресРФ"]["Город"]["НаимГород"] == settings.NAME_CITY:
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
    

def core():
    try:
        au = archive_unpacker(settings.UNPACK_FILES_COUNT)
        while True:
            json_data = next(au)
            analytics(json_data)
    except StopIteration:
        return


if __name__ == '__main__':
    logger.info("app is running...")
    core()
    logger.info("done!")
