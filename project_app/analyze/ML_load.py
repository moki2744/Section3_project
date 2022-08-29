import pickle
import pandas as pd
from datetime import datetime


model = None
with open('model.pkl','rb') as pickle_file:
   model = pickle.load(pickle_file)

with open('encoder.pkl','rb') as pickle_file:
   encoder = pickle.load(pickle_file)

def predict(City, Region, Num_households, Num_mibunyang, Num_trade, Num_permission):
    Date = datetime.today().strftime("%Y-%m-%d")
    df = pd.DataFrame(
        data = [[City, Region, Date, Num_households, Num_mibunyang, Num_trade, Num_permission]],
        columns=['City', 'Region', 'Date', 'Num_households', 'Num_mibunyang', 'Num_trade', 'Num_permission']
    )
    df_encoded = encoder.transform(df)
    pred = model.predict(df_encoded)
    breakpoint()
    print(pred)
predict('대구','달서구',50000,2000,4000,2000)

