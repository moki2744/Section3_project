from flask import Blueprint, render_template, request
import pandas as pd
from datetime import datetime
import plotly
import plotly.express as px
import json
import pickle

with open('project_app/views/model.pkl','rb') as pickle_file:
    model = pickle.load(pickle_file)
with open('project_app/views/encoder.pkl','rb') as pickle_file:
    encoder = pickle.load(pickle_file)
    
# 데이터프레임으로 가져오기(시각화를 위한)
df = pd.read_csv('project_app/test_project.csv')
df.drop(['Unnamed: 0'], axis='columns', inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
category_col = ['City', 'Region']
df[category_col] = df[category_col].astype('category')

predict_bp = Blueprint('predict', __name__, url_prefix='/predict')
City = None
Region = None
Num_households = None
Num_mibunyang = None
Num_trade = None
Num_permission = None

#도시
@predict_bp.route('/City')
def predict():        
    return render_template("ML_predict_City.html"), 200
#지역
@predict_bp.route('/Region',methods = ['POST', 'GET'])
def get_city():
   if request.method == 'POST':
      global City
      City = request.form['city']
      if City == '강원':
        myList = ['춘천시','원주시','강릉시','동해시','태백시','속초시','삼척시']
      elif City == '경기':
        myList = ['수원시','성남시','의정부시','안양시','부천시','광명시','평택시','동두천시','안산시','고양시','과천시','구리시','남양주시','오산시','시흥시','군포시','의왕시','하남시','용인시','파주시','이천시','안성시','김포시','화성시','광주시','양주시','포천시','여주시']
      elif City == '경남':
        myList = ['창원시','진주시','통영시','사천시','김해시','김해시','밀양시','거제시','양산시']
      elif City == '경북':
        myList = ['포항시','경주시','김천시','안동시','구미시','영주시','영천시','상주시','문경시','경산시','칠곡군']
      elif City == '광주':
        myList = ['동구','서구','남구','북구','광산구']
      elif City == '대구':
        myList = ['중구','동구','서구','남구','북구','수성구','달서구','달성군']
      elif City == '대전':
        myList = ['동구','중구','서구','유성구','대덕구']
      elif City == '부산':
        myList = ['중구','서구','동구','영도구','부산진구','동래구','남구','북구','해운대구','사하구','금정구','연제구','수영구','사상구','기장군']
      elif City == '서울':
        myList = ['종로구','중구','용산구','성동구','광진구','동대문구','중랑구','성북구','강북구','도봉구','노원구','은평구','서대문구','마포구','양천구','강서구','구로구','금천구','영등포구','동작구','관악구','서초구','강남구','송파구','강동구']
      elif City == '울산':
        myList = ['중구','남구','동구','북구','울주군']
      elif City == '인천':
        myList = ['중구','동구','미추홀구','연수구','남동구','부평구','계양구','서구']
      elif City == '전남':
        myList = ['목포시','여수시','순천시','나주시','광양시','무안군']
      elif City == '전북':
        myList = ['전주시','익산시','정읍시','남원시','김제시']
      elif City == '제주':
        myList = ['제주시','서귀포시']
      elif City == '충남':
        myList = ['천안시','공주시','보령시','아산시','서산시','논산시','계룡시','당진시']
      elif City == '충북':
        myList = ['청주시','충주시','제천시','음성군']
      return render_template("ML_predict_Region.html", city = City, myList = myList)
# 세대수
@predict_bp.route('/Num_households',methods = ['POST'])
def get_households():
   if request.method == 'POST':
      global Region, City
      Region = request.form['Region']
      recent_Num_households = df[(df['City'] == City) & (df['Region'] == Region)].iloc[-1].Num_households
      return render_template("ML_predict_Num_households.html", City = City, Region = Region, recent_Num_households = recent_Num_households)
#미분양
@predict_bp.route('/Num_mibunyang',methods = ['POST'])
def get_mibunyang():
   if request.method == 'POST':
      global Num_households
      Num_households = request.form['Num_households']
      recent_Num_mibunyang = df[(df['City'] == City) & (df['Region'] == Region)].iloc[-1].Num_mibunyang
      return render_template("ML_predict_Num_Mibunyang.html", City = City, Region = Region, Num_households = Num_households, 
      recent_Num_mibunyang = recent_Num_mibunyang)
#거래량
@predict_bp.route('/Num_trade',methods = ['POST'])
def get_trade():
   if request.method == 'POST':
      global Num_mibunyang
      Num_mibunyang = request.form['Num_mibunyang']
      recent_Num_trade = df[(df['City'] == City) & (df['Region'] == Region)].iloc[-1].Num_trade
      return render_template("ML_predict_Num_trade.html",City = City, Region = Region, Num_households = Num_households, 
      Num_trade = Num_trade, recent_Num_trade = recent_Num_trade)
#건축허가
@predict_bp.route('/Num_permission',methods = ['POST'])
def get_permission():
   if request.method == 'POST':
      global Num_trade
      Num_trade = request.form['Num_trade']
      return render_template("ML_predict_Num_permission.html", City = City, Region = Region, Num_households = Num_households, 
      Num_mibunyang = Num_mibunyang, Num_trade = Num_trade)

#결과 분석
@predict_bp.route('/result', methods = ['POST'])
def get_result():
   if request.method == 'POST':
      global Num_permission, City, Region, Num_households, Num_mibunyang, Num_trade
      Num_permission = request.form['Num_permission']
      pred = predict(City, Region, int(Num_households), int(Num_mibunyang), int(Num_trade), int(Num_permission))

      df_select = df[(df['City']==City) & (df['Region']==Region)]
      fig1 = px.line(df_select, x='Date', y='Num_households', title='세대수 변화')
      graph1JSON = json.dumps(fig1, cls=plotly.utils.PlotlyJSONEncoder)
      fig2 = px.line(df_select, x='Date', y='Num_mibunyang', title='미분양 물량 변화')
      graph2JSON = json.dumps(fig2, cls=plotly.utils.PlotlyJSONEncoder)
      fig3 = px.line(df_select, x='Date', y='Num_trade', title='거래량 변화')
      graph3JSON = json.dumps(fig3, cls=plotly.utils.PlotlyJSONEncoder)
      fig4 = px.line(df_select, x='Date', y='rate', title='가격 지수 변화')
      graph4JSON = json.dumps(fig4, cls=plotly.utils.PlotlyJSONEncoder)
      return render_template("ML_predict_result.html", pred = pred, City = City, Region = Region, graph1JSON = graph1JSON, graph2JSON = graph2JSON, graph3JSON = graph3JSON, graph4JSON = graph4JSON)


def predict(City, Region, Num_households, Num_mibunyang, Num_trade, Num_permission):
    Date = datetime.today().strftime("%Y-%m-%d")
    df = pd.DataFrame(
        data = [[City, Region, Date, Num_households, Num_mibunyang, Num_trade, Num_permission]],
        columns=['City', 'Region', 'Date', 'Num_households', 'Num_mibunyang', 'Num_trade', 'Num_permission']
    )
    df_encoded = encoder.transform(df)
    pred = model.predict(df_encoded)
    return pred