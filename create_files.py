import os
from random import randint

from uuid import uuid4

root_absolute_path = '/Users/karimhamid/PycharmProjects/kasperskyFileTask/test_directory'

for i in range(3):
    with open(
            os.path.join(root_absolute_path, f'dir_1/dir_2/dir_3/file_{uuid4()}'),
            'wb') as file:
        file.write(bytes(
            'a' * randint(0, 30000), 'utf-8'
        ))