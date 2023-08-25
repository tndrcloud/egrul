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
                result = {
                    "name": unit["full_name"],
                    "code": code,
                    "inn": unit["inn"],
                    "kpp": unit["kpp"],
                    "address": city
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
