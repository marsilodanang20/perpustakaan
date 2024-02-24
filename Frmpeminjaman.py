from tkinter import ttk, Scrollbar, messagebox, Entry, Frame, Label, Button, END
import tkinter as tk
from Peminjaman import Peminjaman

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
        res = rs.getById(id_peminjaman)
        rec = rs.affected
        if rec > 0:
            messagebox.showinfo("Peminjaman Ditemukan", "Data Peminjaman Ditemukan")
            self.tampilkanData()
            self.peminjaman_ditemukan = True
        else:
            messagebox.showwarning("Peminjaman Tidak Ditemukan", "Data Peminjaman Tidak Ditemukan") 
            self.peminjaman_ditemukan = False
            self.txtIdBuku.focus()
        return res
        
    def tampilkanData(self, event=None):
        id_peminjaman = self.txtIdAnggota.get()
        rs = Peminjaman()
        res = rs.getById(id_peminjaman)
        self.txtJudulBuku.delete(0, END)
        self.txtJudulBuku.insert(END, rs.judul_buku)
        self.txtIdBuku.delete(0, END)
        self.txtIdBuku.insert(END, rs.id_buku)
        self.txtTanggalPeminjaman.delete(0, END)
        self.txtTanggalPeminjaman.insert(END, rs.tanggal_peminjaman)
        self.txtTanggalPengembalian.delete(0, END)
        self.txtTanggalPengembalian.insert(END, rs.tanggal_pengembalian)
        self.btnSimpan.config(text="Perbarui")
                 
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
        else:
            messagebox.showwarning("Peminjaman Gagal", "Buku tidak dapat dipinjam.")
        
        self.onClear()

    def onExit(self, event=None):
        # Keluar dari aplikasi
        self.parent.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = FrmPeminjaman(root, "Aplikasi Peminjaman Buku")
    root.mainloop()
