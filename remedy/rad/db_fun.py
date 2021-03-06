"""
db_fun.py 

This module contains helper functions for database entry creation. 
"""

from models import Resource, Category
from datetime import datetime


def get_or_create(session, model, **kwargs):
    """
    Determines if a given record already exists in the database.

    Args:
        session: The database session.
        model: The model for the record.
        **kwargs: The properties to set on the model. The first
            specified property will be used to determine if
            the model already exists.

    Returns:
        Two values. The first value is a boolean
        indicating if this item is a new record. The second
        value will be the created/retrieved model.
    """
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return False, instance
    else:
        instance = model(**kwargs)
        return True, instance


def add_get_or_create(database, model, **kwargs):
    """
    Gets or creates an record based on if it already exists.
    If it does not already exist, it will be created.

    Args:
        session: The database session.
        model: The model to get or create.
        **kwargs: The properties to set on the model. The first
            specified property will be used to determine if
            the model already exists.

    Returns:
        Two values. The first value is a boolean
        indicating if this item is a new record. The second
        value will be the created/retrieved model.
    """
    new_record, record = get_or_create(database.session, model, **kwargs)

    if new_record:
        database.session.add(record)

    return new_record, record


def get_or_create_resource(database, rad_record, lazy=True):
    """
    Checks to see if a resource already exists in the database
    and adds it if it does not exist (or is forced to by use of
    the lazy argument).

    Args: 
        database: The current database context. 
        rad_record: The RadRecord to be added.
        lazy: If false, forces the record to be added even if it is a duplicate. 
            Defaults to true.

    Returns:
        Two values. The first value is a boolean
        indicating if a new record was created. The second
        value will be the created/updated model.
    """

    new_record, record = get_or_create(database.session, Resource, name=rad_record.name.strip())

    record.last_updated = datetime.utcnow()

    if new_record:
        record.date_created = datetime.utcnow()

    if new_record or not lazy:

        # See if we have just a normal address field - if not,
        # manually construct one by joining all available
        # fields with commas
        new_address = ''
        if hasattr(rad_record, 'address') and \
            rad_record.address is not None and \
            not rad_record.address.isspace():

            new_address = rad_record.address.strip()
        else:
            new_address = ", ".join(a.strip() for a in [rad_record.street,
                                    rad_record.city, rad_record.state,
                                    rad_record.zipcode, rad_record.country]
                                    if a is not None and a != '' and not a.isspace())

        # Address issue 131 - if we're updating an existing
        # record, and are changing the address (using a lowercase comparison),
        # invalidate the existing geocoding information.
        if not new_record and \
            record.address is not None and \
            record.address.lower() != new_address.lower():
            record.latitude = None
            record.longitude = None

        # Now set the new address
        if new_address != '' and not new_address.isspace():
            record.address = new_address
        else:
            record.address = None

        # Copy over all the other fields verbatim
        record.organization = rad_record.organization
        record.description = rad_record.description

        record.email = rad_record.email
        record.phone = rad_record.phone
        record.fax = rad_record.fax
        record.url = rad_record.url

        record.source = rad_record.source
        record.visible = rad_record.visible

        # Do we have a list of category names?
        # Failing that, do we have a single category name?
        if hasattr(rad_record, 'category_names') and \
            rad_record.category_names is not None and \
            len(rad_record.category_names) > 0:

            for category_name in rad_record.category_names:

                # Try to look up the name of the provided category,
                # get/create as necessary and add the record
                new_category, category_record = add_get_or_create(database, Category,
                                                              name=category_name.strip())

                # Make sure we're not double-adding
                if not category_record in record.categories:
                    record.categories.append(category_record)

        elif hasattr(rad_record, 'category_name') and \
            rad_record.category_name is not None and \
            not rad_record.category_name.isspace():

            # Try to look up the name of the provided category,
            # get/create as necessary and add the record
            new_category, category_record = add_get_or_create(database, Category,
                                                              name=rad_record.category_name.strip())

            # Make sure we're not double-adding
            if not category_record in record.categories:
                record.categories.append(category_record)

        database.session.add(record)

        # Flush the session because otherwise we won't pick up
        # duplicates with UNIQUE constraints (such as in category names) 
        # until we get an error trying to commit such duplicates
        # (which is bad)
        database.session.flush()

    return new_record, record

