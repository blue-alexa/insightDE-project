import glob, os
import shutil
import zipfile

import logging

def unzip_and_save_csv(source_folder, target_folder):
    logger = logging.getLogger("log_download.log_preprocess")

    temp = os.path.join(source_folder, 'temp')

    # make folders
    os.mkdir(temp)
    logger.info(f"Successfully created directory {temp}")

    try:
        os.makedirs(target_folder)
        logger.info(f"Successfully created directory {target_folder}")
    except FileExistsError:
        logger.info(f"Directory already exists {target_folder}")

    source = os.path.join(source_folder, '*.zip')

    # extract all zip files
    for f in glob.glob(source):
        target = os.path.join(temp, os.path.basename(f))
        with zipfile.ZipFile(f, 'r') as zip_ref:
            zip_ref.extractall(target)
            logger.info(f"Successfully extracted {target}")

    # move csv file to target folder
    to_move = []
    for dirpath, dirnames, filenames in os.walk(temp):
        for f in filenames:
            if f.endswith('.csv'):
                to_move.append((os.path.join(dirpath, f), os.path.join(target_folder, f)))

    for s, t in to_move:
        shutil.move(s, t)
        logger.info(f"Moved {s} to {t}")

    # remove temp folder
    try:
        shutil.rmtree(temp)
        logger.info(f"Remove temporary folder {temp}")
    except OSError as e:
        logger.error(f"Error: {e.filename} - {e.strerror}.")



