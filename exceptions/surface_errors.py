class NonequivalentPlanesError(Exception):
    def __init__(self, srf1, srf2):
        self.srf1 = srf1
        self.srf2 = srf2
        self.message = 'Плоскости не совпадают'
        super().__init__(self.message)

    def __str__(self):
        return f'Плоскости {self.srf1} и {self.srf2} не совпадают\nУкажите совпадающие'


class NonequivalentPointsCountError(Exception):
    def __init__(self, srf1, srf2):
        self.srf1 = srf1
        self.srf2 = srf2
        self.message = 'Количество точек на плоскостях не совпадает'
        super().__init__(self.message)

    def __str__(self):
        return f'Количество точек на плоскостях {self.srf1} и {self.srf2} не совпадает\nУкажите корректные плоскости'


class SurfacesNotFoundError(Exception):
    def __init__(self, srf1, srf2):
        self.srf1 = srf1
        self.srf2 = srf2
        self.message = 'Указанные поверхности не обнаружены'
        super().__init__(self.message)

    def __str__(self):
        return f'Одна или обе из указанных поверхностей ({self.srf1} и {self.srf2}) не обнаружены\nУкажите существующие'
