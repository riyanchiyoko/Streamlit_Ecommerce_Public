import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
from datetime import datetime

# Load data
top_5_sellers = pd.read_csv('top_5_sellers.csv')
merged_op = pd.read_csv('merged_op.csv')
merged_df = pd.read_csv('merged_df.csv')

# Data preprocessing
merged_df['order_purchase_timestamp'] = pd.to_datetime(merged_df['order_purchase_timestamp'])
merged_df['year_month'] = merged_df['order_purchase_timestamp'].dt.to_period('M')

category_sales_s = merged_op.groupby('product_category_name')['order_item_id'].count().reset_index()
category_sales_s.rename(columns={'order_item_id': 'total_items_sold'}, inplace=True)
category_sales_sorted = category_sales_s.sort_values(by='total_items_sold', ascending=False)
top_categories_s = category_sales_sorted.head(5)
bottom_categories_s = category_sales_sorted.tail(5)

category_sales = merged_df.groupby(['product_category_name', 'year_month'])['order_item_id'].count().reset_index()
category_sales.rename(columns={'order_item_id': 'total_items_sold'}, inplace=True)
all_categories = category_sales['product_category_name'].unique()

# Mengubah nama bulan menjadi format bahasa Indonesia
month_names = merged_df['year_month'].dt.strftime('%B').unique()

# Sidebar: Pilih visualisasi
st.sidebar.title("Navigasi Dashboard")
option = st.sidebar.selectbox(
    "Pilih visualisasi",
    ["Top Seller", "Top and Bottom Product Categories", "Monthly Sales per Category"]
)

# Fungsi visualisasi
def visualize_top_sellers():
    st.title('Top 5 Seller dengan Total Penjualan Tertinggi')

    # Filter untuk memilih bulan dengan nilai "All" sebagai default
    month_options = ['All'] + [m.capitalize() for m in month_names]
    month_selected = st.sidebar.selectbox(
        "Pilih Bulan",
        options=month_options,
        index=0
    )
    if month_selected == 'All':
        filtered_data = merged_df
    else:
        filtered_data = merged_df[merged_df['order_purchase_timestamp'].dt.strftime('%B') == month_selected]

    top_sellers_filtered = (
        filtered_data.groupby('seller_id')['order_item_id']
        .count()
        .reset_index()
        .rename(columns={'order_item_id': 'total_sales'})
        .sort_values(by='total_sales', ascending=False)
        .head(5)
    )

    # Visualisasi
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(top_sellers_filtered['seller_id'].astype(str), top_sellers_filtered['total_sales'], color='skyblue')
    ax.set_title(
        f'5 Seller dengan Total Penjualan Tertinggi - {month_selected if month_selected != "All" else "Semua Bulan"}',
        fontsize=16
    )
    ax.set_xlabel('Total Penjualan', fontsize=12)
    ax.set_ylabel('Seller ID', fontsize=12)
    formatter = FuncFormatter(lambda x, pos: '{:,.0f}'.format(x))
    ax.xaxis.set_major_formatter(formatter)
    plt.tight_layout()
    st.pyplot(fig)

def visualize_top_and_bottom_categories():
    st.title('Top dan Bottom Kategori Produk Per Bulan')

    # Filter untuk memilih bulan
    month_selected = st.sidebar.selectbox(
        "Pilih Bulan",
        options=[m.capitalize() for m in month_names] 
    )
    filtered_data = category_sales[category_sales['year_month'].dt.strftime('%B') == month_selected]
    top_categories_s = filtered_data.sort_values(by='total_items_sold', ascending=False).head(5)
    bottom_categories_s = filtered_data.sort_values(by='total_items_sold', ascending=True).head(5)

    # Visualisasi
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    axes[0].bar(top_categories_s['product_category_name'], top_categories_s['total_items_sold'], color='green')
    axes[0].set_title(f'5 Kategori Produk Terlaris - {month_selected}')
    axes[0].set_xlabel('Kategori Produk')
    axes[0].set_ylabel('Jumlah Item Terjual')
    axes[0].tick_params(axis='x', rotation=30)
    
    axes[1].bar(bottom_categories_s['product_category_name'], bottom_categories_s['total_items_sold'], color='red')
    axes[1].set_title(f'5 Kategori Produk Terendah - {month_selected}')
    axes[1].set_xlabel('Kategori Produk')
    axes[1].set_ylabel('Jumlah Item Terjual')
    axes[1].tick_params(axis='x', rotation=30)

    plt.tight_layout()
    st.pyplot(fig)

def visualize_monthly_sales_for_categories():
    st.title('Penjualan Bulanan Per Kategori')

    # Sidebar: Filter khusus untuk visualisasi ini
    date_range = st.sidebar.date_input(
        "Pilih rentang tanggal",
        [merged_df['order_purchase_timestamp'].min(), merged_df['order_purchase_timestamp'].max()]
    )
    # Validasi: rentang tanggal awal dan akhir dipilih dengan benar
    if len(date_range) != 2:
        st.warning("Harap pilih rentang tanggal awal dan akhir.")
        return  # Menghentikan eksekusi jika rentang tanggal belum dipilih
    else:
        start_date, end_date = date_range[0], date_range[1]

    # Sidebar: Pilih kategori produk
    selected_categories = st.sidebar.multiselect(
        "Pilih kategori produk",
        options=all_categories,
        default=all_categories[:5]
    )
    # Validasi: Pastikan kategori produk dipilih
    if not selected_categories:
        st.warning("Harap pilih minimal satu kategori produk.")
        return  # Menghentikan eksekusi jika tidak ada kategori yang dipilih

    # Filter data berdasarkan tanggal dan kategori
    filtered_df = merged_df[
        (merged_df['order_purchase_timestamp'] >= pd.Timestamp(start_date)) &
        (merged_df['order_purchase_timestamp'] <= pd.Timestamp(end_date)) &
        (merged_df['product_category_name'].isin(selected_categories))
    ]

    # Validasi: Pastikan data tidak kosong
    if filtered_df.empty:
        st.warning("Tidak ada data untuk rentang tanggal dan kategori yang dipilih.")
        return

    # Visualisasi data
    plt.figure(figsize=(12, 6))
    for category in selected_categories:
        category_data = category_sales[
            (category_sales['product_category_name'] == category) &
            (category_sales['year_month'].dt.to_timestamp() >= pd.Timestamp(start_date)) &
            (category_sales['year_month'].dt.to_timestamp() <= pd.Timestamp(end_date))
        ]
        plt.plot(category_data['year_month'].dt.to_timestamp(), category_data['total_items_sold'], label=category)
    
    plt.xlabel('Bulan')
    plt.ylabel('Jumlah Item Terjual')
    plt.title('Penjualan Bulanan Per Kategori')
    plt.xticks(pd.date_range(start_date, end_date, freq='MS'), rotation=45)
    plt.legend(title='Kategori Produk')
    plt.tight_layout()
    st.pyplot(plt)


# Menampilkan visualisasi sesuai pilihan
if option == "Top Seller":
    visualize_top_sellers()
elif option == "Top and Bottom Product Categories":
    visualize_top_and_bottom_categories()
elif option == "Monthly Sales per Category":
    visualize_monthly_sales_for_categories()
