from dataclasses import dataclass
from dataclasses import asdict
from typing import List

@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration_hour: float
    distance: float
    speed: float
    calories: float
    message = ('Тип тренировки: {training_type}; '
               'Длительность: {duration_hour:0.3f} ч.; '
               'Дистанция: {distance:0.3f} км; '
               'Ср. скорость: {speed:0.3f} км/ч; '
               'Потрачено ккал: {calories:0.3f}.')

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
    pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())
    # возвращает объект класса сообщения.


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        duration_minutes = self.duration * 60
        calories = ((self.coeff_calorie_1
                    * self.get_mean_speed()
                    - self.coeff_calorie_2)
                    * self.weight
                    / self.M_IN_KM
                    * duration_minutes)
        return calories


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    coeff_calorie_3 = 0.035
    coeff_calorie_4 = 2
    coeff_calorie_5 = 0.029

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_minute = self.duration * 60
        spent_calories = ((0.035 * self.weight + (self.get_mean_speed() * 2
                          / self.height)
                          * 0.029 * self.weight)
                          * duration_minute)
        return spent_calories


class Swimming(Training):
    """Тренировка: плавание."""
    coeff_calorie_6 = 1.1
    coeff_calorie_7 = 2

    def __init__(self, action: int,
                 duration: float,
                 weight: float,
                 length_pool: float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.action = action
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Переопределили метод, средняя скорость."""
        speed = self.length_pool + self.count_pool / self.M_IN_KM \
            * self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Переопределили метод, колории."""
        spent_colories = ((self.get_mean_speed()
                          + self.coeff_calorie_6)
                          * self.coeff_calorie_7
                          * self.weight)
        return spent_colories

def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    if workout_type == 'SWM':
       return Swimming(data[0], data[1], data[2], data[3], data[4])
    elif workout_type == 'RUN':
       return Running(data[0], data[1], data[2])
    elif workout_type == 'WLK':
        return SportsWalking(data[0], data[1], data[2], data[3])

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