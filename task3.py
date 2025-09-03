# generate a prediction for if someone is going to default on their loan
from sklearn.model_selection import train_test_split
import xgboost as xgb
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

        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.2,random_state=42)

        self.model = xgb.XGBClassifier(  
            objective='binary:logistic',  
            eval_metric = 'logloss',      
            max_depth=3,
            learning_rate=0.1,
            n_estimators = 1000,
            use_label_encoder=False 
        )

        self.model.fit(
            X_train,y_train,
            eval_set=[(X_test,y_test)],
        )
        

    def generatePrediction(self,input_data):
        print(input_data.columns)
        X = input_data.drop(['customer_id'],axis=1)
        y = self.model.predict(X)

        return y
    
if __name__ == '__main__':
    data = pd.read_csv('loan_data.csv')

    xgboost_model = xgboost_trainer(data)

    pred_data = data.loc[[random.randint(0,len(data)-1)]].reset_index(drop=True).drop(['default'],axis=1)
    prediction = xgboost_model.generatePrediction(pred_data)
    print(pred_data)
    print(f'Prediction Value: {prediction}')