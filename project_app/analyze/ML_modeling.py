import pandas as pd
from sklearn.model_selection import train_test_split
from category_encoders import OrdinalEncoder
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
from sklearn.impute import SimpleImputer
from sklearn.pipeline import make_pipeline
from xgboost import XGBRegressor
import numpy as np
import datetime
import sqlite3
import pickle

df = pd.read_csv('../test_project.csv')
# 간단한 EDA 진행
df.drop(['Unnamed: 0'], axis='columns', inplace=True)
# df['Date'] = pd.to_datetime(df['Date'])?
category_col = ['City', 'Region']
df[category_col] = df[category_col].astype('category')

# target, features 설정
target = 'rate'
features = df.columns.drop(target)

#test, train data 설정
X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

# model 설계
encoder = OrdinalEncoder()
X_train_encoded = encoder.fit_transform(X_train) # 학습데이터
X_test_encoded = encoder.transform(X_test) # 검증데이터

boosting = XGBRegressor(
    n_estimators=2000,
    objective='reg:squarederror', # default
    learning_rate=0.2,
    n_jobs=-1
)

eval_set = [(X_train_encoded, y_train), 
            (X_test_encoded, y_test)]

boosting.fit(X_train_encoded, y_train, 
          eval_set=eval_set,
          early_stopping_rounds=50
         )

def predict(City, Region, Num_households, Num_mibunyang, Num_trade, Num_permission):
    Date = datetime.today().strftime("%Y-%m-%d")
    df = pd.DataFrame(
        data = [[City, Region, Date, Num_households, Num_mibunyang, Num_trade, Num_permission]],
        columns=['City', 'Region', 'Date', 'Num_households', 'Num_mibunyang', 'Num_trade', 'Num_permission']
    )
    df_encoded = encoder.transform(df)
    pred = boosting.predict(df_encoded)

# with open('../model.pkl','wb') as pickle_file:
#     pickle.dump(boosting, pickle_file)

# with open('../encoder.pkl','wb') as pickle_file:
#     pickle.dump(encoder, pickle_file)