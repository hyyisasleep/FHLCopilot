# FHLCopilot

忘川风华录 自动化日常脚本

基于[StarRailCopilot](https://github.com/LmeSzinc/StarRailCopilot/)/ [AzurLaneAutoScript](https://github.com/LmeSzinc/AzurLaneAutoScript)框架开发



![gui](doc/README.assets/gui_cn.png)


## 功能

达成每日100活跃度/金戈清符/每日签到密令

## 安装教程

[安装教程](https://github.com/hyyisasleep/FHLCopilot/wiki/Installation)


## 未来准备开发的功能

1.自动使用本周即将过期的八宝肉

2.商店自定义购买，支持购买每周道具

3.自动躲猫猫（找猫猫和凑天命对

4.做其他的雅社悬赏（抽卡1次，消耗100贡献，知交圈点赞等），领取每日奖励和周奖励

5.展示每周雅社活动（紫薇沙盘征星等

6.昌平文引OCR识别每日任务（但是不做

7.背包物品检测，自动开羁绊礼盒



## 已知bug

活动签到弹窗处理不好，要么不签要么认不出来还把每日签到都跳过了

cdn用不了，直接gitee拉取了

每日签到密令，微信在后台的时候脚本找不到

金戈界面识别待清枕戈符数不会等动画放完再进行识别

（放在这意思是我知道有bug但是暂时解决不了

## 开发
qq群：1015311150

欢迎通过 issue 或者 QQ 群给作者提建议和改bug

## 其他问题

### ===================账号/安装相关==================


### 用了会被封号吗
FHLC的运行基于图像识别，就像你平时打游戏一样看到某个图标出现了才会去点，不涉及任何游戏本体代码数据的修改。

不过还是那句老话用别怕怕别用

### 一定要用模拟器吗
是的。

但是作者只在windows系统和MUMU模拟器12测试过，其他模拟器支持和折腾方法请参考[Alas设备支持文档](https://github.com/LmeSzinc/AzurLaneAutoScript/wiki/Emulator_cn)

### 我的号在渠道服怎么办
作者只玩过官服所以也不知道怎么办。

如果你在模拟器上装过渠道服且运行不了FHLC的话欢迎加q群给作者提供案例。

### 我想清多个账号的日常
目前没写切换账号，需要手动增加一个配置文件，在游戏里切换账号后【关闭游戏】然后在新配置中开启调度器，让调度器自己运行。


### ===================脚本内容相关==================

### 100活跃度怎么算的

由于忘川活跃任务太杂懒得做识别了，所以假设你是每天新登录。

调度器启动后FHLC会帮你做下面的工作：

> 桃源居领午晚饭体力，处理事件，随机制作家具，(非必需：百工图转换、拜访他人领君子兰)
>
> 雅社免费签到，放河灯（默认放第一个名士的碎片）
> 
> 喵居吸猫、一键喂猫
> 
> 忘川速办领供台、虾球奖励，给互动页第一个名士送礼领2碎片，好友界面送友情点
> 
> 一键收取邮箱未领取奖励，知交圈点赞3次、在世界频道发言2次
>

正常点点点完上面这些能得到65活跃度。

（但是不排除一些极端情况，比如你好友不足5个拿不满友情点活跃度，再比如FHLC今天抽风了有的功能没点上

接下来FHLC会去每日任务界面读一下目前的活跃度，不足100的部分会列一个刷本计划补满。

>目前刷本会忽略`即将过期的加成`和`猫车`。
> 
>另外虽然对刷本翻车做了一定的处理但不保证完美，请保证你的队伍练度能稳过所有宝墟12层和镜渊9层。


忘川设置每天4次宝墟、1次镜渊、3次故世、3次金戈都可以补活跃度，一场10点。

但是故世风云要单独切章，每章关卡位置还不一样，我不想挨个截图匹配了所以就没写。

目前只用宝墟和镜渊（可选项金戈）补满活跃度，优先度雅社悬赏 > 宝墟 > 镜渊。

**举个例子**：如果当前活跃度是65，还差35点补满，FHLC会帮你规划打4次宝墟；如果当前活跃度是59，还差41点补满，FHLC会帮你规划打4次宝墟+1次镜渊；

如果今天的雅社悬赏要求打2次宝墟2次镜渊，差35活跃度的情况下FHLC会帮你规划打3次宝墟2次镜渊。

（但是雅社悬赏内容靠OCR，偶尔会抽风认不出来什么任务，欢迎反馈错误识别结果给作者修复）

另外如果你开启了`将金戈3次加入补活跃度方案`选项，且当前金戈段位小于六段，差35活跃度的情况下FHLC会帮你规划打3次金戈+1次宝墟。

但如果你的段位≥六段，只有在11-13点和19-21点之间运行`每日任务`FHLC才会帮你规划打3次金戈+1次宝墟，其他时间还是4次宝墟。

>金戈不是开到14点吗最后一个小时怎么就不打了：防止金戈次数刷到一半时间过了
>
> 六段怎么也限时：防止打着打着上七段限时了



计划刷满后会跳转到每日任务界面再领一次活跃奖励，正常情况是能拿到100活跃度奖励的。

当然实际执行情况下可能遇到各种不正常刷不满活跃的情况，如果你认为是程序的bug欢迎带着完整log来找作者反馈。

### 关于金戈清符

字面意义上的清符，FHLC帮你匹配进战点自动战斗等结束，不管胜负，如果对金戈胜率有追求不要用。

加了过一次金戈时间后等待下次金戈开放再自动接着打的功能，但还没等到测试机会，欢迎反馈。

### 昌平文引每日任务怎么不做

太麻烦了还涉及到消耗敏感资源，洗猫猫词条给名士升级还有千锤百炼这种还是自己手动吧。

~~ch能不能学学隔壁崩铁减负啊~~


### 每日密令功能为什么需要手动启动
微信签到部分会抢鼠标，你也不想挂机忙正事的时候电脑上突然弹出个微信窗口吧。

另外微信签到脚本是pywinauto写的（通过windows系统的UI路径找按键），完全没继承src的优秀状态循环，很脆弱

还有官方公众号偶尔也会不往签到消息里放密令，脚本目前做不到从公众号文章里找密令。

综上所述失败率很高，放进调度器只会徒增血压，欢迎帮笨比作者优化这部分（悲）

### 图标用怀英喵有什么说法吗

没有，夹带私货






