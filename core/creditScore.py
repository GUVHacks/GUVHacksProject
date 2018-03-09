import numpy as np
import pandas as pd

#Param list:
#country: string: "Italy" or "Germany" or "France"
#curIncMo: int or float: current monthly income if user input is hourly wage, 
#            curIncMo = 200*wage (consider working 200 hours per month)
#workExp: boolean. If user has work experience: True, else: False
#bankAcc: Boolean. If user has bank account: True, else: False
#bankBal: int or float: user's bank account balance
#cashBal: int or float: user's cash available for purchase
#arrLenMo: int: months that the user has been to Europe
#outDebt: Boolean: if the user has outstanding debt/loan from bank or NGO: True
#outDebtAmt: int or float: amount of the debt 
#outDebtTerm: int: number of months for the debt
#paidDebt: Boolean: if the user has been issued loan and the loan has been fully repaid
#misPay: Boolean: if the user has any missed payment in the past 2 years 
#misPayFreq: int: total frequencies the user missed a payment in the past 2 years 
 

def creditScore(country, curIncMo, curHouseExp,workExp, bankAcc, bankBal, cashBal,arrLenMo,outDebt, outDebtAmt, outDebtTerm, paidDebt, misPay, misPayFreq):
    arrLen = arrLenMo / 12
    if not workExp and curIncMo ==0:
        return 0
    
    df = pd.read_csv('EUEmployment.csv')
    moneyAvail = bankBal + cashBal

    if outDebt:
        moLIAB = outDebtAmt/outDebtTerm
    else: 
        moLIAB = 0
    pt = 0
    
    if (misPay) & (misPayFreq/arrLen >=2): 
        pt = pt - np.log(misPayFreq)*10/min(arrLen,2)
    else:
        pt = pt+20
        
    if (curHouseExp+moLIAB)/curIncMo > float(df.loc[df['country'] == country,'housePercent']):
        penalty =((curHouseExp+moLIAB)/curIncMo-float(df.loc[df['country'] == country,'housePercent'])) *100
        if penalty > 30:
            penalty = 30
        pt = pt - penalty
    else:
        pt = pt+30
        
    if arrLen > 1:
        pt = pt+np.log(arrLen)*10
        
    if bankAcc:
        pt = pt+5
        
    if moneyAvail < curHouseExp:
        print('Warning, too low cash')
    elif moneyAvail < curHouseExp * 2.5:
        print('Too low cash')
    elif moneyAvail > curIncMo * 2.5:
        pt = pt +20
    if paidDebt:
        pt = pt +30
    
    return int(min(pt,100))
        



