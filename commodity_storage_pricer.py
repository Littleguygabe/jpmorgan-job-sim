import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

def trainModel(data,input_date):
    
    working_df = data.copy()
    days = []
    for row in working_df.itertuples():

        date_obj = datetime.datetime.strptime(row.Dates,'%m/%d/%y').date()
        days.append(date_obj.timetuple().tm_yday)

    output_df = pd.DataFrame(days,columns=['DoY'])
    output_df = output_df.join(working_df['Prices'])

    X = output_df['DoY']
    y = output_df['Prices']

    model = np.poly1d(np.polyfit(X,y,3))


    date_obj = datetime.datetime.strptime(input_date,'%m/%d/%y').date()
    target_day = date_obj.timetuple().tm_yday

    price_prediction = model(target_day)
    return price_prediction


if __name__ == '__main__':
    data = pd.read_csv('Nat_Gas.csv')

    prediction = trainModel(data,input('Enter a date to Predict a Price for (mm/dd/yy): '))
    print(f'Price Prediction is: ${prediction}')