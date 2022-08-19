import pandas as pd
import plotly.graph_objects as go
import plotly.express as px














####################### Profit Page #################################





def profit_by_month_bar(df):
	fig = go.Figure()
	fig = fig.add_trace(
	            go.Bar(
	                x=df['Date_str'],
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
	                        tickfont=dict(size=8), 
	                        type='category'
	                        )
	fig = fig.update_yaxes(title = None,
	                        showgrid=True,
	                        tickfont=dict(size=8))
	fig = fig.update_layout(
	                # width = 600, height = 270,
	                #paper_bgcolor= '#ECF0F1',
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
    fig = px.area(df, x = 'Date_str', y = 'RT',
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
                            #paper_bgcolor= '#ECF0F1'
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
                    #paper_bgcolor= '#ECF0F1',
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
    fig = px.area(df, x = 'Date_str', y = 'Amount_USD',
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
                            tickfont=dict(size=8), 
                            type='category'
                            )
    fig = fig.update_yaxes(title = None,
                            showgrid=True,
                            tickfont=dict(size=8))
    fig = fig.update_layout(
                            #xaxis_range= [-0.1, df['Date'].count() - 0.9],
                            margin=dict(l=20, r=20, t=25, b=20),
                            title={
                                'text': "One year prediction, USD",
                                'x':0.5,
                                    },
                            plot_bgcolor='#F3FEFE',
                            #paper_bgcolor= '#ECF0F1'
                            )
    return fig




























############################## Revenue Page #####################################







def revenue_by_month_plot(df):

	fig = px.bar(df, x = 'Date_str',
    y = 'Amount_USD',
    color = 'Category',
    text = 'Amount_USD')

	fig = fig.update_traces(
	                    texttemplate='%{text:.2s}',
	                    textfont_size = 10,
	                    textangle=0,
	                    textposition="inside",
	                    marker_line_color='#1D475F',
	                    marker_line_width=1

	)
	fig = fig.update_xaxes(title = None,
	                        tickfont=dict(size=8), 
	                        type='category')
	fig = fig.update_yaxes(title = None,
	                        showgrid=True,
	                        tickfont=dict(size=8))
	fig = fig.update_layout(
	                # width = 600, height = 270,
	                #paper_bgcolor= '#ECF0F1',
	                template = 'simple_white',
	                margin=dict(l=20, r=20, t=25, b=20),
	                title={
	                       'text': "Revenue by Month, USD",
	                       'x':0.5
	                             },
	                legend = dict(
	                    orientation = 'h',
	                    y = -0.15,

	                 font=dict(
	                    size=12,
	                            )),
	                plot_bgcolor='#F3FEFE'
	                )

	return fig

def revenue_by_country_plot(df):

	fig = px.bar(df, x = 'Amount_USD',
	    y = 'Country',
	    text = 'Amount_USD', 
	    orientation='h')

	fig = fig.update_traces(
	                    texttemplate='%{text:.2s}',
	                    textfont_size = 10,
	                    textangle=0,
	                    textposition="inside",
	                    marker_line_color='#1D475F',
	                    marker_line_width=1

								)
	fig = fig.update_xaxes(title = None,
	                        tickfont=dict(size=8))
	fig = fig.update_yaxes(title = None,
	                        showgrid=True,
	                        tickfont=dict(size=8))
	fig = fig.update_layout(
	                # width = 600, height = 270,
	                #paper_bgcolor= '#ECF0F1',
	                template = 'simple_white',
	                margin=dict(l=20, r=20, t=25, b=20),
	                title={
	                       'text': "Revenue by Country, USD",
	                       'x':0.5
	                             },
	                legend = dict(
	                    orientation = 'h',
	                    y = -0.15,

	                 font=dict(
	                    size=12,
	                            )),
	                plot_bgcolor='#F3FEFE'
	                )

	return fig


def pie_cat_rev(df):
	fig = px.pie(df, values='Amount_USD',
	names='Category', hole = 0.5
	                        )

	fig = fig.update_xaxes(title = None,
	                        tickfont=dict(size=8))
	fig = fig.update_yaxes(title = None,
	                        showgrid=True,
	                        tickfont=dict(size=8))
	fig = fig.update_layout(
	                # width = 400, height = 270,
	                #paper_bgcolor= '#ECF0F1',
	                template = 'simple_white',
	                margin=dict(l=20, r=20, t=25, b=20),
	                title={
	                       'text': "Revenue by Category",
	                       'x':0.5
	                             },
	                legend = dict(
	                    # orientation = 'h',
	                    # y = -0.15,

	                 font=dict(
	                    size=10,
	                            )),
	                plot_bgcolor='#F3FEFE'
	                )

	return fig


def pie_partner_rev(df):

	fig = px.pie(df, values='Amount_USD',
	names='Counterparty', hole = 0.5
	                        )

	fig = fig.update_xaxes(title = None,
	                        tickfont=dict(size=8))
	fig = fig.update_yaxes(title = None,
	                        showgrid=True,
	                        tickfont=dict(size=8))
	fig = fig.update_layout(
	                # width = 400, height = 270,
	                #paper_bgcolor= '#ECF0F1',
	                template = 'simple_white',
	                margin=dict(l=20, r=20, t=25, b=20),
	                title={
	                       'text': "Revenue by Category",
	                       'x':0.5
	                             },
	                legend = dict(
	                    # orientation = 'h',
	                    # y = -0.15,

	                 font=dict(
	                    size=10,
	                            )),
	                plot_bgcolor='#F3FEFE'
	                )

	return fig











################## Marketing Plots ##########################





def marketing_by_month_plot(df):

	fig = px.bar(df, x = 'Date_str',
	y = 'amount_abs',
	text = 'amount_abs')

	fig = fig.update_traces(
	                    texttemplate='%{text:.2s}',
	                    textfont_size = 10,
	                    textangle=0,
	                    textposition="inside",
	                    marker_line_color='#1D475F',
	                    marker_line_width=1

								)
	fig = fig.update_xaxes(title = None,
	                        tickfont=dict(size=8))
	fig = fig.update_yaxes(title = None,
	                        showgrid=True,
	                        tickfont=dict(size=8))
	fig = fig.update_layout(
	                # width = 600, height = 270,
	                #paper_bgcolor= '#ECF0F1',
	                template = 'simple_white',
	                margin=dict(l=20, r=20, t=25, b=20),
	                title={
	                       'text': "Marketing by Month, USD",
	                       'x':0.5
	                             },
	                legend = dict(
	                    orientation = 'h',
	                    y = -0.15,

	                 font=dict(
	                    size=12,
	                            )),
	                plot_bgcolor='#F3FEFE'
	                )

	return fig



def marketing_by_country_plot(df):

	fig = px.bar(df, x = 'amount_abs',
	    y = 'Country',
	    text = 'amount_abs', 
	    orientation='h')

	fig = fig.update_traces(
	                    texttemplate='%{text:.2s}',
	                    textfont_size = 10,
	                    textangle=0,
	                    textposition="inside",
	                    marker_line_color='#1D475F',
	                    marker_line_width=1

								)
	fig = fig.update_xaxes(title = None,
	                        tickfont=dict(size=8))
	fig = fig.update_yaxes(title = None,
	                        showgrid=True,
	                        tickfont=dict(size=8))
	fig = fig.update_layout(
	                # width = 600, height = 270,
	                #paper_bgcolor= '#ECF0F1',
	                template = 'simple_white',
	                margin=dict(l=20, r=20, t=25, b=20),
	                title={
	                       'text': "Marketing by Country, USD",
	                       'x':0.5
	                             },
	                legend = dict(
	                    orientation = 'h',
	                    y = -0.15,

	                 font=dict(
	                    size=12,
	                            )),
	                plot_bgcolor='#F3FEFE'
	                )

	return fig


def pie_partner_marketing(df):

	fig = px.pie(df, values='amount_abs',
	names='Counterparty', hole = 0.5
	                        )

	fig = fig.update_xaxes(title = None,
	                        tickfont=dict(size=8))
	fig = fig.update_yaxes(title = None,
	                        showgrid=True,
	                        tickfont=dict(size=8))
	fig = fig.update_layout(
	                # width = 400, height = 270,
	                #paper_bgcolor= '#ECF0F1',
	                template = 'simple_white',
	                margin=dict(l=20, r=20, t=25, b=20),
	                title={
	                       'text': "Revenue by Counterparty",
	                       'x':0.5
	                             },
	                legend = dict(
	                    # orientation = 'h',
	                    # y = -0.15,

	                 font=dict(
	                    size=10,
	                            )),
	                plot_bgcolor='#F3FEFE'
	                )

	return fig











############################ Development Plots #################################

def dev_by_month_plot(df):

	fig = px.bar(df, x = 'Date_str',
	    y = 'amount_abs',
	    color = 'Category',
	    text = 'amount_abs')

	fig = fig.update_traces(
	                    texttemplate='%{text:.2s}',
	                    textfont_size = 10,
	                    textangle=0,
	                    textposition="inside",
	                    marker_line_color='#1D475F',
	                    marker_line_width=1

							)
	fig = fig.update_xaxes(title = None,
	                        tickfont=dict(size=8))
	fig = fig.update_yaxes(title = None,
	                        showgrid=True,
	                        tickfont=dict(size=8))
	fig = fig.update_layout(
	                # width = 600, height = 270,
	                #paper_bgcolor= '#ECF0F1',
	                template = 'simple_white',
	                margin=dict(l=20, r=20, t=25, b=20),
	                title={
	                       'text': "Development by Month, USD",
	                       'x':0.5
	                             },
	                legend = dict(
	                    orientation = 'h',
	                    y = -0.15,

	                 font=dict(
	                    size=12,
	                            )),
	                plot_bgcolor='#F3FEFE'
	                )

	return fig





def dev_by_country_plot(df):

	fig = px.bar(df, x = 'amount_abs',
	    y = 'Country',
	    text = 'amount_abs', 
	    orientation='h')

	fig = fig.update_traces(
	                    texttemplate='%{text:.2s}',
	                    textfont_size = 10,
	                    textangle=0,
	                    textposition="inside",
	                    marker_line_color='#1D475F',
	                    marker_line_width=1

								)
	fig = fig.update_xaxes(title = None,
	                        tickfont=dict(size=8))
	fig = fig.update_yaxes(title = None,
	                        showgrid=True,
	                        tickfont=dict(size=8))
	fig = fig.update_layout(
	                # width = 600, height = 270,
	                #paper_bgcolor= '#ECF0F1',
	                template = 'simple_white',
	                margin=dict(l=20, r=20, t=25, b=20),
	                title={
	                       'text': "Development by Country, USD",
	                       'x':0.5
	                             },
	                legend = dict(
	                    orientation = 'h',
	                    y = -0.15,

	                 font=dict(
	                    size=12,
	                            )),
	                plot_bgcolor='#F3FEFE'
	                )

	return fig



def pie_cat_dev(df):
	fig = px.pie(df, values='amount_abs',
	names='Category', hole = 0.5
	                        )

	fig = fig.update_xaxes(title = None,
	                        tickfont=dict(size=8))
	fig = fig.update_yaxes(title = None,
	                        showgrid=True,
	                        tickfont=dict(size=8))
	fig = fig.update_layout(
	                # width = 400, height = 270,
	                #paper_bgcolor= '#ECF0F1',
	                template = 'simple_white',
	                margin=dict(l=20, r=20, t=25, b=20),
	                title={
	                       'text': "Development by Category",
	                       'x':0.5
	                             },
	                legend = dict(
	                    # orientation = 'h',
	                    # y = -0.15,

	                 font=dict(
	                    size=10,
	                            )),
	                plot_bgcolor='#F3FEFE'
	                )

	return fig




def pie_partner_dev(df):

	fig = px.pie(df, values='amount_abs',
	names='Counterparty', hole = 0.5
	                        )

	fig = fig.update_xaxes(title = None,
	                        tickfont=dict(size=8))
	fig = fig.update_yaxes(title = None,
	                        showgrid=True,
	                        tickfont=dict(size=8))
	fig = fig.update_layout(
	                # width = 400, height = 270,
	                #paper_bgcolor= '#ECF0F1',
	                template = 'simple_white',
	                margin=dict(l=20, r=20, t=25, b=20),
	                title={
	                       'text': "Development by Counterparty",
	                       'x':0.5
	                             },
	                legend = dict(
	                    # orientation = 'h',
	                    # y = -0.15,

	                 font=dict(
	                    size=10,
	                            )),
	                plot_bgcolor='#F3FEFE'
	                )

	return fig