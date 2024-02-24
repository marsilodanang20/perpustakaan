-- Struktur tabel untuk sistem perpustakaan
CREATE TABLE `peminjaman` (
  `id_peminjaman` int(11) NOT NULL,
  `judul_buku` varchar(100) NOT NULL,
  `id_anggota` int(11) NOT NULL,
  `id_buku` int(11) NOT NULL,
  `tanggal_peminjaman` date NOT NULL,
  `tanggal_pengembalian` date NOT NULL,
  PRIMARY KEY (`id_peminjaman`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `buku` (
  `id_buku` int(11) NOT NULL,
  `judul` varchar(100) NOT NULL,
  `pengarang` varchar(100) NOT NULL,
  `tahun_terbit` int(4) NOT NULL,
  `stok` int(11) NOT NULL,
  PRIMARY KEY (`id_buku`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

CREATE TABLE `anggota` (
  `id_anggota` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `alamat` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  PRIMARY KEY (`id_anggota`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Insert data contoh untuk tabel perpustakaan
INSERT INTO `buku` (`id_buku`, `judul`, `pengarang` , `tahun_terbit`, `stok`) VALUES
(1001, 'Dilan 1990' , 'Pidi baiq', '1997, 10);

INSERT INTO `anggota` (`id_anggota`, `nama`, `alamat`, `email`) VALUES
(1, 'Danang', 'Cirebon', 'Danang@gmail.com');

INSERT INTO `peminjaman` (`id_peminjaman`, `judul_buku`, `id_anggota`, `id_buku`, `tanggal_peminjaman`, `tanggal_pengembalian`) VALUES
(1001, 'Dilan 1990', '1001', '1001' , '2023-11-29' , '2024-01-30');
