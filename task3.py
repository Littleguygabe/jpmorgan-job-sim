# generate a prediction for if someone is going to default on their loan
from sklearn.model_selection import train_test_split
import xgboost as xgb
import pandas as pd
import matplotlib.pyplot as plt



class xgboost_trainer():
    def __init__(self,input_data) -> None:
        self.raw_data = input_data
        self.target_col = 'default'

        self.trainModel()

    def trainModel(self):
        X = self.raw_data.drop(['customer_id',self.target_col],axis=1)
        print(X.columns)
        y = self.raw_data[self.target_col]

        X_train,X_test,y_train,y_test = train_test_split(X,y,test_size = 0.3,random_state=42)

        self.model = xgb.XGBClassifier(  
            objective='binary:logistic',  
            eval_metric = 'logloss',      
            max_depth=3,
            learning_rate=0.1,
            n_estimators = 500,
            use_label_encoder=False 
        )

        self.model.fit(
            X_train,y_train,
            eval_set=[(X_test,y_test)],
            verbose=False
        )
        

    def generatePrediction(self,input_data):
        X = input_data.drop(['customer_id'],axis=1)
        y = self.model.predict_proba(X)

        return y[0]
    
if __name__ == '__main__':
    data = pd.read_csv('loan_data.csv')

    xgboost_model = xgboost_trainer(data)
 
    test_data = pd.read_csv('loan_testing_data.csv')
    for i in range(len(test_data)):
        pred_data = test_data.loc[[i]].reset_index(drop=True)
        prediction = xgboost_model.generatePrediction(pred_data.drop(['default'],axis=1))
        p0,p1 = prediction
        print(f'Predictions > Non-Default: {round(p0*100,3)}%, Default: {round(p1*100,3)}%\n')

    xgb.plot_importance(xgboost_model.model)
    plt.show()