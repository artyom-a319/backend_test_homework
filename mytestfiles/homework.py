# Объекты этого класса создаются вызовом метода show_training_info().
class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
        self,
        training_type: str,
        duration: str,
        distance: str,
        speed: str,
        calories: str,
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed  # Исправить speed на mean_speed?
        self.calories = calories

    def get_message(self) -> str:
        # БЕЗ ПЛЮСОВ ВЫДАЕТ ОШИБКУ SyntaxError: invalid syntax.
        # print(type(self).__name__)
        return (
            "Тип тренировки: {}; ".format(self.training_type)
            + "Длительность: {:.3f} ч.; ".format(self.duration)
            + "Дистанция: {:.3f} км; ".format(self.distance)
            + "Ср. скорость: {:.3f} км/ч; ".format(self.speed)
            + "Потрачено ккал: {:.3f}.".format(self.calories)
        )


class Training:
    """Базовый класс тренировки."""

    LEN_STEP = 0.65  # Расстояние за один шаг.
    M_IN_KM = 1000  # Перевод из метров в километры.
    MINUTES = 60

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    """Вернуть информационное сообщение о выполненной тренировке."""
    def show_training_info(self) -> InfoMessage:
        message_to_return = InfoMessage(
            type(self).__name__,
            self.duration,
            self.get_distance(),
            self.get_mean_speed(),
            self.get_spent_calories(),
        )
        return message_to_return


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
    ) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((
                self.CALORIES_MEAN_SPEED_MULTIPLIER
                * (self.get_mean_speed())
                + self.CALORIES_MEAN_SPEED_SHIFT) * self.weight / self.M_IN_KM
                * (self.duration * self.MINUTES))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 0.035
    CALORIES_MEAN_SPEED_SHIFT = 0.029
    MIN_TO_SEC = 60
    CM_TO_M = 100
    SPEED_IN_MS = 0.278

    def __init__(
        self, action: int, duration: float, weight: float, height: int
    ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return round((
            self.CALORIES_MEAN_SPEED_MULTIPLIER * self.weight
            + ((self.get_mean_speed() * self.SPEED_IN_MS) ** 2
                / (self.height / self.CM_TO_M))
            * self.CALORIES_MEAN_SPEED_SHIFT
            * self.weight) * (self.duration * self.MIN_TO_SEC), 3)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38  # Расстояние за 1 гребок.
    CALORIES_MEAN_SPEED_MULTIPLIER = 1.1  # Обновленная константа
    CALORIES_MEAN_SPEED_SHIFT = 2  # Обновленная константа

    def __init__(
        self,
        action: int,
        duration: float,
        weight: float,
        length_pool: int,
        count_pool: float,
    ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool  # Длина бассейна.
        self.count_pool = count_pool  # Раз переплыл бассейн.

    def get_mean_speed(self) -> float:
        return (
            self.length_pool * self.count_pool / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return round((
            self.get_mean_speed() + self.CALORIES_MEAN_SPEED_MULTIPLIER
        ) * (self.CALORIES_MEAN_SPEED_SHIFT * self.weight * self.duration), 3)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_data = {"SWM": Swimming, "RUN": Running, "WLK": SportsWalking}
    if workout_type in workout_data:
        return workout_data[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info_message = training.show_training_info()
    print(info_message.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
