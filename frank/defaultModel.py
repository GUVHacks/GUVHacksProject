import random

class applicant:
    # creditScore: int: credit score of the applicant
    # curEmploy: Boolean. If the person is currently employeed, True
    # curIncMo: int or float. if currently employeed, the monthly salary 
    # bankBal: int or float: money in the bank account
    # full_time: boolean: if the person has full time job
    # reminTerm: int: if there person is contracted, how many months remaining for the contract
    # avgInc: int or float: average income 
    def __init__(self,creditScore,curEmploy,curIncMo,bankBal,full_time,remainTerm,avgInc):
        self.creditScore = creditScore
        self.curIncMo= curIncMo
        self.bankBal = bankBal
        self.full_time = full_time
        self.remainTerm = remainTerm
        if full_time:
            self.remainTerm = 12
        self.curIncMo = curIncMo
        if not curEmploy:
            self.curIncMo = avgInc
        self.avgInc = avgInc
        
    
#def defaultRatio(applicantList,rent,employment):
##    df = pd.read_csv('EUEmployment.csv')
#    indivRent = rent/len(applicantList)
#    
#    avgCreditScore = np.mean([i.creditScore for i in applicantList])
#    print(avgCreditScore)
#    for app in applicantList: 
#        groupBal = groupBal+ app.bankBal
#    begBal = groupBal
#    for i in range(12):
#        for app in applicantList: 
#            fixedExp = indivRent*2
#            if app.remainTerm ==0:
#                newJob = np.random.binomial(1,.7)
#                # applicant get the new job 
#                if newJob==1:
#                    app.remainTerm = np.random.randint(0,high = 3)
#                    app.bankBal = app.bankBal + app.curIncMo - fixedExp
#                # the case that applicant doesn't get the new job
#                else:
#                    app.bankBal = app.bankBal - fixedExp
#            else:
#                app.bankBal = app.bankBal + app.curIncMo - fixedExp
#                app.remainTerm  = app.remainTerm - 1
#            if app.bankBal < 0:
#                app.defaultTime = app.defaultTime +1
#                print('gg at month', i +1)
#        groupBal = 0
#        for app in applicantList: 
#            groupBal = groupBal+ app.bankBal
#        if groupBal <0:
#            print('group default')
#        print(groupBal)
#    
#    print('diff', groupBal - begBal)
#    
#        
#a1 = applicant(80,True,1000,200,False,1,900)
#
#defaultRatio([a1],300,'Italy')
#

    
                
def individualDefaultRatio(app,rent,employment):
#    df = pd.read_csv('EUEmployment.csv')
    result = [0]*12
    for j in range(1000):
        for i in range(12):
            fixedExp = rent*2
            if app.remainTerm ==0:
                newJob = 1 if random.uniform(0,1)<.7 else 0
                # applicant get the new job 
                if newJob==1:
                    app.remainTerm = random.randint(0,3)
                    app.bankBal = app.bankBal + app.curIncMo - fixedExp
                # the case that applicant doesn't get the new job
                else:
                    app.bankBal = app.bankBal - fixedExp
            else:
                app.bankBal = app.bankBal + app.curIncMo - fixedExp
                app.remainTerm  = app.remainTerm - 1
            if app.bankBal < 0:
                result[i] = result[i]+1
    return result

a1 = applicant(80,True,1000,200,False,1,900)
individualDefaultRatio(a1,)