from typing import Callable, Dict, Any, List
from threading import Timer

def delay_for(request: Callable) -> Callable:
    """декоратор для запросов"""

    def request_with_delay(*args: list) -> Dict[Any, Any]:
        """возвращаемая обертка с задержкой"""
        timer = MyTimer(delay), request_to_twocan, args)  # type: ignore
        timer.start()
        return timer.join()

    return request_with_delay


class MyTimer(Timer):
    """не блочащий тред таймер"""

    def __init__(self, interval: int, function: Callable, args: List):
        self._original_function = function
        self.result: Dict = {}
        super().__init__(interval, self._do_execute, args)

    def _do_execute(self, *a: list) -> None:
        """выполнить функцию"""
        self.result = self._original_function(*a)

    def join(self) -> Dict[Any, Any]:  # type: ignore
        """получение результатов таймера"""
        super().join()
        return self.result
