import logging

from flask_pymongo import pymongo
from flask import jsonify, request
import pandas as pd
import pickle
import calendar
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import warnings
import itertools
import statsmodels.api as sm
import statsmodels.tsa.api as smt
import statsmodels.formula.api as smf 
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.seasonal import seasonal_decompose



con_string = "mongodb+srv://poojhamuralidharan:tomandjerry@cluster0.o0fvffu.mongodb.net/?retryWrites=true&w=majority"

client = pymongo.MongoClient(con_string)

db = client.get_database('projectdb')

user_collection = pymongo.collection.Collection(db, 'prodb') #(<database_name>,"<collection_name>")
print("MongoDB connected Successfully")


def project_api_routes(endpoints):
    @endpoints.route('/hello', methods=['GET'])
    def hello():
        res = 'Hello world'
        print("Hello world")
        return res
    # def eda():
    #     pickleFile = open(" ","rb")
    #     df = pickle.load(open(" ", "rb"))
    #     dates=pd.date_range(start='2003-01-01',freq='MS',periods=len(df))
    #     df["Month"]=dates.month
    #     df["Year"]=dates.year 
    #     df['Month']=df['Month'].apply(lambda x:calendar.month_abbr[x]) 
    #     df.drop("Month-Year",axis=1,inplace=True)
    #     df.rename(columns={"Number of Tractor Sold":"Tractors-Sold"},inplace=True)     
    #     df["dates"]=dates
    #     df.set_index(dates,inplace=True)
    #     df.drop("dates",axis=1,inplace=True)
    #     tractor_sales=df["Tractors-Sold"]
    #     rolemean=tractor_sales.rolling(window=12).mean()
    #     rolestd=tractor_sales.rolling(window=12).std()
    #     from statsmodels.tsa.stattools import adfuller
    #     dftest=adfuller(tractor_sales,autolag='AIC')


    @endpoints.route('/register-user', methods=['POST'])
    def register_user():
        resp = {}
        try:
            req_body = request.json
            # print(f"Received request body: {req_body}")
            user_data = {
            "name": req_body.get("name"),
            "email": req_body.get("email"),
            "password": req_body.get("pass")
        }
            user_collection.insert_one(user_data)
            # user_collection.insert_one(req_body)            
            print("User Data Stored Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Stored Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp
    # @endpoints.route('/dashboard',methods=['POST'])
    # def
    @endpoints.route('/login',methods=['POST'])
    def login():
        resp={}
        try:
            username=request.json['uname']
            password=request.json['pass']
            # print(username)
            # print(password)
            user=user_collection.find_one({'name':username})
            if user['name']==username and user['password']==password:
                # print(user)
                # print("------------------------------------------")
                # print("------------------------------------------")
                status = {
                "statusCode":200,
                "statusMessage":"User Data Stored Successfully in the Database."
            }
            else:
                status = {
                "statusCode":400,
                "statusMessage":"User Data not Stored Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":400,
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp


   

    @endpoints.route('/read-users',methods=['GET'])
    def read_users():
        resp = {}
        try:
            users = user_collection.find({})
            print(users)
            users = list(users)
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Retrieved Successfully from the Database."
            }
            output = [{'Name' : user['name'], 'Email' : user['email']} for user in users]   #list comprehension
            resp['data'] = output
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp

    @endpoints.route('/update-users',methods=['PUT'])
    def update_users():
        resp = {}
        try:
            req_body = request.json
            # req_body = req_body.to_dict()
            user_collection.update_one({"id":req_body['id']}, {"$set": req_body['updated_user_body']})
            print("User Data Updated Successfully in the Database.")
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Updated Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp    

    @endpoints.route('/delete',methods=['DELETE'])
    def delete():
        resp = {}
        try:
            delete_id = request.args.get('delete_id')
            user_collection.delete_one({"id":delete_id})
            status = {
                "statusCode":"200",
                "statusMessage":"User Data Deleted Successfully in the Database."
            }
        except Exception as e:
            print(e)
            status = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        resp["status"] =status
        return resp
    
    @endpoints.route('/file_upload',methods=['POST'])
    def file_upload():
        resp = {}
        try:
            # req = request.form
            file = request.files.get('file')
            number= int(request.form.get('number'))
            selected=request.form.get('selected')
            periodicity=request.form.get('periodicity'
                                         )
            # df = pd.read_csv(file)
            if periodicity==("Monthly"):
                s='MS'
            elif(periodicity=="Weekly"):
                s='W'   
            else:
                s='YS' 
            dataset=pd.read_csv(file)
            dataset.head(5)
            dates=pd.date_range(start='2003-01-01',freq='MS',periods=len(dataset))
            dataset['month']=dates.month 
            dataset['year']=dates.year
            dataset['month']=dataset['month'].apply(lambda x:calendar.month_abbr[x])
            dataset.drop(['Month-Year'],axis=1,inplace=True)
            dataset.rename(columns={'Number of Tractor Sold':'Tractor-Sales'},inplace=True)
            dataset.set_index(dates,inplace=True)
            dataset=dataset[['month','year','Tractor-Sales']]
            sales_ts=dataset['Tractor-Sales']
            sales_ts.rolling(window=2)
            rolemean=sales_ts.rolling(window=12).mean()
            rolestd=sales_ts.rolling(window=12).std()
            dftest=adfuller(sales_ts,autolag='AIC')
            st=adfuller(sales_ts,autolag='AIC')
            decomposition=seasonal_decompose(sales_ts,model='multiplicative')
            trend=decomposition.trend
            seasonal=decomposition.seasonal
            residual=decomposition.resid
            sales_ts_log = np.log10(sales_ts)
            sales_ts_log.dropna(inplace=True)
            sales_ts_log_diff = sales_ts_log.diff(periods=1) 
            sales_ts_log_diff.dropna(inplace=True)
            p = d = q = range(0, 2)
            pdq = list(itertools.product(p, d, q))
            seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
            best_aic = np.inf
            best_pdq = None
            best_seasonal_pdq = None
            temp_model = None
            for param in pdq:
                for param_seasonal in seasonal_pdq:
                    
                    try:
                        temp_model = sm.tsa.statespace.SARIMAX(sales_ts_log,
                                                        order = param,
                                                        seasonal_order = param_seasonal,
                                                        enforce_stationarity=True,
                                                        enforce_invertibility=True)
                        results = temp_model.fit()
                        if results.aic < best_aic:
                            best_aic = results.aic
                            best_pdq = param
                            best_seasonal_pdq = param_seasonal
                    except:
                        #print("Unexpected error:", sys.exc_info()[0])
                        continue
        #print("Best SARIMAX{}x{}12 model - AIC:{}".format(best_pdq, best_seasonal_pdq, best_aic))
            best_model = sm.tsa.statespace.SARIMAX(sales_ts_log,
                                      order=(0, 1, 1),
                                      seasonal_order=(1, 0, 1, 12),
                                      enforce_stationarity=True,
                                      enforce_invertibility=True)
            best_results = best_model.fit()
            pred_dynamic = best_results.get_prediction(start=pd.to_datetime('2012-01-01'), dynamic=True, full_results=True)
            pred_dynamic_ci = pred_dynamic.conf_int()
            sales_ts_truth = sales_ts_log['2011-01-01':]
            sales_ts_forecasted = pred_dynamic.predicted_mean
            axis = sales_ts['2006':].plot(label='Observed', figsize=(10, 6))
            np.power(10, pred_dynamic.predicted_mean).plot(ax=axis, label='Dynamic Forecast', alpha=0.7)
            axis.fill_between(pred_dynamic_ci.index, pred_dynamic_ci.iloc[:, 0], pred_dynamic_ci.iloc[:, 1], color='k', alpha=.25)
            axis.fill_betweenx(axis.get_ylim(), pd.to_datetime('2011-01-01'), sales_ts.index[-1], alpha=.1, zorder=-1)
            axis.set_xlabel('Years')
            axis.set_ylabel('Tractor Sales')
            plt.legend(loc='best')
            plt.show()
            plt.close()

            pred_uc_99 = best_results.get_forecast(steps=number, alpha=0.01) 
            pred_uc_95 = best_results.get_forecast(steps=number, alpha=0.05) 
            pred_ci_99 = pred_uc_99.conf_int()
            pred_ci_95 = pred_uc_95.conf_int()
            idx = pd.date_range(sales_ts.index[-1], periods=number, freq=s)
            fc_95 = pd.DataFrame(np.column_stack([np.power(10, pred_uc_95.predicted_mean), np.power(10, pred_ci_95)]), 
                                index=idx, columns=['forecast', 'lower_ci_95', 'upper_ci_95'])
            fc_99 = pd.DataFrame(np.column_stack([np.power(10, pred_ci_99)]), 
                                index=idx, columns=['lower_ci_99', 'upper_ci_99'])
            fc_all = fc_95.combine_first(fc_99)
            fc_all = fc_all[['forecast', 'lower_ci_95', 'upper_ci_95', 'lower_ci_99', 'upper_ci_99']] 
            axis = sales_ts.plot(label='Observed', figsize=(15, 6))
            fc_all['forecast'].plot(ax=axis, label='Forecast', alpha=0.7)
            axis.set_xlabel('Years')
            axis.set_ylabel('Tractor Sales')
            plt.legend(loc='best')
            plt.show()



        




            resp['data']=dataset.to_dict(orient='records')
            resp['status']={
            status := {
                "statusCode":"200",
                "statusMessage":"File uploaded Successfully."
            }
            }
        except Exception as e:
            print(e)
            resp['status'] = {
                "statusCode":"400",
                "statusMessage":str(e)
            }
        # resp["status"] =status
        return jsonify(resp)


    return endpoints
