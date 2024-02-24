from db import DBConnection as mydb
from datetime import datetime, timedelta
import Peminjaman

class Library:

    def __init__(self):
        self.conn = None
        self.affected = None
        self.result = None

    @property
    def judul(self):
        return self.__judul

    @judul.setter
    def judul(self, value):
        self.__judul = value

    @property
    def pengarang(self):
        return self.__pengarang

    @pengarang.setter
    def pengarang(self, value):
        self.__pengarang = value

    @property
    def tahun_terbit(self):
        return self.__tahun_terbit

    @tahun_terbit.setter
    def tahun_terbit(self, value):
        self.__tahun_terbit = value

    @property
    def jumlah_halaman(self):
        return self.__jumlah_halaman

    @jumlah_halaman.setter
    def jumlah_halaman(self, value):
        self.__jumlah_halaman = value

    @property
    def stok(self):
        return self.__stok

    @stok.setter
    def stok(self, value):
        self.__stok = value

    def simpan(self):
        self.conn = mydb()
        val = (self.__judul, self.__pengarang, self.__tahun_terbit, self.__jumlah_halaman, self.__stok)
        sql = "INSERT INTO buku (judul, pengarang, tahun_terbit, jumlah_halaman, stok) VALUES (%s, %s, %s, %s, %s)"
        self.affected = self.conn.insert(sql, val)
        self.conn.disconnect()
        return self.affected

    def update(self, id_buku):
        self.conn = mydb()
        val = (self.__judul, self.__pengarang, self.__tahun_terbit, self.__jumlah_halaman, self.__stok, id_buku)
        sql = "UPDATE buku SET judul=%s, pengarang=%s, tahun_terbit=%s, jumlah_halaman=%s, stok=%s WHERE id_buku=%s"
        self.affected = self.conn.update(sql, val)
        self.conn.disconnect()
        return self.affected

    def delete(self, id_buku):
        self.conn = mydb()
        sql = "DELETE FROM buku WHERE id_buku=%s"
        self.affected = self.conn.delete(sql, (id_buku,))
        self.conn.disconnect()
        return self.affected

    def getById(self, id_buku):
        self.conn = mydb()
        sql = "SELECT * FROM buku WHERE id_buku=%s"
        self.result = self.conn.findOne(sql, (id_buku,))
        if self.result:
            self.__judul = self.result['judul']
            self.__pengarang = self.result['pengarang']
            self.__tahun_terbit = self.result['tahun_terbit']
            self.__jumlah_halaman = self.result['jumlah_halaman']
            self.__stok = self.result['stok']
        self.conn.disconnect()
        return self.result

    def getAllData(self):
        self.conn = mydb()
        sql = "SELECT * FROM buku"
        self.result = self.conn.findAll(sql)
        return self.result

    def peminjaman(self, judul_buku, id_anggota, id_buku, tanggal_peminjaman, tanggal_pengembalian):
        self.conn = mydb()
        buku = self.getById(id_buku)

        if buku:
            if buku['stok'] >= 1:  # Minimal pinjam 1 buku
                sql_pinjam = "INSERT INTO peminjaman (judul_buku, id_anggota, id_buku, tanggal_peminjaman, tanggal_pengembalian) VALUES (%s, %s, %s, %s, %s)"
                val_pinjam = (judul_buku, id_anggota, id_buku, tanggal_peminjaman, tanggal_pengembalian)
                self.conn.insert(sql_pinjam, val_pinjam)

                stok_baru = buku['stok'] - 1
                sql_update_stok = "UPDATE buku SET stok=%s WHERE id_buku=%s"
                val_update_stok = (stok_baru, id_buku)
                self.conn.update(sql_update_stok, val_update_stok)

                self.affected = 1  # Peminjaman berhasil
            else:
                self.affected = 0  # Stok buku tidak mencukupi
        else:
            self.affected = -1  # Buku tidak ditemukan

        self.conn.disconnect()
        return self.affected

    def kembalikan(self, id_peminjaman, jumlah_kembali):
        self.conn = mydb()
        sql_get_peminjaman = "SELECT * FROM peminjaman WHERE id_peminjaman=%s"
        result_peminjaman = self.conn.findOne(sql_get_peminjaman, (id_peminjaman,))

        if result_peminjaman:
            id_buku = result_peminjaman['id_buku']
            tanggal_kembali = datetime.now().strftime('%Y-%m-%d')

            sql_kembali = "INSERT INTO pengembalian (id_peminjaman, tanggal_kembali, jumlah_kembali) VALUES (%s, %s, %s)"
            val_kembali = (id_peminjaman, tanggal_kembali, jumlah_kembali)
            self.conn.insert(sql_kembali, val_kembali)

            buku = self.getById(id_buku)
            stok_baru = buku['stok'] + jumlah_kembali
            sql_update_stok = "UPDATE buku SET stok=%s WHERE id_buku=%s"
            val_update_stok = (stok_baru, id_buku)
            self.conn.update(sql_update_stok, val_update_stok)

            sql_hapus_peminjaman = "DELETE FROM peminjaman WHERE id_peminjaman=%s"
            self.conn.delete(sql_hapus_peminjaman, (id_peminjaman,))

            self.affected = 1  # Pengembalian berhasil
        else:
            self.affected = 0  # Peminjaman tidak ditemukan

        self.conn.disconnect()
        return self.affected

# Contoh penggunaan:
# buku_instance = Library()
# data_buku = buku_instance.getAllData()
# print(data_buku)
