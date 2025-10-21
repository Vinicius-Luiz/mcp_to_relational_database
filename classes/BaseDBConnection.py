from abc import ABC, abstractmethod

class BaseDBConnection(ABC):
    """
    Interface base para conectar e executar queries em diferentes bancos de dados.
    """

    @abstractmethod
    def conectar(self):
        pass

    @abstractmethod
    def executar_query(self, query):
        pass

    @abstractmethod
    def fechar(self):
        pass