from tkinter import * 
from tkinter import messagebox 
import mysql.connector 
from tkinter import ttk 

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
 
class Data_Pasien(Tk): 
    def __init__(self): 
        super().__init__() 
        self.title("Daftar Pasien") 
        self.geometry("850x600") 
 
        # Koneksi ke database 
        self.db = mysql.connector.connect( 
            host="localhost", 
            user="root", 
            password="", 
            database="registrasi" 
        )
 # Membuat kursor 
        self.cursor = self.db.cursor() 
 
        # Membuat dan menampilkan GUI 
        self.tampilan_gui() 
 
    def tampilan_gui(self): 
 
        Label(self, text="Id Pasien").grid(row=0, column=0, padx=10, pady=10) 
        self.id_pasien_entry = Entry(self, width=50) 
        self.id_pasien_entry.grid(row=0, column=1, padx=10, pady=10) 
 
        Label(self, text="Nama Pasien").grid(row=1, column=0, padx=10, pady=10) 
        self.nama_pasien_entry = Entry(self, width=50) 
        self.nama_pasien_entry.grid(row=1, column=1, padx=10, pady=10) 
 
        Label(self, text="Ruang").grid(row=2, column=0, padx=10, pady=10) 
        self.ruang_entry = Entry(self, width=50) 
        self.ruang_entry.grid(row=2, column=1, padx=10, pady=10) 
 
        Label(self, text="Diagnosa").grid(row=3, column=0, padx=10, pady=10) 
        self.diagnosa_entry = Entry(self, width=37, ) 
        self.diagnosa_entry.grid(row=3, column=1, padx=10, pady=10) 

        Label(self, text="Nama Dokter").grid(row=4, column=0, padx=10, pady=10) 
        self.nama_dokter_entry = Text(self, width=37, height=5) 
        self.nama_dokter_entry.grid(row=4, column=1, padx=10, pady=10) 
 
        Button(self, text="Simpan Data",  
               command=self.simpan_data).grid(row=5, column=0, columnspan=2, pady=10) 
         
        # Menambahkan Treeview 
        self.tree = ttk.Treeview(self, columns=("id_pasien", "nama_pasien", "ruang", "diagnosa", "nama_dokter"), show="headings") 
        self.tree.heading("id_pasien", text="Id Pasien") 
        self.tree.heading("nama_pasien", text="Nama Pasien") 
        self.tree.heading("ruang", text="Ruang") 
        self.tree.heading("diagnosa", text="Diagnosa") 
        self.tree.heading("nama_dokter", text="Nama Dokter") 
        self.tree.grid(row=6, column=0, columnspan=6, pady=10, padx=10) 
 
        # Menambahkan tombol refresh data 
        Button(self, text="Refresh Data", command=self.tampilkan_data).grid(row=7, column=0, columnspan=2, pady=10, padx=10) 
 
        # Menambahkan tombol delete data 
        Button(self, text="Delete Data", command=self.hapus_data).grid(row=7, column=1, columnspan=2, pady=10, padx=10) 
 
        # Menambahkan tombol update data 
        Button(self, text="Update Data", command=self.update_data).grid(row=7, column=2, columnspan=2, pady=10, padx=10)

        Button(self, text="Print Data", command=self.cetak_ke_pdf).grid(row=7,column=3, columnspan=2, pady=10, padx=10)
        self.tampilkan_data() 
 
    def simpan_data(self): 
        id_pasien = self.id_pasien_entry.get() 
        nama_pasien= self.nama_pasien_entry.get() 
        ruang = self.ruang_entry.get() 
        diagnosa = self.diagnosa_entry.get()
        nama_dokter = self.nama_dokter_entry.get("1.0", END) 
 
        query = "INSERT INTO pasien (id_pasien, nama_pasien, ruang, diagnosa, nama_dokter) VALUES (%s, %s, %s, %s, %s)" 
        values = (id_pasien, nama_pasien, ruang, diagnosa, nama_dokter) 
 
        try: 
            self.cursor.execute(query, values) 
            self.db.commit() 
            messagebox.showinfo("Sukses", "Data berhasil disimpan!") 
        except Exception as e: 
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}") 
 
        self.id_pasien_entry.delete(0, END) 
        self.nama_pasien_entry.delete(0, END) 
        self.ruang_entry.delete(0, END) 
        self.diagnosa_entry.delete(0, END) 
        self.nama_dokter_entry.delete("1.0", END) 
     
    def tampilkan_data(self): 
        # Hapus data pada treeview 
        for row in self.tree.get_children(): 
            self.tree.delete(row) 
 
        # Ambil data dari database 
        self.cursor.execute("SELECT * FROM pasien") 
        data = self.cursor.fetchall() 
 
        # Masukkan data ke treeview 
        for row in data: 
            self.tree.insert("", "end", values=row) 
     
    def hapus_data(self): 
        selected_item = self.tree.selection() 
 
        if not selected_item: 
            messagebox.showwarning("Peringatan", "Pilih data yang akan dihapus.") 
            return 
 
        confirmation = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?") 
        if confirmation:
         for item in selected_item: 
                data = self.tree.item(item, 'values') 
                nis_to_delete = data[0] 
                 
                query = "DELETE FROM pasien WHERE id_pasien = %s" 
                values = (nis_to_delete,) 
 
                try: 
                    self.cursor.execute(query, values) 
                    self.db.commit() 
                    messagebox.showinfo("Sukses", "Data berhasil dihapus!") 
                except Exception as e: 
                    messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}") 
 
                    self.tampilkan_data() 
         
    def update_data(self): 
        selected_item = self.tree.selection() 
 
        if not selected_item: 
            messagebox.showwarning("Peringatan", "Pilih data yang akan diupdate.") 
            return 
 
        # Ambil data terpilih dari treeview 
        data = self.tree.item(selected_item[0], 'values') 
 
        # Tampilkan form update dengan data terpilih 
        self.id_pasien_entry.insert(0, data[0]) 
        self.nama_pasien_entry.insert(0, data[1]) 
        self.ruang_entry.insert(0, data[2]) 
        self.diagnosa_entry.insert(0, data[3]) 
        self.nama_dokter_entry.insert("1.0", data[4]) 
 
        # Menambahkan tombol update di form 
        Button(self, text="Update", command=lambda: 
self.proses_update(data[0])).grid(row=5, column=1, columnspan=2, pady=10) 
 
    def proses_update(self, nis_to_update): 
        id_pasien = self.id_pasien_entry.get() 
        nama_pasien = self.nama_pasien_entry.get() 
        ruang = self.ruang_entry.get() 
        diagnosa = self.diagnosa_entry.get() 
        nama_dokter = self.nama_dokter_entry.get("1.0", END) 
 
        query = "UPDATE pasien SET id_pasien=%s, nama_pasien=%s, ruang=%s, diagnosa=%s, nama_dokter=%s WHERE id_pasien=%s" 
        values = (id_pasien, nama_pasien, ruang, diagnosa, nama_dokter, nis_to_update) 
 
        try: 
            self.cursor.execute(query, values)
            self.db.commit() 
            messagebox.showinfo("Sukses", "Data berhasil diupdate!") 
        except Exception as e: messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}") 

# Bersihkan form setelah update 
        self.id_pasien_entry.delete(0, END) 
        self.nama_pasien_entry.delete(0, END) 
        self.ruang_entry.delete(0, END) 
        self.diagnosa_entry.delete(0, END) 
        self.nama_dokter_entry.delete("1.0", END) 
# Tampilkan kembali data setelah diupdate 
        self.tampilkan_data() 

    def cetak_ke_pdf(self):
        doc = SimpleDocTemplate("data_pasien.pdf", pagesize=letter)
        styles = getSampleStyleSheet()
        # Membuat data untuk tabel PDF

        data = [["id_pasien", "nama_pasien", "ruang", "diagnosa", "nama_dokter"]]
        for row_id in self.tree.get_children():
            row_data = [self.tree.item(row_id, 'values')[0],
                    self.tree.item(row_id, 'values')[1],
                    self.tree.item(row_id, 'values')[2],
                    self.tree.item(row_id, 'values')[3],
                    self.tree.item(row_id, 'values')[4]]
            data.append(row_data)

        # Membuat tabel PDF
        table = Table(data)
        table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)]))
        
        # Menambahkan tabel ke dokumen PDF
        doc.build([table])
        messagebox.showinfo("Sukses", "Data berhasil dicetak ke PDF(data_pasien.pdf).")

if __name__ == "__main__": 
    app = Data_Pasien() 
    app.mainloop()