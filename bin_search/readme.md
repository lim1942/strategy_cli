# 一 变量说明：
一个订单申请时，会携带很多变量维度，风控人员主要关注这些变量维度，来评估用户的风险。策略评估的变量分析只分析符合命名规范的变量列。其他列当业务字段处理。

# 二 变量节点
- credit节点，授信节点变量，评估用户的可借产品数，可借额度，还款周期等。取数函数指定var_type='creidt'即可取到
- verify节点，批核节点变量，评估订单可否通过。取数函数指定var_type='verify'即可取到。

# 三.变量数据类型
1. 离散数值型：比如年龄，收入，资产金额等
2. 连续数值型：比如月收入，资产负债比等，模型分
3. 离散分类型：比如性别，是否有车，是否有房等.campaign等

# 四.变量类型和命名规范
1. 基础信息：base*** 
2. 业务：biz*** 
3. 全平台: all*** 
4. 设备：dev*** 
5. 通讯录：con***
6. 短信变量：sms***
7. app：app***
8. 通话记录：call***
9. acq: acq***
10. 模型分:model***
### 三方变量
1. advance： adv**
2. izi：izi***  
3. 同盾: td***
4. tyla：tyla***
5. 探知：tz***
6. 云盾：cloudun***
7. aws：aws***
8. pal：pal***
9. nian(刘念)：nian***
10. est(刘念)：est***
11. URisk(锋远)：URisk***
12. 冰鉴：bingjian***
13. tBei（天贝）：tBei***
14. oneApi： oneApi***
15. 豆包api：doubao***
16. 阿里云API：aly***
17. 贝融黑名单：br***
18. fp黑名单：fp***
19. ben黑名单：Ben***
20. MobileWella：Mob***
21. 尖兵：pen***
22. DynaAi：Dyna***
23. operator：operator***
24. SURFIN：        Sur***
25. 飞盾：fd***
26. 数森：ss***
