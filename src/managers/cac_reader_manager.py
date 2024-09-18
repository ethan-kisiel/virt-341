"""
Handles the storage and reading of cac cards
"""


class CACData:
    """
    Represents the data that comes from readinga  cac card
    """

    barcode_version: str
    personal_designator_identifier: str
    personal_designator_type: str

    dod_id_number: str

    first_name: str

    last_name: str

    # TODO: Implement the rest


class CACReaderManager:
    """
    Manages reading cac information


    INFO: bar-code type will determine if there is a midddle initial
    “1” is 88 characters and does not have the middle initial.
    “N” is 89 characters, the last one being the MI.
    """

    @staticmethod
    def parse_data(data: str) -> CACData:
        """takes scanned cac data and parses out the information needed

        Keyword arguments:
        data -- string of the scanned cac data
        Return: CACData object populated with live data
        """

        return CACData()

    @staticmethod
    def parse_card_version(data: str):
        """sumary_line

        Keyword arguments:
        argument -- description
        Return: return_description
        """
