import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.header('Sales Insight Application for Business Owner', divider=True)

uploaded_file = st.file_uploader("Upload File Excel yang ingin dianalisis")

if uploaded_file is not None:
    st.success(f"Upload File Berhasil !")
    
    df_init = pd.read_excel(uploaded_file, header=4)
    st.write('Sample data:',df_init.head(2))

    with st.sidebar:
        st.write('Pilih filter untuk melihat lebih detail\n')

        unique_region = ['All']+df_init['Region'].unique().tolist()
        selected_region = st.selectbox("Region", unique_region)

        unique_sales_method = ['All']+df_init['Sales Method'].unique().tolist()
        selected_sales_method = st.selectbox("Sales Method", unique_sales_method)

    if selected_region != 'All' and selected_sales_method != 'All':
        df = df_init[(df_init['Region'] == selected_region) & (df_init['Sales Method'] == selected_sales_method)]
    elif selected_region != 'All':
        df = df_init[df_init['Region'] == selected_region]
    elif selected_sales_method != 'All':
        df = df_init[df_init['Sales Method'] == selected_sales_method]
    else:
        df = df_init.copy()

    st.subheader('Sales Overview', divider=True)
    col1, col2, col3 = st.columns(3)
    col1.metric(label="Total Sales", value=f"Rp. {np.round(df['Total Sales'].sum()/1000000, 2)} Jt")
    col2.metric(label="#Units Sold", value=f"{df['Units Sold'].sum()} item")
    col3.metric(label="Avg Operating Margin", value=f"Rp. {np.round(df['Operating Margin'].mean()*100,2)} %")

    st.subheader('Total Sales by Retailer and Product', divider=True)
    barchart_data = df.groupby(['Product','Retailer'])['Total Sales'].sum().reset_index()
    st.bar_chart(barchart_data, x="Product", y="Total Sales", color="Retailer")

    # Fungsi untuk melakukan agregasi harian untuk setiap produk
    def aggregate_daily_sales(df):
        df['Invoice Date'] = pd.to_datetime(df['Invoice Date'])
        df = df.groupby(['Product', pd.Grouper(key='Invoice Date', freq='M')])['Total Sales'].sum().reset_index()
        return df
    # Agregat harian untuk setiap produk
    df_daily = aggregate_daily_sales(df)

    st.subheader('Monthly Sales Product', divider=True)
    # Buat line chart menggunakan Plotly Express dengan produk sebagai warna
    fig = px.line(df_daily, x='Invoice Date', y='Total Sales', color='Product')
    st.plotly_chart(fig)


















# # Fungsi untuk mengenerate data dummy
# def generate_df(n):
#     # Generate tanggal-tanggal random dari 2022 hingga 2023
#     dates = pd.date_range(start='2022-01-01', end='2023-12-31', freq='D')
#     # Generate kategori produk secara random
#     categories = ['Electronics', 'Home and Kitchen', 'Sports and Outdoors']
#     # Generate status pesanan secara random
#     statuses = ['Completed', 'Cancelled']
#     # Generate jumlah penjualan secara random
#     amounts = np.random.randint(100, 10000, size=n)
#     # Generate jumlah barang yang terjual secara random
#     quantities = np.random.randint(1, 10, size=n)
#     # Gabungkan data ke dalam DataFrame
#     data = {'date': np.random.choice(dates, size=n),
#             'order_status': np.random.choice(statuses, size=n),
#             'sales_amount': amounts,
#             'sales_qty': quantities,
#             'product_category': np.random.choice(categories, size=n)}
#     df = pd.DataFrame(data)
#     return df

# # Generate data dummy dengan 500 baris
# df = generate_df(500)

# # Judul aplikasi
# st.title("Sales Report")

# # Deskripsi aplikasi
# st.write("Aplikasi ini menampilkan laporan penjualan dalam bentuk tabel dan visualisasi.")

# # Filter berdasarkan status pesanan dan kategori produk
# statuses = np.append(df['order_status'].unique(), 'All')
# categories = np.append(df['product_category'].unique(), 'All')

# with st.sidebar:
#     from PIL import Image
#     image = Image.open('ecommerse.png')
#     st.image(image, width=150)
#     st.write("Filter")
#     selected_status = st.selectbox("Status Pesanan", statuses)
#     selected_category = st.selectbox("Kategori Produk", categories)

# if selected_status != 'All' and selected_category != 'All':
#     filtered_data = df[(df['order_status'] == selected_status) & 
#                                (df['product_category'] == selected_category)]
# elif selected_status != 'All':
#     filtered_data = df[df['order_status'] == selected_status]
# elif selected_category != 'All':
#     filtered_data = df[df['product_category'] == selected_category]
# else:
#     filtered_data = df.copy()

# # definisikan tabnya
# statistic_descriptive_tab, trend_analysis_tab = st.tabs(['Statistik Deskriptif','Trend Analysis'])

# with statistic_descriptive_tab:
#     st.dataframe(filtered_data.describe().T)
#     from plotly.subplots import make_subplots
#     # membuat subplots dengan 1 baris dan 2 kolom
#     fig = make_subplots(rows=1, cols=2)
#     # membuat boxplot untuk sales_amount dan menambahkannya ke subplot di kolom pertama
#     fig.add_trace(px.box(filtered_data, y='sales_amount', labels={'value': 'Jumlah'}).data[0], row=1, col=1)
#     # memberikan judul pada boxplot pertama
#     fig.update_yaxes(title_text='Sales Amount', row=1, col=1)
#     # membuat boxplot untuk sales_qty dan menambahkannya ke subplot di kolom kedua
#     fig.add_trace(px.box(filtered_data, y='sales_qty', labels={'value': 'Jumlah'}).data[0], row=1, col=2)
#     # memberikan judul pada boxplot kedua
#     fig.update_yaxes(title_text='Sales Quantity', row=1, col=2)
#     # mengatur judul pada subplot
#     fig.update_layout(title='Sales Amount dan Sales Qty Distribution', xaxis={'visible': False})
#     # menampilkan subplot
#     st.plotly_chart(fig)


# with trend_analysis_tab:
#     # Tab kedua: Trend Analysis
#     st.write("Berikut ini adalah trend penjualan per bulan dan per kuartal:")
#     # Monthly Sales Trend
#     monthly_sales = filtered_data.resample('M', on='date').sum().reset_index()
#     monthly_sales_chart = px.line(monthly_sales, x='date', y='sales_amount', 
#                                 labels={'date': 'Bulan', 'sales_amount': 'Penjualan'},
#                                 title='Trend Penjualan Bulanan', markers=True)
#     st.plotly_chart(monthly_sales_chart)

#     # Quarterly Sales Trend
#     filtered_data['quarter'] = filtered_data['date'].dt.quarter
#     quarter_sales = filtered_data.groupby(['quarter']).agg({'sales_amount': 'sum', 'sales_qty': 'sum'}).reset_index()
#     fig = make_subplots(specs=[[{"secondary_y": True}]])
#     # membuat bar chart untuk sales_amount
#     fig.add_trace(px.bar(quarter_sales, x='quarter', y='sales_amount',
#                         labels={'quarter': 'Kuartal', 'sales_amount': 'Penjualan'}).data[0], secondary_y=False)
#     # membuat line chart untuk sales_qty
#     fig.add_trace(px.line(quarter_sales, x='quarter', y='sales_qty',
#                         labels={'sales_qty': 'Jumlah'}).update_traces(line=dict(color='orange')).data[0], secondary_y=True)
#     # mengatur judul dan label sumbu pada chart
#     fig.update_layout(title='Trend Penjualan Kuartalan',
#                     xaxis={'title': 'Kuartal'},
#                     yaxis={'title': 'Penjualan'},
#                     yaxis2={'title': 'Jumlah'})
#     # menampilkan chart
#     st.plotly_chart(fig)
