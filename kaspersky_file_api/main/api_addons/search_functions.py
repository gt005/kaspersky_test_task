import os
import fnmatch
import datetime
import tempfile
import zipfile

conditions_functions = {
    'eq': lambda x, y: x == y,
    'gt': lambda x, y: x > y,
    'lt': lambda x, y: x < y,
    'ge': lambda x, y: x >= y,
    'le': lambda x, y: x <= y,
}


def make_search(root_directory_path: str, file_find_criteria: dict) -> list[str]:
    """ Выполняет поиск файлов по заданным параметрам

    :param root_directory_path: Путь к директории, в которой будет производиться поиск
    :param file_find_criteria: Параметры, заданные условием задачи
    :return: Список всех путей к файлам, удовлетворяющих заданным параметрам
    """

    found_files_path = []

    for root, dirs, files in os.walk(root_directory_path):
        for file_name in files:
            if fnmatch.fnmatch(file_name, '*.zip'):
                # Проверяем, что файл имеет расширение .zip
                # Тогда извлекаем его во временную директорию
                # и ищем в ней нужные файлы, а затем удаляем временную директорию
                #
                # Конфликтов быть не должно, так как для каждого файла создается
                # уникальная временная директория
                with tempfile.TemporaryDirectory() as tmpdir:
                    with zipfile.ZipFile(
                            os.path.join(root, file_name),
                            'r'
                    ) as zip_archive:
                        # Извлекаем архив во временную директорию
                        zip_archive.extractall(tmpdir)

                        for zipfile_root, zipfile_dirs, zipfile_files in os.walk(tmpdir):
                            for zipfile_file_name in zipfile_files:
                                if is_file_matching_criteria(
                                        zipfile_root,
                                        zipfile_file_name,
                                        file_find_criteria
                                ):
                                    found_files_path.append(
                                        os.path.join(
                                            root,
                                            file_name,
                                            zipfile_file_name
                                        )
                                    )
            elif is_file_matching_criteria(
                    root,
                    file_name,
                    file_find_criteria
            ):
                found_files_path.append(os.path.join(root, file_name))

    return found_files_path


def is_file_matching_criteria(
        root: str,
        filename: str,
        file_find_criteria: dict
) -> bool:
    """ Проверяет, удовлетворяет ли файл заданным параметрам

    :param root: Путь к директории, в которой находится файл
    :param filename: Имя файла
    :param file_find_criteria: Параметры, заданные условием задачи
    :return: True, если файл удовлетворяет заданным параметрам, иначе False
    """
    file_absolute_path = os.path.join(root, filename)

    file_mask = file_find_criteria.get('file_mask')
    if file_mask is not None:
        if not fnmatch.fnmatch(filename, file_mask):
            return False

    file_size = file_find_criteria.get('size')
    if file_size is not None:
        file_size_operator = file_find_criteria.get('size').get('operator')
        if not conditions_functions[file_size_operator](
            os.path.getsize(file_absolute_path),
            file_size.get('value')
        ):
            return False

    creation_time = file_find_criteria.get('creation_time')
    if creation_time:
        creation_time_operator = file_find_criteria.get('creation_time').get(
            'operator')
        creation_time = datetime.datetime.strptime(
            creation_time.get('value'), '%Y-%m-%dT%H:%M:%SZ'
        )

        if not conditions_functions[creation_time_operator](
            datetime.datetime.fromtimestamp(
                os.path.getctime(file_absolute_path)
            ),
            creation_time
        ):
            return False

    text = file_find_criteria.get('text')
    if text is not None:
        with open(file_absolute_path, 'rb') as file:
            if bytes(text, 'utf-8') not in file.read():
                return False

    return True