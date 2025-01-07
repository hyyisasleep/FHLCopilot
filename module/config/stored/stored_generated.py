from module.config.stored.classes import (
    StoredBase,
    StoredBattlePassLevel,
    StoredBuySuperCatBallWhenArriveRankNine,
    StoredCosplaySendStatusTimes,
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
    DailyBaoXuPlan = StoredDailyBaoXu("Dungeon.Dungeon.DailyBaoXuPlan")
    DailyJingYuanPlan = StoredDailyBaoXu("Dungeon.Dungeon.DailyJingYuanPlan")
    DailyGuShiFengYunPlan = StoredDailyBaoXu("Dungeon.Dungeon.DailyGuShiFengYunPlan")
    DailyJinGePlan = StoredDailyBaoXu("Dungeon.Dungeon.DailyJinGePlan")
    DailyGuildMission = StoredDailyGuildMission("Guild.GuildMission.DailyGuildMission")
    SendStatusTimes = StoredCosplaySendStatusTimes("Guild.Cosplay.SendStatusTimes")
    MonthlyCard30 = StoredInt("Shop.MonthlyCard.MonthlyCard30")
    MonthlyCard68 = StoredInt("Shop.MonthlyCard.MonthlyCard68")
    BattlePassLevel = StoredBattlePassLevel("BattlePass.BattlePassStorage.BattlePassLevel")
    Copper = StoredInt("DataUpdate.ItemStorage.Copper")
    TongBao = StoredInt("DataUpdate.ItemStorage.TongBao")
    Power = StoredPower("DataUpdate.ItemStorage.Power")
    TalismanToClean = StoredTalismanToClean("ClearJinGeTalisman.JinGeStorage.TalismanToClean")
    JinGeLevel = StoredJinGeLevel("ClearJinGeTalisman.JinGeStorage.JinGeLevel")
    BuySuperCatBall = StoredBuySuperCatBallWhenArriveRankNine("ClearJinGeTalisman.JinGeStorage.BuySuperCatBall")
    OneWeekPasswordList = StoredWeeklyPassword("DailyPassword.DailyPassword.OneWeekPasswordList")
