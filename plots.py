import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

def profit_by_month_bar(df):
	fig = go.Figure()
	fig = fig.add_trace(
	            go.Bar(
	                x=df['Date'],
	                y=df['Amount_USD'],
	                #marker_color=df['Color'],
	                text = df['Amount_USD']
	                )
	                    )
	fig = fig.update_traces(
	                    texttemplate='%{text:.2s}',
	                    textfont_size = 10,
	                    textangle=0,
	                    textposition="inside",
	                    marker_line_color='#1D475F',
	                    marker_line_width=1.5

	)
	fig = fig.update_xaxes(title = None,
	                        tickfont=dict(size=8), type='category')
	fig = fig.update_yaxes(title = None,
	                        showgrid=True,
	                        tickfont=dict(size=8))
	fig = fig.update_layout(
	                # width = 600, height = 270,
	                paper_bgcolor= '#ECF0F1',
	                template = 'simple_white',
	                margin=dict(l=20, r=20, t=25, b=20),
	                title={
	                       'text': "Profit by Month, USD",
	                       'x':0.5
	                             },
	                plot_bgcolor='#F3FEFE'
	                )

	return fig

  
def cumline(df):
    fig = px.area(df, x = 'Date', y = 'RT',
            text = 'RT',
            markers = True,
            color_discrete_sequence= df['color_RT'],
            template = 'simple_white'
                    )
    fig = fig.update_traces(
                            texttemplate='%{text:.2s}',
                            textposition = 'top center',
                            textfont_size = 10,
                            marker_color=df['color_RT'],
                            )
    fig = fig.update_xaxes(title = None,
                            tickfont=dict(size=8), type='category')
    fig = fig.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    fig = fig.update_layout(
                            xaxis_range= [-0.1, df['Date'].count() - 0.9],
                            margin=dict(l=20, r=20, t=25, b=20),
                            title={
                                'text': "Cumulative profit, USD",
                                'x':0.5,
                                    },
                            plot_bgcolor='#F3FEFE',
                            paper_bgcolor= '#ECF0F1'
                            )
    return fig

 
def bar_project(df):
    fig = go.Figure()
    fig = fig.add_trace(
                go.Bar(
                    x=df['Project'],
                    y=df['Amount_USD'],
                    marker_color=df['color'],
                    text = df['Amount_USD']
                    )
                        )
    fig = fig.update_traces(
                        texttemplate='%{text:.2s}',
                        textfont_size = 10,
                        textangle=0,
                        textposition="inside",
                        marker_line_color='#1D475F',
                        marker_line_width=1.5

    )
    fig = fig.update_xaxes(title = None,
                            tickfont=dict(size=8))
    fig = fig.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    fig = fig.update_layout(
                    # width = 600, height = 270,
                    paper_bgcolor= '#ECF0F1',
                    template = 'simple_white',
                    margin=dict(l=20, r=20, t=25, b=20),
                    title={
                           'text': "Profit by Project, USD",
                           'x':0.5
                                 },
                    plot_bgcolor='#F3FEFE'
                    )
    return fig


def predictions(df):
    fig = px.area(df, x = df.index, y = 'Amount_USD',
            text = 'Amount_USD',
            markers = True,
            #color_discrete_sequence= df['color_RT'],
            template = 'simple_white'
                    )
    fig = fig.update_traces(
                            texttemplate='%{text:.2s}',
                            textposition = 'top center',
                            textfont_size = 10,
                            #marker_color=df['color_RT'],
                            )
    fig = fig.update_xaxes(title = None,
                            tickfont=dict(size=8), type='category')
    fig = fig.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    fig = fig.update_layout(
                            xaxis_range= [-0.1, df['Date'].count() - 0.9],
                            margin=dict(l=20, r=20, t=25, b=20),
                            title={
                                'text': "One year prediction, USD",
                                'x':0.5,
                                    },
                            plot_bgcolor='#F3FEFE',
                            paper_bgcolor= '#ECF0F1'
                            )
    return fig