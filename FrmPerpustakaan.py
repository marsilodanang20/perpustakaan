import tkinter as tk
from tkinter import Frame, Label, Entry, Button, ttk, END, StringVar, messagebox, Scrollbar
from Perpustakaan import Library
from Users import Users

class FrmPerpustakaan:
    
    def __init__(self, parent, title):
        self.parent = parent       
        self.parent.geometry("800x600")  
        self.parent.title(title)
        self.parent.protocol("WM_DELETE_WINDOW", self.onExit)
        self.buku_ditemukan = None
        self.setupKomponen()
        self.onReload()
        
    def setupKomponen(self):
        mainFrame = Frame(self.parent, bd=10)
        mainFrame.pack(fill=tk.BOTH, expand=tk.YES)
        
        # Labels
        Label(mainFrame, text='Judul Buku:').grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.txtJudulBuku = Entry(mainFrame) 
        self.txtJudulBuku.grid(row=1, column=1, padx=5, pady=5) 
        self.txtJudulBuku.bind("<Return>", self.onCari) 

        Label(mainFrame, text='Pengarang:').grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.txtPengarang = Entry(mainFrame) 
        self.txtPengarang.grid(row=2, column=1, padx=5, pady=5) 

        Label(mainFrame, text='Tahun Terbit:').grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.txtTahunTerbit = Entry(mainFrame) 
        self.txtTahunTerbit.grid(row=3, column=1, padx=5, pady=5) 

        Label(mainFrame, text='Jumlah Halaman:').grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        self.txtJumlahHalaman = Entry(mainFrame) 
        self.txtJumlahHalaman.grid(row=4, column=1, padx=5, pady=5) 

        Label(mainFrame, text='Genre:').grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        self.cboGenre = ttk.Combobox(mainFrame, width=27) 
        self.cboGenre.grid(row=5, column=1, padx=5, pady=5)
        self.cboGenre['values'] = ('Fiksi', 'Non-Fiksi', 'Fiksi Ilmiah', 'Romance')
        self.cboGenre.current(0)      

        Label(mainFrame, text='Stok:').grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)
        self.txtStok = Entry(mainFrame) 
        self.txtStok.grid(row=6, column=1, padx=5, pady=5) 

        # Buttons Frame untuk aplikasi perpustakaan
        btnFrame = Frame(mainFrame)
        btnFrame.grid(row=7, columnspan=2, pady=10)

        # Buttons untuk aplikasi perpustakaan
        self.btnCari = Button(btnFrame, text='Cari', command=self.onCari, width=10, bg='green', fg='white')
        self.btnCari.pack(side=tk.LEFT, padx=5)
        self.btnSimpan = Button(btnFrame, text='Simpan', command=self.onSimpan, width=10, bg='blue', fg='white')
        self.btnSimpan.pack(side=tk.LEFT, padx=5)
        self.btnClear = Button(btnFrame, text='Clear', command=self.onClear, width=10, bg='gray', fg='white')
        self.btnClear.pack(side=tk.LEFT, padx=5)
        self.btnHapus = Button(btnFrame, text='Hapus', command=self.onDelete, width=10, bg='red', fg='white')
        self.btnHapus.pack(side=tk.LEFT, padx=5)

        # Define columns for book list
        columns = ('id', 'judul', 'pengarang', 'tahun_terbit', 'jumlah_halaman', 'genre', 'stok')

        self.tree = ttk.Treeview(mainFrame, columns=columns, show='headings')
        # Define headings for book list
        self.tree.heading('id', text='ID')
        self.tree.column('id', width=30, anchor=tk.CENTER)
        self.tree.heading('judul', text='Judul Buku')
        self.tree.column('judul', width=150, anchor=tk.CENTER)
        self.tree.heading('pengarang', text='Pengarang')
        self.tree.column('pengarang', width=100, anchor=tk.CENTER)
        self.tree.heading('tahun_terbit', text='Tahun Terbit')
        self.tree.column('tahun_terbit', width=80, anchor=tk.CENTER)
        self.tree.heading('jumlah_halaman', text='Jumlah Halaman')
        self.tree.column('jumlah_halaman', width=80, anchor=tk.CENTER)
        self.tree.heading('genre', text='Genre')
        self.tree.column('genre', width=100, anchor=tk.CENTER)
        self.tree.heading('stok', text='Stok')
        self.tree.column('stok', width=50, anchor=tk.CENTER)

        # Set tree position for book list and scrollbar
        self.tree.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NSEW)
        self.tree_scroll = Scrollbar(mainFrame, orient='vertical', command=self.tree.yview)
        self.tree_scroll.grid(row=0, column=1, padx=(0,5), pady=5, sticky='ns')
        self.tree.configure(yscrollcommand=self.tree_scroll.set)

        self.onReload()
        
    def onClear(self, event=None):
        self.txtJudulBuku.delete(0, END)
        self.txtPengarang.delete(0, END)
        self.txtTahunTerbit.delete(0, END)
        self.txtJumlahHalaman.delete(0, END)
        self.cboGenre.current(0)  # Set default value for genre combobox
        self.txtStok.delete(0, END)
        self.btnSimpan.config(text="Simpan")
        self.onReload()
        self.buku_ditemukan = False
    
    def onReload(self, event=None):
        # Get book data
        rs = Library()
        result = rs.getAllData()
        for item in self.tree.get_children():
            self.tree.delete(item)
        bukus = []
        for row_data in result:
            bukus.append(row_data)

        for buku in bukus:
            self.tree.insert('', END, values=buku)
    
    def onCari(self, event=None):
        judul_buku = self.txtJudulBuku.get()
        rs = Library()
        res = rs.getByJudulBuku(judul_buku)
        rec = rs.affected
        if rec > 0:
            messagebox.showinfo("Buku Ditemukan", "Data Buku Ditemukan")
            self.tampilkanData()
            self.buku_ditemukan = True
        else:
            messagebox.showwarning("Buku Tidak Ditemukan", "Data Buku Tidak Ditemukan") 
            self.buku_ditemukan = False
            self.txtPengarang.focus()
        return res
        
    def tampilkanData(self, event=None):
        judul_buku = self.txtJudulBuku.get()
        rs = Library()
        res = rs.getByJudulBuku(judul_buku)
        self.txtPengarang.delete(0, END)
        self.txtPengarang.insert(END, rs.pengarang)
        self.txtTahunTerbit.delete(0, END)
        self.txtTahunTerbit.insert(END, rs.tahun_terbit)
        self.txtJumlahHalaman.delete(0, END)
        self.txtJumlahHalaman.insert(END, rs.jumlah_halaman)
        self.cboGenre.set(rs.genre)
        self.txtStok.delete(0, END)
        self.txtStok.insert(END, rs.stok)   
        self.btnSimpan.config(text="Perbarui")
                 
    def onSimpan(self, event=None):
        judul_buku = self.txtJudulBuku.get()
        pengarang = self.txtPengarang.get()
        tahun_terbit = self.txtTahunTerbit.get()
        jumlah_halaman = self.txtJumlahHalaman.get()
        genre = self.cboGenre.get()
        stok = self.txtStok.get()
        
        rs = Library()
        rs.judul = judul_buku
        rs.pengarang = pengarang
        rs.tahun_terbit = tahun_terbit
        rs.jumlah_halaman = jumlah_halaman
        rs.genre = genre
        rs.stok = stok
        
        if self.buku_ditemukan:
            res = rs.perbaruiByJudulBuku(judul_buku)
            message = 'Diperbarui'
        else:
            res = rs.simpan()
            message = 'Disimpan'
            
        rec = rs.affected
        if rec > 0:
            messagebox.showinfo("Operasi Berhasil", f"Data Buku Berhasil {message}")
        else:
            messagebox.showwarning("Operasi Gagal", f"Gagal {message} Data Buku")
        self.onClear()
        return rec

    def onDelete(self, event=None):
        judul_buku = self.txtJudulBuku.get()
        rs = Library()
        rs.judul = judul_buku
        if self.buku_ditemukan:
            res = rs.hapusByJudulBuku(judul_buku)
            rec = rs.affected
        else:
            messagebox.showinfo("Buku Tidak Ditemukan", "Buku harus ditemukan sebelum dihapus")
            rec = 0
        
        if rec > 0:
            messagebox.showinfo("Operasi Berhasil", "Data Buku Berhasil Dihapus")
        
        self.onClear()

    def onExit(self, event=None):
        # Keluar dari aplikasi
        self.parent.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    app = FrmPerpustakaan(root, "Aplikasi Data Perpustakaan")
    root.mainloop()
