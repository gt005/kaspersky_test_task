# /Users/karimhamid/PycharmProjects/kasperskyFileTask/test_directory/dir_1/dir_2/dir_3/file_2b6c7241-fb51-4621-b25d-49a71ace3909
import os.path
import unittest
from search_functions import is_file_matching_criteria, make_search

root_path = '../../../test_directory'


class SearchFunctionsTestCase(unittest.TestCase):
    def test_is_file_matching_criteria(self):
        self.assertEqual(
            is_file_matching_criteria(
                root_path,
                'empty_file',
                {
                    'size': {
                        'value': -1,
                        'operator': 'gt'
                    }
                }
            ), True
        )
        self.assertEqual(
            is_file_matching_criteria(
                root_path,
                'text_one_symbol.txt',
                {
                    'text': 'a',
                    'file_mask': '*.txt',
                    'size': {
                        'value': 0,
                        'operator': 'eq'
                    }
                }
            ), False
        )
        self.assertEqual(
            is_file_matching_criteria(
                root_path,
                'text_one_symbol.txt',
                {
                    'text': 'a',
                    'file_mask': '*.txt',
                    'size': {
                        'value': 1,
                        'operator': 'ge'
                    }
                }
            ), True
        )

    def test_my_function2(self):
        self.assertEqual(
            make_search(
                root_path,
                {
                    'text': 'a',
                }
            ), [
                '../../../test_directory/file_3de853da-0616-4bc4-90b3-e3a96b5c628d',
                '../../../test_directory/dir_1/dir_2/dir_3.zip/file_from_zip',
                '../../../test_directory/dir_1/dir_2/dir_4/file_3f9471b2-1de0-41f0-8b84-1962799494ab',
                '../../../test_directory/dir_1/dir_2/dir_4/file_2b6c7241-fb51-4621-b25d-49a71ace3909'
            ]
        )
