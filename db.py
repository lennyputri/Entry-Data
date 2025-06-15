import mysql.connector

# Fungsi koneksi ke database
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Lenny190402",
        database="customer_guidance_db"
    )

# Ambil data dari tabel customer_guidance_invoice
def fetch_customer_data():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM customer_guidance_invoice")
    data = cursor.fetchall()
    conn.close()
    return data

# Tambah data ke tabel customer_guidance_invoice
def insert_customer_data(values):
    conn = connect_db()
    cursor = conn.cursor()
    sql = """
    INSERT INTO customer_guidance_invoice (
        business_segment, division, kode_debtor, debtor_name, sales_name,
        id_pol, id_pod, cabang_tagih, alamat_kirim_invoice, invoice_type, dokumen_terkait
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(sql, values)
    conn.commit()
    conn.close()

# Hapus data berdasarkan list ID
def delete_customer_data(id_list):
    if not id_list:
        return
    conn = connect_db()
    cursor = conn.cursor()
    # Buat placeholder sebanyak ID yang akan dihapus
    format_strings = ','.join(['%s'] * len(id_list))
    sql = f"DELETE FROM customer_guidance_invoice WHERE ID IN ({format_strings})"
    try:
        cursor.execute(sql, tuple(id_list))
        conn.commit()
    except Exception as e:
        print(f"Error saat menghapus data: {e}")
        conn.rollback()
    finally:
        conn.close()

def update_customer_data(id, data):
    import mysql.connector
    conn = mysql.connector.connect(
        host="localhost", user="root", password="", database="namadbmu"
    )
    cursor = conn.cursor()

    query = """
        UPDATE customer_guidance
        SET 
            business_segment=%s,
            division=%s,
            kode_debtor=%s,
            debtor_name=%s,
            sales_name=%s,
            id_pol=%s,
            id_pod=%s,
            cabang_tagih=%s,
            alamat_kirim_invoice=%s,
            invoice_type=%s,
            dokumen_terkait=%s
        WHERE id=%s
    """

    cursor.execute(query, data + (id,))
    conn.commit()
    cursor.close()
    conn.close()
