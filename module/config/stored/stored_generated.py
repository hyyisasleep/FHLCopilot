from module.config.stored.classes import (
    StoredAutoDailyPassword,
    StoredBase,
    StoredBattlePassLevel,
    StoredBuySuperCatBallWhenArriveRankNine,
    StoredCatteryFeedCat,
    StoredCatteryPlayWithCat,
    StoredCelebrityInteract,
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
    StoredGetFriendshipPoint,
    StoredGuildSignIn,
    StoredGuildWeeklyLiveness,
    StoredInt,
    StoredJinGeDailyWinReward,
    StoredJinGeLevel,
    StoredMonthlyCard,
    StoredMonthlyCard30,
    StoredMonthlyCard68,
    StoredOfficeAffair,
    StoredOfficeBuildFurniture,
    StoredPower,
    StoredTalisman,
    StoredTalismanToClean,
    StoredWeeklyPassword,
)


# This file was auto-generated, do not modify it manually. To generate:
# ``` python -m module/config/config_updater.py ```

class StoredGenerated:
    DailyLiveness = StoredDailyLiveness("DailyQuest.DailyStorage.DailyLiveness")
    JinGeDailyWinReward = StoredJinGeDailyWinReward("DailyQuest.DailyStorage.JinGeDailyWinReward")
    CelebrityInteract = StoredCelebrityInteract("DailyQuest.DailyStorage.CelebrityInteract")
    GuildSignIn = StoredGuildSignIn("DailyQuest.DailyStorage.GuildSignIn")
    OfficeAffair = StoredOfficeAffair("DailyQuest.DailyStorage.OfficeAffair")
    OfficeBuildFurniture = StoredOfficeBuildFurniture("DailyQuest.DailyStorage.OfficeBuildFurniture")
    CatteryPlayWithCat = StoredCatteryPlayWithCat("DailyQuest.DailyStorage.CatteryPlayWithCat")
    CatteryFeedCat = StoredCatteryFeedCat("DailyQuest.DailyStorage.CatteryFeedCat")
    GetFriendshipPoint = StoredGetFriendshipPoint("DailyQuest.DailyStorage.GetFriendshipPoint")
    DailyBaoXuPlan = StoredDailyBaoXu("Dungeon.Dungeon.DailyBaoXuPlan")
    DailyJingYuanPlan = StoredDailyJingYuan("Dungeon.Dungeon.DailyJingYuanPlan")
    DailyGuShiFengYunPlan = StoredDailyBaoXu("Dungeon.Dungeon.DailyGuShiFengYunPlan")
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
