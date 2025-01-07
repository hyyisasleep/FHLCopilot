from datetime import datetime
from functools import cached_property as functools_cached_property

from module.base.decorator import cached_property
from module.config.utils import DEFAULT_TIME, deep_get, get_server_last_monday_update, get_server_last_update
from module.exception import ScriptError


def now():
    return datetime.now().replace(microsecond=0)


def iter_attribute(cls):
    """
    Args:
        cls: Class or object

    Yields:
        str, obj: Attribute name, attribute value
    """
    for attr in dir(cls):
        if attr.startswith('_'):
            continue
        value = getattr(cls, attr)
        if type(value).__name__ in ['function', 'property']:
            continue
        yield attr, value


class StoredBase:
    time = DEFAULT_TIME

    def __init__(self, key):
        self._key = key
        self._config = None

    @cached_property
    def _name(self):
        return self._key.split('.')[-1]

    def _bind(self, config):
        """
        Args:
            config (AzurLaneConfig):
        """
        self._config = config

    @functools_cached_property
    def _stored(self):
        assert self._config is not None, 'StoredBase._bind() must be called before getting stored data'
        from module.logger import logger

        out = {}
        stored = deep_get(self._config.data, keys=self._key, default={})
        for attr, default in self._attrs.items():
            value = stored.get(attr, default)
            if attr == 'time':
                if not isinstance(value, datetime):
                    try:
                        value = datetime.fromisoformat(value)
                    except ValueError:
                        logger.warning(f'{self._name} has invalid attr: {attr}={value}, use default={default}')
                        value = default
            else:
                if not isinstance(value, type(default)):
                    logger.warning(f'{self._name} has invalid attr: {attr}={value}, use default={default}')
                    value = default

            out[attr] = value
        return out

    @cached_property
    def _attrs(self) -> dict:
        """
        All attributes defined
        """
        attrs = {
            # time is the first one
            'time': DEFAULT_TIME
        }
        for attr, value in iter_attribute(self.__class__):
            if attr.islower():
                attrs[attr] = value
        return attrs

    def __setattr__(self, key, value):
        if key in self._attrs:
            stored = self._stored
            stored['time'] = now()
            stored[key] = value
            self._config.modified[self._key] = stored
            if self._config.auto_update:
                self._config.update()
        else:
            super().__setattr__(key, value)

    def __getattribute__(self, item):
        if not item.startswith('_') and item in self._attrs:
            return self._stored[item]
        else:
            return super().__getattribute__(item)

    def is_expired(self) -> bool:
        return False

    def show(self):
        """
        Log self
        """
        from module.logger import logger
        logger.attr(self._name, self._stored)


class StoredExpiredAt0600(StoredBase):
    def is_expired(self):
        from module.logger import logger
        self.show()
        expired = self.time < get_server_last_update('06:00')
        logger.attr(f'{self._name} expired', expired)
        return expired


class StoredExpiredAtMonday0600(StoredBase):
    def is_expired(self):
        from module.logger import logger
        self.show()
        expired = self.time < get_server_last_monday_update('06:00')
        logger.attr(f'{self._name} expired', expired)
        return expired


class StoredInt(StoredBase):
    value = 0

    def clear(self):
        self.value = 0


class StoredCounter(StoredBase):
    value = 0
    total = 0

    FIXED_TOTAL = 0

    def set(self, value, total=0):
        if self.FIXED_TOTAL:
            total = self.FIXED_TOTAL
        with self._config.multi_set():
            self.value = value
            self.total = total

    def clear(self):
        self.value = 0

    def clear_total(self):
        self.value = 0
        self.total = 0

    def to_counter(self) -> str:
        return f'{self.value}/{self.total}'

    def is_full(self) -> bool:
        return self.value >= self.total

    def get_remain(self) -> int:
        return self.total - self.value

    def add(self, value=1):
        self.value += value

    @cached_property
    def _attrs(self) -> dict:
        attrs = super()._attrs
        if self.FIXED_TOTAL:
            attrs['total'] = self.FIXED_TOTAL
        return attrs

    @functools_cached_property
    def _stored(self):
        stored = super()._stored
        if self.FIXED_TOTAL:
            stored['total'] = self.FIXED_TOTAL
        return stored

class StoredDailyLiveness(StoredCounter, StoredExpiredAt0600):
    FIXED_TOTAL = 100

class StoredGuildWeeklyLiveness(StoredCounter, StoredExpiredAtMonday0600):
    FIXED_TOTAL = 8000

class StoredMonthlyCard(StoredInt):
    value = 0
    def predict_current(self) -> int:
        """
        Predict current stamina from records
        """
        # Overflowed
        value = self.value
        if value <= 0:
            return value

        # Invalid time, record in the future
        record = self.time
        now = datetime.now()
        if record >= now:
            return value
        # Calculate
        # 月卡减去当前天数
        diff = int(now - record)
        value = max(value - diff,0)
        return value
    pass

class StoredMonthlyCard68(StoredMonthlyCard):
    pass

class StoredMonthlyCard30(StoredMonthlyCard):
    pass

class StoredBattlePassLevel(StoredCounter):
    FIXED_TOTAL = 60

# 体力
class StoredPower(StoredCounter):


    def predict_current(self) -> int:
        """
        Predict current stamina from records
        """
        # 修改上限，有月卡是250没有是150
        # if StoredMonthlyCard30.value > 0 or StoredMonthlyCard68.value > 0:
        #     self.FIXED_TOTAL = 250
        # else:
        #     self.FIXED_TOTAL = 150
        # Overflowed

        value = self.value
        if value >= self.total:
            return value
        # Invalid time, record in the future
        record = self.time
        now = datetime.now()
        if record >= now:
            return value
        # Calculate
        # ?
        # Recover 1 power each 6 minutes(?
        diff = (now - record).total_seconds()
        value += int(diff // 360)
        return value

# =============副本===============
class StoredDailyBaoXu(StoredCounter,StoredExpiredAt0600):
    pass

class StoredDailyJingYuan(StoredCounter,StoredExpiredAt0600):
    pass

class StoredDailyGuShiFengYun(StoredCounter,StoredExpiredAt0600):
    pass

class StoredDailyJinGe(StoredCounter,StoredExpiredAt0600):
    pass

# =============金戈===============
class StoredBuySuperCatBallWhenArriveRankNine(StoredCounter, StoredExpiredAtMonday0600):
    FIXED_TOTAL = 1

class StoredTalismanToClean(StoredInt):
    pass

class StoredTalisman(StoredInt):
    pass

class StoredJinGeLevel(StoredInt, StoredExpiredAtMonday0600):
    pass

#=============每日密令============
class StoredWeeklyPassword(StoredCounter, StoredExpiredAtMonday0600):
    # 自己新加的变量不要用全大写……
    p1 = ''
    p2 = ''
    p3 = ''
    p4 = ''
    p5 = ''
    p6 = ''
    p7 = ''

    FIXED_TOTAL = 7

    def write_daily_password(self, day, value):
        with self._config.multi_set():
            if day == 1:
                if self.p1 == '':
                    self.value += 1
                self.p1 = value
            elif day == 2:
                if self.p2 == '':
                    self.value += 1
                self.p2 = value
            elif day == 3:
                if self.p3 == '':
                    self.value += 1
                self.p3 = value
            elif day == 4:
                if self.p4 == '':
                    self.value += 1
                self.p4 = value
            elif day == 5:
                if self.p5 == '':
                    self.value += 1
                self.p5 = value
            elif day == 6:
                if self.p6 == '':
                    self.value += 1
                self.p6 = value
            elif day == 7:
                if self.p7 == '':
                    self.value += 1
                self.p7 = value

    def clear(self):
        with self._config.multi_set():
            self.p1 = ''
            self.p2 = ''
            self.p3 = ''
            self.p4 = ''
            self.p5 = ''
            self.p6 = ''
            self.p7 = ''
            self.value = 0

#=============雅社==============
class StoredDailyGuildMission(StoredCounter, StoredExpiredAt0600):
    mission1 = ''
    mission2 = ''
    mission3 = ''
    FIXED_TOTAL = 3


    def load_missions(self):
        """
        Returns:
            list[DailyMission]: Note that must check if quests are expired
        """
        # DailyQuest should be lazy loaded
        # from tasks.daily.keywords import DailyQuest
        missions = []
        for name in [self.mission1, self.mission2, self.mission3]:
            if not name:
                continue
            try:
                # quest = DailyQuest.find(name)
                missions.append(name)
            except ScriptError:
                pass
        return missions

    def write_missions(self, missions):
        """
        Args:
            missions (list[DailyMission, str]):
        """
        # from tasks.daily.keywords import DailyQuest
        missions = [m for m in missions]
        with self._config.multi_set():
            self.set(value=max(self.FIXED_TOTAL - len(missions), 0))
            try:
                self.mission1 = missions[0]
            except IndexError:
                self.mission1 = ''
            try:
                self.mission2 = missions[1]
            except IndexError:
                self.mission2 = ''
            try:
                self.mission3 = missions[2]
            except IndexError:
                self.mission3 = ''


    def clear(self):
        with self._config.multi_set():
            self.mission1 = ''
            self.mission2 = ''
            self.mission3 = ''

class StoredCosplaySendStatusTimes(StoredCounter, StoredExpiredAt0600):
    FIXED_TOTAL = 4
# class StoredResersed(StoredCounter):
#     FIXED_TOTAL = 2400
#
#
# class StoredImmersifier(StoredCounter):
#     FIXED_TOTAL = 8
#
#
# class StoredSimulatedUniverse(StoredCounter, StoredExpiredAtMonday0600):
#     pass
#
#
# class StoredSimulatedUniverseElite(StoredCounter, StoredExpiredAtMonday0600):
#     # These variables are used in Rogue Farming feature.
#
#     # FIXED_TOTAL --- Times of boss drop chance per week. In current version of StarRail, this value is 100.
#     FIXED_TOTAL = 100
#
#     # value --- Times left to farm. Resets to 100 every Monday 04:00, and decreases each time the elite boss is cleared.
#
#
# class StoredAssignment(StoredCounter):
#     pass
#
#
# class StoredDaily(StoredCounter, StoredExpiredAt0600):
#     quest1 = ''
#     quest2 = ''
#     quest3 = ''
#     quest4 = ''
#     quest5 = ''
#     quest6 = ''
#     quest7 = ''
#     quest8 = ''
#
#     FIXED_TOTAL = 8
#
#     def load_quests(self):
#         """
#         Returns:
#             list[DailyQuest]: Note that must check if quests are expired
#         """
#         # DailyQuest should be lazy loaded
#         from tasks.daily.keywords import DailyQuest
#         quests = []
#         for name in [self.quest1, self.quest2, self.quest3, self.quest4,
#                      self.quest5, self.quest6, self.quest7, self.quest8]:
#             if not name:
#                 continue
#             try:
#                 quest = DailyQuest.find(name)
#                 quests.append(quest)
#             except ScriptError:
#                 pass
#         return quests
#
#     def write_quests(self, quests):
#         """
#         Args:
#             quests (list[DailyQuest, str]):
#         """
#         from tasks.daily.keywords import DailyQuest
#         quests = [q.name if isinstance(q, DailyQuest) else q for q in quests]
#         with self._config.multi_set():
#             self.set(value=max(self.FIXED_TOTAL - len(quests), 0))
#             try:
#                 self.quest1 = quests[0]
#             except IndexError:
#                 self.quest1 = ''
#             try:
#                 self.quest2 = quests[1]
#             except IndexError:
#                 self.quest2 = ''
#             try:
#                 self.quest3 = quests[2]
#             except IndexError:
#                 self.quest3 = ''
#             try:
#                 self.quest4 = quests[3]
#             except IndexError:
#                 self.quest4 = ''
#             try:
#                 self.quest5 = quests[4]
#             except IndexError:
#                 self.quest5 = ''
#             try:
#                 self.quest6 = quests[5]
#             except IndexError:
#                 self.quest6 = ''
#             try:
#                 self.quest7 = quests[6]
#             except IndexError:
#                 self.quest7 = ''
#             try:
#                 self.quest8 = quests[7]
#             except IndexError:
#                 self.quest8 = ''
#
#     def clear(self):
#         with self._config.multi_set():
#             self.quest1 = ''
#             self.quest2 = ''
#             self.quest3 = ''
#             self.quest4 = ''
#             self.quest5 = ''
#             self.quest6 = ''
#             self.quest7 = ''
#             self.quest8 = ''
#
#
# class StoredDungeonDouble(StoredExpiredAt0600):
#     calyx = 0
#     relic = 0
#     rogue = 0
#
#

#
#

#
#
# class StoredBattlePassWeeklyQuest(StoredCounter, StoredExpiredAtMonday0600):
#     quest1 = ''
#     quest2 = ''
#     quest3 = ''
#     quest4 = ''
#     quest5 = ''
#     quest6 = ''
#     quest7 = ''
#
#     FIXED_TOTAL = 7
#
#     def load_quests(self):
#         """
#         Returns:
#             list[DailyQuest]: Note that must check if quests are expired
#         """
#         # BattlePassQuest should be lazy loaded
#         from tasks.battle_pass.keywords import BattlePassQuest
#         quests = []
#         for name in [self.quest1, self.quest2, self.quest3, self.quest4, self.quest5, self.quest6, self.quest7]:
#             if not name:
#                 continue
#             try:
#                 quest = BattlePassQuest.find(name)
#                 quests.append(quest)
#             except ScriptError:
#                 pass
#         return quests
#
#     def write_quests(self, quests):
#         """
#         Args:
#             quests (list[DailyQuest, str]):
#         """
#         from tasks.battle_pass.keywords import BattlePassQuest
#         quests = [q.name if isinstance(q, BattlePassQuest) else q for q in quests]
#         with self._config.multi_set():
#             self.set(value=max(self.FIXED_TOTAL - len(quests), 0))
#             try:
#                 self.quest1 = quests[0]
#             except IndexError:
#                 self.quest1 = ''
#             try:
#                 self.quest2 = quests[1]
#             except IndexError:
#                 self.quest2 = ''
#             try:
#                 self.quest3 = quests[2]
#             except IndexError:
#                 self.quest3 = ''
#             try:
#                 self.quest4 = quests[3]
#             except IndexError:
#                 self.quest4 = ''
#             try:
#                 self.quest5 = quests[4]
#             except IndexError:
#                 self.quest5 = ''
#             try:
#                 self.quest6 = quests[5]
#             except IndexError:
#                 self.quest6 = ''
#             try:
#                 self.quest7 = quests[6]
#             except IndexError:
#                 self.quest7 = ''
#
#     def clear(self):
#         with self._config.multi_set():
#             self.quest1 = ''
#             self.quest2 = ''
#             self.quest3 = ''
#             self.quest4 = ''
#             self.quest5 = ''
#             self.quest6 = ''
#             self.quest7 = ''
#
#
# class StoredBattlePassSimulatedUniverse(StoredCounter):
#     FIXED_TOTAL = 1
#
#
# class StoredBattlePassQuestCalyx(StoredCounter):
#     FIXED_TOTAL = 20
#
#
# class StoredBattlePassQuestEchoOfWar(StoredCounter):
#     FIXED_TOTAL = 2
#
#
# class StoredBattlePassQuestCredits(StoredCounter):
#     FIXED_TOTAL = 300000
#
#
# class StoredBattlePassQuestSynthesizeConsumables(StoredCounter):
#     FIXED_TOTAL = 10
#
#
# class StoredBattlePassQuestStagnantShadow(StoredCounter):
#     FIXED_TOTAL = 3
#
#
# class StoredBattlePassQuestCavernOfCorrosion(StoredCounter):
#     FIXED_TOTAL = 8
#
#
# class StoredBattlePassQuestTrailblazePower(StoredCounter):
#     # Dynamic total from 100 to 1400
#     LIST_TOTAL = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400]
#
#
# class StoredPlanner(StoredBase):
#     value: int
#     total: int
#     synthesize: int
#
#
# class StoredPlannerOverall(StoredBase):
#     value: str = '??%'
#     comment: str = '<??d'
