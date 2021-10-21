import json
import ntpath
import os
import re
import shutil
import numpy as np

import cv2
from flask_sqlalchemy import SQLAlchemy

from Database_tables import *

SCALE_LENGTH = {
    "2.5x.png": ["1mm", 325],
    "5x.png": ["500um", 325],
    "20x.png": ["125um", 325],
    "50x.png": ["50um", 325],
    "100x.png": ["25um", 325],
}


def add_scalebar(file_path):

    img = cv2.imread(file_path)
    file_dir = os.path.dirname(file_path)
    img_name = ntpath.basename(file_path)
    img_scalebar_name = f"{img_name}_scalebar.png"
    img_scalebar_path = os.path.join(file_dir, img_scalebar_name)

    x1, y1 = 50, 50
    x2, y2 = SCALE_LENGTH[img_name][1] + x1, 70

    font = cv2.FONT_HERSHEY_SIMPLEX

    img = cv2.rectangle(img, (x1, y1), (x2, y2), (255, 255, 255), thickness=-1)

    cv2.putText(
        img,
        SCALE_LENGTH[img_name][0],
        (50, 120),
        font,
        2,
        (255, 255, 255),
        4,
    )

    cv2.imwrite(img_scalebar_path, img)

    return img_scalebar_path


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


def get_unique_thicknesses(db: SQLAlchemy):
    # The [:,0] is to get the first column of the array and not the empty ones
    return np.array(db.session.query(flake.thickness).distinct().all())[:, 0].tolist()


def get_unique_materials(db: SQLAlchemy):
    return np.array(db.session.query(scan.exfoliated_material).distinct().all())[
        :, 0
    ].tolist()


def get_scan_metadata(db: SQLAlchemy, scan_id: int):

    RETURNED_VALUES = {
        "flake_id": flake._id,
        "flake_size": flake.size,
        "flake_thickness": flake.thickness,
        "flake_used": flake.used,
        "flake_height": flake.height,
        "flake_width": flake.width,
        "flake_aspect_ratio": flake.aspect_ratio,
        "flake_entropy": flake.entropy,
        "flake_position_x": flake.position_x,
        "flake_position_y": flake.position_y,
        "flake_mean_contrast_r": flake.mean_contrast_r,
        "flake_mean_contrast_g": flake.mean_contrast_g,
        "flake_mean_contrast_b": flake.mean_contrast_b,
        "flake_proximity_stddev": flake.proximity_stddev,
        "chip_id": chip._id,
        "chip_thickness": chip.chip_thickness,
        "scan_id": scan._id,
        "scan_name": scan.name,
        "scan_user": scan.user,
        "scan_exfoliated_material": scan.exfoliated_material,
        "scan_time": scan.time,
        "scan_exfoliation_method": scan.exfoliation_method,
    }

    flakes = (
        db.session.query(*RETURNED_VALUES.values())
        .join(chip, chip._id == flake.chip_id)
        .join(scan, scan._id == chip.scan_id)
        .filter(scan._id == scan_id)
    )
    return flakes.all(), RETURNED_VALUES.keys()


def get_unique_users(db: SQLAlchemy):
    return np.array(db.session.query(scan.user).distinct().all())[:, 0].tolist()


def delete_scan(db: SQLAlchemy, IMAGE_DIRECTORY: str, scan_id: int):
    """Removes every Image, flake and chip from the DB belonging to the Scan
    Lastly removes the scan

    Args:
        db (SQLAlchemy): The database object
        IMAGE_DIRECTORY (str): The directory where the images are saved
        scan_id (int): The ID of the scan to be removed
    """
    # get the current scan
    current_scan = scan.query.get(scan_id)

    # gets the directory of the scan
    scan_dir = os.path.join(IMAGE_DIRECTORY, current_scan.name)

    # Get all the chips belonging to the scan
    chips = chip.query.filter(chip.scan_id == current_scan._id).all()

    for chip_obj in chips:

        # Get all the flakes belonging to the scan
        flakes = flake.query.filter(chip_obj._id == flake.chip_id).all()

        for flake_obj in flakes:

            # get and delete the images
            image.query.filter(flake_obj._id == image.flake_id).delete()

        # Delete the Flake
        flakes = flake.query.filter(chip_obj._id == flake.chip_id).delete()

    # Delete the Chip
    chip.query.filter(chip.scan_id == current_scan._id).delete()

    # Delete The current Scan
    db.session.delete(current_scan)

    # Commit the Changes
    db.session.commit()

    # Removes the Directory and every subdirectory from the computer
    print(f"Removing {scan_dir}")
    shutil.rmtree(scan_dir)


def delete_flake(db: SQLAlchemy, IMAGE_DIRECTORY: str, flake_id: int):
    # get the current flake
    current_flake = flake.query.get(flake_id)

    # gets the directory of the Flake
    flake_dir = os.path.join(IMAGE_DIRECTORY, current_flake.path)

    # Removes the Directory from the computer
    shutil.rmtree(flake_dir)

    # removes the images from the from the db
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
            SCAN_LIMIT = query_dict["query_limit"]
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

        # First get all the Scans
        # Then filter the Scans
        # Then order the Scans
        # Then limit the Scans
        scans = (
            db.session.query(*RETURNED_VALUES.values())
            .filter(*querys)
            .order_by(scan.time.desc())
            .limit(SCAN_LIMIT)
        )

        new_dict = [
            {key: value for (key, value) in zip(RETURNED_VALUES.keys(), s)}
            for s in scans
        ]

        return new_dict
    except KeyError as ke:
        print(ke)
        return []
    except OSError as e:
        print(e)
        return []


def get_flakes(db: SQLAlchemy, query_dict: dict):
    try:
        RETURNED_VALUES = {
            "flake_id": flake._id,
            "flake_path": flake.path,
            "flake_size": flake.size,
            "flake_thickness": flake.thickness,
            "flake_used": flake.used,
            "flake_height": flake.height,
            "flake_width": flake.width,
            "flake_aspect_ratio": flake.aspect_ratio,
            "flake_entropy": flake.entropy,
            "chip_id": chip._id,
            "chip_used": chip.used,
            "chip_thickness": chip.chip_thickness,
            "scan_id": scan._id,
            "scan_name": scan.name,
            "scan_user": scan.user,
            "scan_exfoliated_material": scan.exfoliated_material,
            "scan_time": scan.time,
        }

        if "query_limit" in query_dict:
            FLAKE_LIMIT = query_dict["query_limit"]
            if int(FLAKE_LIMIT) < 1:
                FLAKE_LIMIT = 10000
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

        matching_flakes = [
            {key: value for (key, value) in zip(RETURNED_VALUES.keys(), f)}
            for f in flakes
        ]

        return matching_flakes
    except KeyError as ke:
        print(ke)
        return []
    except OSError as e:
        print(e)
        return []


def Upload_scan_directory_to_db(
    db: SQLAlchemy,
    scan_directory,
):
    scan_meta_path = os.path.join(scan_directory, "meta.json")

    with open(scan_meta_path) as f:
        scan_meta = json.load(f)

    # Really Scuffed Extraction of Data
    exfoliation_method = None
    if "scan_exfoliation_method" in scan_meta.keys():
        exfoliation_method = scan_meta["scan_exfoliation_method"]

    current_scan = scan(
        name=scan_meta["scan_name"],
        user=scan_meta["scan_user"],
        time=scan_meta["scan_time"],
        exfoliated_material=scan_meta["scan_exfoliated_material"],
        exfoliation_method=exfoliation_method,
    )

    db.session.add(current_scan)
    db.session.commit()
    current_scan_id = current_scan._id

    chip_directory_names = [
        chip_directory_name
        for chip_directory_name in sorted_alphanumeric(os.listdir(scan_directory))
        if os.path.isdir(os.path.join(scan_directory, chip_directory_name))
    ]

    for chip_directory_name in chip_directory_names:
        chip_directory = os.path.join(scan_directory, chip_directory_name)

        # Create a new chip and push it to the DB
        current_chip = chip(
            current_scan_id,
            chip_thickness=scan_meta["chip_thickness"],
        )
        db.session.add(current_chip)
        db.session.commit()
        # get the created ID
        current_chip_id = current_chip._id

        flake_directory_names = [
            flake_directory_name
            for flake_directory_name in sorted_alphanumeric(os.listdir(chip_directory))
            if os.path.isdir(os.path.join(chip_directory, flake_directory_name))
        ]

        for flake_directory_name in flake_directory_names:
            flake_directory = os.path.join(chip_directory, flake_directory_name)

            # Open the JSON File
            meta_path = os.path.join(flake_directory, "meta.json")
            with open(meta_path, "r") as f:
                meta_data = json.load(f)
                flake_data = meta_data["flake"]
                image_data = meta_data["images"]

            if "path" not in flake_data.keys():
                ##### REMOVE THIS LATER
                path = os.path.normpath(flake_directory)
                flake_data["path"] = "/".join(path.split(os.sep)[-3:])
                #####

            if "chip_id" in flake_data.keys():
                del flake_data["chip_id"]

            current_flake = flake(chip_id=current_chip_id, **flake_data)
            db.session.add(current_flake)
            db.session.commit()

            current_flake_id = current_flake._id

            for key, value in image_data.items():
                image_path = os.path.join(flake_data["path"], f"{key}.png")
                current_image = image(
                    flake_id=current_flake_id,
                    path=image_path,
                    **value,
                )
                db.session.add(current_image)
                db.session.commit()
