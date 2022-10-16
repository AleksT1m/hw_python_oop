from dataclasses import dataclass
from email import message
from typing import Dict, List, Callable

@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: int # в часах!!!
    distance: float # в км
    speed: float
    calories: float
    
    def get_message(self) -> str:
        return(
            f'Тип тренировки: {self.training_type}; '
            f'Длительность: {self.duration} ч.; '
            f'Дистанция: {self.distance: .3f} км; '
            f'Ср. скорость: {self.speed: .3f} км/ч; '
            f'Потрачено ккал: {self.calories: .3f}')

class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000 # константа для перевода метров в километры
    LEN_STEP = 0.65 # метров за один шаг
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        
    def show(self):
        print(f'{self.action} {self.duration} {self.weight} {self.LEN_STEP}')

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
        raise NotImplementedError()

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        training_info = InfoMessage(type(self).__name__, 
                                    self.duration, 
                                    self.get_distance(), 
                                    self.get_mean_speed(), 
                                    self.get_spent_calories())
        return training_info

class Running(Training):
    """Тренировка: бег."""
    def get_spent_calories(self) -> float:
        coeff_calorie_1: int = 18
        coeff_calorie_2: float = 1.79
        """Получить количество затраченных калорий.""" #переопределяем
        spent_calories = (coeff_calorie_1 * self.get_mean_speed() + coeff_calorie_2) * self.weight / self.M_IN_KM * self.duration
        return spent_calories

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height
    
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.""" #переопределить
        coeff_calorie_3: float = 0.035
        coeff_calorie_4: float = 0.029
        spent_calories =  (coeff_calorie_3 * self.weight + (self.get_mean_speed()**2 / self.height) * coeff_calorie_4 * self.weight) * self.duration
        return spent_calories

class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
    
    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий.""" #переопределить
        coeff_calorie_5: float = 1.1
        coeff_calorie_6: int = 2
        spent_calories =  (self.get_mean_speed() + coeff_calorie_5) * coeff_calorie_6 * self.weight
        return spent_calories

    def get_mean_speed(self) -> float: #переопределить
        """Получить среднюю скорость движения."""
        mean_speed = self.length_pool * self.count_pool /  self.M_IN_KM / self.duration
        return mean_speed

def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    training1: Dict[str, type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
        }
    return training1[workout_type](*data)

def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())

"""заготовка для тестирования: перебираются пакеты"""
if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)