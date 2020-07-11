"""
Query genomic data file and save in json format

@author: Yilin Xu <yilinxu@uchicago.edu>
"""

import json
from datetime import date

import requests

from gen3_augur_pyutils.common.io import IO
from gen3_augur_pyutils.common.logger import Logger
from gen3_augur_pyutils.common.types import ArgParserT, NamespaceT, LoggerT
from gen3_augur_pyutils.subcommands import Subcommand


class Gen3Query(Subcommand):
    @classmethod
    def __add_arguments__(cls, parser: ArgParserT) -> None:
        """
        Add the arguments to the parser
        :param parser: parsed arguments
        :return: None
        """
        parser.add_argument('--url', required=True, help='data common url')
        parser.add_argument('--type', required=True, help='define type in guppy query')
        parser.add_argument('--fields', required=True,
                            help='properties')
        parser.add_argument('--filter', required=False, help='property name for filtering')
        parser.add_argument('--value', required=False, help='property value for filtering')
        parser.add_argument('--logfile', required=True, help='path of the log file')

    @classmethod
    def get_token(cls, url: str) -> str:
        """
        Helper function for generating token.
        :params url: data common url to query from
        """
        abs_path = IO.abs_path(2, 'config/country_region_mapper.csv')
        with open(abs_path, "r") as f:
            creds = json.load(f)
        token_url = url + "user/credentials/api/access_token"
        token = requests.post(token_url, json=creds).json()["access_token"]
        return token

    @classmethod
    def query_manifest(cls, headers: dict, query_obj: dict, logger: LoggerT) -> dict:
        """
        Query metadata from gen3 data common guppy download endpoint
        :params headers: header for requests which has token
        :params query_obj: dictionary object that has parameters for query
        """
        api_url = query_obj.url + "guppy/download"
        if query_obj.filter:
            query = {
                "type": query_obj.type,
                "fields": query_obj.fields,
                "filter": {
                    "=": {
                        query_obj.filter: query_obj.value
                    }
                }
            }
        else:
            query = {
                "type": query_obj.type,
                "fields": query_obj.fields,
            }

        response = requests.post(
            api_url,
            json=query,
            headers=headers,
        )
        try:
            data = json.loads(response.text)
            IO.write_json(query_obj.file, data[0])
        except requests.exceptions.Timeout:
            logger.error("Error querying Guppy, object data query failed")

    @classmethod
    def main(cls, options: NamespaceT):
        """
        Entrypoint for Gen3Query
        :param options:
        :return:
        """
        logger = Logger.get_logger(cls.__tool_name__(), options.logfile)
        logger.info(cls.__get_description__())

        # Construct object with argument information
        today = date.today()
        day = str(today.strftime("%m%d%y"))
        file_name = options.type + "_" + day + "_manifest.json"
        query_obj = {'type': options.type, 'fields': options.fields, 'filter': options.filter, 'value': options.value,
                     'file': file_name, 'ulr': options.url}

        # Get token
        token = cls.get_token(query_obj.url)
        headers = {"Authorization": "bearer " + token}

        # Query metadata from Gen3 data common
        cls.query_manifest(headers, query_obj, logger)
