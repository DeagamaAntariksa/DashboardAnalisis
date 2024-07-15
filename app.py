import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go

# Load data
data1 = pd.read_csv('modified.csv')  # Sesuaikan dengan jalur data Anda

# Konversi kolom tanggal ke format datetime
data1['D.O.A'] = pd.to_datetime(data1['D.O.A'], format='%Y-%m-%d', errors='coerce')
data1['D.O.D'] = pd.to_datetime(data1['D.O.D'], format='%Y-%m-%d', errors='coerce')

# Tambahkan kolom tahun
data1['year'] = data1['D.O.A'].dt.year.astype(str)  # Convert year to string

# Konversi kolom kategori
columns_to_convert = ['GENDER', 'RURAL', 'TYPE OF ADMISSION-EMERGENCY/OPD', 'OUTCOME', 'SMOKING', 'ALCOHOL',
                      'DM', 'HTN', 'CAD', 'PRIOR CMP', 'CKD', 'RAISED CARDIAC ENZYMES', 'SEVERE ANAEMIA',
                      'ANAEMIA', 'STABLE ANGINA', 'ACS', 'STEMI', 'ATYPICAL CHEST PAIN', 'HEART FAILURE',
                      'HFREF', 'HFNEF', 'VALVULAR', 'CHB', 'SSS', 'AKI', 'CVA INFRACT', 'CVA BLEED', 'AF',
                      'VT', 'PSVT', 'CONGENITAL', 'UTI', 'NEURO CARDIOGENIC SYNCOPE', 'ORTHOSTATIC',
                      'INFECTIVE ENDOCARDITIS', 'DVT', 'CARDIOGENIC SHOCK', 'SHOCK', 'PULMONARY EMBOLISM',
                      'CHEST INFECTION']
data1[columns_to_convert] = data1[columns_to_convert].astype('category')

# Setup Streamlit
st.title("Dashboard Kinerja Rumah Sakit")

# Sidebar for navigation
st.sidebar.title("Navigasi")
options = st.sidebar.selectbox("Pilih Analisis:", [
    "Distribusi Pasien Berdasarkan Gender",
    "Rata-rata Durasi Tinggal Berdasarkan Kebiasaan Merokok",
    "Rata-rata Usia Pasien dengan Heart Failure",
    "Persentase Pasien Berdasarkan Outcome",
    "Distribusi Kondisi Medis Berdasarkan Outcome",
    "Pengaruh Durasi Tinggal terhadap Outcome",
    "Faktor Risiko pada Pasien dengan dan tanpa Heart Failure",
    "Tren Tipe Admission dari Tahun ke Tahun",
    "Perubahan Rata-rata Durasi Tinggal dari Waktu ke Waktu"
])

# 1. Distribusi Pasien Berdasarkan Gender
if options == "Distribusi Pasien Berdasarkan Gender":
    st.subheader("Distribusi Pasien Berdasarkan Gender")
    gender_distribution = data1['GENDER'].value_counts()
    st.write(gender_distribution)
    fig = px.bar(gender_distribution, x=gender_distribution.index, y=gender_distribution.values, 
                 labels={'x': 'Gender', 'y': 'Jumlah Pasien'}, title='Distribusi Pasien Berdasarkan Gender')
    st.plotly_chart(fig)

# 2. Rata-rata Durasi Tinggal Berdasarkan Kebiasaan Merokok
elif options == "Rata-rata Durasi Tinggal Berdasarkan Kebiasaan Merokok":
    st.subheader("Rata-rata Durasi Tinggal Berdasarkan Kebiasaan Merokok")
    duration_by_smoking = data1.groupby('SMOKING')['DURATION OF STAY'].mean().reset_index()
    st.write(duration_by_smoking)
    fig = px.bar(duration_by_smoking, x='SMOKING', y='DURATION OF STAY', 
                 labels={'SMOKING': 'Kebiasaan Merokok', 'DURATION OF STAY': 'Rata-rata Durasi Tinggal'}, 
                 title='Rata-rata Durasi Tinggal Berdasarkan Kebiasaan Merokok')
    st.plotly_chart(fig)

# 3. Rata-rata Usia Pasien dengan Heart Failure
elif options == "Rata-rata Usia Pasien dengan Heart Failure":
    st.subheader("Rata-rata Usia Pasien dengan Heart Failure")
    heart_failure_age = data1[data1['HEART FAILURE'] == 'Ya']['AGE'].mean()
    st.write(f"Rata-rata Usia Pasien dengan HEART FAILURE: {heart_failure_age:.2f} tahun")

# 4. Persentase Pasien Berdasarkan Outcome
elif options == "Persentase Pasien Berdasarkan Outcome":
    st.subheader("Persentase Pasien Berdasarkan Outcome")
    outcome_distribution = data1['OUTCOME'].value_counts(normalize=True) * 100
    st.write(outcome_distribution)
    fig = px.pie(outcome_distribution, values=outcome_distribution.values, names=outcome_distribution.index, 
                 title='Persentase Pasien Berdasarkan OUTCOME', labels={'label': 'Outcome', 'value': 'Persentase'})
    st.plotly_chart(fig)

# 5. Distribusi Kondisi Medis Berdasarkan Outcome
elif options == "Distribusi Kondisi Medis Berdasarkan Outcome":
    st.subheader("Distribusi Kondisi Medis Berdasarkan Outcome")
    discharged_patients = data1[data1['OUTCOME'] == 'DISCHARGE']
    expired_patients = data1[data1['OUTCOME'] == 'EXPIRY']
    dama_patients = data1[data1['OUTCOME'] == 'DAMA']
    conditions = ['DM', 'HTN', 'CAD', 'PRIOR CMP', 'CKD']

    discharged_conditions_distribution = discharged_patients[conditions].apply(pd.Series.value_counts).fillna(0)
    expired_conditions_distribution = expired_patients[conditions].apply(pd.Series.value_counts).fillna(0)
    dama_conditions_distribution = dama_patients[conditions].apply(pd.Series.value_counts).fillna(0)

    st.write("Distribusi kondisi medis pada pasien dengan outcome DISCHARGE:")
    st.write(discharged_conditions_distribution)
    st.write("\nDistribusi kondisi medis pada pasien dengan outcome EXPIRY:")
    st.write(expired_conditions_distribution)
    st.write("\nDistribusi kondisi medis pada pasien dengan outcome DAMA:")
    st.write(dama_conditions_distribution)

    def plot_conditions_distribution(distribution, title):
        distribution = distribution.T
        fig = go.Figure()
        for condition in distribution.columns:
            fig.add_trace(go.Bar(name=condition, x=distribution.index, y=distribution[condition]))
        fig.update_layout(barmode='stack', title=title, xaxis_title='Kondisi Medis', yaxis_title='Jumlah Pasien')
        st.plotly_chart(fig)

    plot_conditions_distribution(discharged_conditions_distribution, "Distribusi Kondisi Medis pada Pasien dengan Outcome 'DISCHARGE'")
    plot_conditions_distribution(expired_conditions_distribution, "Distribusi Kondisi Medis pada Pasien dengan Outcome 'EXPIRY'")
    plot_conditions_distribution(dama_conditions_distribution, "Distribusi Kondisi Medis pada Pasien dengan Outcome 'DAMA'")

# 6. Pengaruh Durasi Tinggal terhadap Outcome
elif options == "Pengaruh Durasi Tinggal terhadap Outcome":
    st.subheader("Pengaruh Durasi Tinggal terhadap Outcome")
    duration_outcome = data1.groupby('OUTCOME')['DURATION OF STAY'].mean().reset_index()
    st.write(duration_outcome)
    fig = px.bar(duration_outcome, x='OUTCOME', y='DURATION OF STAY', 
                 labels={'OUTCOME': 'Outcome', 'DURATION OF STAY': 'Rata-rata Durasi Tinggal'}, 
                 title='Pengaruh Durasi Tinggal terhadap Outcome Pasien')
    st.plotly_chart(fig)

# 7. Faktor Risiko pada Pasien dengan dan tanpa Heart Failure
elif options == "Faktor Risiko pada Pasien dengan dan tanpa Heart Failure":
    st.subheader("Faktor Risiko pada Pasien dengan dan tanpa Heart Failure")
    heart_failure_yes = data1[data1['HEART FAILURE'] == 'Ya']
    heart_failure_no = data1[data1['HEART FAILURE'] == 'Tidak']

    heart_failure_risks_yes = heart_failure_yes[['DM', 'HTN', 'CAD']].apply(pd.Series.value_counts).fillna(0)
    st.write("Faktor Risiko pada Pasien dengan HEART FAILURE (Ya):")
    st.write(heart_failure_risks_yes)

    heart_failure_risks_no = heart_failure_no[['DM', 'HTN', 'CAD']].apply(pd.Series.value_counts).fillna(0)
    st.write("Faktor Risiko pada Pasien tanpa HEART FAILURE (Tidak):")
    st.write(heart_failure_risks_no)

    risk_factors = ['DM', 'HTN', 'CAD']
    fig = go.Figure()
    for factor in risk_factors:
        fig.add_trace(go.Bar(name=f"{factor} - Heart Failure (Ya)", x=heart_failure_risks_yes.index, y=heart_failure_risks_yes[factor]))
        fig.add_trace(go.Bar(name=f"{factor} - Heart Failure (Tidak)", x=heart_failure_risks_no.index, y=heart_failure_risks_no[factor]))

    fig.update_layout(barmode='group', title='Faktor Risiko pada Pasien dengan dan tanpa HEART FAILURE', 
                      xaxis_title='Status', yaxis_title='Jumlah Pasien')
    st.plotly_chart(fig)

# 8. Tren Tipe Admission dari Tahun ke Tahun
elif options == "Tren Tipe Admission dari Tahun ke Tahun":
    st.subheader("Tren Tipe Admission dari Tahun ke Tahun")
    admission_trends = data1.groupby('year')['TYPE OF ADMISSION-EMERGENCY/OPD'].value_counts().unstack().fillna(0)
    st.write(admission_trends)
    fig = px.bar(admission_trends, barmode='stack', title='Tren TYPE OF ADMISSION-EMERGENCY/OPD dari Tahun ke Tahun', 
                 labels={'year': 'Tahun', 'value': 'Jumlah Pasien'})
    fig.update_xaxes(type='category')  # Ensure x-axis is treated as categorical
    st.plotly_chart(fig)

# 9. Perubahan Rata-rata Durasi Tinggal dari Waktu ke Waktu
elif options == "Perubahan Rata-rata Durasi Tinggal dari Waktu ke Waktu":
    st.subheader("Perubahan Rata-rata Durasi Tinggal dari Waktu ke Waktu")
    average_duration_by_year = data1.groupby(data1['D.O.A'].dt.year.astype(str))['DURATION OF STAY'].mean().reset_index()
    st.write(average_duration_by_year)
    fig = px.line(average_duration_by_year, x='D.O.A', y='DURATION OF STAY', 
                  labels={'D.O.A': 'Tahun', 'DURATION OF STAY': 'Rata-rata Durasi Tinggal'}, 
                  title='Perubahan dalam Rata-rata Durasi Tinggal dari Waktu ke Waktu')
    fig.update_xaxes(type='category')  # Ensure x-axis is treated as categorical
    st.plotly_chart(fig)
