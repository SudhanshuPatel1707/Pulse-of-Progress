import io
import pandas as pd
import streamlit as st
# import ydata_profiling
from streamlit-player import st_player
from streamlit_pandas_profiling import st_profile_report
from streamlit_extras.metric_cards import style_metric_cards
from streamlit_extras.add_vertical_space import add_vertical_space
import plotly.express as px
import json
import altair as alt
import seaborn as sns

st.set_page_config(page_title="Pulse Of Progress",page_icon='images/Logo.png')
# Reading csv files

agg_user_df = pd.read_csv('agg_user.csv')
agg_trans_df = pd.read_csv('agg_trans.csv')
map_user_df = pd.read_csv('map_user.csv')
map_trans_df = pd.read_csv('map_trans.csv')
top_trans_dist_df = pd.read_csv('top_trans_dist.csv')
top_trans_pin_df = pd.read_csv('top_trans_pin.csv')
top_user_dist_df = pd.read_csv('top_user_dist.csv')
top_user_pin_df = pd.read_csv('top_user_pin.csv')

st.sidebar.title("Pulse Of Progress")

st.sidebar.image('images/Logo.png')
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Overview','Overall Analysis','Transactions Analysis','Trend Analysis','User Analysis','Comparative Analysis')
)

if user_menu == 'Overview':

    st.title(':violet[Pulse Of Progress : Analyzing the Rise of Digital Payments in India]')

    add_vertical_space(2)

    phonepe_description = '''PhonePe has recently unveiled PhonePe Pulse, a sophisticated data analytics platform designed to
                             provide comprehensive insights into the behaviors and patterns of digital payment usage among 
                             Indian consumers. This innovative platform utilizes data from PhonePe's vast user base, which 
                             consists of over 300 million registered users and processes an impressive 20 billion transactions. 
                             As India's leading digital payments platform, PhonePe boasts a substantial 46% market share in 
                             UPI transactions, affording it an unparalleled vantage point from which to observe and understand 
                             the digital payments landscape in India. With PhonePe Pulse, users now have the ability to seamlessly 
                             access and visually interpret the wealth of data provided by the platform, enabling them to gain deep 
                             and valuable insights into the intricate trends and patterns associated with digital payment transactions 
                             within India.'''

    st.write(phonepe_description)

    add_vertical_space(2)

    st_player(url="https://www.youtube.com/watch?v=c_1H6vivsiA", height=480)

    add_vertical_space(2)

    st.image('https://blog.m2pfintech.com/wp-content/uploads/2022/06/Blog-Banner_WP_02.jpg')

    add_vertical_space(2)

    col1, col2, col3 = st.columns(3)

    total_registered_users = top_user_dist_df[top_user_dist_df['Year'] == 2022]['Registered_users'].sum()
    col1.metric(
        label='Total Registered Users till 2022',
        value='{:.2f} Cr'.format(total_registered_users / 100000000),
        delta='Forward Trend'
    )

    app_opens_count = map_user_df['App_opens'].sum()
    col2.metric(
        label='Total App Opens', value='{:.2f} Cr'.format(app_opens_count / 100000000),
        delta='Forward Trend'
    )

    col3.metric(label='Total Transaction Count per month', value='500 Cr +', delta='Forward Trend')

    style_metric_cards(background_color='purple')

    add_vertical_space(2)

    st.image('https://www.phonepe.com/pulsestatic/799/pulse/static/home_og_image-adc70b0401140d689c55d37cfce6161e.jpeg',
             use_column_width=True)

    add_vertical_space(2)

    col, buff = st.columns([2, 4])

if user_menu == 'Overall Analysis':

    agg_trans = pd.read_csv('agg_trans.csv')
    map_trans = pd.read_csv('map_trans.csv')
    map_user = pd.read_csv('map_user.csv')

    # functions

    # First

    trans_type_count = agg_trans.groupby('Transaction_type')['Transaction_count'].sum()

    total_trans_count = agg_trans['Transaction_count'].sum()

    trans_type_perc = round(trans_type_count / total_trans_count * 100, 2).reset_index()

    trans_type_fig = px.pie(
        trans_type_perc, names='Transaction_type',
        values='Transaction_count', hole=.65,
        hover_data={'Transaction_count': False}
    )

    trans_type_fig.update_layout(width=900, height=500)

    # Second

    trans_state = agg_trans.groupby('State')['Transaction_count'].sum().reset_index().sort_values(
        by='Transaction_count', ascending=False).head(12)
    trans_state_fig = px.bar(
        trans_state, x='Transaction_count',
        y='State', orientation='h',
        text='Transaction_count', text_auto='.2s',
        labels={'Transaction_count': "Transaction Count"}
    )

    trans_state_fig.update_layout(
        yaxis=dict(autorange="reversed"),
        width=900, height=500
    )

    # Third

    trans_dist = map_trans.groupby(['State', 'District']).agg({
        'Transaction_count': 'sum'
    }).reset_index().sort_values(by='Transaction_count', ascending=False).head(12)

    trans_district_fig = px.bar(
        trans_dist, x='Transaction_count',
        y='District', orientation='h',
        text='Transaction_count', text_auto='.2s',
        labels={'Transaction_count': "Transaction Count"},
        hover_name='State',
        hover_data={'State': False, 'District': True}
    )

    trans_district_fig.update_layout(
        yaxis=dict(autorange="reversed"),
        width=900, height=500
    )

    # Fourth

    user_state = map_user.groupby('State')['Registered_users'].sum().reset_index()

    with open(r"miscs/india_states.json") as f:
        geojson = json.load(f)

    if 'geojson' not in st.session_state:
        st.session_state["geojson"] = geojson

    user_state_fig = px.choropleth(
        user_state, geojson=geojson,
        locations='State',
        featureidkey='properties.ST_NM',
        color='Registered_users', projection='orthographic',
        labels={'Registered_users': "Registered Users"},
        color_continuous_scale='reds'
    )

    user_state_fig.update_geos(fitbounds='locations', visible=False)
    user_state_fig.update_layout(height=600, width=900)

    st.title(':violet[Overall Analysis]')

    add_vertical_space(2)

    # First

    st.subheader(":green[Transaction Breakdown by Type]")
    st.plotly_chart(trans_type_fig)

    # Second

    st.subheader(":green[Transaction Count by State]")
    st.plotly_chart(trans_state_fig)

    # Third

    st.subheader(":green[Transaction Count by District]")
    st.plotly_chart(trans_district_fig)

    # Fourth

    st.subheader(':green[Registered User Count by State]')
    st.plotly_chart(user_state_fig, use_container_width=True)

if user_menu == 'Transactions Analysis':
    agg_trans = pd.read_csv('agg_trans.csv')
    trans_df = pd.read_csv('agg_trans.csv')
    map_df = pd.read_csv('map_trans.csv')

    states = agg_trans["State"].unique()
    years = agg_trans["Year"].unique()
    quarters = agg_trans["Quarter"].unique()

    if 'states' not in st.session_state:
        st.session_state["states"] = states
    if 'years' not in st.session_state:
        st.session_state["years"] = years
    if 'quarters' not in st.session_state:
        st.session_state["quarters"] = quarters

    # App

    st.title(':violet[Transactions Analysis]')
    add_vertical_space(3)

    # Transaction amount breakdown

    st.subheader(':violet[Transaction amount breakdown]')

    col1, col2, col3 = st.columns([5, 3, 1])

    state1 = col1.selectbox('State', states, key='state1')
    year1 = col2.selectbox("Year", years, key='year1')
    quarter_options = ["All"] + list(map(str, quarters))
    quarter1 = col3.selectbox("Quarter", quarter_options, key='quarter1')

    trans_df = trans_df[(trans_df["State"] == state1) & (trans_df["Year"] == year1)]

    if quarter1 != 'All':
        trans_df = trans_df[(trans_df["Quarter"] == int(quarter1))]

    trans_df = trans_df.sort_values("Transaction_amount", ascending=False).reset_index(drop=True)

    suffix1 = " quarters" if quarter1 == 'All' else "st" if quarter1 == '1' else "nd" if quarter1 == '2' else "rd" if quarter1 == '3' else "th"

    title1 = f"Transaction details of {state1} for {quarter1.lower()}{suffix1} {'' if quarter1 == 'All' else 'quarter'} of {year1}"

    fig1 = px.bar(
        trans_df, x="Transaction_type", y="Transaction_amount",
        color="Transaction_type",
        color_discrete_sequence=px.colors.qualitative.Plotly,
        title=title1,
        labels=dict(Transaction_amount='Transaction Amount', Transaction_type='Transaction Type'),
        hover_data={'Quarter': True}
    )

    fig1.update_layout(
        showlegend=False,
        title={
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.9,
            'yanchor': 'top'
        },
        width=900, height=500
    )

    fig1.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))

    st.plotly_chart(fig1)

    expander1 = st.expander(label='Detailed view')
    expander1.write(trans_df.loc[:, ['Quarter', 'Transaction_type', 'Transaction_amount']].reset_index(drop=True))

    # Transaction Hotspots - Districts

    st.subheader(':violet[Transaction Hotspots - Districts]')

    year_col, quarter_col, buff = st.columns([1, 1, 4])

    year2 = year_col.selectbox("Year", years, key='year2')
    quarter2 = quarter_col.selectbox("Quarter", quarter_options, key='quarter2')

    map_df = map_df[map_df["Year"] == year2]

    if quarter2 != 'All':
        map_df = map_df[(map_df["Quarter"] == int(quarter2))]

    suffix2 = " quarters" if quarter2 == 'All' else "st" if quarter2 == '1' else "nd" if quarter2 == '2' else "rd" if quarter2 == '3' else "th"

    title2 = f"Transaction hotspots for {quarter2.lower()}{suffix2} {'' if quarter2 == 'All' else 'quarter'} of {year2}"

    fig2 = px.scatter_mapbox(map_df, lat="Latitude", lon="Longitude",
                             size="Transaction_amount", hover_name="District",
                             hover_data={"Transaction_count": True, "Transaction_amount": True, 'Quarter': True},
                             title=title2,
                             color_discrete_sequence=px.colors.sequential.Plotly3
                             )

    fig2.update_layout(mapbox_style='carto-positron',
                       mapbox_zoom=3.45, mapbox_center={"lat": 20.93684, "lon": 78.96288},
                       geo=dict(scope='asia', projection_type='equirectangular'),
                       title={
                           'x': 0.5,
                           'xanchor': 'center',
                           'y': 0.04,
                           'yanchor': 'bottom',
                           'font': dict(color='black')
                       },
                       margin={"r": 0, "t": 0, "l": 0, "b": 0}, width=900, height=500
                       )

    st.plotly_chart(fig2)

    expander2 = st.expander(label='Detailed view')
    expander2.write(map_df.loc[:, ['State', 'District', 'Quarter', 'Transaction_amount']].reset_index(drop=True))

    # Breakdown by transaction count proportion

    st.subheader(":violet[Breakdown by transaction count proportion]")

    state_pie, year_pie, quarter_pie = st.columns([5, 3, 1])

    state3 = state_pie.selectbox('State', options=states, key='state3')
    year3 = year_pie.selectbox('Year', options=years, key='year3')
    quarter3 = quarter_pie.selectbox('Quarter', options=quarter_options, key='quarter3')

    trans_df_2 = pd.read_csv('agg_trans.csv')
    filtered_trans = trans_df_2[(trans_df_2.State == state3) & (trans_df_2.Year == year3)]

    if quarter3 != 'All':
        filtered_trans = filtered_trans[filtered_trans.Quarter == int(quarter3)]

    fig3 = px.pie(
        filtered_trans, names='Transaction_type',
        values='Transaction_count', hole=.65
    )

    fig3.update_layout(width=900, height=500)

    st.plotly_chart(fig3)

    expander3 = st.expander(label='Detailed view')
    expander3.write(filtered_trans.loc[:, ['Quarter', 'Transaction_type', 'Transaction_count']].reset_index(drop=True))

if user_menu == 'User Analysis':
    agg_user_df1 = pd.read_csv('agg_user.csv')
    map_user_df1 = pd.read_csv('map_user.csv')
    top_user_dist_df1 = pd.read_csv('top_user_dist.csv')

    states = agg_user_df1["State"].unique()
    years = agg_user_df1["Year"].unique()
    quarters = agg_user_df1["Quarter"].unique()

    st.title(':violet[Users]')
    add_vertical_space(3)

    # 1

    st.subheader(':green[Transaction Count and Percentage by Brand]')

    col1, col2, col3 = st.columns([5, 3, 1])

    state_options = ['All'] + [state for state in states]
    quarter_options = ["All"] + list(map(str, quarters))

    state1 = col1.selectbox('State', options=state_options, key='state1')
    year1 = col2.selectbox('Year', options=years, key='year1')
    quarter1 = col3.selectbox("Quarter", options=quarter_options, key='quarter1')

    if state1 == "All":

        agg_user_df_filtered = agg_user_df1[(agg_user_df1['Year'] == year1)]

        if quarter1 != 'All':
            agg_user_df_filtered = agg_user_df_filtered[agg_user_df_filtered['Quarter'] == int(quarter1)]

        suffix1 = " quarters" if quarter1 == 'All' else "st" if quarter1 == '1' else "nd" if quarter1 == '2' else "rd" if quarter1 == '3' else "th"

        title1 = f"Transaction Count and Percentage across all states for {quarter1.lower()}{suffix1} {'' if quarter1 == 'All' else 'quarter'} of {year1}"

    else:

        agg_user_df_filtered = agg_user_df1[(agg_user_df1['State'] == state1) & (agg_user_df1['Year'] == year1)]

        if quarter1 != 'All':
            agg_user_df_filtered = agg_user_df_filtered[agg_user_df_filtered['Quarter'] == int(quarter1)]

        suffix1 = " quarters" if quarter1 == 'All' else "st" if quarter1 == '1' else "nd" if quarter1 == '2' else "rd" if quarter1 == '3' else "th"

        title1 = f"Transaction Count and Percentage in {state1} for {quarter1.lower()}{suffix1} {'' if quarter1 == 'All' else 'quarter'} of {year1}"

    fig1 = px.treemap(
        agg_user_df_filtered,
        path=['Brand'],
        values='Transaction_count',
        color='Percentage',
        color_continuous_scale='ylorbr',
        hover_data={'Percentage': ':.2%'},
        hover_name='Brand'
    )

    fig1.update_layout(
        width=975, height=600,
        coloraxis_colorbar=dict(tickformat='.1%', len=0.85),
        margin=dict(l=20, r=20, t=0, b=20),
        title={
            "text": title1,
            'x': 0.45,
            'xanchor': 'center',
            'y': 0.007,
            'yanchor': 'bottom'
        }
    )

    fig1.update_traces(
        hovertemplate=
        '<b>%{label}</b><br>Transaction Count: %{value}<br>Percentage: %{color:.2%}<extra></extra>'
    )

    st.plotly_chart(fig1)

    expander1 = st.expander(label='Detailed view')
    expander1.write(agg_user_df_filtered.loc[:, ['State', 'Quarter', 'Brand', 'Percentage']])

    add_vertical_space(2)

    # 2

    st.subheader(':green[Registered Users Hotspots - Disrict]')

    col4, col5, col6 = st.columns([5, 3, 1])

    state2 = col4.selectbox('State', options=state_options, key='state2')
    year2 = col5.selectbox('Year', options=years, key='year2')
    quarter2 = col6.selectbox("Quarter", options=quarter_options, key='quarter2')

    if state2 == 'All':
        map_user_df_filtered = map_user_df1[(map_user_df1["Year"] == year2)]

        if quarter2 != 'All':
            map_user_df_filtered = map_user_df_filtered[map_user_df_filtered['Quarter'] == int(quarter2)]
    else:
        map_user_df_filtered = map_user_df1[(map_user_df1["State"] == state2) & (map_user_df1["Year"] == year2)]

        if quarter2 != 'All':
            map_user_df_filtered = map_user_df_filtered[map_user_df_filtered['Quarter'] == int(quarter2)]

    fig2 = px.scatter_mapbox(
        map_user_df_filtered,
        lat="Latitude",
        lon="Longitude",
        size="Registered_users",
        hover_name="District",
        hover_data={'State': True, 'Quarter': True},
        title=f"Registered Users by District",
        color_discrete_sequence=px.colors.sequential.Plotly3
    )

    fig2.update_layout(
        mapbox_style='carto-positron',
        mapbox_zoom=3.5, mapbox_center={"lat": 20.93684, "lon": 78.96288},
        geo=dict(scope='asia', projection_type='equirectangular'),
        title={
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.05,
            'yanchor': 'bottom',
            'font': dict(color='black')
        },
        height=600, width=900,
        margin={"r": 0, "t": 0, "l": 0, "b": 0}
    )

    st.plotly_chart(fig2)

    expander2 = st.expander(label='Detailed view')
    expander2.write(map_user_df_filtered.loc[:, ['District', 'Quarter', 'Registered_users']].reset_index(drop=True))

    add_vertical_space(2)

    # 3

    st.subheader(':green[Top Districts by Registered Users]')

    col7, col8, buff1 = st.columns([5, 2, 5])

    state3 = col7.selectbox('State', options=state_options, key='state3')
    year3 = col8.selectbox('Year', options=years, key='year3')

    if state3 == "All":

        top_user_dist_df_filtered = top_user_dist_df1[
            top_user_dist_df1['Year'] == year3
            ].groupby('District').sum().reset_index()

        top_user_dist_df_filtered = top_user_dist_df_filtered.sort_values(
            by='Registered_users',
            ascending=False
        ).head(10)

        title3 = f'Top 10 districts across all states by registered users in {year3}'

    else:

        top_user_dist_df_filtered = top_user_dist_df1[
            (top_user_dist_df1['State'] == state3)
            &
            (top_user_dist_df1['Year'] == year3)
            ].groupby('District').sum().reset_index()

        top_user_dist_df_filtered = top_user_dist_df_filtered.sort_values(
            by='Registered_users',
            ascending=False
        ).head(10)

        title3 = f'Top districts in {state3} by registered users in {year3}'

    fig3 = px.bar(
        top_user_dist_df_filtered,
        x='Registered_users',
        y='District',
        color='Registered_users',
        color_continuous_scale='Greens',
        orientation='h', labels={'Registered_users': 'Registered Users'},
        hover_name='District',
        hover_data=['Registered_users']
    )

    fig3.update_traces(hovertemplate='<b>%{hovertext}</b><br>Registered users: %{x:,}<br>')

    fig3.update_layout(
        height=500, width=950,
        yaxis=dict(autorange="reversed"),
        title={
            'text': title3,
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.007,
            'yanchor': 'bottom'
        }
    )

    st.plotly_chart(fig3)

    expander3 = st.expander(label='Detailed view')
    expander3.write(top_user_dist_df_filtered.loc[:, ['District', 'Registered_users']].reset_index(drop=True))

    add_vertical_space(2)

if user_menu == 'Trend Analysis' :
    map_trans = pd.read_csv('map_trans.csv')
    top_trans_dist = pd.read_csv('top_trans_dist.csv')
    dist_trans = pd.read_csv('top_trans_dist.csv')
    pin_trans = pd.read_csv('top_trans_pin.csv')
    years = map_trans['Year'].unique()
    states = map_trans['State'].unique()
    quarters = map_trans['Quarter'].unique().tolist()

    top_states = dist_trans.groupby('State')['Transaction_amount'].sum().reset_index().sort_values('Transaction_amount',
                                                                                                   ascending=False).head(
        10)

    top_districts = dist_trans.groupby('District')[
        'Transaction_amount'
    ].sum().reset_index().sort_values(
        'Transaction_amount',
        ascending=False
    ).head(10)

    top_pincodes = pin_trans.groupby('Pincode')[
        'Transaction_amount'
    ].sum().reset_index().sort_values(
        'Transaction_amount',
        ascending=False
    ).head(10)


    # Function Definition

    def filter_top_trans_dist(top_trans_dist, year, quarter):
        filtered_top_trans_dist = top_trans_dist[top_trans_dist['Year'] == year]
        if quarter != 'All':
            filtered_top_trans_dist = filter_top_trans_dist[(filter_top_trans_dist['Quarter'] == quarter)]
        return filtered_top_trans_dist

    # App

    st.title(':blue[Trend Analysis]')
    add_vertical_space(3)

    # 1

    st.subheader(':blue[Transaction Count and Amount - Trend over the years]')
    add_vertical_space(1)

    col1, col2, col3, col4 = st.columns([3, 4, 4, 2])

    region1 = col1.selectbox('Region', map_trans["Region"].unique(), key='region1')

    df = map_trans[map_trans['Region'] == region1]

    state1 = col2.selectbox('State', df['State'].unique(), key='state1')

    df = df[df['State'] == state1]

    district1 = col3.selectbox('District', df['District'].unique(), key='district1')

    df = df[df['District'] == district1]

    year_options = ['All'] + [year for year in years]
    year1 = col4.selectbox('Year', year_options, key='year1')

    title1 = f'Transaction count trend for {district1} district in {state1} across {str(year1).lower()} years'
    title2 = f'Transaction amount trend for {district1} district in {state1} across {str(year1).lower()} years'

    if year1 != 'All':
        df = df[df['Year'] == year1]

        title1 = f'Transaction count trend for {district1} district in {state1} during {year1}'
        title2 = f'Transaction amount trend for {district1} district in {state1} during {year1}'

    fig1 = px.line(df, x='Quarter', y='Transaction_count', color='Year', title=title1)

    fig1.update_xaxes(tickmode='array', tickvals=list(range(1, 5)))

    fig1.update_layout(
        height=500, width=900,
        yaxis_title='Transaction Count',
        title={
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.9,
            'yanchor': 'bottom'
        }
    )

    fig2 = px.line(df, x='Quarter', y='Transaction_amount', color='Year', title=title2)

    fig2.update_xaxes(tickmode='array', tickvals=list(range(1, 5)))

    fig2.update_layout(
        height=500, width=900,
        yaxis_title='Transaction Amount',
        title={
            'x': 0.5,
            'xanchor': 'center',
            'y': 0.9,
            'yanchor': 'bottom'
        }
    )

    tab1, tab2 = st.tabs(['🫰Transaction Count Trend', '💰Transaction Amount Trend'])

    tab1.plotly_chart(fig1)

    expander1 = tab1.expander('Detailed view')
    expander1.write(df.loc[:, ['Region', 'District', 'Year', 'Quarter', 'Transaction_count']].reset_index(drop=True))

    tab2.plotly_chart(fig2)

    expander2 = tab2.expander('Detailed view')
    expander2.write(df.loc[:, ['Region', 'District', 'Year', 'Quarter', 'Transaction_amount']].reset_index(drop=True))

    # 2

    st.subheader(':blue[Transaction Count and Amount - Top Districts]')

    col5, col6, col7 = st.columns([5, 3, 1])

    state_options = ["All"] + states
    year_options = years
    quarter_options = ["All"] + quarters

    state2 = col5.selectbox("State", state_options, key="state2")
    year2 = col6.selectbox("Year", year_options, key="year2")
    quarter2 = col7.selectbox("Quarter", quarter_options, key="quarter2")

    if state2 != "All":
        top_trans_dist = top_trans_dist[top_trans_dist["State"] == state2]

    top_trans_dist = top_trans_dist[top_trans_dist["Year"] == year2]

    if quarter2 != "All":
        top_trans_dist = top_trans_dist[top_trans_dist["Quarter"] == quarter2]

    top_dist_grouped_1 = top_trans_dist.groupby("District")["Transaction_count"].sum().nlargest(10).index.tolist()

    top_trans_dist_filtered_1 = top_trans_dist[top_trans_dist["District"].isin(top_dist_grouped_1)]

    suffix1 = " quarters" if quarter2 == 'All' else "st" if quarter2 == 1 else "nd" if quarter2 == 2 else "rd" if quarter2 == 3 else "th"

    title3 = f"Top districts in {'India' if state2 == 'All' else state2} by Transaction count during {str(quarter2).lower()}{suffix1} {'' if quarter2 == 'All' else 'quarter'} of {year2}"

    axis_format = '~s'

    chart1 = alt.Chart(
        top_trans_dist_filtered_1,
        height=500, width=900
    ).mark_bar(size=18).encode(
        x=alt.X(
            "Transaction_count",
            title="Transaction Count",
            axis=alt.Axis(format=axis_format)
        ),
        y=alt.Y(
            "District",
            sort=top_dist_grouped_1,
            title=None
        ),
        color="State",
        tooltip=[
            "District", "State", "Year",
            "Quarter", "Transaction_count"
        ]
    ).properties(
        title=alt.TitleParams(
            text=title3,
            align="center",
            anchor='middle',
            baseline="bottom"
        )
    ).configure_axis(grid=False)

    top_dist_grouped_2 = top_trans_dist.groupby("District")["Transaction_amount"].sum().nlargest(10).index.tolist()

    top_trans_dist_filtered_2 = top_trans_dist[top_trans_dist["District"].isin(top_dist_grouped_2)]

    title4 = f"Top districts in {'India' if state2 == 'All' else state2} by Transaction amount during {str(quarter2).lower()}{suffix1} {'' if quarter2 == 'All' else 'quarter'} of {year2}"

    chart2 = alt.Chart(
        top_trans_dist_filtered_2,
        height=500, width=900
    ).mark_bar(size=18).encode(
        x=alt.X(
            "sum(Transaction_amount)",
            title="Transaction Amount",
            axis=alt.Axis(format=axis_format)
        ),
        y=alt.Y(
            "District", sort=top_dist_grouped_2,
            title=None
        ),
        color="State",
        tooltip=[
            "District", "State", "Year",
            "Quarter", "Transaction_amount"
        ]
    ).properties(
        title=alt.TitleParams(
            text=title4,
            align="center",
            anchor='middle',
            baseline="bottom"
        )
    ).configure_axis(grid=False)

    tab3, tab4 = st.tabs(['🫰Transaction Count - Top Districts', '💰Transaction Amount - Top Districts'])

    tab3.altair_chart(chart1, use_container_width=True)

    expander3 = tab3.expander('Detailed view')
    expander3.write(top_trans_dist_filtered_1.loc[
                    :,
                    [
                        'State', 'District', 'Quarter', 'Transaction_count'
                    ]
                    ].reset_index(drop=True))

    tab4.altair_chart(chart2, use_container_width=True)

    expander4 = tab4.expander('Detailed view')
    expander4.write(top_trans_dist_filtered_2.loc[
                    :,
                    [
                        'State', 'District', 'Quarter', 'Transaction_amount'
                    ]
                    ].reset_index(drop=True))

    # 3

    st.subheader(':blue[Other Key Trends over the years]')

    col8, col9, col10 = st.columns([5, 3, 1])

    trend3 = col8.selectbox(
        'Trend',
        (
            'Top 10 States by Transaction Volume',
            'Top 10 Districts by Transaction Volume',
            'Top 10 Pincodes by Transaction Volume'
        ),
        key='trend3'
    )

    year3 = col9.selectbox('Year', years, key='year3')

    quarter3 = col10.selectbox('Quarter', quarter_options, key='quarter3')

    filtered_dist_trans = filter_top_trans_dist(dist_trans, year3, quarter3)
    filtered_pin_trans = filter_top_trans_dist(pin_trans, year3, quarter3)

    filtered_top_states = filtered_dist_trans.groupby('State')[
        'Transaction_amount'
    ].sum().reset_index().sort_values(
        'Transaction_amount',
        ascending=False
    ).head(10)

    filtered_top_districts = filtered_dist_trans.groupby('District')[
        'Transaction_amount'
    ].sum().reset_index().sort_values(
        'Transaction_amount',
        ascending=False
    ).head(10)

    filtered_top_pincodes = filtered_pin_trans.groupby('Pincode')[
        'Transaction_amount'
    ].sum().reset_index().sort_values(
        'Transaction_amount',
        ascending=False
    ).head(10)
    filtered_top_pincodes['Pincode'] = filtered_top_pincodes['Pincode'].astype(str)

    suffix2 = " quarters" if quarter3 == 'All' else "st" if quarter3 == 1 else "nd" if quarter3 == 2 else "rd" if quarter3 == 3 else "th"

    title5 = f"Top 10 states by Transaction volume {'across' if quarter3 == 'All' else 'in'} {str(quarter3).lower()}{suffix2} {'' if quarter3 == 'All' else 'quarter'} of {year3}"

    title6 = f"Top 10 districts by Transaction volume {'across' if quarter3 == 'All' else 'in'} {str(quarter3).lower()}{suffix2} {'' if quarter3 == 'All' else 'quarter'} of {year3}"

    title7 = f"Top 10 pincode locations by Transaction volume {'across' if quarter3 == 'All' else 'in'} {str(quarter3).lower()}{suffix2} {'' if quarter3 == 'All' else 'quarter'} of {year3}"

    if trend3 == 'Top 10 States by Transaction Volume':

        chart3 = alt.Chart(
            filtered_top_states,
            height=500, width=900
        ).mark_bar(size=18).encode(
            x=alt.X(
                'Transaction_amount',
                axis=alt.Axis(format=axis_format),
                title="Transaction Amount"
            ),
            y=alt.Y('State', sort='-x'),
            tooltip=[
                'State', alt.Tooltip('Transaction_amount', format='.2f')
            ]
        ).properties(
            title=alt.TitleParams(
                text=title5,
                align="center",
                anchor='middle'
            )
        )

    elif trend3 == 'Top 10 Districts by Transaction Volume':

        chart3 = alt.Chart(
            filtered_top_districts,
            height=500, width=900
        ).mark_bar(size=18).encode(
            x=alt.X(
                'Transaction_amount',
                axis=alt.Axis(format=axis_format),
                title="Transaction Amount"
            ),
            y=alt.Y('District', sort='-x'),
            tooltip=[
                'District', alt.Tooltip('Transaction_amount', format='.2f')
            ]
        ).properties(
            title=alt.TitleParams(
                text=title6,
                align="center",
                anchor='middle'
            )
        )

    elif trend3 == 'Top 10 Pincodes by Transaction Volume':

        chart3 = alt.Chart(
            filtered_top_pincodes,
            height=500, width=900
        ).mark_bar(size=18).encode(
            x=alt.X(
                'Transaction_amount',
                axis=alt.Axis(format=axis_format),
                title="Transaction Amount"
            ),
            y=alt.Y('Pincode', sort='-x'),
            tooltip=[
                'Pincode', alt.Tooltip('Transaction_amount', format='.2f')
            ]
        ).properties(
            title=alt.TitleParams(
                text=title7,
                align="center",
                anchor='middle'
            )
        )

    st.altair_chart(chart3, use_container_width=True)

    expander5 = st.expander('Detailed view')
    data = filtered_top_states if trend3 == 'Top 10 States by Transaction Volume' else filtered_top_districts if trend3 == 'Top 10 Districts by Transaction Volume' else filtered_top_pincodes
    expander5.dataframe(data.reset_index(drop=True))

if user_menu == 'Comparative Analysis' :
    trans_df1 = pd.read_csv('agg_trans.csv')
    trans_df2 = pd.read_csv('agg_trans.csv')
    user_df = pd.read_csv('agg_user.csv')
    quarters = trans_df1['Quarter'].unique().tolist()
    states = trans_df1['State'].unique().tolist()
    years = trans_df1['Year'].unique().tolist()

    trans_df1["Transaction_amount(B)"] = trans_df1["Transaction_amount"] / 1e9
    year_order = sorted(trans_df1["Year"].unique())
    trans_df1["Year"] = pd.Categorical(trans_df1["Year"], categories=year_order, ordered=True)

    quarter_options = ["All"] + quarters
    transaction_types = trans_df1['Transaction_type'].unique()

    # App

    st.title(':violet[Comparitive Analysis]')
    add_vertical_space(3)

    # 1

    st.subheader(':green[Regionwise Transaction volume comparison]')

    fig1 = sns.catplot(
        x="Year", y="Transaction_amount",
        col="Region", data=trans_df1,
        kind="bar", errorbar=None,
        height=5, aspect=1.5, col_wrap=2,
        sharex=False
    )

    for ax in fig1.axes.flat:
        ax.set_yticklabels(['₹. {:,.0f}B'.format(y / 1e9) for y in ax.get_yticks()])
        ax.set_ylabel('Transaction Amount')

    sns.set_style("white")
    st.pyplot(fig1)

    # 2

    st.subheader(':green[Transaction breakdown by Transaction type]')

    col1, col2, col3 = st.columns([5, 3, 1])

    selected_states = col1.multiselect("Select state(s)", states, key='selected_states')
    year1 = col2.selectbox("Year", years, key='year1')
    quarter1 = col3.selectbox("Quarter", quarter_options, key='quarter1')

    trans_df1 = trans_df1[(trans_df1["Year"] == year1)]

    if quarter1 != "All":
        trans_df1 = trans_df1[(trans_df1["Quarter"] == quarter1)]

    suffix1 = " quarters" if quarter1 == 'All' else "st" if quarter1 == 1 else "nd" if quarter1 == 2 else "rd" if quarter1 == 3 else "th"

    title1 = f"Transaction details comparison of the selected states for {str(quarter1).lower()}{suffix1} {'' if quarter1 == 'All' else 'quarter'} of {year1}"

    if len(selected_states) == 1:
        state_str = ''.join(selected_states)
        title1 = f"Transaction details of {state_str} for {str(quarter1).lower()}{suffix1} {'' if quarter1 == 'All' else 'quarter'} of {year1}"

    if selected_states:

        trans_df1 = trans_df1[trans_df1["State"].isin(selected_states)]
        trans_df1 = trans_df1.sort_values("Transaction_count", ascending=False)

        fig2 = px.bar(
            trans_df1, x="Transaction_type", y="Transaction_count",
            color="State",
            color_discrete_sequence=px.colors.qualitative.Plotly,
            barmode='group',
            title=title1,
            labels=dict(Transaction_count='Transaction Count', Transaction_type='Transaction Type'),
            hover_data={'Quarter': True}
        )

        fig2.update_layout(
            width=900, height=550,
            title={
                'x': 0.5,
                'xanchor': 'center',
                'y': 0.9,
                'yanchor': 'top'
            }
        )

        fig2.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))

        st.plotly_chart(fig2)

    else:

        column, buffer = st.columns([5, 4])
        column.info("Please select atleast one state to display the plot.")
        add_vertical_space(8)

    # 3

    st.subheader(':green[Transaction amount comparison - Quarterwise]')

    col4, col5, buff = st.columns([3, 2, 4])

    region2 = col4.selectbox('Region', trans_df2['Region'].unique(), key='region2')
    year2 = col5.selectbox('Year', years, key='year2')

    filtered_df = trans_df2[(trans_df2['Region'] == region2) & (trans_df2['Year'] == year2)]

    filtered_df['Quarter'] = 'Quarter ' + filtered_df['Quarter'].astype(str)

    fig3 = px.pie(
        filtered_df, values='Transaction_amount',
        names='Quarter', color='Quarter',
        title=f'Transaction amount Comparison of {region2} for the year {year2}'
    )

    fig3.update_layout(
        width=850, height=550,
        title={
            'x': 0.45,
            'xanchor': 'center',
            'y': 0.9,
            'yanchor': 'top'
        }
    )

    fig3.update_traces(textposition='inside', textinfo='percent+label')

    st.plotly_chart(fig3)

    filtered_df['Year'] = filtered_df["Year"].astype(int)

    expander1 = st.expander('Detailed view')
    expander1.dataframe(
        filtered_df.groupby(
            [
                'Year', 'Quarter'
            ]
        ).agg(
            {
                'Transaction_amount': sum
            }
        ).reset_index().sort_values(
            'Transaction_amount',
            ascending=False
        ).loc[:, ['Quarter', 'Transaction_amount']].reset_index(drop=True))
