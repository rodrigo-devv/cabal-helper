from source.logger import logger

_attack = False
_resumeAttack = False
_windows = []

# Function observer that will be called when the property attack is changed


def attack_observer():
    if _attack:
        logger("⚔️ Ataque ativado")
    else:
        logger("⚔️ Ataque pausado")


class Config:
    @property
    def attack(self):
        return _attack

    @attack.setter
    def attack(self, value):
        global _attack
        _attack = value
        # Call the observer function whenever the attack property is changed
        attack_observer()

    @property
    def resumeAttack(self):
        return _resumeAttack

    @resumeAttack.setter
    def resumeAttack(self, value):
        global _resumeAttack
        _resumeAttack = value
        # Call the observer function whenever the attack property is changed

    @property
    def windows(self):
        return _windows

    @windows.setter
    def windows(self, value):
        global _windows
        _windows = value


class CountdownConfig:
    hours = 0
    minutes = 0
    seconds = 0

    @classmethod
    def set_countdown(cls, h, m, s):
        cls.hours = h
        cls.minutes = m
        cls.seconds = s

    @classmethod
    def get_countdown(cls):
        return cls.hours, cls.minutes, cls.seconds


config = Config()
