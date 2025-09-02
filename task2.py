# any trade agreement is as valuable as the price you can sell minus the price at which you are able to buy. 
# Any cost incurred as part of executing this agreement is also deducted from the overall value.
    # basically value of the agreement is:
#       sell price - (buy price + execution costs)   (so total diff between selling value and cost)

# from example:
#   calculate the value before any execution costs, then subtract the execution costs from the value if there were no extra costs

from commodity_storage_pricer import generatePrediction #to be able to price the purchase price of natural gas at any given point
from datetime import datetime

def commodityPricingModel(inj_dates,wd_dates,max_volume,storage_costs,inj_amount_arr,wd_amount_arr):
    total_inj_cost = 0
    remaining_vol = max_volume

    if sum(inj_amount_arr)>max_volume:
        print(f'Will not be able to Store all the gas as max Volume - {max_volume} - is less than Total Injection Amount - {sum(inj_amount_arr)}')

    for date,vol in zip(inj_dates,inj_amount_arr):
        price = generatePrediction(date)
        vol_injected = min(vol,remaining_vol)

        total_inj_cost+= (price*vol_injected)
        remaining_vol-=vol


    amount_stored = max_volume-remaining_vol

    total_wd_amnt = sum(wd_amount_arr)
    if total_wd_amnt>amount_stored:
        print('Currently Trying to withdraw more volume than there is stored')

    total_sell_price = 0
    for date,vol in zip(wd_dates,wd_amount_arr):
        sell_price = generatePrediction(date)
        vol_withdrawn = min(amount_stored,vol)
        total_sell_price+= sell_price*vol_withdrawn

        amount_stored -= vol_withdrawn

    # find the amount of time volume was stored for
    # find the number of days between each injection and the amount being stored

    # find the time to the first withdrawal (ie how long we spend with the most volume stored)
    # find the number of days between each injection until there is no volume left 

    total_storage_costs = 0

    negated_wd_arr = [x*-1 for x in wd_amount_arr]
    all_dates = inj_dates+wd_dates
    all_movements = inj_amount_arr+negated_wd_arr

    for i in range(len(all_dates)-1):
        months_between = getMonthsBetween(all_dates[i],all_dates[i+1])
        

def getMonthsBetween(date_1,date_2):
    format = '%m/%d/%y'
    d1 = datetime.
    
        


if __name__ == '__main__':
    inj_dates = ['11/20/21','6/4/23']
    wd_dates = ['8/27/24']
    max_storage_volume = 1000 #units
    storage_costs = 2 #cost per unit
    inj_amount_arr = [500,200]
    wd_amount_arr = [700]

    commodityPricingModel(inj_dates,wd_dates,max_storage_volume,storage_costs,inj_amount_arr,wd_amount_arr)
