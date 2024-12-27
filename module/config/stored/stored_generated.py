from module.config.stored.classes import (
    StoredBase,
    StoredBuySuperCatBallWhenArriveRankNine,
    StoredCounter,
    StoredDailyBaoXu,
    StoredDailyGuShiFengYun,
    StoredDailyGuildMission,
    StoredDailyJinGe,
    StoredDailyJingYuan,
    StoredDailyLiveness,
    StoredExpiredAt0600,
    StoredExpiredAtMonday0600,
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
    DailyBaoXuPlan = StoredDailyBaoXu("DailyQuest.Dungeon.DailyBaoXuPlan")
    DailyJingYuanPlan = StoredDailyBaoXu("DailyQuest.Dungeon.DailyJingYuanPlan")
    DailyGuShiFengYunPlan = StoredDailyBaoXu("DailyQuest.Dungeon.DailyGuShiFengYunPlan")
    DailyJinGePlan = StoredDailyBaoXu("DailyQuest.Dungeon.DailyJinGePlan")
    DailyGuildMission = StoredDailyGuildMission("Guild.GuildMission.DailyGuildMission")
    MonthlyCard30 = StoredInt("Shop.MonthlyCard.MonthlyCard30")
    MonthlyCard68 = StoredInt("Shop.MonthlyCard.MonthlyCard68")
    TalismanToClean = StoredTalismanToClean("ClearJinGeTalisman.JinGeStorage.TalismanToClean")
    JinGeLevel = StoredJinGeLevel("ClearJinGeTalisman.JinGeStorage.JinGeLevel")
    BuySuperCatBall = StoredBuySuperCatBallWhenArriveRankNine("ClearJinGeTalisman.JinGeStorage.BuySuperCatBall")
    OneWeekPasswordList = StoredWeeklyPassword("DailyPassword.DailyPassword.OneWeekPasswordList")
