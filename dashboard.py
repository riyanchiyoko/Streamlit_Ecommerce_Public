import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from datetime import datetime

top_5_sellers = pd.read_csv('top_5_sellers.csv')
merged_op = pd.read_csv('merged_op.csv')
merged_df = pd.read_csv('merged_df.csv')

category_sales_s = merged_op.groupby('product_category_name')['order_item_id'].count().reset_index()
category_sales_s.rename(columns={'order_item_id': 'total_items_sold'}, inplace=True)
category_sales_sorted = category_sales_s.sort_values(by='total_items_sold', ascending=False)
top_categories_s = category_sales_sorted.head(5)
bottom_categories_s = category_sales_sorted.tail(5)

merged_df['order_purchase_timestamp'] = pd.to_datetime(merged_df['order_purchase_timestamp'])
merged_df['year_month'] = merged_df['order_purchase_timestamp'].dt.to_period('M')
merged_df = merged_df[merged_df['order_purchase_timestamp'].dt.year == 2018]
category_sales = merged_df.groupby(['product_category_name', 'year_month'])['order_item_id'].count().reset_index()
category_sales.rename(columns={'order_item_id': 'total_items_sold'}, inplace=True)
top_categories = category_sales.groupby('product_category_name')['total_items_sold'].sum().nlargest(5).index
top_category_sales = category_sales[category_sales['product_category_name'].isin(top_categories)].copy()
top_category_sales['year_month'] = top_category_sales['year_month'].dt.to_timestamp()

# Fungsi Visualisasi untuk Top 5 Sellers
def visualize_top_sellers():
    st.title('Top 5 Seller dengan Total Penjualan Tertinggi di Tahun 2018')
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_5_sellers['seller_id'].astype(str), top_5_sellers['total_sales'], color='skyblue')
    ax.set_title('5 Seller dengan Total Penjualan Tertinggi di Tahun 2018', fontsize=16)
    ax.set_xlabel('Total Penjualan', fontsize=12)
    ax.set_ylabel('Seller ID', fontsize=12)

    # Menambahkan format pada sumbu X agar menunjukkan angka dengan pemisah ribuan
    formatter = FuncFormatter(lambda x, pos: '{:,.0f}'.format(x))
    ax.xaxis.set_major_formatter(formatter)

    # Menyusun layout agar lebih rapi
    plt.tight_layout()

    # Menampilkan grafik di Streamlit
    st.pyplot(fig)

# Fungsi Visualisasi untuk Top 5 dan Bottom 5 Categories
def visualize_top_and_bottom_categories():
    st.title(' 5 Top dan Bottom Kategori Produk di Tahun 2018')
    # Plot kategori produk
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Grafik untuk 5 kategori produk dengan penjualan terlaris
    axes[0].bar(top_categories_s['product_category_name'], top_categories_s['total_items_sold'], color='green')
    axes[0].set_title('5 Kategori Produk Terlaris di Tahun 2018')
    axes[0].set_xlabel('Kategori Produk')
    axes[0].set_ylabel('Jumlah Item Terjual')
    axes[0].tick_params(axis='x', rotation=30)

    # Grafik untuk 5 kategori produk dengan penjualan terendah
    axes[1].bar(bottom_categories_s['product_category_name'], bottom_categories_s['total_items_sold'], color='red')
    axes[1].set_title('5 Kategori Produk Terendah di Tahun 2018')
    axes[1].set_xlabel('Kategori Produk')
    axes[1].set_ylabel('Jumlah Item Terjual')
    axes[1].tick_params(axis='x', rotation=30)

    # Menyusun layout agar tidak saling tumpang tindih
    plt.tight_layout()

    # Menampilkan grafik di Streamlit
    st.pyplot(fig)

# Fungsi Visualisasi untuk Penjualan Bulanan per Kategori
def visualize_monthly_sales_for_categories():
    st.title('5 Kategori Produk Terlaris Per Bulan di Tahun 2018')
    plt.figure(figsize=(12, 6))
    
    for category in top_categories:
        category_data = top_category_sales[top_category_sales['product_category_name'] == category]
        plt.plot(category_data['year_month'], category_data['total_items_sold'], label=category)
    
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Item Terjual')
    plt.title('5 Kategori Produk dengan Total Penjualan Tertinggi Setiap Bulan di Tahun 2018')
    plt.xticks(pd.date_range('2018-01-01', '2018-12-31', freq='MS'), rotation=45)
    plt.legend(title='Kategori Produk')
    plt.tight_layout()
    st.pyplot(plt)

# Streamlit interactivity
st.sidebar.title("Navigasi Dashboard")
option = st.sidebar.selectbox(
    "Pilih visualisasi",
    ["Top Seller", "Top and Bottom Product Categories", "Monthly Sales per Category"]
)

if option == "Top Seller":
    visualize_top_sellers()
elif option == "Top and Bottom Product Categories":
    visualize_top_and_bottom_categories()
elif option == "Monthly Sales per Category":
    visualize_monthly_sales_for_categories()
