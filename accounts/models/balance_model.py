from dataclasses import dataclass


@dataclass
class BalanceModel():
    """
    Класс описания таблицы расчета балансов
    """
    """Диспетчерский номер ТП"""
    Dtp: str
    """Населенный пункт"""
    Locality: str
    """Наименование точки учета"""
    NameOfAccountingPoint: str
    """S тр-ра, кВА"""
    STrRa: int
    """Pхх"""
    Pxx: float
    """Потери ХХ за период, кВт*ч"""
    LossXX: float
    """Ktt"""
    Ktt: int
    """Зав.№ счетчика"""
    HeadOfCounter: int
    """Начало периода"""
    StartPeriod: float
    """Конец периода"""
    EndPeriod: float
    """Расход за период"""
    ConsumptionPeriod: float

    def __init__(self, id_tu, dtp, locality, nameofaccountingpoint, strra, pxx, lossxx, ktt, headofcounter,
                 startperiod, endperiod, consumptionperiod, time_start_write):
        self.Id_tu = id_tu
        self.Dtp = dtp
        self.Locality = locality
        self.NameOfAccountingPoint = nameofaccountingpoint
        self.STrRa = strra
        self.Pxx = pxx
        self.LossXX = lossxx
        self.Ktt = ktt
        self.HeadOfCounter = headofcounter
        self.StartPeriod = startperiod
        self.EndPeriod = endperiod
        self.ConsumptionPeriod = consumptionperiod
        self.Time_Start_Write = time_start_write

    def __repr__(self):
        return 'Id_tu:{}, Dtp:{}, Locality:{}, NameOfAccountingPoint:{}, STrRa:{}, Pxx:{}, LossXX:{}, Ktt:{},' \
               'HeadOfCounter:{}, StartPeriod:{}, EndPeriod:{}, ConsumptionPeriod:{}, Time_Start_Write:{} ' \
            .format(self.Id_tu, self.Dtp, self.Locality, self.NameOfAccountingPoint, self.STrRa, self.Pxx, self.LossXX,
                    self.Ktt, self.HeadOfCounter, self.StartPeriod, self.EndPeriod, self.ConsumptionPeriod,
                    self.Time_Start_Write)
