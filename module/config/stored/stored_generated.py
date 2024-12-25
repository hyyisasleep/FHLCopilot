from module.config.stored.classes import (
    StoredBase,
    StoredBuySuperCatBallWhenArriveRankNine,
    StoredCounter,
    StoredDailyLiveness,
    StoredExpiredAt0400,
    StoredExpiredAtMonday0400,
    StoredGuildWeeklyLiveness,
    StoredInt,
    StoredJinGeLevel,
    StoredMonthlyCard,
    StoredMonthlyCard30,
    StoredMonthlyCard68,
    StoredPower,
    StoredTalisman,
    StoredTalismanToClean,
    StoredWeeklyPassword,
)


# This file was auto-generated, do not modify it manually. To generate:
# ``` python -m module/config/config_updater.py ```

class StoredGenerated:
    DailyLiveness = StoredDailyLiveness("DailyQuest.DailyStorage.DailyLiveness")
    TalismanToClean = StoredTalismanToClean("ClearJinGeTalisman.JinGeStorage.TalismanToClean")
    JinGeLevel = StoredJinGeLevel("ClearJinGeTalisman.JinGeStorage.JinGeLevel")
    BuySuperCatBall = StoredBuySuperCatBallWhenArriveRankNine("ClearJinGeTalisman.JinGeStorage.BuySuperCatBall")
    OneWeekPasswordList = StoredWeeklyPassword("DailyPassword.DailyPassword.OneWeekPasswordList")
