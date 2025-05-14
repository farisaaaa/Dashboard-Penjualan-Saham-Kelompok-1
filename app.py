import streamlit as st # Library untuk membuat aplikasi web interaktif
import pandas as pd  # Library untuk manipulasi data
import numpy as np  # Library untuk operasi numerik
import plotly.express as px  # Library untuk membuat grafik interaktif

# Menambahkan navbar untuk navigasi
st.sidebar.header("Navigasi")
page = st.sidebar.radio("Pilih Halaman", ["Dashboard Umum", "Dashboard Filter", "Dashboard Keuntungan"])

# Membaca dataset dari file CSV
df = pd.read_csv('dataset/penjualan_saham.csv')

# Halaman Dashboard Umum
if page == "Dashboard Umum":
    # Menampilkan judul halaman
    st.markdown("<h1 style='text-align: center;'>Dashboard Data Saham</h1>", unsafe_allow_html=True)
    
    # Menampilkan informasi struktur dataframe
    st.subheader("Informasi Dataframe")
    st.write("Berikut adalah informasi keseluruhan dari dataset:")
    st.write(df.info())  # Menampilkan informasi struktur dataframe
    
    # Menampilkan seluruh data dalam dataframe
    st.subheader("Dataframe Keseluruhan")
    st.dataframe(df)
    
    # Menampilkan statistik deskriptif untuk kolom numerik
    st.subheader("Statistik Deskriptif")
    st.write(df.describe())

# Halaman Dashboard Filter
if page == "Dashboard Filter":
    # Menampilkan judul halaman
    st.markdown("<h1 style='text-align: center;'>Dashboard Saham Perusahaan</h1>", unsafe_allow_html=True)

    # Sidebar untuk filter data
    st.sidebar.header("Filter")
    companies = df['Perusahaan'].unique()  # Mendapatkan daftar unik perusahaan
    selected_company = st.sidebar.selectbox("Pilih Perusahaan", companies)  # Dropdown untuk memilih perusahaan

    # Menambahkan filter rentang waktu
    min_date, max_date = pd.to_datetime(df['Tanggal']).min(), pd.to_datetime(df['Tanggal']).max()
    start_date = st.sidebar.date_input("Pilih Tanggal Awal", min_date)  # Input untuk memilih tanggal awal
    end_date = st.sidebar.date_input("Pilih Tanggal Akhir", max_date)  # Input untuk memilih tanggal akhir

    # Menambahkan filter untuk memilih kolom yang akan ditampilkan di grafik
    columns_to_display = st.sidebar.multiselect(
        "Pilih Kolom yang Akan Ditampilkan di Grafik",
        options=["Harga Saham", "Volume Perdagangan", "Keuntungan"],
        default=["Harga Saham", "Volume Perdagangan", "Keuntungan"]
    )

    # Filter data berdasarkan perusahaan dan rentang waktu
    filtered_df = df[
        (df['Perusahaan'] == selected_company) &
        (pd.to_datetime(df['Tanggal']) >= pd.to_datetime(start_date)) &
        (pd.to_datetime(df['Tanggal']) <= pd.to_datetime(end_date))
    ]

    # Menampilkan informasi dataset yang difilter
    st.subheader("Informasi Dataset")
    st.write(f"Dataset ini berisi data saham dari perusahaan: {selected_company}")
    st.write(filtered_df.info())

    # Menambahkan kolom tahun, bulan, dan memformat tanggal
    filtered_df['Tahun'] = pd.to_datetime(filtered_df['Tanggal']).dt.year
    filtered_df['Bulan'] = pd.to_datetime(filtered_df['Tanggal']).dt.strftime('%B')
    filtered_df['Tanggal'] = pd.to_datetime(filtered_df['Tanggal']).dt.strftime('%d/%m/%y')

    # Menampilkan data saham yang difilter
    st.subheader(f"Data Saham: {selected_company}")
    st.dataframe(filtered_df[["Tanggal", "Perusahaan", "Tahun", "Bulan"] + columns_to_display])

    # Menampilkan grafik interaktif untuk tren harian
    st.subheader(f"Tren Harian Harga Saham, Volume Perdagangan, dan Keuntungan - {selected_company}")
    filtered_df['Tanggal'] = pd.to_datetime(filtered_df['Tanggal'], format='%d/%m/%y')

    # Grafik interaktif untuk harga saham
    fig_harga = px.line(filtered_df, x='Tanggal', y='Harga Saham', title=f"Tren Harian Harga Saham - {selected_company}")
    st.plotly_chart(fig_harga)

    # Grafik interaktif untuk volume perdagangan
    fig_volume = px.line(filtered_df, x='Tanggal', y='Volume Perdagangan', title=f"Tren Harian Volume Perdagangan - {selected_company}")
    st.plotly_chart(fig_volume)

    # Grafik interaktif untuk keuntungan
    fig_keuntungan = px.line(filtered_df, x='Tanggal', y='Keuntungan', title=f"Tren Harian Keuntungan - {selected_company}")
    st.plotly_chart(fig_keuntungan)

    # Menampilkan ringkasan statistik
    st.subheader("Ringkasan Statistik")
    perusahaan_terpilih = filtered_df['Perusahaan'].unique()
    total_harga_saham = filtered_df['Harga Saham'].sum()
    total_volume_perdagangan = filtered_df['Volume Perdagangan'].sum()
    total_keuntungan = filtered_df['Keuntungan'].sum()
    rata_rata_harga_saham = filtered_df['Harga Saham'].mean()
    rata_rata_volume_perdagangan = filtered_df['Volume Perdagangan'].mean()
    rata_rata_keuntungan = filtered_df['Keuntungan'].mean()

    # Menampilkan ringkasan statistik
    st.write(f"- **Nama Perusahaan Terpilih**: {', '.join(perusahaan_terpilih)}")
    st.write(f"- **Total Harga Saham**: {total_harga_saham:,}")
    st.write(f"- **Total Volume Perdagangan**: {total_volume_perdagangan:,}")
    st.write(f"- **Total Keuntungan**: {total_keuntungan:,}")
    st.write(f"- **Rata-rata Harga Saham**: {rata_rata_harga_saham:.2f}")
    st.write(f"- **Rata-rata Volume Perdagangan**: {rata_rata_volume_perdagangan:.2f}")
    st.write(f"- **Rata-rata Keuntungan**: {rata_rata_keuntungan:.2f}")

# Halaman Dashboard Keuntungan
elif page == "Dashboard Keuntungan":
    # Menampilkan judul halaman
    st.markdown("<h1 style='text-align: center;'>Dashboard Keuntungan Saham Antar Perusahaan</h1>", unsafe_allow_html=True)

    # Sidebar untuk filter data
    st.sidebar.header("Filter Perbandingan")
    years = pd.to_datetime(df['Tanggal']).dt.year.unique()
    months = pd.to_datetime(df['Tanggal']).dt.month_name().unique()

    # Input untuk memilih tahun dan bulan
    selected_year = st.sidebar.selectbox("Pilih Tahun", sorted(years))
    selected_month = st.sidebar.selectbox("Pilih Bulan", months)
    selected_companies = st.sidebar.multiselect("Pilih Perusahaan", df['Perusahaan'].unique())

    # Konversi bulan ke angka dan filter data
    month_to_number = {month: i + 1 for i, month in enumerate(months)}
    start_date = pd.Timestamp(year=selected_year, month=month_to_number[selected_month], day=1)
    end_date = start_date + pd.offsets.MonthEnd(0)

    filtered_df = df[
        (pd.to_datetime(df['Tanggal']) >= start_date) &
        (pd.to_datetime(df['Tanggal']) <= end_date) &
        (df['Perusahaan'].isin(selected_companies))
    ]
    filtered_df['Tahun'] = pd.to_datetime(filtered_df['Tanggal']).dt.year

    # Menghitung total keuntungan per tahun untuk setiap perusahaan
    yearly_profit = filtered_df.groupby(['Tahun', 'Perusahaan'])['Keuntungan'].sum().reset_index()

    # Menampilkan tabel keuntungan per tahun
    st.subheader("Keuntungan Per Tahun Berdasarkan Perusahaan")
    st.dataframe(yearly_profit)

    # Menampilkan grafik interaktif untuk perbandingan keuntungan antar perusahaan
    st.subheader("Grafik Perbandingan Keuntungan Antar Perusahaan")
    fig_keuntungan_perusahaan = px.bar(
        yearly_profit,
        x='Tahun',
        y='Keuntungan',
        color='Perusahaan',
        barmode='group',
        title=f"Perbandingan Keuntungan Antar Perusahaan ({selected_month} {selected_year})"
    )
    st.plotly_chart(fig_keuntungan_perusahaan)

    # Menampilkan kesimpulan keuntungan
    st.subheader("Kesimpulan")
    company_profits = filtered_df.groupby('Perusahaan')['Keuntungan'].sum().reset_index()
    company_profits = company_profits.sort_values(by='Keuntungan', ascending=False)

    # Menampilkan keuntungan masing-masing perusahaan
    st.write("Keuntungan masing-masing perusahaan:")
    for _, row in company_profits.iterrows():
        st.write(f"- {row['Perusahaan']}: **{row['Keuntungan']:,}**")

    # Menentukan perusahaan dengan keuntungan terbesar
    if not company_profits.empty:
        top_company = company_profits.iloc[0]
        st.write(f"\nPerusahaan dengan keuntungan paling besar adalah **{top_company['Perusahaan']}** dengan total keuntungan **{top_company['Keuntungan']:,}**.")
    else:
        st.write("Tidak ada data keuntungan untuk perusahaan yang dipilih.")