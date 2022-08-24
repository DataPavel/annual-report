import utils
from pmdarima.arima import auto_arima
import pandas as pd
import numpy as np
from pandas.tseries.offsets import MonthEnd
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from keras.models import Sequential
from keras.layers import LSTM, Dense
from keras.preprocessing.sequence import TimeseriesGenerator



def list_of_dfs(df):
    dfs = list()
    for i in list(df['Project'].unique()):
        dfs.append(df[df['Project']==i])
    return dfs


def make_arima(df, company, studio, project):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    model = auto_arima(df['Amount_USD'], m=4, seasonal=True, start_p=0, start_q=0, max_order=1,
                  test='adf', error_action='ignore', suppress_warnings=True, stepwise=True, trace=False)
    model.fit(df['Amount_USD'])
    forecast = model.predict(n_periods=12, return_conf_int=True)
    forecast_df = pd.DataFrame(forecast[0], index= df.index[-12:] + MonthEnd(12), columns=['Amount_USD'])
    forecast_df['Company'] = company
    forecast_df['Studio'] = studio
    forecast_df['Project'] = project
    forecast_df = forecast_df[['Company', 'Studio', 'Project', 'Amount_USD']]
    df = pd.concat([df, forecast_df], axis=0)
    return df





def display_all_predictions(df):
    by_project = df.groupby(['Date', 'Company', 'Studio', 'Project']).sum('Amount_USD').reset_index()
    dfs = list_of_dfs(by_project)
    dfs_with_preds = list()
    for i in dfs:
        df_pred = make_arima(i, list(i['Company'])[0], list(i['Studio'])[0], list(i['Project'])[0])
        dfs_with_preds.append(df_pred)
    df_pred = pd.concat(dfs_with_preds, axis=0)
    return df_pred


def model_creation(df, train_portion, window_size, epochs, product):
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Project']==product]
    df_original = df.copy()
    df.set_index('Date', drop=True, inplace=True)
    df['pct_change'] = df.Amount_USD.pct_change()
    df_normalized = df.copy().dropna()
    df1 = df[['pct_change']]
    df1.dropna(inplace=True)

    df_val = df1.values
    # Train test split
    split = int(len(df_val) * train_portion)
    train = df_val[:split]
    test = df_val[split:]
    # Scaling
    scaler = MinMaxScaler(feature_range=(0,1)).fit(train)
    train_scaled = scaler.transform(train)
    test_scaled = scaler.transform(test)
    # Generate X and y
    n_features = 1
    generator = TimeseriesGenerator(train_scaled, train_scaled, length=window_size, batch_size=1)
    #Modeling
    model = Sequential()
    model.add(LSTM(100, activation='relu', input_shape=(window_size, n_features)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    # Fitting the model
    model.fit(generator, epochs=epochs, verbose=False);
    #Return loss per epoch for plotting
    loss_per_epoch = model.history.history['loss']
    # Make predictions
    test_predictions = list()
    first_eval_batch = train_scaled[-window_size:]
    current_batch = first_eval_batch.reshape((1, window_size, n_features))
    for i in range(len(test)):
        current_pred = model.predict(current_batch)[0]
        test_predictions.append(current_pred)
        current_batch = np.append(current_batch[:, 1:, :], [[current_pred]], axis=1)
    # Inverse Transform
    true_predictions = scaler.inverse_transform(test_predictions)
    # Validation
    test_val = df1[:-len(test)]
    test_val['preds'] = np.nan
    pred_val = df1[-len(test):]
    pred_val['preds'] = [x[0] for x in true_predictions]
    test_preds = pd.concat([test_val, pred_val], axis=0).reset_index()
    test_preds['Date_str'] = test_preds['Date'].apply(lambda x: x.strftime("%Y-%m"))
    # Root Mean squared error
    testScore = mean_squared_error(pred_val['pct_change'], pred_val['preds'], squared=False)
    return test_preds, loss_per_epoch, testScore, df_original, df_normalized




def forecast(df, nr_months, window_size, epochs, product):  
   
    df['Date'] = pd.to_datetime(df['Date'])
    df = df[df['Project']==product]
    df_original = df.copy()
    df.set_index('Date', drop=True, inplace=True)
    df['pct_change'] = df.Amount_USD.pct_change()
    df1 = df[['pct_change']]
    df1.dropna(inplace=True)

    df_val = df1.values

    # Scaling
    scaler = MinMaxScaler(feature_range=(0,1)).fit(df_val)
    df_scaled = scaler.transform(df_val)
    # Generate X and y
    n_features = 1
    generator = TimeseriesGenerator(df_scaled, df_scaled, length=window_size, batch_size=1)
    #Modeling
    model = Sequential()
    model.add(LSTM(100, activation='relu', input_shape=(window_size, n_features)))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    # Fitting the model
    model.fit(generator, epochs=epochs, verbose=False);

    # Make predictions
    predictions = list()
    first_eval_batch = df_scaled[-window_size:]
    current_batch = first_eval_batch.reshape((1, window_size, n_features))
    for i in range(nr_months):
        current_pred = model.predict(current_batch)[0]
        predictions.append(current_pred)
        current_batch = np.append(current_batch[:, 1:, :], [[current_pred]], axis=1)
    # Inverse Transform
    true_predictions = scaler.inverse_transform(predictions)
    # Concat with original dataframe
    pct_list = list(df['pct_change'])[1:]+list(true_predictions.flatten())
    amount = list()
    amount.append(df['Amount_USD'][0])
    for i in pct_list:
        amount.append(amount[-1] * (1+i))

    preds = pd.DataFrame(index = df1.index[-nr_months:] + MonthEnd(nr_months))
    # preds.index = df1.index[-nr_months:] + MonthEnd(nr_months)


    preds['Date_str'] = preds.index.strftime("%Y-%m")
    preds['Company'] = df['Company'][0]
    preds['Studio'] = df['Studio'][0]
    preds['Project'] = df['Project'][0]
    preds['Amount_USD'] = np.nan
    preds['pct_change'] = true_predictions.flatten()
    preds['color'] = np.where(preds['Amount_USD']<0, '#F43B76', '#037A9C')
    act_preds = pd.concat([df, preds], axis=0)
    act_preds['Amount_USD']=amount
    act_preds = act_preds.reset_index()
    return act_preds