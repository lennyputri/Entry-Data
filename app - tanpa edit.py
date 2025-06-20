import streamlit as st
from db import fetch_customer_data, insert_customer_data, delete_customer_data
import pandas as pd

# ==== Harus di paling atas ====
st.set_page_config(page_title="Customer Guidance Invoicing", layout="wide")

# ==== CSS Styling ====
st.markdown("""
    <style>
        /* Input dan Textarea */
        div[data-baseweb="input"] input,
        div[data-baseweb="textarea"] textarea,
        div[data-baseweb="select"] {
            background-color: #ffffff;
            color: black;
            border: 2px solid #d90429;
            border-radius: 8px;
            padding: 8px;
        }

        /* Label */
        label {
            font-weight: bold;
            color: white !important;
        }

        /* Background form box */
        div[data-testid="stForm"] {
            background-color: #0A2647;
            padding: 30px;
            border-radius: 15px;
        }

        /* Tombol Submit */
        button[kind="primary"] {
            background-color: #d90429;
            color: white;
            font-weight: bold;
            border-radius: 8px;
        }

        button[kind="primary"]:hover {
            background-color: #a4001d;
            color: white;
        }

        /* Sidebar background */
        section[data-testid="stSidebar"] {
            background-color: #0A2647;
            color: white;
        }

        /* Sidebar radio button label */
        section[data-testid="stSidebar"] label {
            color: white !important;
            font-weight: bold;
        }

        /* Warna teks radio button */
        section[data-testid="stSidebar"] .stRadio div {
            color: white !important;
        }

        /* Warna ikon dan teks radio */
        section[data-testid="stSidebar"] svg, 
        section[data-testid="stSidebar"] span {
            color: white !important;
            fill: white !important;
        }

        /* Jika radio terlihat seperti 'mati' */
        section[data-testid="stSidebar"] .css-1n76uvr {
            opacity: 1 !important;
        }

        /* Judul utama */
        h1 {
            color: #0A2647;
        }
    </style>
""", unsafe_allow_html=True)

# ==== Header & Sidebar ====
st.markdown(
    '<img src="https://www.freight-hub.co/wp-content/uploads/2023/11/Logo-MGLog.png.webp" width="240"/>',
    unsafe_allow_html=True
)
st.title("Customer Guidance Invoicing Form")

menu = st.sidebar.radio("Menu", ["📄 Lihat Data", "➕ Entri Data Baru"])

# ==== Lihat Data ====
if menu == "📄 Lihat Data":
    st.subheader("📋 Data Customer Guidance Invoicing")
    data = fetch_customer_data()
    if data:
        df = pd.DataFrame(data, columns=[
            "ID", "Business Segment", "Division", "Kode Debtor", "Debtor Name",
            "Sales Name", "ID POL", "ID POD", "Cabang Tagih", "Alamat Kirim Invoice",
            "Invoice Type", "Dokumen Terkait"
        ])

        # State untuk data yang sedang ditampilkan
        if 'df_display' not in st.session_state:
            st.session_state.df_display = df.copy()

        # SEARCH BOX UNTUK DEBTOR NAME
        # Ambil list debtor unik dari dataframe
        debtor_names = sorted(st.session_state.df_display['Debtor Name'].dropna().unique())

        selected_debtor = st.selectbox(
            "Pilih atau cari Debtor Name:",
            options=["Semua"] + sorted(debtor_names),
            index=0,
        )

        # Filter dataframe berdasarkan pilihan
        if selected_debtor != "Semua":
            filtered_df = st.session_state.df_display[
                st.session_state.df_display['Debtor Name'] == selected_debtor
            ]
        else:
            filtered_df = st.session_state.df_display
        
        st.dataframe(filtered_df, use_container_width=True)

        #Garis Pemisah Visual
        st.markdown("---")

        #Judul Hapus Baris 
        st.markdown("### Hapus Baris")
        
        # Pilih baris untuk dihapus berdasarkan ID yang ada di filtered_df
        ids_to_delete = st.multiselect(
            "Pilih baris yang ingin dihapus (berdasarkan ID):",
            options=filtered_df['ID'].tolist()
        )

        if st.button("Hapus Data Terpilih"):
            if ids_to_delete:
                # Hapus data dari database (MySQL)
                for id_del in ids_to_delete:
                    delete_customer_data(ids_to_delete) 

                # Refresh data di aplikasi
                data = fetch_customer_data()
                st.session_state.df_display = pd.DataFrame(data, columns=[
                    "ID", "Business Segment", "Division", "Kode Debtor", "Debtor Name",
                    "Sales Name", "ID POL", "ID POD", "Cabang Tagih", "Alamat Kirim Invoice",
                    "Invoice Type", "Dokumen Terkait"
                ])

                st.success(f"Berhasil menghapus baris dengan ID: {ids_to_delete}")
            else:
                st.warning("Pilih minimal satu baris untuk dihapus.")

# ==== Entri Baru ====
elif menu == "➕ Entri Data Baru":
    st.subheader("📝 Tambah Data Customer Guidance Invoicing")

    with st.form("form_customer_invoice"):
        col1, col2 = st.columns(2)
        with col1:
            business_segment = st.selectbox("Business Segment".upper(), ["Domestic", "International"])
            division = st.selectbox("Division".upper(), ["Sea Freight", "Air Freight", "Custom", "Industrial Project", "Wh and Transport"])
            kode_debtor = st.text_input("Kode Debtor".upper())
            debtor_name = st.text_input("Debtor Name".upper())
            sales_name = st.text_input("Sales Name".upper())
            id_pol_pod_cabangtagih_options = [
            "IDAMP", "IDAMQ", "IDBDJ", "IDBIT", "IDBLW", "IDBPN", "IDENE", "IDGTO", "IDJKT", "IDKDI", "IDKID", "IDKOE",
            "IDKTG", "IDLBO", "IDMKS", "IDMOF", "IDOTH", "IDPAP", "IDPDG", "IDPKX", "IDPNK", "IDPTL", "IDPWG", "IDSMG", "IDSMQ",
            "IDSRI", "IDSUB", "IDTKG", "IDTLI", "IDTRK", "IDTTE", "IDWIN"]
            id_pol = st.selectbox("ID POL".upper(), ["Select"] + id_pol_pod_cabangtagih_options)
            id_pod = st.selectbox("ID POD".upper(), ["Select"] + id_pol_pod_cabangtagih_options)

        with col2:
            cabang_tagih = st.selectbox("Cabang Tagih".upper(), ["Select"] + id_pol_pod_cabangtagih_options)
            alamat_kirim_invoice = st.text_area("Alamat Kirim Invoice".upper(), height=150)
            invoice_type = st.selectbox("Invoice Type".upper(), ["Select"] + ["Hardcopy", "Softcopy"])
            document_options = ["KWITANSI", "REKAPAN", "INV FP", "RESI", "BATSB", "SI", "BL"]
            dokumen_dipilih = st.multiselect("Supporting Documents".upper(), document_options)
            
            dokumen_tambahan = st.text_input("Tambah Dokumen Lain (pisahkan dengan koma jika lebih dari satu)".upper())
            st.caption("Kosongkan jika tidak ada dokumen tambahan.")

            # Gabung semua dokumen jadi satu list
            if dokumen_tambahan:
                dokumen_tambahan_list = [d.strip() for d in dokumen_tambahan.split(",") if d.strip()]
            else:
                dokumen_tambahan_list = []

            dokumen_terkait = dokumen_dipilih + dokumen_tambahan_list


        submitted = st.form_submit_button("SIMPAN DATA")
        if submitted:
            # Validasi kolom wajib
            if not all([
                business_segment, division, kode_debtor.strip(), debtor_name.strip(), sales_name.strip(),
                id_pol, id_pod, cabang_tagih.strip(), alamat_kirim_invoice.strip(), invoice_type, dokumen_terkait
            ]):
                st.markdown("""
                    <div style='background-color: white; padding: 15px; border-radius: 10px;'>
                        <span style='color: red; font-weight: bold;'>❌ Terdapat data yang belum diisi. Harap lengkapi semua kolom wajib.</span>
                    </div>
                """, unsafe_allow_html=True)
            else:
                insert_customer_data((
                    business_segment, division, kode_debtor.strip(), debtor_name.strip(), sales_name.strip(),
                    id_pol, id_pod, cabang_tagih.strip(), alamat_kirim_invoice.strip(), invoice_type, ", ".join(dokumen_terkait)
                ))
                st.markdown("""
                    <div style='background-color: white; padding: 15px; border-radius: 10px;'>
                        <span style='color: green; font-weight: bold;'>✅ Data Customer Guidance Invoicing berhasil disimpan!</span>
                    </div>
                """, unsafe_allow_html=True)
