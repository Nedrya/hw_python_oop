from dataclasses import dataclass
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
        return InfoMessage.message

class Training:
    """Базовый класс тренировки."""
    len_step = 0,65
    m_in_km = 1000
    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
       

    def get_distance(self, len_step: float, m_in_km: int) -> float:
        """Получить дистанцию в км."""
        self.len_step = len_step
        self.m_in_km = m_in_km
        distance = self.action * self.len_step / self.m_in_km
        return distance
    

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed = self.get_distance() / self.duration
        return speed
    
    #преодоленная_дистанция_за_тренировку / время_тренировки

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
    pass
    # оставляем pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage.get_message(self.training_type, self.duration, self.distance, self.speed, self.calories)
    # возвращает объект класса сообщения.


class Running(Training):
    """Тренировка: бег."""
    coeff_calorie_1 = 18
    coeff_calorie_2 = 20 

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)
        duration_minutes = duration * 60
        calories = (Running.coeff_calorie_1 * Training.get_mean_speed - Running.coeff_calorie_2) * self.weight / self.m_in_km * duration_minutes 

    def show_training_info(self) -> InfoMessage:
        """Возврат информации."""
        return InfoMessage.get_message(self.training_type, self.duration, self.distance, self.speed, self.calories)




class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self, action: int, duration: float, weight: float, height : float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
    
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        duration_minute = self.duration * 60
        (0.035 * self.weight + (self.get_mean_speed **2 // self.height) * 0.029 * self.weight) * duration_minute 
    
    def show_training_info(self) -> InfoMessage:
        """Возврат информации."""
        return InfoMessage.get_message(self.training_type, self.duration, self.distance, self.speed, self.calories)

#Конструктор этого класса принимает дополнительный параметр height — рост спортсмена.
#(0.035 * вес + (средняя_скорость**2 // рост) * 0.029 * вес) * время_тренировки_в_минутах 
#Числовым коэффициентам тоже нужны имена, не забывайте про это.

class Swimming(Training):
    """Тренировка: плавание."""
    coeff_calorie_5 = 1.1
    coeff_calorie_6 = 2
    def __init__(self, action: int, duration: float, weight: float, length_pool : float, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.action = action
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Переопределили метод, средняя скорость."""
        mean_speed= self.length_pool + self.count_pool / self.m_in_km * self.duration
        #длина_бассейна * count_pool / M_IN_KM / время_тренировки
        return mean_speed

    def get_spent_calories(self) -> float:
        """Переопределили метод, колории."""
        spent_colories = (self.get_mean_speed + Swimming.coeff_calorie_5) * Swimming.coeff_calorie_6 * self.weight 
        #(средняя_скорость + 1.1) * 2 * вес 
        return spent_colories

    def show_training_info(self) -> InfoMessage:
        """Возврат информации."""
        return InfoMessage.get_message(self.training_type, self.duration, self.distance, self.speed, self.calories)
    


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
    info = InfoMessage.show_training_info(main)
    print(info.get_message(info))
    

if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)

