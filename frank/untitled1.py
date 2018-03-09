import numpy as np
import pandas as pd

def creditScore(country, curIncMo, curHouseExp,workExp, bankAcc, bankBal, cashBal,arrLen,outDebt, outDebtAmt, outDebtTerm, paidDebt, misPay, misPayFreq):
    if not workExp and curIncMo ==0:
        return 0
    
    df = pd.read_csv('EUEmployment.csv')
    moneyAvail = bankBal + cashBal
    if outDebt:
        moLIAB = outDebtAmt/outDebtTerm
    else: 
        moLIAB = 0
    pt = 50
    
    if (misPay) & (misPayFreq/arrLen >=2): 
        pt = pt - np.log(misPayFreq)*5/arrLen
    else:
        pt = pt+10
        
    if (curHouseExp+moLIAB)/curIncMo > float(df.loc[df['country'] == country,'housePercent']):
        penalty =((curHouseExp+moLIAB)/curIncMo-float(df.loc[df['country'] == country,'housePercent'])) *100
        if penalty > 20:
            penalty = 20
        pt = pt - penalty
    else:
        pt = pt+10

    if arrLen >=3:
        pt = pt+10
    elif arrLen >= 2:
        pt = pt +5
    
    if bankAcc:
        pt = pt+5
        
    if moneyAvail < curHouseExp:
        print('Warning, too low cash')
#        pt = pt - 10
    elif moneyAvail < curHouseExp * 2.5:
        print('Too low cash')
#        pt = pt - 5
    elif moneyAvail > curIncMo * 2.5:
        pt = pt +5
    if paidDebt:
        pt = pt +30
    
    return min(pt,100)
        
#creditScore('Italy',1000,300,True,100,100,2,False,0,0,False,False,0)   
#    
#creditScore('Italy',1000,200,True,1000,100,5,False,0,0,False,False,0)   


creditScore('Italy',200,200,True, True,50,100,1,False,0,0,False,False,0)   





