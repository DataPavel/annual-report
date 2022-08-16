import utils
from pmdarima.arima import auto_arima
import pandas as pd
from pandas.tseries.offsets import MonthEnd


def list_of_dfs(df):
    dfs = list()
    for i in list(df['Project'].unique()):
        dfs.append(df[df['Project']==i])
    return dfs


def make_arima(df, project):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    model = auto_arima(df['Amount_USD'], m=2, seasonal=True, start_p=0, start_q=0, max_order=1,
                  test='adf', error_action='ignore', suppress_warnings=True, stepwise=True, trace=False)
    model.fit(df['Amount_USD'])
    forecast = model.predict(n_periods=12, return_conf_int=True)
    forecast_df = pd.DataFrame(forecast[0], index= df.index + MonthEnd(12), columns=['Amount_USD'])
    forecast_df['Project'] = project
    forecast_df = forecast_df[['Project', 'Amount_USD']]
    df = pd.concat([df, forecast_df], axis=0)
    return df





def display_all_predictions(df):
    by_project = df.groupby(['Date', 'Project']).sum('Amount_USD').reset_index()
    dfs = list_of_dfs(by_project)
    dfs_with_preds = list()
    for i in dfs:
        df_pred = make_arima(i, list(i['Project'])[0])
        dfs_with_preds.append(df_pred)
    df_pred = pd.concat(dfs_with_preds, axis=0)
    return df_pred


