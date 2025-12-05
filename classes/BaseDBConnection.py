from abc import ABC, abstractmethod

class BaseDBConnection(ABC):
    """
    Interface base para conectar e executar queries em diferentes bancos de dados.
    """

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def execute_query(self, query):
        pass

    @abstractmethod
    def close(self):
        pass