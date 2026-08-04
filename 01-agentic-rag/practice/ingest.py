import json

def load_and_flatten_data(file_path : str = "documents.json") -> list[dict]:
    """
    Reads the nested JSON document and flattens it for the search engine.
    Returns a list of flat dictionaries
    """

    with open(file_path, "rt") as f_in:
        docs_raw = json.load(f_in)

    documents = []

    for category_dict in docs_raw:
        category_name = category_dict["category"]

        for doc in category_dict["documents"]:
            doc["category"] = category_name
            documents.append(doc)

    return documents