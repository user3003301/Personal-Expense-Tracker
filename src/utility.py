# Utility function

from datetime import datetime, date

def string_to_date(date_string: str) -> date | None:
    """Return a date value based on a date represented as a string.

    The date string must be in the format day/month/year    
    """
    if date_string == "":
        return None
    date_obj = datetime.strptime(date_string, "%d/%m/%Y").date()
    return date_obj

def date_to_string(date_obj: date) -> str:
    """Return a date represented as a string based on a date value"""
    formatted_date = date_obj.strftime("%d/%m/%Y")
    return formatted_date

