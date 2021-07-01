from flask_sqlalchemy import SQLAlchemy
from Database_tables import *
import os
import re
import shutil


def sorted_alphanumeric(data):
    """
    sorts an array of strings alphanumericly
    """

    def convert(text):
        return int(text) if text.isdigit() else text.lower()

    def alphanum_key(key):
        return [convert(c) for c in re.split("([0-9]+)", key)]

    return sorted(data, key=alphanum_key)


def get_chip_directorys(scan_directory):
    """Yields all the chip directorys in the Current scan Directory

    Args:
        scan_directory (string): The path of the current scan

    Yields:
        string: A path to a chip Directory
    """
    chip_directory_names = [
        chip_directory_name
        for chip_directory_name in sorted_alphanumeric(os.listdir(scan_directory))
        if os.path.isdir(os.path.join(scan_directory, chip_directory_name))
    ]

    # iterate over all chip directory names
    for chip_directory_name in chip_directory_names:

        # get the full path to the chip dir
        chip_directory = os.path.join(scan_directory, chip_directory_name)

        yield chip_directory


def delete_scan(db: SQLAlchemy, IMAGE_DIRECTORY: str, scan_id: int):
    # get the current flake
    current_scan = scan.query.get(scan_id)

    # gets the directory of the scan
    scan_dir = os.path.join(
        IMAGE_DIRECTORY, current_scan.exfoliated_material, current_scan.name
    )

    # Removes the Directory from the computer
    shutil.rmtree(scan_dir)

    # removes the images froom the from the db
    image.query.filter(image.flake_id == current_scan._id).delete()

    # delete the Flake from the Database
    db.session.delete(current_scan)
    db.session.commit()


def delete_flake(db: SQLAlchemy, IMAGE_DIRECTORY: str, flake_id: int):
    # get the current flake
    current_flake = flake.query.get(flake_id)

    # gets the directory of the Flake
    flake_dir = os.path.join(IMAGE_DIRECTORY, current_flake.path)

    # Removes the Directory from the computer
    shutil.rmtree(flake_dir)

    # removes the images froom the from the db
    image.query.filter(image.flake_id == current_flake._id).delete()

    # delete the Flake from the Database
    db.session.delete(current_flake)
    db.session.commit()


def get_scans(db: SQLAlchemy, query_dict: dict):
    try:
        RETURNED_VALUES = {
            "scan_id": scan._id,
            "scan_name": scan.name,
            "scan_exfoliated_material": scan.exfoliated_material,
            "scan_user": scan.user,
            "scan_time": scan.time,
        }

        try:
            SCAN_LIMIT = query_dict["flake_limit"]
        except:
            SCAN_LIMIT = 100

        querys = []
        # Building the Querys, First iterate through the Returned values keys, as these are the only ones we want to filter for
        for key in RETURNED_VALUES.keys():
            # Now look if that keys is also present in the query dict
            if key in query_dict.keys():
                # case 1: Size is not an exact comparison
                if key == "flake_size":
                    querys.append(RETURNED_VALUES[key] > query_dict[key])
                    continue
                # case 2: The other ones are all exact Comparisons
                querys.append(RETURNED_VALUES[key] == query_dict[key])

        flakes = (
            db.session.query(*RETURNED_VALUES.values())
            .filter(*querys)
            .limit(SCAN_LIMIT)
        )

        new_dict = [
            {key: value for (key, value) in zip(RETURNED_VALUES.keys(), f)}
            for f in flakes
        ]

        return new_dict
    except KeyError as ke:
        print(ke)
        return []


def get_flakes(db: SQLAlchemy, query_dict: dict):
    try:
        RETURNED_VALUES = {
            "flake_id": flake._id,
            "scan_name": scan.name,
            "scan_id": scan._id,
            "scan_exfoliated_material": scan.exfoliated_material,
            "chip_id": chip._id,
            "flake_thickness": flake.thickness,
            "flake_size": flake.size,
            "flake_used": flake.used,
            "flake_path": flake.path,
        }

        if "query_limit" in query_dict:
            FLAKE_LIMIT = query_dict["query_limit"]
            if int(FLAKE_LIMIT) < 1:
                FLAKE_LIMIT = 100000
        else:
            FLAKE_LIMIT = 100

        querys = []

        if "flake_id" in query_dict:
            querys = [flake._id == query_dict["flake_id"]]
        else:
            # Building the Querys, First iterate through the Returned values keys, as these are the only ones we want to filter for
            for key in RETURNED_VALUES.keys():
                # Now look if that keys is also present in the query dict
                if key in query_dict.keys():
                    # case 1: Size is not an exact comparison
                    if key == "flake_size":
                        querys.append(RETURNED_VALUES[key] > query_dict[key])
                        continue
                    # case 2: The other ones are all exact Comparisons
                    querys.append(RETURNED_VALUES[key] == query_dict[key])

        flakes = (
            db.session.query(*RETURNED_VALUES.values())
            .join(chip, chip._id == flake.chip_id)
            .join(scan, scan._id == chip.scan_id)
            .filter(*querys)
            .limit(FLAKE_LIMIT)
        )

        new_dict = [
            {key: value for (key, value) in zip(RETURNED_VALUES.keys(), f)}
            for f in flakes
        ]

        return new_dict
    except KeyError as ke:
        print(ke)
        return []
