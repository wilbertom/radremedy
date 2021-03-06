"""
bootstrap.py 

Imports data from database files and from the scrapers. 
"""
from rad.db_fun import add_get_or_create, get_or_create_resource
from rad.models import Category
from radremedy import db
from get_save_data import run as run_scrapers
from data_importer.data_importer import seconds, open_dict_csv, open_csv, minus_key, rename_key, data_dir
from radrecord import rad_record
import sys

def strap(application):
    """
    First, this function runs the data importers and adds them to the database.
    Then, it runs the scrapers and does the same. 
    """

    with application.app_context():

        # Try a sample join to make sure that our
        # data_dir is good and add a helpful error message
        # when it's not.
        try:
            data_dir('rad_resource.csv')
        except:
            sys.exit('The source data directory is missing or invalid. ' \
                'This is typically due to a missing RAD_DATA_BASE environment variable.')

        # Load all the resources' data, but we drop the id
        # column because our database will assign them on its own.
        # We also want to attempt to rename the "category" row, if provided,
        # to "category_name", as that's consistent with the RadRecord format.
        raw_resources = map(lambda row: rename_key(minus_key(row, 'id'), 
                                'category', 'category_name'),
                            open_dict_csv(data_dir('rad_resource.csv')))

        # Now save every record. To support multiple delimited
        # categories in the category_name field, we invoke
        # convert_category_name() on the raw rad_record
        # generated from the data row.
        map(lambda row: get_or_create_resource(db, 
            rad_record(**row).convert_category_name()),
            raw_resources)

        db.session.commit()

        # run all the scrapers
        run_scrapers(application)
