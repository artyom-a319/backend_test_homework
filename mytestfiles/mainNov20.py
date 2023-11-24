# Объекты этого класса создаются вызовом метода show_training_info().
class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self, training_type: str, duration: str,
                 distance: str, speed: str, calories: str) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        # БЕЗ ПЛЮСОВ ВЫДАЕТ ОШИБКУ SyntaxError: invalid syntax.
        return ('Тип тренировки: {}; '.format(self.training_type) +
                'Длительность: {:.3f} ч.; '.format(self.duration) +
                'Дистанция: {:.3f} км.; '.format(self.distance) +
                'Ср. скорость: {:.3f} км/ч; '.format(self.speed) +
                'Потрачено ккал: {:.3f}'.format(self.spent_calories))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65  # Расстояние за один шаг.
    M_IN_KM = 1000  # Перевод из метров в километры.
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.distance / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = (self, __class__.__name__,
                   self.duration,
                   self.get_distance,
                   self.get_mean_speed,
                   self.get_spent_calories)
        return message


class Running(Training):
    """Тренировка: бег."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        calories_count = (self.CALORIES_MEAN_SPEED_MULTIPLIER *
                          self.mean_speed +
                          self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / (
                          self.M_IN_KM * self.duration)
        return calories_count


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_SHIFT = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        calories_count = ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight +
                          (self.mean_speed**2 / self.height) *
                           self.CALORIES_MEAN_SPEED_SHIFT * (
                           self.weight) * self.duration))
        return calories_count


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38  # Расстояние за 1 гребок.
    CALORIES_MEAN_SPEED_MULTIPLIER = 1.1  # Обновленная константа
    CALORIES_MEAN_SPEED_SHIFT = 2  # Обновленная константа

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = self.length_pool  # Длина бассейна.
        self.count_pool = self.count_pool  # Раз переплыл бассейн.

    def get_spent_calories(self) -> float:
        spent_calories = (
            (self.mean_speed + self.CALORIES_MEAN_SPEED_MULTIPLIER) * (
             self.CALORIES_MEAN_SPEED_SHIFT * (
              self.weight * self.duration)))
        return spent_calories

    def get_mean_speed(self) -> float:
        mean_speed = self.length_pool * self.count_pool / (
                     self.M_IN_KM / self.duration)
        return mean_speed


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_data = {
     'SWM': Swimming,
     'RUN': Running,
     'WLK': SportsWalking
    }
    if workout_type not in workout_data:
        raise ValueEror('Введён неверный код тренировки')
        return workout_data(workout_type)[data]


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
