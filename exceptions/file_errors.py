class FileFormatError(Exception):
    def __init__(self, path):
        self.path = path
        self.message = 'Неверный формат файла'
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} {self.path}. Ожидается .vol или .dat'


class FileStructureError(Exception):
    def __init__(self, path):
        self.path = path
        self.message = 'Неверная структура файла'
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} {self.path}. Блоки данных не соответствуют ожидаемым'


class FileWriteError(Exception):
    def __init__(self, path):
        self.path = path
        self.message = 'Ошибка записи в файл'
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} {self.path}. Facemesh и Tetmesh is None'