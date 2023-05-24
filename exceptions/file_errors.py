class FileExtensionError(Exception):
    def __init__(self, path):
        self.path = path
        self.message = 'Неверное расширение файла'
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} {self.path}\nОжидается .vol или .dat'


class FileStructureError(Exception):
    def __init__(self, path):
        self.path = path
        self.message = 'Неверная структура файла'
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message} {self.path}\nБлоки данных не соответствуют ожидаемым'
