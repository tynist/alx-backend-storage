#!/usr/bin/env python3
"""
List all documents in Python
"""

from pymongo.collection import Collection


def list_all(mongo_collection: Collection) -> list[dict]:
    """
    Retrieves all documents from a MongoDB collection.
    Args:
        mongo_collection: A PyMongo collection object representing the collection.
    Returns:
        A list of dictionaries representing the documents in the collection.
    """
    # Use the find() method to retrieve all documents from the collection
    cursor = mongo_collection.find()

    # Convert the cursor to a list of dictionaries
    documents = list(cursor)

    return documents
