import streamlit as st
import gspread
from streamlit_folium import st_folium
import folium
from datetime import datetime

# ===== Google Sheets =====
creds = st.secrets["textkey"]
client = gspread.service_account_from_dict(creds)
sheet_name = "Monitoring_Air"  # Pastikan nama sheet sesuai
sheet = client.open(sheet_name).sheet1

st.title("Monitoring Kualitas Air")

# ===== Form Input Data =====
with st.form("form_air"):
    ph = st.number_input("pH", min_value=0.0, max_value=14.0, step=0.1)
    suhu = st.number_input("Suhu Air (°C)", min_value=0.0, step=0.1)
    tds = st.number_input("TDS (ppm)", min_value=0)
    salinitas = st.number_input("Salinitas (ppt)", min_value=0.0, step=0.1)
    turbiditas = st.number_input("Turbiditas (NTU)", min_value=0.0, step=0.1)

    # Koordinat otomatis dengan fallback manual
    latitude = st.text_input("Latitude")
    longitude = st.text_input("Longitude")

    submit = st.form_submit_button("Simpan Data")

    if submit:
        if latitude == "" or longitude == "":
            st.warning("Koordinat belum diisi!")
        else:
            try:
                lat = float(latitude)
                lon = float(longitude)
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sheet.append_row([now, ph, suhu, tds, salinitas, turbiditas, lat, lon])
                st.success("Data berhasil disimpan ke Google Sheets!")

                # Tampilkan peta setelah submit
                m = folium.Map(location=[lat, lon], zoom_start=15)
                folium.Marker([lat, lon], tooltip="Lokasi Sample").add_to(m)
                st_folium(m, width=700, height=500)
            except ValueError:
                st.error("Koordinat tidak valid. Pastikan latitude & longitude berupa angka.")

# ===== Ambil GPS otomatis di browser =====
st.markdown("Klik tombol ini untuk mengisi koordinat otomatis (harus di HP atau laptop dengan GPS):")
st.components.v1.html("""
<script>
navigator.geolocation.getCurrentPosition(
    (position) => {
        document.querySelector('#lat').value = position.coords.latitude;
        document.querySelector('#lon').value = position.coords.longitude;
    },
    (err) => alert('Gagal mengambil lokasi. Pastikan GPS diizinkan.')
);
</script>
<input id="lat" type="hidden">
<input id="lon" type="hidden">
""", height=0)
