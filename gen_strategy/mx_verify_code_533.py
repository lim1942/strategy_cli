def DZ3003_B12(row):
    # 竞品app安装限制
    if row['app140InstallAutoJingpinAIAppNum7d']>26:
        return 'REJECT'
    return 'PASS'

def DZ3004_B12(row):
    if row['sms057WhiteOverdue7d']>25:
        return 'REJECT'
    return 'PASS'

def DZ6002_B12(row):
    '''
    历史最大逾期天数
    '''
    if (row['biz009MaxOverdueDays'] >= 7 or row['all002MaxOverdueDays'] >= 7):
        return 'REJECT'
    elif (row['biz009MaxOverdueDays'] > 0 or row['all002MaxOverdueDays'] > 0) and row['model135BcardV57longtrain'] <=510 and row['biz037AppId']!="sst001_NBR-640" and row['biz209RegistDate']>="2025-09-01":
        return 'REJECT'
    elif (row['biz009MaxOverdueDays'] > 0 or row['all002MaxOverdueDays'] > 0) and row['model135BcardV57longtrain'] <=500 and row['biz209RegistDate']>="2025-09-01":
        return 'REJECT'
    return 'PASS'

def DZ6010_B12(row):
    if row['biz185OldCreditRank'] >=5 and row['all093OrderLoanTimes5d']>7:
        return 'REJECT'
    else:
        return 'PASS' 
    
def DZ6011_B12(row):
    if row['all100AllappNotLimitRefuseBatchCnt'] > 6 and row['biz037AppId'] == "sst001_NBR-010":
        return 'REJECT'
    return 'PASS' 


def DZ7018_B12(row):
    if row['all068OrderLoanNowTimesAll'] > 24:
        return 'REJECT'
    elif row['all068OrderLoanNowTimesAll'] > 12 and row['model092MxBcardCreditScoreV18'] <= 495 and row['biz037AppId'] != "sst001_NBR-010":
        return 'REJECT' 
    elif row['all068OrderLoanNowTimesAll'] > 8 and row['model092MxBcardCreditScoreV18'] <= 490 and row['biz037AppId'] != "sst001_NBR-010":
        return 'REJECT' 
    elif row['all068OrderLoanNowTimesAll'] > 5 and row['model225MxBcardCreditScoreV141'] <= 485:
        return 'REJECT' 
    elif row['all068OrderLoanNowTimesAll'] > 7 and row['biz185OldCreditRank'] > 3 and row['biz037AppId'] == "sst001_NBR-010" and row['biz502Random2']<=5000:
        return 'REJECT' 
    else:
        return 'PASS'

def DZ7023_B12(row):
    if row['biz041IsProductReloan']==0 and row['biz113CurrentOTNloaningNum'] > 6:
        return 'REJECT'
    elif row['biz037AppId']=="sst001_NBR-009" and row['biz186FirstGetCreditTime'] < "2025-07-02 02:51:18" and row['model135BcardV57longtrain']<=505 and row['biz041IsProductReloan']==0 and row['biz113CurrentOTNloaningNum']>0:
        return 'REJECT'
    elif row['model092MxBcardCreditScoreV18Rank']==5 and row['biz041IsProductReloan']==0:
        if row['biz037AppId']!="sst001_NBR-640" and row['biz186FirstGetCreditTime'] < "2025-07-02 02:51:18":
            return 'REJECT'
        elif row['biz037AppId']=="sst001_NBR-640" and row['biz186FirstGetCreditTime'] < "2025-05-28 21:53:27":
            return 'REJECT'
    return 'PASS'

def DZ7031_B12(row):
    if row['model092MxBcardCreditScoreV18']<=470:
        return 'REJECT'
    elif row['model092MxBcardCreditScoreV18']<=485 and row['biz039TransBatchCnt'] <= 12 and row['biz502Random2']<=5000:
        return 'REJECT'
    return 'PASS'

def DZ7033_B12(row):
    if row['model135BcardV57shortall']<=490  and row['biz502Random2']<=5000 and row['biz037AppId'] != "sst001_NBR-010":
        return 'REJECT'
    return 'PASS'

def DZ7035_B12(row):
    if row['model171MxBcardV88Low']<=525 and row['model225MxBcardCreditScoreV141']<=525:
        return 'REJECT'
    elif row['model171MxBcardV88Low']<=525 and row['biz037AppId'] == "sst001_NBR-010":
        return 'REJECT'
    return 'PASS'

def DZ7036_B12(row):
    if row['model230MxBcardV146']<=515 and row['biz037AppId'] != "sst001_NBR-010":
        return 'REJECT'
    return 'PASS'


def DZ7037_B12(row):
    if row['biz037AppId'] == "sst001_NBR-010" and row['biz185OldCreditRank']>=5 and row['biz502Random2']<=7000:
        return 'REJECT'
    return 'PASS'

def DZ5001_B12(row):
    if row['biz037AppId'] == "sst001_NBR-010" and (row['biz103RepayMoneyTotal'] < float(row['biz042NewBeginAmount'])) and row['biz041IsProductReloan']==0 and row['biz502Random2']<=5000:
        return 'REJECT'
    elif row['biz037AppId'] == "sst001_NBR-009-2" and row['biz186FirstGetCreditTime'] >= "2026-04-13" and (row['biz103RepayMoneyTotal'] < float(row['biz042NewBeginAmount'])) and row['biz041IsProductReloan']==0:
        return 'REJECT'
    return 'PASS'


# -----------------B12结束


# -----------------B13开始
def DZ3003_B13(row):
    # 竞品app安装限制
    if row['app039InstalljingpinCombineNum']> 30:
        return 'REJECT'
    elif row['app108InstallAutoCumJingpinAppNum7d']> 19:
        return 'REJECT'      
    return 'PASS'



def DZ6002_B13(row):
    '''
    历史最大逾期天数
    '''
    if (row['biz009MaxOverdueDays'] >= 7 or row['all002MaxOverdueDays'] >= 7):
        return 'REJECT'

    elif (row['biz009MaxOverdueDays'] > 3 or row['all002MaxOverdueDays'] > 3) and row['biz209RegistDate']>="2025-06-01":
        return 'REJECT'
    return 'PASS'

def DZ6003_B13(row):
    '''
    历史最大逾期天数
    '''
    if row['all007AllSystemBlacklist'] == 1:
        return 'REJECT'
    return 'PASS'


def DZ5001_B13(row):
    '''
    历史最大逾期天数
    '''
    if (row['biz103RepayMoneyTotal'] < row['biz042NewBeginAmount']) and row['biz041IsProductReloan']==0:
        return 'REJECT'
    return 'PASS'

def DZ7007_B13(row):
    # 竞品app安装限制
    if row['model019Bcardv3oldtonew'] <= 460:
        return 'REJECT'
    else:
        return 'PASS'


def DZ7018_B13(row):
    '''
    '''
    if row['all068OrderLoanNowTimesAll'] > 17:
        return 'REJECT'
    else:
        return 'PASS'

def DZ7023_B13(row):
    if row['biz041IsProductReloan']==0 and row['biz113CurrentOTNloaningNum'] > 5:
        return 'REJECT'
    return 'PASS'

def DZ7030_B13(row):
    if row['model074BcardV17']<=460:
        return 'REJECT'
    return 'PASS'

def DZ7031_B13(row):
    if row['model092MxBcardCreditScoreV18']<=480:
        return 'REJECT'
    return 'PASS'

# -----------------B13结束

# C02
def DD1001_C02(row):
    if row['base001Age'] > 75 or row['base001Age'] < 18:
        return 'REJECT'
    elif row['biz037AppId'] == "sst001_NBR-009":
        return 'REJECT'
    return 'PASS'

def DD6003_C02(row):
    if row['all007AllSystemBlacklist']==1 and row['biz503Random3']<=7000 and row['all055PrivateBlackSource'] != "42":
        return 'REJECT'
    else:
        return 'PASS'
def DD3007_C02(row):
    if row['biz057OSTypeIsIOS']==0 and row['app040InstalljingpinCombineNum7d']>20:
        return 'REJECT'
    return 'PASS'
# def DD3008_C02(row):
#     if (row['app041InstalljingpinCombineNum14d']>5  and row['biz503Random3']<=5000) or row['app041InstalljingpinCombineNum14d']>10:
#         return 'REJECT'
#     return 'PASS'
# def DD7017_C02(row):
#     if (row['model048P35Acardv9']<=520 and row['base030appCode']=="7fb773d7241846b1ff429f196499c8dd"):
#         return 'REJECT'
#     return 'PASS'
# def DD7018_C02(row):
#     if row['model063Acardv16']<=540  and row['biz503Random3']<=7000:
#         return 'REJECT'
#     return 'PASS'
def DD7019_C02(row):
    if row['biz057OSTypeIsIOS']==0 and row['model083MxAcardV23']<=525:
        return 'REJECT'
    return 'PASS'
def DD7020_C02(row):
    if row['biz057OSTypeIsIOS']==0 and row['model162MxAcardV81Stack']<=520:
        return 'REJECT'
    return 'PASS'
def DD7021_C02(row):
    if row['biz057OSTypeIsIOS']==1 and row['model178MXAcardV94IosH5']<=495:
        return 'REJECT'
    return 'PASS'


# ----C02结束

# A09
def DD1001_A09(row):
    if row['base001Age'] > 75 or (row['biz096IsAllappExcellentUser']== 0 and row['base001Age'] < 21) or (row['biz096IsAllappExcellentUser']==1 and row['base001Age'] < 18):
        return 'REJECT'
    elif row['biz037AppId']=="sst001_NBR-009" or row['biz037AppId']=="sst001_NBR-003":
        return 'REJECT'
    return 'PASS'

def DD1008_A09(row):
    if row['base022IsOverdueHalfYear']==1:
        return 'REJECT'
    return 'PASS'

def DD1009_A09(row):
    # if row['biz037AppId']=="sst001_NBR-640" and row['all045SamePhoneRegister']>1:
    #     return 'REJECT'
    return 'PASS'

def DD3007_A09(row):
    if row['app040InstalljingpinCombineNum7d']>20:
        return 'REJECT'
    elif row['biz037AppId']=="sst001_NBR-009" and (row['app147InstallAutoCumJingpinAIAppNum']>25 or row['app147InstallAutoCumJingpinAIAppNum']<=1) and row['biz503Random3']<=5000:
        return 'REJECT'
    # elif row['biz037AppId']=="sst001_NBR-640" and row['model145MxAcardV65Stack']<=560 and row['app126JpInstallNum7d']<=0:
    #     return 'REJECT'
    return 'PASS'

def DD4001_A09(row):
    if row['sms057WhiteOverdue1d']>5 and row['biz037AppId']=="sst001_NBR-009":
        return 'REJECT'
    return 'PASS'

def DD4002_A09(row):
    # if row['sms056WhiteMarketing1d']>20 and row['biz037AppId']=="sst001_NBR-640":
    #     return 'REJECT'
    return 'PASS'

def DD6003_A09(row):
    if row['all007AllSystemBlacklist']==1 and row['biz503Random3']<=7000 and row['all055PrivateBlackSource'] != "42":
        return 'REJECT'
    if row['biz037AppId']=="sst001_NBR-640" and row['all007AllSystemBlacklist']==1 and row['all055PrivateBlackSource'] != "42":
        return 'REJECT'
    else:
        return 'PASS'

def DD6006_A09(row):
    # MX004差异化收紧
    if row['biz037AppId'] == 'sst001_NBR-640':
        if row['biz224Last0dNotLimitRefuseBatchCnt'] > 0 or row['biz224Last30dNotLimitRefuseBatchCnt'] > 2 or row['all100AllappNotLimitRefuseBatchCnt']>6:
            return 'REJECT'

    if row['biz037AppId'] == 'sst001_NBR-009':
        if row['biz224Last0dNotLimitRefuseBatchCnt'] > 0 or (row['biz224Last30dNotLimitRefuseBatchCnt'] > 5):
            return 'REJECT'
    return 'PASS'

def DD7017_A09(row):
    # 收紧
    if row['model048P35Acardv9']<=485:
        return 'REJECT'
    # elif row['model048P35Acardv9']<=485 and row['biz503Random3']<=8000:
    #     return 'REJECT'
    return 'PASS'

def DD7018_A09(row):
    # 收紧
    if row['model063Acardv16']<=520: 
        return 'REJECT'
    elif row['model063Acardv16']<=530 and row['biz503Random3']<=8000: 
        return 'REJECT'
    return 'PASS'


def DD7022_A09(row):
    if row['model136MxAcardV58P0089']<=515 and row['biz037AppId']=="sst001_NBR-640":
        return 'REJECT'
    return 'PASS'

def DD7023_A09(row):
    # if row['model123MxAcardV47'] <= 515 and row['biz037AppId']=="sst001_NBR-008" and row['biz503Random3']<=5000:
    #     return 'REJECT'
    return 'PASS'

def DD7026_A09(row):
    if row['model145MxAcardV65Stack'] <= 525 and row['biz037AppId']=="sst001_NBR-009":
        return 'REJECT'
    elif row['model145MxAcardV65Stack'] <= 520 and row['biz037AppId']=="sst001_NBR-640":
        return 'REJECT'
    return 'PASS'

def DD7027_A09(row):
    if row['model162MxAcardV81Stack'] <= 510:
        return 'REJECT'
    elif row['model162MxAcardV81Stack'] <= 520 and row['biz503Random3'] <= 8000: 
        return 'REJECT'
    return 'PASS'

def DD7028_A09(row):
    if row['model083MxAcardV23']<=515: 
        return 'REJECT'
    return 'PASS'

def DD7029_A09(row):
    if row['model195MxAcardV111']<=510 and row['biz176MediaSource']=='google' and row['biz503Random3']<=8000 : 
        return 'REJECT'
    return 'PASS'


# def DD8018_A09(row):
#     return 'PASS'



# --A09结束
# #######################################
# ###A12

def DD1008_A12(row):
    if row['base022IsOverdueHalfYear'] == 1 and row['model195MxAcardV111'] <= 510:
        return 'REJECT'
    elif row['biz038SurveyIsAllPerfect'] == 1 and row['model195MxAcardV111'] <= 500:
        return 'REJECT'
    return 'PASS'

def DD1001_A12(row):
    if row['base001Age'] > 75 or (row['biz096IsAllappExcellentUser']== 0 and row['base001Age'] < 21) or (row['biz096IsAllappExcellentUser']==1 and row['base001Age'] < 18):
        return 'REJECT'
    return 'PASS'

def DD3007_A12(row): 
    return 'PASS'

def DD6006_A12(row):
    if row['biz224Last0dNotLimitRefuseBatchCnt'] > 0 or row['biz224Last30dNotLimitRefuseBatchCnt'] > 1:
        return 'REJECT'
    elif row['all100AllappNotLimitRefuseBatchCnt'] >4:
        return 'REJECT'
    return 'PASS'

# def DD6009_A12(row):
#     if row['biz053MediaSource'] =="" and row['biz037AppId']=="sst001_NBR-010":
#         return 'REJECT'
#     elif row['model195MxAcardV111']<=510 and row['biz053MediaSource']=="Organic" and row['biz037AppId']=="sst001_NBR-010":
#         return 'REJECT'
#     return 'PASS'

def DD7017_A12(row):
    if row['model048P35Acardv9'] <=490 and row['model271MxAcardV188Value60dSample']<=540:
        return 'REJECT'
    elif row['model048P35Acardv9'] <=495 and row['biz053MediaSource']!="Facebook Ads" and row['biz037AppId']=="sst001_NBR-012":
        return 'REJECT'
    return 'PASS'


def DD7026_A12(row):  
    # if row['model148MxAcardRankV3'] >=6:
    #     return 'REJECT'
    # elif row['model145MxAcardV65Stack'] <=535 and row['biz053MediaSource']!="Facebook Ads" and row['biz037AppId']=="sst001_NBR-012":
    #     return 'REJECT'
    return 'PASS'


def DD7027_A12(row):
    if row['model162MxAcardV81Stack'] <= 515:
        return 'REJECT'
    return 'PASS'

def DD7032_A12(row):
    if row['model255MxAcardV171Refuse']<=510:
        return 'REJECT'
    elif row['model255MxAcardV171Refuse']<=530 and row['model089acardv27MX30'] <=525 and row['biz037AppId']!="sst001_NBR-012":
        return 'REJECT'
    return 'PASS'

def DD7033_A12(row):
    if row['model270MxAcardV187']<=510 and row['biz503Random3']<=8000 and row['biz037AppId']=="sst001_NBR-012":
        return 'REJECT'
    return 'PASS'

def DD8020_A12(row):
    # if row['biz037AppId']=="sst001_NBR-008" and 0<row['bj004PostLoanV2']<=450:
    #     return 'REJECT'
    return 'PASS'

##
# ###A13
def DD1001_A13(row):
    if row['base001Age'] > 75 or (row['biz096IsAllappExcellentUser']== 0 and row['base001Age'] < 21) or (row['biz096IsAllappExcellentUser']==1 and row['base001Age'] < 18):
        return 'REJECT'
    return 'PASS'

def DD1008_A13(row):
    if  row['biz038SurveyIsAllPerfect'] == 1 and row['model063Acardv16'] <= 540:
        return 'REJECT'
    return 'PASS'

def DD6003_A13(row):
    if row['all007AllSystemBlacklist']==1 and row['all055PrivateBlackSource'] != "42":
        return 'REJECT'
    return 'PASS'

def DD6006_A13(row):
    if row['biz223NotLimitRefuseBatchCnt'] > 1:
        return 'REJECT'
    return 'PASS'

def DD6007_A13(row):
    if row['all067LoanNowPlatformCnt']>0:
        return 'REJECT'
    return 'PASS'


def DD7014_A13(row):
    if row['model039Acardv6all']<=485 or (row['model039Acardv6all']<=490 and  row['biz503Random3']<=8000 ):
        return 'REJECT'
    return 'PASS'

def DD7015_A13(row):
    # if row['model027Fcardv2all'] <= 535:
    #     return 'REJECT'
    return 'PASS'


def DD7017_A13(row):
    if row['model048P35Acardv9']<=495 or (row['model048P35Acardv9']<=500 and row['biz503Random3']<=8000):
        return 'REJECT'
    return 'PASS'


def DD7019_A13(row):
    if row['model083MxAcardV23'] <= 520:
        return 'REJECT'
    return 'PASS'

# ###A14

def DD1014_A14(row):
    if row['all067LoanNowPlatformCnt'] > 0 and row['all089MailLoanOnlineNumSeq'] == 0:
        return 'REJECT'
    return 'PASS'

def DD1015_A14(row):
    if row['all067LoanNowPlatformCnt'] < 0 and row['all088SameIDcardAppyLoanOnlineNum'] > 0:
        return 'REJECT'
    return 'PASS'

def DD1016_A14(row):
    if row['all067LoanNowPlatformCnt'] < 0 and row['all087SameBirthdayApplyLoanOnlineNum'] > 0:
        return 'REJECT'
    return 'PASS'

def DD3007_A14(row): 
    if row['app126JpInstallNum7d']>12:
        return 'REJECT'
    elif (row['app126JpInstallNum1d']>3 or row['app126JpInstallNum1d']==0) and row['biz053MediaSource']=="Organic":
        return 'REJECT'
    return 'PASS'


def DD7017_A14(row):
    if row['model048P35Acardv9'] <=505:
        return 'REJECT'
    return 'PASS'

def DD7027_A14(row):
    if row['model162MxAcardV81Stack'] <= 505:
        return 'REJECT'
    elif row['model162MxAcardV81Stack'] <= 530 and row['biz503Random3']<=7000 :
        return 'REJECT'
    return 'PASS'

def DD7031_A14(row):
    if row['model245MxAcardV161']<=500:
        return 'REJECT'
    elif row['model245MxAcardV161']<=515 and row['biz503Random3']<=5000:
        return 'REJECT'
    return 'PASS'

def DD7032_A14(row):
    if row['model255MxAcardV171Refuse']<=525:
        return 'REJECT'
    return 'PASS'

# ###A15

def DD1001_A15(row):
    if row['base001Age'] > 75 or (row['biz096IsAllappExcellentUser']== 0 and row['base001Age'] < 21) or (row['biz096IsAllappExcellentUser']==1 and row['base001Age'] < 18):
        return 'REJECT'
    return 'PASS'


def DD1008_A15(row):
    if row['base022IsOverdueHalfYear'] == 1 and row['model195MxAcardV111'] <= 510:
        return 'REJECT'
    elif row['biz038SurveyIsAllPerfect'] == 1 and row['model195MxAcardV111'] <= 500:
        return 'REJECT'
    return 'PASS'

def DD6006_A15(row):
    if row['biz224Last0dNotLimitRefuseBatchCnt'] > 0 or row['biz224Last30dNotLimitRefuseBatchCnt'] > 1:
        return 'REJECT'
    elif row['all100AllappNotLimitRefuseBatchCnt'] >4:
        return 'REJECT'
    return 'PASS'


def DD7017_A15(row):
    if row['model048P35Acardv9'] <=490:
        return 'REJECT'
    return 'PASS'


def DD7026_A15(row):  
    if row['model148MxAcardRankV3'] >=6:
        return 'REJECT'
    elif row['model145MxAcardV65Stack'] <=540:
        return 'REJECT'
    return 'PASS'

def DD7027_A15(row):
    if row['model162MxAcardV81Stack'] <= 520:
        return 'REJECT'
    return 'PASS'

def DD7029_A15(row):
    if row['model203MxAcardV119']<=500:
        return 'REJECT'
    elif row['model203MxAcardV119']<=515 and row['model048P35Acardv9'] <=505 and row['biz503Random3']<=8000:
        return 'REJECT'
    return 'PASS'




##############################################################################3 A07
def DD1001_A07(row):
    if row['base001Age'] > 75 or (row['biz096IsAllappExcellentUser']== 0 and row['base001Age'] < 21) or (row['biz096IsAllappExcellentUser']==1 and row['base001Age'] < 18):
        return 'REJECT'
    return 'PASS'


def DD3003_A07(row):
    return 'PASS'

def DD6003_A07(row):
    if row['all007AllSystemBlacklist']==1 and row['all055PrivateBlackSource']!="42" and row['biz503Random3']<=7000:
        return 'REJECT'
    return 'PASS'

def DD6007_A07(row):
    if (row['all068OrderLoanNowTimesAll']>10) or (row['all067LoanNowPlatformCnt']>=0 and row['model048P35Acardv9']<=500) or (row['all067LoanNowPlatformCnt']>=1 and row['model048P35Acardv9']<=510) or (row['all067LoanNowPlatformCnt']>=2):
        return 'REJECT'
    return 'PASS'


# def DD7012_A07(row):
#     if (row['model032Acardv5'] <= 470 and row['model039Acardv6all']<=525):
#         return 'REJECT'
#     return 'PASS'



# def DD7014_A07(row):
    # if row['model032Acardv5'] <= 490 and row['model039Acardv6all']<=495 and row['biz096IsAllappExcellentUser']==0:
        # return 'REJECT'
    # return 'PASS'

def DD7015_A07(row):
    # if row['model027Fcardv2all'] <= 535:
    #     return 'REJECT'
    return 'PASS'

def DD7017_A07(row):
    if row['model048P35Acardv9'] <= 495:
        return 'REJECT'
    return 'PASS'

def DD3007_A07(row):
    if row['app040InstalljingpinCombineNum7d']>15:
        return 'REJECT'
    return 'PASS'



### A06
def DD1001_A06(row):
    """
    年龄限制
    """
    if row['biz037AppId'] == "sst001_C635-001":
        return 'REJECT'
    else:
        if row['base001Age']<18 or row['base001Age']>75:
            return 'REJECT'
        else:
            return 'PASS'

# 收紧
def DD1008_A06(row):
    if row['biz038SurveyIsAllPerfect']==1 and row['model063Acardv16']<=540:
        return 'REJECT'
    return 'PASS'

def DD3007_A06(row):
    return 'PASS'

def DD3008_A06(row):
    # if row['app080InstallJingpin241014TOP20AppNum']>10:
    #     return 'REJECT'
    return 'PASS'

def DD6003_A06(row):
    if row['all007AllSystemBlacklist']==1 and row['all055PrivateBlackSource'] != "42":
        return 'REJECT'
    return 'PASS'
##########re
def DD6006_A06(row):
    if row['biz223NotLimitRefuseBatchCnt']>1:
        return 'REJECT'
    return 'PASS'


def DD7010_A06(row):
    # if row['model029Acardv4all']<=500 and row['biz503Random3']<=5000:
    #     return 'REJECT'
    return 'PASS'

# 下线
# def DD7011_A06(row):
#     return 'PASS'

# 新收紧
def DD7014_A06(row):
    if (row['model089acardv27MX30']<=525 and row['model039Acardv6all']<=490) or (row['model039Acardv6all']<=485):
        return 'REJECT'
    return 'PASS'

# 灰度放松
def DD7017_A06(row):
    if row['model048P35Acardv9']<=490 or (row['model048P35Acardv9']<=495 and row['biz503Random3']<=6000):
        return 'REJECT'
    return 'PASS'

def DD7019_A06(row):
    if row['model089acardv27MX30']<=510:
        return 'REJECT'
    return 'PASS'


# 灰度放松
def DD7020_A06(row):
    # if row['model027Fcardv2all']<=535 and row['biz503Random3']<=8000:
    #     return 'REJECT'
    return 'PASS'


# ## A06结束

def DD1001(row):
    if (row['base001Age'] < 18) or (row['base001Age'] > 75):
        return 'REJECT'
    return 'PASS'


def DD1002(row):
    if row['base003PhoneSameNearContact'] == 1:
        return 'REJECT'
    return 'PASS'


def DD1003(row):
    if row['base016SameIDcardAppyNum'] > 0:
        return 'REJECT'
    return 'PASS'

def DD1003_all(row):
    if row['all088SameIDcardAppyLoanOnlineNum'] > 1:
        return 'REJECT'
    return 'PASS'


def DD1004(row):
    if row['base018MailNumSeq'] > 0:
        return 'REJECT'
    return 'PASS'

def DD1004_all(row):
    if row['all089MailLoanOnlineNumSeq'] > 1:
        return 'REJECT'
    return 'PASS'


def DD1005(row):
    if row['base017SameBankcardAppyNum'] > 0:
        return 'REJECT'
    return 'PASS'

def DD1005_all(row):
    if row['all090SameBankcardAppyLoanOnlineNum'] > 1:
        return 'REJECT'
    return 'PASS'


def DD1006(row):
    if row['base015SameBirthdayApplyNum'] >= 1:
        return 'REJECT'
    return 'PASS'

def DD1006_all(row):
    if row['all087SameBirthdayApplyLoanOnlineNum'] > 1:
        return 'REJECT'
    return 'PASS'


def DD1007(row):
    if row['base001Age'] < 18 or row['base001Age'] > 75:
        return 'REJECT'
    return 'PASS'


def DD1011(row):
    if (row['biz098MinFaceDistance'] < 0.4) and (row['biz098MinFaceDistance'] >= 0):
        return 'REJECT'
    return 'PASS'


def DD1012(row):
    if row['all102RegTimeIntervalMin'] < 15 and row['all102RegTimeIntervalMin'] > 0:
        return 'REJECT'
    return 'PASS'

def DD1013(row):
    if row['all067LoanNowPlatformCnt'] > 0 and row['all088SameIDcardAppyLoanOnlineNum'] == 0 and row['biz037AppId'] != "sst001_NBR-008":
        return 'REJECT'
    return 'PASS'


# # iOS
def DD1001_iOS(row):
    """
    年龄限制
    """
    if row['base001Age'] <= 20 or row['base001Age'] > 75:
        return 'REJECT'
    elif row['base001Age'] <= 25 and row['model052IosAcardv2'] <= 540:
        return 'REJECT'
    return 'PASS'


def DD1010_iOS(row):
    """
    问卷完美回答限制
    """
    if row['model120IosAcardV44IosH5']<=495 and row['biz038SurveyIsAllPerfect']==1:
        return 'REJECT'
    elif row['model120IosAcardV44IosH5']<=510 and row['base026LoanNumHistory']<=0 and row['biz037AppId']=="sst001_IOS-NBR-010":
        return 'REJECT'
    else:
        return 'PASS'

def DD1011_iOS(row):
    """
    人脸对比相似度限制
    """
    if (row['biz098MinFaceDistance'] <= 0.4 and row['biz098MinFaceDistance'] >= 0 ) :
        return 'REJECT'
    return 'PASS'

def DD1012_iOS(row):
    """
    设备内存限制
    """
    # if row['dev038RamTotalSize'] == 2147483648  and row['model060IosAcardv3']<=520 and row['biz053MediaSource'] != "SST-Tanzhi":
    #     return 'REJECT'
    return 'PASS'


def DD1013_iOS(row):
    """
    欺诈团伙经纬度拒贷
    """
    if row['base031Latitude'] == "25.69" and row['base032Longitude']=="-100.17":
        return 'REJECT'
    elif row['base031Latitude'] == "25.70" and row['base032Longitude']=="-100.18":
        return 'REJECT'
    # elif row['biz053MediaSource']=="" and row['all056IsPrivateWhite']==0:
    #     return 'REJECT'
    return 'PASS'

def DD1014_iOS(row):
    """
    欺诈团伙通讯录相似拒贷
    """
    if row['con001ConPhoneNum']!=-9999979 and row['con005ConSameContactCnt'] >=1500 or row['con022MaxSameRate'] >= 0.5 or row['con023HitPhoneRate'] >= 0.5:
        return 'REJECT'
    return 'PASS'

def DD5001_iOS(row):
    # if row['con001ConPhoneNum']!=-9999979 and row['con001ConPhoneNum'] > 0 and row['con001ConPhoneNum'] <= 1 and row['biz503Random3'] <= 5000:
    #     return 'REJECT'
    return 'PASS'

def DD5002_iOS(row):
    if row['con001ConPhoneNum']!=-9999979 and row['con002ConPhoneRegitst30d'] > 5 and row['biz503Random3'] <= 5000:
        return 'REJECT'
    return 'PASS'

def DD5003_iOS(row):
    if row['con001ConPhoneNum']!=-9999979 and row['con003ConPhoneApply48h'] >= 3 and row['biz503Random3'] <= 5000:
        return 'REJECT'
    return 'PASS'

def DD5004_iOS(row):
    if row['con001ConPhoneNum']!=-9999979 and row['con004ConPhoneApply'] > 10 and row['biz503Random3'] <= 5000:
        return 'REJECT'
    return 'PASS'


def DD6008_iOS(row):
    if (row['model052IosAcardv2'] <= 560 and row['all100AllappNotLimitRefuseBatchCnt']>5):
        return 'REJECT'
    return 'PASS'

def DD7002_iOS(row):
    if row['model052IosAcardv2'] <= 525:
        return 'REJECT' 
    return 'PASS'  

def DD2007_iOS(row):
    if row['all045SamePhoneRegister'] > 0 and row['biz037AppId']=="sst001_IOS-NBR-010":
        return 'REJECT' 
    return 'PASS'


def DD7004_iOS(row):
    if row['model120IosAcardV44IosH5'] <= 490 and row['biz037AppId']=="sst001_IOS-NBR-010":
        return 'REJECT' 
    return 'PASS'  

def DD7005_iOS(row):
    if row['model148MxAcardV68IosH5'] <= 495:
        return 'REJECT'
    elif row['model148MxAcardV68IosH5'] <= 505 and row['biz037AppId']=="sst001_IOS-NBR-010":
        return 'REJECT'
    return 'PASS'

def DD7006_iOS(row):
    if row['model178MXAcardV94IosH5'] <= 500:
        return 'REJECT'
    elif row['model178MXAcardV94IosH5'] <= 505 and row['model052IosAcardv2'] <= 535 and row['biz503Random3']<=5000:
        return 'REJECT'
    return 'PASS'


# # iOS_A05 无通讯录版本
# def DD2003_iOS_A05(row):
#     if (row['dev027SameDevIdNum30d'] > 0 or row['all084SameDevIdLoanOnlineNum30d'] > 0):
#         return 'REJECT'
#     return 'PASS'


def DD1001_iOS_A05(row):
    """
    年龄限制
    """
    if row['base001Age'] <= 20 or row['base001Age'] > 70:
        return 'REJECT'
    elif (row['base030appCode']=="59ldl3u1uc01kt4uqyoqi1p9f7173j6g" or row['base030appCode']=="r6sgkp4n53k018bh1dhb66wn3597efu0") and row['biz037AppId']=="sst001_IOS-NBR-008":
        return 'REJECT'
    elif row['biz037AppId']=="sst001_IOS-EMI-MX-001" or row['biz037AppId'] == 'sst001_IOS-NBR-011':
        return 'REJECT'
    return 'PASS'


def DD1010_iOS_A05(row):
    """
    问卷调查完美回答
    """
    if row['model120IosAcardV44IosH5']<=500 and row['base026LoanNumHistory']==0 and row['biz096IsAllappExcellentUser']==0:
        return 'REJECT'
    elif row['model120IosAcardV44IosH5']<=510 and row['base026LoanNumHistory']==0 and row['biz037AppId'] != "sst001_IOS-NBR-008" and row['biz096IsAllappExcellentUser']==0:
        return 'REJECT'
    elif row['model178MXAcardV94IosH5']<=510 and row['biz038SurveyIsAllPerfect']==1 and row['biz037AppId'] == "sst001_IOS-NBR-H5-3":
        return 'REJECT'
    return 'PASS'



def DD1011_iOS_A05(row):
    """
    人脸对比相似度限制
    """
    if (row['biz098MinFaceDistance'] <= 0.4 and row['biz098MinFaceDistance'] >= 0 ) :
        return 'REJECT'
    return 'PASS'

def DD1012_iOS_A05(row):
    # """
    # OCR与手写不一致
    # """
    # if row['base028OcrWithNameSimilar'] > 6 and row['biz503Random3']<=8000:
    #     return 'REJECT'
    return 'PASS'

def DD1013_iOS_A05(row):
    if (row['all067LoanNowPlatformCnt'] < 0 and row['all087SameBirthdayApplyLoanOnlineNum'] == 1 and row['biz037AppId'] != "sst001_IOS-NBR-008" ) :
        return 'REJECT'
    return 'PASS'

def DD6009_iOS_A05(row):
    if row['biz053MediaSource']=="" and row['biz037AppId'] == "sst001_IOS-NBR-H5-3":
        return 'REJECT'
    return 'PASS'



def DD7004_iOS_A05(row):
    if row['model120IosAcardV44IosH5'] <= 490 and row['biz503Random3']<=5000:
        return 'REJECT' 
    return 'PASS'


def DD7005_iOS_A05(row):
    # if row['model148MxAcardV68IosH5'] <= 500 and row['biz053MediaSource'] == "Organic": 
    #     return 'REJECT'
    # if row['biz053MediaSource'] == "SST-Tanzhi" and row['biz037AppId'] == "sst001_IOS-NBR-008":
    #     return 'REJECT'
    return 'PASS'


def DD7006_iOS_A05(row):
    if row['model178MXAcardV94IosH5'] <= 500:
        return 'REJECT'
    return 'PASS'

def DD7007_iOS_A05(row):
    if row['model213MxAcardV129IosH5'] <= 495 and row['biz096IsAllappExcellentUser']==0:
        return 'REJECT'
    return 'PASS'

def DD7008_iOS_A05(row):
    if row['model148MxAcardV68IosH5'] <= 500 and row['biz037AppId'] != "sst001_IOS-NBR-008":
        return 'REJECT'
    return 'PASS'


def DD8001_iOS_A05(row):
    if row['izi004LivenessScore'] == 0:
        return 'REJECT'
    return 'PASS'

def DD8019_iOS_A05(row):
#     # 首先获取值，然后处理None值
#     id_sear_num = row.get('advMulti018IDSearNum')
#     id_sear_pct = row.get('advMulti019IDSearPct')
    
#     # 处理None值
#     if id_sear_num is None:
#         id_sear_num = -9999979
#     if id_sear_pct is None:
#         id_sear_pct = -9999979
    
#     if (row['biz037AppId'] == "sst001_IOS-NBR-008" and 
#         (id_sear_num > 10 or id_sear_pct > 0.8)):
#         return 'REJECT'
    return 'PASS'

def DD8020_iOS_A05(row):
    if 0 < row['model275MxAcardV192IosAdvNew'] <= 475 and row['biz096IsAllappExcellentUser']==0 and row['biz503Random3']<=7000:
        return 'REJECT'
    elif 0 < row['model275MxAcardV192IosAdvNew'] <= 480 and row['biz037AppId'] != "sst001_IOS-NBR-008" and row['biz096IsAllappExcellentUser']==0:
        return 'REJECT'    
    return 'PASS'


## iOS009 15天周期
def DD1001_iOS_A08(row):
    """
    年龄限制
    """
    if row['base001Age'] <= 20 or row['base001Age'] > 70:
        return 'REJECT'
    elif row['base001Age'] <= 25 and row['model052IosAcardv2'] <= 540:
        return 'REJECT'
    return 'PASS'

def DD1010_iOS_A08(row):
    """
    问卷完美回答限制
    """
    if row['model120IosAcardV44IosH5']<=495 and row['biz038SurveyIsAllPerfect']==1:
        return 'REJECT'
    else:
        return 'PASS'

def DD7002_iOS_A08(row):
    if row['model052IosAcardv2'] <= 525:
        return 'REJECT' 
    return 'PASS'  

def DD7005_iOS_A08(row):
    if row['model148MxAcardV68IosH5'] <= 495:
        return 'REJECT'
    return 'PASS'

def DD7006_iOS_A08(row):
    if row['model178MXAcardV94IosH5'] <= 500:
        return 'REJECT'
    elif row['model178MXAcardV94IosH5'] <= 505 and row['model052IosAcardv2'] <= 535 and row['biz503Random3']<=5000:
        return 'REJECT'
    return 'PASS'

def DD1014_iOS_A08(row):
    """
    欺诈团伙通讯录相似拒贷
    """
    if row['con001ConPhoneNum']!=-9999979 and row['con005ConSameContactCnt'] >=1500 or row['con022MaxSameRate'] >= 0.5 or row['con023HitPhoneRate'] >= 0.5:
        return 'REJECT'
    return 'PASS'

def DD5001_iOS_A08(row):
    if row['con001ConPhoneNum']!=-9999979 and row['con001ConPhoneNum'] > 0 and row['con001ConPhoneNum'] <= 1:
        return 'REJECT'
    return 'PASS'

def DD5002_iOS_A08(row):
    if row['con001ConPhoneNum']!=-9999979 and row['con002ConPhoneRegitst30d'] > 5 and row['biz503Random3'] <= 5000:
        return 'REJECT'
    return 'PASS'

def DD5003_iOS_A08(row):
    if row['con001ConPhoneNum']!=-9999979 and row['con003ConPhoneApply48h'] >= 3 and row['biz503Random3'] <= 5000:
        return 'REJECT'
    return 'PASS'

def DD5004_iOS_A08(row):
    if row['con001ConPhoneNum']!=-9999979 and row['con004ConPhoneApply'] > 10 and row['biz503Random3'] <= 5000:
        return 'REJECT'
    return 'PASS'


# # iOS_A10 H5网页版本
# def DD2003_iOS_A10(row):
#     if (row['dev027SameDevIdNum30d'] > 0 or row['all084SameDevIdLoanOnlineNum30d'] > 0):
#         return 'REJECT'
#     return 'PASS'


def DD1001_iOS_A10(row):
    """
    年龄限制
    """
    if row['base001Age'] <= 20 or row['base001Age'] > 70:
        return 'REJECT'
    elif row['base001Age'] <= 25 and row['model052IosAcardv2'] <= 540:
        return 'REJECT'
    elif row['base030appCode']=="m2v5kb6mry644cxk53eb363zy0pt0r74":
        return 'REJECT'
    return 'PASS'

def DD1010_iOS_A10(row):
    """
    问卷完美回答限制
    """
    if row['model178MXAcardV94IosH5']<=510 and row['biz038SurveyIsAllPerfect']==1:
        return 'REJECT'
    else:
        return 'PASS'


def DD1011_iOS_A10(row):
    """
    人脸对比相似度限制
    """
    if (row['biz098MinFaceDistance'] <= 0.4 and row['biz098MinFaceDistance'] >= 0 ) :
        return 'REJECT'
    return 'PASS'

def DD1012_iOS_A10(row):
    """
    设备内存限制
    """
    # if row['dev038RamTotalSize'] == 2147483648  and row['model052IosAcardv2']<=540 and row['biz053MediaSource'] != "SST-Tanzhi"  and row['biz503Random3']<=8000:
    #     return 'REJECT'
    return 'PASS'

# def DD2004_iOS_A10(row):
#     if row['dev010DevIdNum30d'] > 3:
#         return 'REJECT'
#     return 'PASS'

def DD6008_iOS_A10(row):
    if row['biz223NotLimitRefuseBatchCnt']>0:
        return 'REJECT'
    return 'PASS'

def DD6009_iOS_A10(row):
    if row['biz053MediaSource']=="":
        return 'REJECT'
    elif  row['biz053MediaSource']=="LaoK":
        return 'REJECT'
    return 'PASS'

#def DD7002_iOS_A10(row):
    #if row['model052IosAcardv2'] <= 525:
        #return 'REJECT' 
    #return 'PASS'   

def DD7004_iOS_A10(row):
    if row['model120IosAcardV44IosH5']<=485 and row['biz503Random3'] <= 5000:
        return 'REJECT'
    return 'PASS'

def DD7005_iOS_A10(row):
    # if row['model148MxAcardV68IosH5'] <= 500 and row['biz503Random3']<=8000 and row['biz037AppId']=="sst001_IOS-NBR-010":
    #     return 'REJECT'
    return 'PASS'



def DD7006_iOS_A10(row):
    if row['model178MXAcardV94IosH5'] <= 500 or (row['model178MXAcardV94IosH5'] <= 510 and row['model181PhAcardV97IosH5'] <= 505):
        return 'REJECT'
    return 'PASS'

# def DD7007_iOS_A10(row):
#     # if row['model213MxAcardV129IosH5'] <= 500 and row['biz503Random3'] <= 3000:
#     #     return 'REJECT'
#     return 'PASS'


def DD8001_iOS_A10(row):
    if row['izi004LivenessScore'] == 0:
        return 'REJECT'
    return 'PASS'

# def DD8015(row):
#     if row['doubao001IsSticker'] == 1:
#         return 'REJECT'
#     return 'PASS'


def DD8016(row):
    # if row['doubao002IsMakeup'] == 1:
    #     return 'REJECT'
    return 'PASS'

def DD8017(row):
    if row['adv016IDFraud'] != -9999979 and row['adv017IsIDFraud'] == 1 and  ("face_tampering" in row['adv016IDFraud'] ):
        return 'REJECT'
    elif row['adv016IDFraud'] != -9999979 and row['adv017IsIDFraud'] == 1 and  ("retake" in row['adv016IDFraud'] ) and ("screenshot" in row['adv016IDFraud'] ):
        return 'REJECT'
    return 'PASS'

def DD8018_iOS_A10(row):
    # if row['biz037AppId']=="sst001_IOS-NBR-H5" and row['ss001PrinNum3y'] != -9999979 and row['ss002PrinNum5y'] > 5:
    #     return 'REJECT'
    return 'PASS'

# def DD8013_iOS_A10(row):
#     if row['izi005IsExpressionAbnorma'] == "true":
#         return 'REJECT'
#     return 'PASS'

# ## ios结束

def DD2001(row):
    if row['dev028SameGaidNum30d'] > 0:
        return 'REJECT'
    return 'PASS'

def DD2001_all(row):
    if row['all085SameGaidLoanOnlineNum30d'] > 1:
        return 'REJECT'
    elif row['base030appCode'] =="f615934745d373caddca94604469fd56":
        return 'REJECT'
    return 'PASS'


def DD2002(row):
    if row['dev007WiFimacNum30d'] > 1:
        return 'REJECT'
    return 'PASS'

def DD2002_all(row):
    if row['all086WiFimacLoanOnlineNum30d'] > 1:
        return 'REJECT'
    return 'PASS'


def DD2003(row):
    if row['dev027SameDevIdNum30d'] > 0:
        return 'REJECT'
    return 'PASS'

def DD2003_all(row):
    if row['all084SameDevIdLoanOnlineNum30d'] > 1:
        return 'REJECT'
    return 'PASS'


def DD2004(row):
    if row['dev010DevIdNum30d'] > 3:
        return 'REJECT'
    return 'PASS'


def DD2005(row):
    if row['dev005IsRoot'] == 1:
        return 'REJECT'
    return 'PASS'

def DD2006(row):
    if row['dev008IsUsingVpn'] == 1:
        return 'REJECT'
    return 'PASS'


def DD3001(row):
    if row['app004Appnumall'] <= 10:
        return 'REJECT'
    return 'PASS'


def DD3002(row):
    if row['app017InstallSocialAppNum'] <= 0:
        return 'REJECT'
    return 'PASS'


def DD3003(row):
    # if (row['app034UpdateJingpin9YueNum1d'] > 6 and row['model026Fcardv2train'] <= 550) or (row['biz037AppId'] =="sst001_NBR-635" and row['app013CompeteAppsum'] <= 0):
    #     return 'REJECT'
    return 'PASS'


def DD3004(row):
    """
    竞品安装限制
    """

    if row['app024InstallCompeteAppNumAll14Days'] > 16:
        return 'REJECT'
    return 'PASS'

def DD3005(row):
    if row['app025InstallGambleAppNum'] > 2 and row['model016AcardRefusev1'] <= 495 and row['model015Acardv2'] <= 540 and row['biz037AppId']=="sst001_NBR-635":
        return 'REJECT'
    elif row['biz037AppId']=="sst001_NBR-635" and row['biz053MediaSource'] not in ["Facebook Ads","restricted"]:
        if (row['model046AcardRongheRank35'] >=5 and row['app048InstallAppNum1d'] > 3):
            return 'REJECT'
        return 'PASS'
    elif row['biz037AppId']=="sst001_NBR-635" and row['biz053MediaSource'] in ["Facebook Ads","restricted"]:
        if (row['model046AcardRongheRank35'] >=5 and row['app048InstallAppNum1d'] > 5):
            return 'REJECT'
        return 'PASS'

    elif row['biz037AppId']=="sst001_C635-001" and row['biz053MediaSource'] not in ["Facebook Ads","restricted"]:
        if (row['model046AcardRongheRank35'] >=5 and row['app048InstallAppNum1d'] > 5):
            return 'REJECT'
        return 'PASS'

    return 'PASS'

def DD3005_A03(row):
    return 'PASS'


def DD6001(row):
    if row['all001OverdueNowNum'] > 0 and row['biz209RegistDate']>="2025-06-01":
        return 'REJECT'
    return 'PASS'


def DD6002(row):
    if row['all002MaxOverdueDays'] > 3 and row['biz209RegistDate']>="2025-06-01":
        return 'REJECT'
    return 'PASS'


def DD6003(row):
    if row['all007AllSystemBlacklist']==1 and row['all055PrivateBlackSource'] != "42":
        return 'REJECT'
    else:
        return 'PASS'

def DD6005(row):
    if row['all049SystemPostLoanBlack'] == 1:
        return 'REJECT'
    return 'PASS'


# 003迭代
def DD6006(row):
    if row['all057PrivateWhiteSource']!=41:
        if row['biz224Last0dNotLimitRefuseBatchCnt'] > 5:
            return 'REJECT'
        elif row['biz224Last3dNotLimitRefuseBatchCnt'] > 15:
            return 'REJECT'
        elif row['biz224Last30dNotLimitRefuseBatchCnt'] > 150:
            return 'REJECT'

        # MXiOS差异化收紧
        if row['biz044RiskFlow']=="A10":
            if row['biz223NotLimitRefuseBatchCnt'] > 0 and row['all056IsPrivateWhite'] == 0:
                return 'REJECT'

        # MXiOS在架包差异化收紧
        if row['biz044RiskFlow']=="A04":
            if row['biz223NotLimitRefuseBatchCnt'] > 0 and row['all056IsPrivateWhite'] == 0:
                return 'REJECT'

        # MX003差异化收紧
        if row['biz037AppId'] == 'sst001_NBR-003':
            if row['biz223NotLimitRefuseBatchCnt'] > 5:
                return 'REJECT'

        # MX004差异化收紧
        if row['biz037AppId'] == 'sst001_NBR-640':
            if row['biz224Last0dNotLimitRefuseBatchCnt'] > 0:
                return 'REJECT'

        # MX002差异化收紧
        if row['biz037AppId']=="sst001_C635-001":
            if row['biz224Last30dNotLimitRefuseBatchCnt'] > 10:
                return 'REJECT'

        # MX005差异化收紧
        if row['biz037AppId']=="sst001_NBR-635":
            if row['biz224Last30dNotLimitRefuseBatchCnt']>2 or row['biz223NotLimitRefuseBatchCnt'] > 3:
                return 'REJECT'

        # MX008差异化收紧
        if row['biz044RiskFlow']=="A12":
            if row['all100AllappNotLimitRefuseBatchCnt'] > 10:
                return 'REJECT'

    return 'PASS'

# 新增, C01分支
def DD6007(row):
    if row['all067LoanNowPlatformCnt']>1:
        return 'REJECT'
    return 'PASS'


# 新增, C01分支
def DD3007(row):
    if row['biz037AppId'] in ['sst001_NBR-003', 'sst001_NBR-640'] and row['app040InstalljingpinCombineNum7d'] > 19:
        return 'REJECT'
    return 'PASS'


def DD7001(row):
    # if (row['biz037AppId'] !="sst001_NBR-635" and row['model029Acardv4all'] <= 505 and row['model003Acardv1']<=510) or (row['biz037AppId'] =="sst001_NBR-635" and row['model029Acardv4all'] <= 505 and row['model003Acardv1']<=515) or (row['biz053MediaSource'] == "Organic" and row['model004Acardv1'] <=500):
    #     return 'REJECT'
    return 'PASS'



def DD7016(row):
    if row['biz037AppId'] == "sst001_NBR-635" and ((row['model046AcardRongheRank35'] == 6 and row['biz044RiskFlow']!="C01" and row['biz053MediaSource'] in ["Facebook Ads","restricted"]) or (row['model046AcardRongheRank35'] >= 5 and row['biz044RiskFlow']!="C01" and row['biz053MediaSource'] not in ["Facebook Ads","restricted"])):
        return 'REJECT'
    if row['biz037AppId'] == "sst001_C635-001" and row['model048P35Acardv9'] <= 500 and ((row['model046AcardRongheRank35'] == 6 and row['biz044RiskFlow']!="C01" and row['biz053MediaSource'] in ["Facebook Ads","restricted"]) or (row['model046AcardRongheRank35'] >= 5 and row['biz044RiskFlow']!="C01" and row['biz053MediaSource'] not in ["Facebook Ads","restricted"])):
        return 'REJECT'
    return 'PASS'




def DD8001(row):
    return 'PASS'

def DD8001_iOS(row):
    if row['izi004LivenessScore'] == 0:
        return 'REJECT'
    return 'PASS'


def DD8002(row):
    if row['izi002FaceSimilarityScore'] <= 45 and row['izi002FaceSimilarityScore'] >= 0:
        return 'REJECT'
    return 'PASS'

def DD8002_iOS(row):
    if row['izi002FaceSimilarityScore'] <= 45 and row['izi002FaceSimilarityScore'] >= 0:
        return 'REJECT'
    return 'PASS'

def DD8003(row):
    if row['izi001IsWhatsapp'] == 0:
        return 'REJECT'
    elif row['izi001IsWhatsapp'] < 0 and row['biz037AppId'] != "sst001_NBR-008":
        return 'REJECT'
    elif row['izi001IsWhatsapp'] < 0 and row['model148MxAcardRankV3']>=5:
        return 'REJECT'
    return 'PASS'


def DD8003_007(row):
    if row['izi001IsWhatsapp'] == 0:
        return 'REJECT'
    return 'PASS'


def DD8003_iOS(row):
    if row['izi001IsWhatsapp'] == 0:
        return 'REJECT'
    return 'PASS'


def DD8004(row):
    # if (row['biz037AppId'] == "sst001_NBR-635" and row['model028Acardv4train'] <= 540 and
    #         row['biz053MediaSource'] != "Facebook Ads" and row['adv002CurpStatusCode'] == "CURP_NOT_EXIST"):
    #     return 'REJECT'
    return 'PASS'


def DD8004_iOS(row):
    if row['biz503Random3'] <= 9000 and (row['adv002CurpStatusCode'] == "CURP_NOT_EXIST"
                                         or row['adv002CurpStatusCode'] =="PARAMETER_ERROR" or row['adv002CurpStatusCode']=="WRONG_INPUT"):
        return 'REJECT'
    return 'PASS'


def DD8009(row):
    return 'PASS'

def DD8012(row):
    return 'PASS'

def DD8012_iOS(row):
    return 'PASS'


# 老户
# --------------------B09
def DZ7030_B09(row):
    if row['biz037AppId'] in ['sst001_NBR-008','sst001_NBR-640']:
        if row['model074BcardV17']<=460:
            return 'REJECT'
        else:
            return 'PASS'
    elif row['biz037AppId'] == 'sst001_NBR-635':
        if row['model074BcardV17']<=500:
            return 'REJECT'
        else:
            return 'PASS'
    else:
        return 'PASS'

def DZ7022_B09(row):
    if (row['biz037AppId'] in ['sst001_NBR-003','sst001_NBR-640','sst001_NBR-008','sst001_NBR-009']) and ((row['biz103RepayMoneyTotal'] < float(row['biz042NewBeginAmount'])) and  row['biz041IsProductReloan'] ==0):
        return 'REJECT'
    else:
        return 'PASS'


def DZ7023_B09(row):
    if row['biz041IsProductReloan']==0 and row['biz113CurrentOTNloaningNum'] > 5 and row['biz037AppId'] in ["sst001_NBR-003","sst001_NBR-008","sst001_NBR-009","sst001_NBR-640"]:
        return 'REJECT'
    elif row['biz041IsProductReloan']==0 and row['biz037AppId'] != "sst001_NBR-009" and row['model020Bcardv3pureold'] <= 525 and row['biz113CurrentOTNloaningNum'] >0:
        return 'REJECT'
    elif row['biz041IsProductReloan']==0 and row['biz037AppId'] in ["sst001_NBR-009","sst001_NBR-640"] and row['model019Bcardv3oldtonew'] <= 505 and row['biz113CurrentOTNloaningNum'] > 0:
        return 'REJECT'
    return 'PASS'

def DZ7031_B09(row):
    '''
    v5分拒贷,605
    '''
    if row['model053Bcardv12Rate35'] <= 480 and row['biz037AppId'] != 'sst001_NBR-640': 
        return 'REJECT'
    return 'PASS'


def DZ7007(row):
    if row['model019Bcardv3oldtonew'] <= 460 and row['biz037AppId'] in ["sst001_NBR-009","sst001_NBR-008"]:
        return 'REJECT'
    elif row['model019Bcardv3oldtonew'] <= 470 and row['biz037AppId'] =="sst001_NBR-635":
        return 'REJECT'
    elif row['model019Bcardv3oldtonew'] <= 480 and row['biz037AppId'] == "sst001_C635-001":
        return 'REJECT'
    return 'PASS'


def DZ2001(row):
    '''
    老户近30天同Gaid账户数
    '''
    if row['dev028SameGaidNum30d'] > 0 or row['base030appCode'] =="f615934745d373caddca94604469fd56":
        return 'REJECT'
    elif row['biz037AppId'] =="sst001_NBR-003":
        return 'REJECT' 
    return 'PASS'



def DZ1002_iOS(row):

    if row['biz098MinFaceDistance'] <=0.4  and row['biz098MinFaceDistance'] >= 0:
        return 'REJECT'
    return 'PASS'


def DZ2003(row):
    if row['dev027SameDevIdNum30d'] > 0:
        return 'REJECT'
    return 'PASS'


def DZ2006(row):
    if row['dev008IsUsingVpn'] == 1:
        return 'REJECT'
    return 'PASS'



def DZ6001(row):
    if (row['all001OverdueNowNum'] > 0 or row['biz008OverdueNowNum'] > 0)  and row['biz209RegistDate']>="2025-06-01":
        return 'REJECT'
    return 'PASS'




def DZ6002(row):
    '''
    历史最大逾期天数
    '''
    if (row['biz009MaxOverdueDays'] > 7 or row['all002MaxOverdueDays'] > 7):
        return 'REJECT'
    elif row['model047BcardRongheRankTotal'] > 3 and (
            row['biz009MaxOverdueDays'] >= 3 or row['all002MaxOverdueDays'] >= 3):
        return 'REJECT'
    elif row['model047BcardRongheRankTotal'] > 4 and (
            row['biz009MaxOverdueDays'] > 1 or row['all002MaxOverdueDays'] > 1):
        return 'REJECT'
    else:
        return 'PASS'

def DZ6002_B09(row):
    '''
    历史最大逾期天数
    '''
    if (row['biz009MaxOverdueDays'] >= 7 or row['all002MaxOverdueDays'] >= 7):
        return 'REJECT'
    elif (row['biz009MaxOverdueDays'] > 3 or row['all002MaxOverdueDays'] > 3) and row['model135BcardV57longtrain'] <= 510 and row['biz209RegistDate']>="2025-06-01": 
        return 'REJECT'
    elif (row['biz009MaxOverdueDays'] > 1 or row['all002MaxOverdueDays'] > 1) and row['model135BcardV57longtrain'] <= 500 and row['biz209RegistDate']>="2025-06-01":
        return 'REJECT'

    return 'PASS'


def DZ6003(row):
    if row['all007AllSystemBlacklist'] == 1 and row['all055PrivateBlackSource'] != "42":
        return 'REJECT'
    else:
        return 'PASS'

def DZ6003_B09(row):
    if row['biz037AppId'] == "sst001_NBR-640" and row['all011SystemIsEmailBlack']==1:
        return 'REJECT'
    elif row['all010SystemIsDevBlack']==1 :
        return 'REJECT'
    else:
        return 'PASS'

def DZ6004(row):
    '''
    老转新结合命中自有黑名单
    '''
    if row['biz037AppId'] in ['sst001_NBR-003','sst001_NBR-640']:
        if (row['all008AllSystemIsIDcardNumBlack']==1 or row['all012SystemIsBankAccountBlack']==1):
            return 'REJECT'
        return 'PASS'
    return 'PASS'


def DZ6005(row):
    if row['all049SystemPostLoanBlack'] == 1:
        return 'REJECT'
    return 'PASS'



def DZ7003(row):
    '''
    V2评分拒贷
    '''
    if (row['model018Bcardv2all'] <= 515 and row['biz503Random3'] <= 2000) or (
            row['model018Bcardv2all'] <= 525 and row['biz037AppId'] != "sst001_C635-001"):
        return 'REJECT'
    return 'PASS'


def DZ7005(row):
    '''
    L1共贷限制
    '''
    if ((row['biz042NewBeginAmount'] <= 500 and (
            row['all006LoanNowTimesAll'] > 0 and 525 < row['model018Bcardv2all'] <= 535 and row[
        'biz039TransBatchCnt'] > 3))
        and row['biz037AppId'] != "sst001_C635-001") and row['biz503Random3'] <= 8000 and row[
        'biz041IsProductReloan'] == 0:
        return 'REJECT'
    return 'PASS'


def DZ7006(row):
    '''
    复借v3模型
    '''
    if (row['biz037AppId'] != "sst001_C635-001" and row['biz037AppId'] != "sst001_NBR-635") and (
            row['model019Bcardv3oldtonew'] <= 515 and row['model020Bcardv3pureold'] <= 520) and row[
        'biz502Random2'] <= 9000: return 'REJECT'
    return 'PASS'


def DZ7008(row):
    if ((row['biz042NewBeginAmount'] > 500 and row['biz042NewBeginAmount'] <= 1000 and
         (row['all006LoanNowTimesAll'] > 0 and 525 < row['model018Bcardv2all'] <= 535 and row[
             'biz039TransBatchCnt'] > 3))
        and row['biz037AppId'] != "sst001_C635-001") and row['biz503Random3'] <= 8000 and row[
        'biz041IsProductReloan'] == 0:
        return 'REJECT'
    return 'PASS'


def DZ7009(row):
    '''
    L3共贷限制
    '''
    if ((row['biz042NewBeginAmount'] > 1000 and row['biz042NewBeginAmount'] <= 2000 and
         (row['all006LoanNowTimesAll'] > 3 and 525 < row['model018Bcardv2all'] <= 535 and row[
             'biz039TransBatchCnt'] > 4))
        and row['biz037AppId'] != "sst001_C635-001") and row['biz503Random3'] <= 8000 and row[
        'biz041IsProductReloan'] == 0:
        return 'REJECT'
    return 'PASS'


def DZ7010(row):
    '''
    L4共贷限制
    '''
    if (row['biz042NewBeginAmount'] > 2000 and (
            row['all006LoanNowTimesAll'] > 4 and 525 < row['model018Bcardv2all'] <= 535 and row[
        'biz039TransBatchCnt'] > 5)
            and row['biz503Random3'] <= 8000 and row['biz041IsProductReloan'] == 0 and row[
                'biz037AppId'] != "sst001_C635-001"):
        return 'REJECT'
    return 'PASS'


def DZ7011(row):
    '''
    L4共贷限制
    '''
    if row['model022Bcardv4all'] <= 525 and row['biz037AppId'] != "sst001_C635-001" and row[
        'model018Bcardv2all'] <= 545 and row['biz041IsProductReloan'] == 0:
        return 'REJECT'
    return 'PASS'


def DZ7013(row):
    '''
    共贷限制
    '''
    if (row['all006LoanNowTimesAll'] > 2 and row['model007Bcardv1'] <= 460 and row['biz503Random3'] <= 6000):
        return 'REJECT'
    return 'PASS'


def DZ7018_B09(row):
    '''
    放松，620:近3天放5笔，620-680:近3天放8笔
    '''
    if row['model092MxBcardCreditScoreV18Rank'] > 3  and row['biz037AppId'] == "sst001_C635-001":
        return 'REJECT'
    elif row['model110AllCountryBcardV36Train'] <= 520 and row['all068OrderLoanNowTimesAll'] > 10 and row['biz037AppId']=='sst001_NBR-009':
        return 'REJECT'
    elif  row['all068OrderLoanNowTimesAll'] > 16 and row['biz037AppId']=='sst001_NBR-640':
        return 'REJECT'
    elif row['all068OrderLoanNowTimesAll'] > 24:
        return 'REJECT'
    else:
        return 'PASS'

def DZ7014(row):
    '''
    L4共贷限制
    '''
    if row['biz051OldAmountRateUsed'] > row["biz052OldAmountRateLimit"]:
        return 'REJECT'
    return 'PASS'

def DZ7014_B09(row):
    if row['biz051OldAmountRateUsed'] > row["biz052OldAmountRateLimit"]:
        return 'REJECT'
    return 'PASS'

def DZ7034_B09(row):
    '''
    v36分拒贷,605
    '''
    if row['model110AllCountryBcardV36Train']<=520 and row['biz037AppId']!='sst001_NBR-009':
        return 'REJECT' 
    return 'PASS'


def DZ7021(row):
    if row['biz039TransBatchCnt'] <= 5 and row['model135BcardV57longtrain']<=500:
        return 'REJECT'
    elif row['biz039TransBatchCnt'] <= 1 and row['model135BcardV57longtrain']<=520:
        return 'REJECT'
    elif row['biz037AppId'] == "sst001_NBR-640" and row['model135BcardV57longtrain']<=505:
        return 'REJECT'
    else:
        return 'PASS'




def DZ6008(row):
    if row['biz037AppId'] in ['sst001_C635-001', 'sst001_NBR-635', 'sst001_NBR-003', 'sst001_NBR-640']:
        if row['all045SamePhoneRegister'] > 5 and row['model047BcardRongheRankTotal'] >= 4:
            return 'REJECT'
        if row['all045SamePhoneRegister'] > 1 and row['model047BcardRongheRankTotal'] >= 6:
            return 'REJECT'
    return 'PASS'



def DZ5005(row):
    # 上一笔有逾期且低额度
    if row['biz005LastSettleOverdueDays'] > 0 and row['biz050LoanAmountTotal'] < 2000:
        return 'REJECT'
    else:
        return 'PASS'
    return 'PASS'




def DZ7006_B07(row):
    if row['model020Bcardv3pureold'] <= 520 and row['model019Bcardv3oldtonew'] <= 515: 
        return 'REJECT'
    return 'PASS'



def DZ6002_B06(row):
    '''
    历史最大逾期天数
    '''
    if (row['biz009MaxOverdueDays'] >= 7 or row['all002MaxOverdueDays'] >= 7):
        return 'REJECT'
    # elif row['model135BcardV57longtrain'] <=510 and (row['biz009MaxOverdueDays'] > 3 or row['all002MaxOverdueDays'] > 3):
    #     return 'REJECT'
    # elif row['model135BcardV57longtrain'] <=500 and (row['biz009MaxOverdueDays'] > 1 or row['all002MaxOverdueDays'] > 1):
    #     return 'REJECT'
    else:
        return 'PASS'

def DZ6003_B06(row):
    '''
    设备黑名单
    '''
    # if row['all011SystemIsEmailBlack']==1 and row['biz037AppId']=="sst001_IOS-NBR-H5":
    #     return 'REJECT'
    # else:
    #     return 'PASS'
    return 'PASS'

def DZ7023_B06(row):
    '''
    v5分拒贷,605
    '''
    if (row['biz113CurrentOTNloaningNum'] > 2 and row['biz039TransBatchCnt']<=10) and row['biz041IsProductReloan']==0 and row['biz037AppId']=="sst001_C635-001": 
        return 'REJECT'
    elif row['biz041IsProductReloan']==0 and row['biz113CurrentOTNloaningNum'] > 6 and row['biz037AppId'] in ("sst001_IOS-NBR-H5","sst001_IOS-NBR-H5-2"):
        return 'REJECT'
    return 'PASS'


def DZ7018_B07(row):
    if row['all068OrderLoanNowTimesAll'] > 24:
        return 'REJECT'
    elif row['all068OrderLoanNowTimesAll'] > 16 and row['model110AllCountryBcardV36Train']<=510:
        return 'REJECT'
    elif row['biz057OSTypeIsIOS']==0 and row['all068OrderLoanNowTimesAll'] > 10 and row['model110AllCountryBcardV36Train']<=550 and row['biz037AppId']!="sst001_NBR-008" and row['biz037AppId']!="sst001_NBR-010" and row['biz037AppId']!="sst001_NBR-012" and row['biz037AppId']!="sst001_NBR-009-2" and row['biz502Random2']<=5000:
        return 'REJECT'
    elif row['biz057OSTypeIsIOS']==1 and row['model135BcardV57shortall'] <= 495 and row['all068OrderLoanNowTimesAll'] > 10 and row['biz037AppId']!="sst001_IOS-NBR-007" and row['biz037AppId']!="sst001_IOS-NBR-008" and row['biz037AppId']!="sst001_IOS-NBR-011"  and row['biz037AppId']!="sst001_IOS-NBR-010-2" and row['biz037AppId']!="sst001_IOS-NBR-H5-3":
        return 'REJECT'
    else:
        return 'PASS'

def DZ7014_B07(row):
    if row['biz051OldAmountRateUsed'] > row["biz052OldAmountRateLimit"]:
        return 'REJECT'
    return 'PASS'



def DZ2003_iOS(row):
    return 'PASS'

def DZ6002_iOS(row):
    '''
    历史最大逾期天数
    '''
    if (row['biz009MaxOverdueDays'] >= 7 or row['all002MaxOverdueDays'] >=7) :
        return 'REJECT'
    elif (row['biz009MaxOverdueDays'] >= 4 or row['all002MaxOverdueDays'] >=4)  and row['biz209RegistDate']>="2026-01-01" and row['biz185OldCreditRank']>1:
        return 'REJECT'
    elif  (row['biz009MaxOverdueDays'] > 1 or row['all002MaxOverdueDays'] > 1) and row['model110AllCountryBcardV36Train'] <= 530 and row['biz037AppId']!="sst001_IOS-NBR-001"  and row['biz209RegistDate']>="2026-01-01":
        return 'REJECT'
    elif (row['biz009MaxOverdueDays'] > 1 or row['all002MaxOverdueDays'] > 1) and (row['biz037AppId']=="sst001_IOS-NBR-010"  or row['biz037AppId']=="sst001_IOS-NBR-H5-2"):
        return 'REJECT'
    else:
        return 'PASS'

def DZ6003_iOS(row):
    if row['all010SystemIsDevBlack'] == 1:
        return 'REJECT'
    else:
        return 'PASS'

def DZ7018_iOS(row):
    if row['all068OrderLoanNowTimesAll'] > 20 and (row['biz037AppId']!="sst001_IOS-NBR-008" or row['biz037AppId']!="sst001_IOS-NBR-H5") :
        return 'REJECT'
    elif row['all068OrderLoanNowTimesAll'] > 21 :
        return 'REJECT'
    elif row['biz185OldCreditRank']==3 and row['all068OrderLoanNowTimesAll'] > 18 and row['biz037AppId']=="sst001_IOS-NBR-H5":
        return 'REJECT'
    elif row['biz185OldCreditRank']==3 and row['all068OrderLoanNowTimesAll'] > 10 and row['model249MxBcardV165High']<=530 and row['biz037AppId']!="sst001_IOS-NBR-H5":
        return 'REJECT'
    else:
        return 'PASS'


def DZ7023_iOS(row):
    if row['biz041IsProductReloan']==0 and row['biz113CurrentOTNloaningNum'] > 6 and row['biz037AppId']!="sst001_IOS-NBR-001":
        return 'REJECT'
    elif row['biz041IsProductReloan']==0 and row['biz113CurrentOTNloaningNum'] > 8 and row['biz037AppId']=="sst001_IOS-NBR-001":
        return 'REJECT'
    return 'PASS'

def DZ7019_iOS(row):
    if row['model092MxBcardCreditScoreV18']<=495 and row['biz037AppId']=="sst001_IOS-NBR-H5":
        return 'REJECT'
    elif row['model092MxBcardCreditScoreV18']<=525 and row['biz037AppId']=="sst001_IOS-NBR-H5-2":
        return 'REJECT'
    return 'PASS'


def DZ6009(row):
    if row['all067LoanNowPlatformCnt'] > 1:
        return 'REJECT'
    else:
        return 'PASS'

def DZ6010_iOS(row):
    # if (row['model092MxBcardCreditScoreV18Rank'] >=2 and row['all093OrderLoanTimes5d']>8) and row['biz037AppId'] == "sst001_IOS-NBR-010":
    #     return 'REJECT'
    return 'PASS'  

def DZ6011_iOS(row):
    # if (row['biz146CollectionOutConcatCount7d'] >=25 or row['biz142Sms7dRemindTypeCount']>2) and row['biz037AppId'] == "sst001_IOS-NBR-010":
    #     return 'REJECT'
    return 'PASS'

def DZ6012_iOS(row):
    # if (row['base023MaxDayOverdue'] >3 or row['base028OcrWithNameSimilar']>5 or row['base031Education']<=2) and row['biz037AppId'] == "sst001_IOS-NBR-010":
    #     return 'REJECT'
    return 'PASS'

def DZ5001_iOS(row):
    '''
    历史最大逾期天数
    '''
    if (row['biz103RepayMoneyTotal'] < float(row['biz042NewBeginAmount'])) and row['biz041IsProductReloan']==0 and (row['biz037AppId'] == "sst001_IOS-NBR-010-2" or row['biz037AppId'] == "sst001_IOS-NBR-007"):
        return 'REJECT'
    elif (row['biz103RepayMoneyTotal'] < float(row['biz042NewBeginAmount'])) and row['biz041IsProductReloan']==0 and (row['biz037AppId'] == "sst001_IOS-NBR-H5-3" and row['biz186FirstGetCreditTime'] >= "2026-04-14"):
        return 'REJECT'
    return 'PASS'

def DZ8009(row):
    return 'PASS'

def DZ8001_iOS(row):
    if row['izi004LivenessScore'] == 0:
        return 'REJECT'
    return 'PASS'

def DZ8002_iOS(row):
    if row['izi002FaceSimilarityScore'] >= 0 and row['izi002FaceSimilarityScore'] < 100:
        return 'REJECT'
    return 'PASS'

def DZ7001_iOS(row):
    '''
    iOS贷中模型v1
    '''
    # if row['model010Bcardv1'] <=500 and row['biz504Random4']<=5000:
    #     return 'REJECT'
    return 'PASS'


def DZ7002_iOS(row):
    '''
    iOS贷中模型v5
    '''
    # if row['model023Bcardv5'] <=600:
    #     return 'REJECT'
    # elif row['model023Bcardv5'] <=610  and row['biz504Random4']<=7000 and row['biz037AppId'] != "sst001_IOS-NBR-001":
    #     return 'REJECT'
    return 'PASS'

def DZ7003_iOS(row):
    # if (row['biz037AppId']=="sst001_IOS-NBR-004" and row['model061IosBcardv3'] <=500) :
    #     return 'REJECT'
    return 'PASS'


def DZ7005_iOS(row):
    if row['model074BcardV17'] <=470:
        return 'REJECT'
    elif row['model074BcardV17'] <=520 and row['biz037AppId']=="sst001_IOS-NBR-010":
        return 'REJECT'
    elif row['model074BcardV17'] <=570 and row['biz037AppId']=="sst001_IOS-NBR-009":
        return 'REJECT'
    return 'PASS'

def DZ7006_iOS(row):
    if row['model135BcardV57longtrain'] <=490  and row['biz037AppId']!="sst001_IOS-NBR-001" and row['biz502Random2'] <=5000:
        return 'REJECT'
    elif row['model135BcardV57shortall'] <=485  and row['biz037AppId']=="sst001_IOS-NBR-H5":
        return 'REJECT'
    return 'PASS'

def DZ7007_iOS(row):
    if row['base030appCode'] =="59ldl3u1uc01kt4uqyoqi1p9f7173j6g" and row['biz209RegistDate']<="2025-08-25" and row['biz037AppId']=="sst001_IOS-NBR-H5":
        return 'REJECT'
    elif row['base030appCode'] =="59ldl3u1uc01kt4uqyoqi1p9f7173j6g" and row['biz209RegistDate']<="2025-08-25" and row['biz037AppId']=="sst001_IOS-EMI-MX-001":
        return 'REJECT'
    return 'PASS'

def DZ7008_iOS(row):
    if row['model135BcardV57shortall']<=495 and row['biz039TransBatchCnt']<=3 and row['biz037AppId'] == "sst001_IOS-NBR-010":
        return 'REJECT'
    return 'PASS'

def DZ7009_iOS(row):
    if row['model225MxBcardCreditScoreV141Rank']>=2 and row['all003OverdueTimes']>1:
        return 'REJECT'
    return 'PASS'

def DZ7010_iOS(row):
    if row['model249MxBcardV165High']<=500 and row['biz037AppId'] == "sst001_IOS-NBR-008" :
        return 'REJECT'    
    return 'PASS'

def DZ7011_iOS(row):
    if row['model230MxBcardV146']<=520 and row['biz037AppId'] != "sst001_IOS-NBR-008":
        return 'REJECT' 
    elif row['model230MxBcardV146']<=530 and row['biz037AppId'] == "sst001_IOS-NBR-010-2" and row['biz502Random2'] <=5000:
        return 'REJECT'
    return 'PASS'

def DZ7024_iOS(row):
    if row['model110AllCountryBcardV36Train']<=530 and row['biz037AppId']=="sst001_IOS-NBR-009":
        return 'REJECT'
    return 'PASS'


class VerifyTree:
    
    def A12(self, row):
        free_rules = [DD1001_A12, DD2001, DD2002, DD2003, DD2004, DD2005, DD1002, DD1003, DD1004, DD1005, 
                      DD6001, DD6002, DD6003, DD6006_A12, DD1006, DD1008_A12, DD6005, DD6007, 
                      DD7017_A12, DD1011, DD7027_A12, DD2001_all, DD2002_all, DD2003_all, 
                      DD1003_all, DD1004_all, DD1005_all, DD1006_all, DD7032_A12, DD1012, DD1013, DD7033_A12]
        paid_rules = [DD8002, DD8003, DD8020_A12]
        return free_rules, paid_rules

    def A10(self, row):
        free_rules = [DD1001_iOS_A10, DD2001, DD2002, DD2003, DD2004, DD2005, DD1002, DD1003, DD1004, DD1005, 
                      DD6001, DD6002, DD6003, DD1006, DD6005, DD6007, DD6008_iOS_A10,
                      DD1010_iOS_A10,  DD8001_iOS_A10, 
                      DD1011_iOS_A10,DD2006, DD1013_iOS,DD7004_iOS_A10, DD7005_iOS_A10, DD7006_iOS_A10,DD6009_iOS_A10,
                      DD2001_all, DD2002_all, DD2003_all, DD1003_all, DD1004_all, DD1005_all, DD1006_all, DD1012, DD1013]
        paid_rules = [DD8003_iOS, DD8002_iOS, DD8017, DD8018_iOS_A10]
        return free_rules, paid_rules

    def C02(self, row):
        free_rules = [DD1001_C02, DD2001, DD2002, DD2003, DD2004, DD2005, DD1002, DD1003, DD1004, DD1005, DD6001, DD6002,
                      DD6003_C02, DD8001, DD1006, DD6005,DD3007_C02, DD6007,DD7019_C02,DD1011,
                      DD2001_all, DD2002_all, DD2003_all, DD1003_all, DD1004_all, DD1005_all, DD1006_all, DD1012, DD1013,DD7020_C02,DD7021_C02]
        paid_rules = [DD8002, DD8003]
        return free_rules, paid_rules

    def A09(self, row):
        free_rules = [DD1001_A09, DD2001, DD2002, DD2003, DD2004, DD2005, DD1002, DD1003, DD1004, DD1005, DD4001_A09, 
                      DD6001, DD6002, DD1006, DD1008_A09, DD6005, DD6006_A09,DD6007, DD3007_A09, DD6003_A09, 
                      DD7017_A09, DD7018_A09, DD1011,DD7027_A09,DD7028_A09,DD7029_A09,
                      DD2001_all, DD2002_all, DD2003_all, DD1003_all, DD1004_all, DD1005_all, DD1006_all, DD1012, DD1013]
        paid_rules = [DD8002, DD8003]
        return free_rules, paid_rules
        
    def A14(self, row):
        free_rules = [DD1001_A12, DD2001, DD2002, DD2003, DD2004, DD2005, DD1002, DD1003, DD1004, DD1005, 
                      DD6001, DD6002, DD6003, DD6006_A12, DD1006, DD6005, DD6007, DD3007_A14, DD1011, 
                      DD2001_all, DD2002_all, DD2003_all, DD1003_all, DD1004_all, DD1005_all, DD1006_all, DD7031_A14,
                      DD7017_A14, DD7027_A14, DD1012, DD1013, DD1014_A14, DD1015_A14, DD1016_A14, DD7032_A14]
        paid_rules = [DD8002, DD8003]
        return free_rules, paid_rules
    
    def A15(self, row):
        free_rules = [DD1001_A15, DD2001, DD2002, DD2003, DD2004, DD2005, DD1002, DD1003, DD1004, DD1005, 
                      DD6001, DD6002, DD6003, DD6006_A15, DD1006, DD6005, DD6007, DD1011, 
                      DD2001_all, DD2002_all, DD2003_all, DD1003_all, DD1004_all, DD1005_all, DD1006_all, DD1013, 
                      DD1008_A15, DD7017_A15, DD7026_A15, DD7027_A15, DD7029_A15]
        paid_rules = [DD8002, DD8003]
        return free_rules, paid_rules

    def A05(self, row):
        free_rules = [DD1001_iOS_A05, DD2001, DD2002, DD2003, DD2004, DD2005, DD1002, DD1003, DD1004, DD1005, 
                      DD6001, DD6002, DD6003, DD1006, DD6005, DD6007, DD6008_iOS_A10, DD2006,
                      DD1013_iOS, DD1010_iOS_A05, DD8001_iOS_A05, 
                      DD1011_iOS_A05, DD7006_iOS_A05,DD2007_iOS,
                      DD2001_all, DD2002_all, DD2003_all, DD1003_all, DD1004_all, DD1005_all, DD1006_all, 
                      DD7007_iOS_A05, DD1012, DD1013,DD7008_iOS_A05,DD1013_iOS_A05,DD6009_iOS_A05]
        paid_rules = [DD8003_iOS, DD8002_iOS, DD8017, DD8020_iOS_A05]
        return free_rules, paid_rules

    def B06(self, row):
        free_rules = [DZ2003,DZ2001, DZ6001, DZ6002_B06, DZ6005,DZ7018_B07,DZ6009,DZ7023_B06]
        paid_rules = []
        return free_rules, paid_rules

    def B09(self, row):
        free_rules = [DZ2003,DZ2001,DZ6002_B09,DZ6001,DZ6003_B09,DZ7007,DZ6005,DZ5005,DZ7018_B09,DZ7014_B09,DZ6009,DZ7021,DZ7023_B09,DZ7022_B09,DZ7030_B09,DZ7031_B09,DZ7034_B09]
        paid_rules = []
        return free_rules, paid_rules
    
    
    def B11(self, row):
        free_rules = [DZ2001,DZ6001, DZ6002_iOS, DZ6003_iOS, DZ6005, DZ2006, DZ8001_iOS, DZ6009, 
                      DZ7018_iOS,  DZ1002_iOS, DZ7023_iOS, DZ7006_iOS, DZ7007_iOS,DZ7019_iOS,DZ7024_iOS,DZ5001_iOS, DZ7009_iOS,DZ7010_iOS,DZ7011_iOS]
        paid_rules = []
        return free_rules, paid_rules
    def B12(self, row):
        free_rules = [DZ2003,DZ2001,DZ6002_B12,DZ6001,DZ6003_B09,
                      DZ6005,DZ3003_B12,DZ7018_B12,DZ6009,DZ6010_B12,
                      DZ7023_B12,DZ7031_B12,DZ7033_B12,DZ3004_B12,DZ7035_B12,DZ7036_B12,DZ6011_B12,DZ7037_B12,DZ5001_B12]
        paid_rules = []
        return free_rules, paid_rules
    
    def B13(self, row):
        free_rules = [DZ2003, DZ2001, DZ6002_B13, DZ6001, DZ6003_B13, DZ5001_B13,DZ7007_B13, DZ6005, DZ3003_B13,
                      DZ7018_B13,DZ6009,DZ7023_B13,DZ7030_B13,DZ7031_B13]
        paid_rules = []
        return free_rules, paid_rules

    def _calculate(self, free_rules, paid_rules, row):
        reject_code, refuse_code, hit_free = 'PASS', [], 0

        for free_rule in free_rules:
            if free_rule(row) == 'REJECT':
                code = free_rule.__name__
                if reject_code == 'PASS':
                    reject_code = code
                refuse_code.append(code)
                hit_free = 1

        if hit_free == 0:
            for paid_rule in paid_rules:
                code = paid_rule.__name__
                if paid_rule(row) == 'REJECT':
                    if reject_code == 'PASS':
                        reject_code = code
                    refuse_code.append(code)
                    break
        return reject_code, str(refuse_code)

    # 根据传入的{'A01':['DD8009'], 'B01':[],...}过滤字典，来指定每个风控流需要执行的拒贷函数
    def filter_rules(self, row, risk_flow, risk_flow_filters=None):
        free_rules, paid_rules = getattr(self, risk_flow)(row)
        if risk_flow_filters:
            rule_filter = risk_flow_filters[risk_flow]
            free_rules = [rule for rule in free_rules if rule.__name__ in rule_filter]
            paid_rules = [rule for rule in paid_rules if rule.__name__ in rule_filter]
        return free_rules, paid_rules

    def calculate(self, row, assign=None, risk_flow_filters=None):
        risk_flow = assign or row['biz044RiskFlow']
        free_rules, paid_rules = self.filter_rules(row, risk_flow, risk_flow_filters)
        return self._calculate(free_rules, paid_rules, row)
