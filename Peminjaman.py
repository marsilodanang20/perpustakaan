import tkinter as tk
from tkinter import Frame, Label, Entry, Button, ttk, END, StringVar, messagebox, Scrollbar
from db import DBConnection as mydb
from datetime import datetime, timedelta

class Peminjaman:

    def __init__(self):
        self.conn = None
        self.affected = None
        self.result = None
        self.__judul_buku = None
        self.__id_anggota = None
        self.__id_buku = None
        self.__id_peminjaman = None
        self.__tanggal_peminjaman = None
        self.__tanggal_pengembalian = None

    @property
    def judul_buku(self):
        return self.__judul_buku

    @judul_buku.setter
    def judul_buku(self, value):
        self.__judul_buku = value

    @property
    def id_anggota(self):
        return self.__id_anggota

    @id_anggota.setter
    def id_anggota(self, value):
        self.__id_anggota = value

    @property
    def id_buku(self):
        return self.__id_buku

    @id_buku.setter
    def id_buku(self, value):
        self.__id_buku = value

    @property
    def id_peminjaman(self):
        return self.__id_peminjaman

    @id_peminjaman.setter
    def id_peminjaman(self, value):
        self.__id_peminjaman = value

    @property
    def tanggal_peminjaman(self):
        return self.__tanggal_peminjaman

    @tanggal_peminjaman.setter
    def tanggal_peminjaman(self, value):
        self.__tanggal_peminjaman = value

    @property
    def tanggal_pengembalian(self):
        return self.__tanggal_pengembalian

    @tanggal_pengembalian.setter
    def tanggal_pengembalian(self, value):
        self.__tanggal_pengembalian = value

    def pinjam(self):
        self.conn = mydb()
        
        # Ambil stok buku
        buku = self.get_buku_by_id(self.__id_buku)
        
        if buku is not None:  # Periksa apakah buku ditemukan
            if buku[3] > 0:  # Menggunakan indeks integer untuk mengakses stok buku
                # Kurangi stok buku yang dipinjam
                stok_baru = buku[3] - 1  # Menggunakan indeks integer untuk mengakses stok buku
                self.update_buku_stok(self.__id_buku, stok_baru)
                
                # Tanggal peminjaman dan pengembalian
                self.__tanggal_peminjaman = datetime.now().strftime('%Y-%m-%d')
                self.__tanggal_pengembalian = (datetime.now() + timedelta(days=7)).strftime('%Y-%m-%d')
                
                # Simpan data peminjaman ke database
                sql_pinjam = "INSERT INTO peminjaman (judul_buku, id_anggota, id_buku, tanggal_peminjaman, tanggal_pengembalian) VALUES (%s, %s, %s, %s, %s)"
                val_pinjam = (self.__judul_buku, self.__id_anggota, self.__id_buku, self.__tanggal_peminjaman, self.__tanggal_pengembalian)
                self.affected = self.conn.insert(sql_pinjam, val_pinjam)
            else:
                self.affected = -1  # Stok buku habis
        else:
            self.affected = 0  # Buku tidak ditemukan

        self.conn.disconnect()
        return self.affected

    def kembalikan(self):
        self.conn = mydb()
        
        # Ambil data peminjaman berdasarkan id peminjaman
        peminjaman = self.get_peminjaman_by_id(self.__id_peminjaman)
        
        if peminjaman:
            # Tambahkan kembali stok buku yang dikembalikan
            stok_baru = self.get_buku_by_id(peminjaman['id_buku'])['qt_barang'] + 1
            self.update_buku_stok(peminjaman['id_buku'], stok_baru)
            
           
    def getAllData(self):
        self.conn = mydb()
        sql = "SELECT * FROM peminjaman"
        self.result = self.conn.findAll(sql)
        self.conn.disconnect()
        return self.result

    def get_buku_by_id(self, id_buku):
        sql = "SELECT * FROM buku WHERE id_buku=%s"
        result = self.conn.findone(sql, (id_buku,))
        if result:
            return result
        else:
            return None

    def update_buku_stok(self, id_buku, stok_baru):
        sql_update_stok = "UPDATE buku SET qt_barang=%s WHERE id_buku=%s"
        self.conn.execute_query(sql_update_stok, (stok_baru, id_buku))

    def get_peminjaman_by_id(self, id_peminjaman):
        sql = "SELECT * FROM peminjaman WHERE id_peminjaman=%s"
        return self.conn.findone(sql, (id_peminjaman,))

    def delete_peminjaman_by_id(self, id_peminjaman):
        sql = "DELETE FROM peminjaman WHERE id_peminjaman=%s"
        self.conn.execute_query(sql, (id_peminjaman,))


class FrmPeminjaman:
    
    def __init__(self, parent, title):
        self.parent = parent       
        self.parent.geometry("800x600")  
        self.parent.title(title)
        self.parent.protocol("WM_DELETE_WINDOW", self.onExit)
        self.peminjaman_ditemukan = None
        self.setupKomponen()
        self.onReload()
        
    def setupKomponen(self):
        mainFrame = Frame(self.parent, bd=10)
        mainFrame.pack(fill=tk.BOTH, expand=tk.YES)
        
        # Labels
        Label(mainFrame, text='Judul Buku:').grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.txtJudulBuku = Entry(mainFrame) 
        self.txtJudulBuku.grid(row=0, column=1, padx=5, pady=5) 

        Label(mainFrame, text='ID Anggota:').grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.txtIdAnggota = Entry(mainFrame) 
        self.txtIdAnggota.grid(row=1, column=1, padx=5, pady=5) 

        Label(mainFrame, text='ID Buku:').grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.txtIdBuku = Entry(mainFrame) 
        self.txtIdBuku.grid(row=2, column=1, padx=5, pady=5) 

        Label(mainFrame, text='Tanggal Peminjaman:').grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.txtTanggalPeminjaman = Entry(mainFrame) 
        self.txtTanggalPeminjaman.grid(row=3, column=1, padx=5, pady=5) 
        
        Label(mainFrame, text='Tanggal Pengembalian:').grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.txtTanggalPengembalian = Entry(mainFrame) 
        self.txtTanggalPengembalian.grid(row=4, column=1, padx=5, pady=5) 

        # Buttons Frame untuk aplikasi peminjaman
        btnFrame = Frame(mainFrame)
        btnFrame.grid(row=5, columnspan=2, pady=10)

        # Buttons untuk aplikasi peminjaman
        self.btnCari = Button(btnFrame, text='Cari', command=self.onCari, width=10, bg='green', fg='white')
        self.btnCari.pack(side=tk.LEFT, padx=5)
        self.btnSimpan = Button(btnFrame, text='Pinjam', command=self.onPinjam, width=10, bg='blue', fg='white')
        self.btnSimpan.pack(side=tk.LEFT, padx=5)
        self.btnClear = Button(btnFrame, text='Clear', command=self.onClear, width=10, bg='gray', fg='white')
        self.btnClear.pack(side=tk.LEFT, padx=5)

        # Define columns for loan list
        columns = ('judul_buku', 'id_anggota', 'tanggal_peminjaman', 'tanggal_pengembalian')

        self.tree = ttk.Treeview(mainFrame, columns=columns, show='headings')
        # Define headings for loan list
        self.tree.heading('judul_buku', text='Judul Buku')
        self.tree.column('judul_buku', width=150, anchor=tk.CENTER)
        self.tree.heading('id_anggota', text='ID Anggota')
        self.tree.column('id_anggota', width=100, anchor=tk.CENTER)
        self.tree.heading('tanggal_peminjaman', text='Tanggal Peminjaman')
        self.tree.column('tanggal_peminjaman', width=150, anchor=tk.CENTER)
        self.tree.heading('tanggal_pengembalian', text='Tanggal Pengembalian')
        self.tree.column('tanggal_pengembalian', width=150, anchor=tk.CENTER)
        
        # Set tree position for loan list and scrollbar
        self.tree.grid(row=6, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self.tree_scroll = Scrollbar(mainFrame, orient='vertical', command=self.tree.yview)
        self.tree_scroll.grid(row=6, column=1, padx=(0,5), pady=5, sticky='ns')
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

        self.onReload()
        
    def onClear(self, event=None):
        self.txtJudulBuku.delete(0, END)
        self.txtIdAnggota.delete(0, END)
        self.txtIdBuku.delete(0, END)
        self.txtTanggalPeminjaman.delete(0, END)
        self.txtTanggalPengembalian.delete(0, END)
        self.btnSimpan.config(text="Pinjam")
        self.onReload()
        self.peminjaman_ditemukan = False
    
    def onReload(self, event=None):
        # Get loan data
        rs = Peminjaman()
        result = rs.getAllData()
        for item in self.tree.get_children():
            self.tree.delete(item)
        loans = []
        for row_data in result:
            loans.append(row_data)

        for loan in loans:
            self.tree.insert('', END, values=loan)
    
    def onCari(self, event=None):
        id_peminjaman = self.txtIdAnggota.get()  # Menyimpan id anggota di sini
        rs = Peminjaman()
        result = rs.getAllData()  # Mengambil semua data peminjaman
        found = False
        for row in result:
            if row[1] == id_peminjaman:  # Mengecek apakah id_peminjaman ditemukan
                found = True
                break
        if found:
            messagebox.showinfo("Peminjaman Ditemukan", "Data Peminjaman Ditemukan")
            self.tampilkanData()  # Menampilkan data peminjaman yang ditemukan
        else:
            messagebox.showwarning("Peminjaman Tidak Ditemukan", "Data Peminjaman Tidak Ditemukan")
            self.peminjaman_ditemukan = False
            self.txtIdBuku.focus()
    
    def tampilkanData(self, event=None):
        id_peminjaman = self.txtIdAnggota.get()
        rs = Peminjaman()
        result = rs.getAllData()
        for row in result:
            if row[1] == id_peminjaman:
                self.txtJudulBuku.delete(0, END)
                self.txtJudulBuku.insert(END, row[0])
                self.txtIdBuku.delete(0, END)
                self.txtIdBuku.insert(END, row[1])
                self.txtTanggalPeminjaman.delete(0, END)
                self.txtTanggalPeminjaman.insert(END, row[2])
                self.txtTanggalPengembalian.delete(0, END)
                self.txtTanggalPengembalian.insert(END, row[3])
                self.btnSimpan.config(text="Perbarui")
                break
                 
    def onPinjam(self, event=None):
        judul_buku = self.txtJudulBuku.get()
        id_anggota = self.txtIdAnggota.get()
        id_buku = self.txtIdBuku.get()
        tanggal_peminjaman = self.txtTanggalPeminjaman.get()
        tanggal_pengembalian = self.txtTanggalPengembalian.get()
        
        rs = Peminjaman()
        rs.judul_buku = judul_buku
        rs.id_anggota = id_anggota
        rs.id_buku = id_buku
        rs.tanggal_peminjaman = tanggal_peminjaman
        rs.tanggal_pengembalian = tanggal_pengembalian
        
        res = rs.pinjam()
        if res > 0:
            messagebox.showinfo("Peminjaman Berhasil", "Buku berhasil dipinjam.")
        elif res == -1:
            messagebox.showwarning("Peminjaman Gagal", "Stok buku habis.")
        else:
            messagebox.showwarning("Peminjaman Gagal", "Buku tidak ditemukan.")
        
        self.onClear()

    def onExit(self, event=None):
        # Keluar dari aplikasi
        self.parent.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = FrmPeminjaman(root, "Aplikasi Peminjaman Buku")
    root.mainloop()
