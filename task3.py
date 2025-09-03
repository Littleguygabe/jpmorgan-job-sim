# generate a prediction for if someone is going to default on their loan
from sklearn.model_selection import train_test_split
import xgboost as xgb
import numpy as np
from sklearn.metrics import r2_score,mean_squared_error
import pandas as pd
import random



class xgboost_trainer():
    def __init__(self,input_data) -> None:
        self.raw_data = input_data
        self.target_col = 'default'

        self.trainModel()

    def trainModel(self):
        X = self.raw_data.drop(['customer_id',self.target_col],axis=1)
        y = self.raw_data[self.target_col]

        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.1,random_state=42)

        self.model = xgb.XGBRegressor(
            objective='reg:squarederror',
            max_depth=3,
            learning_rate=0.1,
            eval_metric = 'rmse',
            n_estimators = 100
        )

        self.model.fit(
            X_train,y_train,
            eval_set=[(X_test,y_test)],
            verbose=False
        )

        preds = self.model.predict(X_test)

        rmse = np.sqrt(mean_squared_error(y_test, preds))
        r2 = r2_score(y_test, preds)
        print('XGboost Algorithm Finished Training')
        print(f"Root Mean Squared Error (RMSE): {rmse}")
        print(f"R-squared: {r2}")

    def generatePrediction(self,input_data):
        X = input_data.drop(['customer_id'])
        y = self.model.predict(X)

        return y
    
if __name__ == '__main__':
    data = pd.read_csv('loan_data.csv')

    xgboost_model = xgboost_trainer(data)

    pred_data = data.iloc[random.randint(0,len(data)-1)]
    prediction = xgboost_model.generatePrediction(pred_data)
    print(pred_data)
    print(f'Prediction Value: {prediction}')