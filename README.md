# Curiousity

Curiousity adalah prototipe game arena survival 2D dengan Python dan pygame-ce. Kamera mengikuti pemain, musuh muncul bertahap dari luar layar, dan senjata menyerang otomatis sesuai pengaturan bidikan.

## Menjalankan game

Dari folder yang berisi `curiousity.py`, jalankan di PowerShell:

```powershell
py -3 -m pip install pygame-ce
py -3 curiousity.py
```

| Kontrol | Aksi |
| --- | --- |
| W/S atau panah atas/bawah | Pindah pilihan di menu |
| Enter | Konfirmasi pilihan |
| WASD atau panah | Bergerak saat bermain |
| P, Esc, atau klik tombol Pause | Jeda saat bermain |
| P atau Esc | Lanjut dari Pause |

Di **Settings**, **Auto** membidik musuh hidup terdekat dalam jangkauan. **Manual** menembak otomatis mengikuti arah gerakan terakhir. Pilihan tersebut berlaku untuk mode Stage maupun Endless.

## Menambahkan karakter pertama

Untuk karakter yang memakai pistol, cukup tambahkan **satu entri JSON dan aset gambarnya**. Class `Karakter` dipakai bersama oleh karakter yang berbeda.

1. Simpan spritesheet PNG transparan di [assets/](assets/). Untuk uji pertama, kamu bisa langsung memakai `assets/test.png`.
2. Buka [data/characters.json](data/characters.json). Tambahkan properti `"nara"` dari contoh di bawah ke dalam objek terluar yang sudah berisi `"riela"` dan `"test"`. Pertahankan entri yang ada dan beri koma di antara entri. Kurung kurawal terluar pada contoh hanya menunjukkan struktur JSON.
3. Jalankan game, lalu pilih **Start → Nara → Stage** atau **Endless**. Nara otomatis muncul di menu karena `sprite` berbentuk objek dan entri memiliki `senjata`.

```json
{
  "nara": {
    "name": "Nara",
    "max_hp": 160,
    "rad": 14,
    "spd": 250,
    "atk": 30,
    "aspd": 0.5,
    "color": [118, 180, 255],
    "senjata": {
      "tipe": "pistol",
      "range": 600,
      "rof": 450
    },
    "sprite": {
      "file": "assets/test.png",
      "frame_size": [48, 48],
      "scale": 2,
      "side_faces": "right",
      "animations": {
        "idle": {
          "side": {"row": 1, "count": 6, "fps": 6}
        },
        "walk": {
          "side": {"row": 4, "count": 6, "fps": 10}
        },
        "attack": {
          "side": {"row": 7, "count": 4, "fps": 12}
        }
      }
    }
  }
}
```

| Key | Arti |
| --- | --- |
| `nara` | ID unik di JSON. Menu menampilkan nilai `name`. |
| `max_hp`, `rad`, `spd` | HP maksimum, radius tabrakan, kecepatan gerak dalam piksel/detik. |
| `atk`, `aspd` | Damage per tembakan dan jeda antar tembakan dalam detik. Jeda yang lebih kecil membuat tembakan lebih sering. |
| `senjata.tipe` | Tipe senjata. Gunakan `pistol` untuk versi saat ini. |
| `senjata.range` | Jangkauan bidik Auto sekaligus jarak tempuh maksimum peluru, dalam piksel dunia. |
| `senjata.rof` | Nama key yang saat ini dibaca sebagai **kecepatan peluru**, dalam piksel/detik. |
| `color` | Warna RGB yang ada pada skema data karakter. |

### Menggunakan spritesheet sendiri

Ubah `sprite.file` ke lokasi PNG baru, relatif terhadap folder utama proyek. Sesuaikan konfigurasi dengan susunan gambar milikmu:

- `frame_size` adalah `[lebar, tinggi]` satu frame sumber, dalam piksel. `scale` memperbesar frame saat dimuat. Radius tabrakan tetap ditentukan oleh `rad`.
- `row` dimulai dari **0**. Loader membaca `count` frame berurutan dari kolom pertama pada baris itu. Hitung frame yang berisi gambar saja supaya animasi tidak berkedip.
- Isi masing-masing `idle.side`, `walk.side`, dan `attack.side` dengan `row`, `count`, dan `fps`. Ketiganya dipakai game. Idle dan jalan berulang. Attack mulai saat pistol menembak dan diputar satu kali, lalu kembali ke idle atau jalan. Tembakan berikutnya dapat memulai ulang animasi.
- `side_faces` adalah arah asli gambar samping, yaitu `"right"` atau `"left"`. Game membalik gambar untuk arah sebaliknya.
- Coba berdiri diam, berjalan ke kiri dan kanan, lalu menembak. Cek ikon di HUD dan pastikan semua frame tampil utuh.

### Kalau ada masalah

| Gejala | Yang perlu dicek |
| --- | --- |
| Karakter tidak muncul di menu | Pastikan entri berada di level yang sama dengan `test`, punya `senjata`, dan `sprite` berupa objek JSON. Riela masih berupa contoh lama dengan `sprite` berupa path teks. |
| `JSONDecodeError` | Periksa koma pemisah, tanda kutip ganda, dan kurung kurawal. |
| Error saat memuat gambar atau memotong frame | Periksa path PNG dan pastikan `row`, ukuran frame, serta `count` muat di spritesheet. |
| Gambar hilang sebentar atau arah hadap terbalik | Periksa frame kosong dan nilai `side_faces`. |
| Serangan gagal saat karakter baru dipilih | Pastikan tipe senjatanya `pistol`, `range` dan `rof` terisi, serta `attack.side` ada. |

## Peta kode

| File | Tanggung jawab |
| --- | --- |
| [curiousity.py](curiousity.py) | Membuka game. |
| [game.py](game.py) | Mengatur layar, menu, kamera, dan loop. `start_game()` membuat pemain dan senjata berdasarkan ID yang dipilih. |
| [karakter/karakter.py](karakter/karakter.py) | Statistik saat bermain, gerak, HP, arah hadap, dan animasi pemain. |
| [systems/assets.py](systems/assets.py) | Membaca JSON serta memotong dan memuat frame spritesheet. |
| [senjata/pistol.py](senjata/pistol.py) dan [senjata/peluru.py](senjata/peluru.py) | Bidikan, jeda tembakan, gerak peluru, dan tabrakan. |
| [enemies/enemy.py](enemies/enemy.py) dan [systems/spawn.py](systems/spawn.py) | Gerak musuh, serangan sentuh, dan kemunculan musuh. |
| [ui/select_char.py](ui/select_char.py), [ui/menu.py](ui/menu.py), dan [ui/hud.py](ui/hud.py) | Pemilihan karakter, navigasi menu, serta tampilan HP, XP, skor, dan waktu. |
| [data/characters.json](data/characters.json) dan [data/enemies.json](data/enemies.json) | Konfigurasi karakter dan musuh. |

Untuk menambah **perilaku senjata baru**, buat class di `senjata/` dengan pola `update(timer, player, list_musuh, mode)` dan `gambar(layar, cam)`. Kembalikan `True` dari `update()` ketika serangan benar-benar dimulai agar `Game` memicu animasi karakter. Tambahkan cabang tipe baru di `Game.start_game()`, lalu pakai tipe itu di JSON. `pedang.py` masih kosong.

Pada versi ini, Stage membatasi total spawn hingga 20 musuh, sedangkan Endless tidak membatasi totalnya. Keduanya membatasi enam musuh aktif. Perpindahan setelah 20 kill per stage, lima stage, dan sistem XP/level masih direncanakan.

## Referensi fungsi

`timer` adalah selang waktu antar-frame dalam detik. `layar` adalah tempat menggambar, dan `cam` adalah posisi kamera di dunia. Posisi di layar didapat dari posisi objek dikurangi `cam`. HUD dan menu memakai koordinat layar langsung.

### Loop permainan · `game.py` → `Game`

| Method | Fungsi dan kapan dipanggil |
| --- | --- |
| `__init__()` | Menyiapkan Pygame, layar, data, HUD, dan menu. Berjalan ketika `curiousity.py` membuat `Game()`. |
| `start_game()` | Membuat pemain, spawn, dan senjata serta mereset statistik run. Dipakai saat inisialisasi, mulai bermain, atau mengulang. Tambahkan tipe senjata baru di sini. |
| `read_input()` | Membaca event keyboard, mouse, dan tutup jendela. Menangani perpindahan halaman menu dan Pause setiap frame. |
| `update(timer)` | Menjalankan gerak, spawn, serangan, skor, dan kamera. Gameplay diperbarui saat kondisi `playing`. |
| `gambar()` | Menampilkan menu aktif atau dunia dan HUD, lalu memperbarui jendela. Dipanggil setelah update. |
| `running()` | Menjalankan loop input → update → gambar, lalu menutup Pygame saat selesai. Dipanggil oleh `curiousity.py`. |

### Pemain · `karakter/karakter.py` → `Karakter`

| Method | Fungsi dan kapan dipanggil |
| --- | --- |
| `__init__(data, posisi_awal)` | Memuat statistik dan animasi dari satu entri karakter. Dipanggil oleh `start_game()`. |
| `update(timer, button)` | Membaca tombol yang sedang ditekan, menggerakkan pemain, dan memperbarui arah serta animasi. Dipanggil tiap frame gameplay. |
| `gambar(layar, cam)` | Memilih frame dan menggambar pemain sesuai koordinat layar. |
| `terserang(dmg)` | Mengurangi HP pemain hingga minimum nol. Dipanggil saat serangan musuh mengenai pemain. |
| `serang()` | Memulai animasi attack dari frame pertama. Dipanggil oleh `Game` ketika update senjata menghasilkan `True`. |

### Loader · `systems/assets.py`

| Fungsi | Fungsi dan kapan dipanggil |
| --- | --- |
| `read_json(nmfile)` | Membaca JSON dari path relatif terhadap folder proyek dan mengembalikan data Python. Dipakai saat menyiapkan konfigurasi. |
| `load_frame(nmfile, szframe, row, jum, skala=2)` | Memotong `jum` frame dari satu baris PNG. `szframe` berisi ukuran satu frame. Panggil setelah layar Pygame dibuat. |
| `load_animasi(datasprite)` | Membaca konfigurasi sprite dan mengembalikan frame serta FPS menurut nama animasi dan arah. Dipakai saat objek pemain atau musuh dibuat. |

### Musuh dan spawn · `enemies/enemy.py` dan `systems/spawn.py`

| Method | Fungsi dan kapan dipanggil |
| --- | --- |
| `Musuh.__init__(data, posisi_awal)` | Membuat satu musuh dengan HP, cooldown, dan animasinya sendiri. Dipanggil oleh `Spawn`. |
| `Musuh.update(timer, target)` | Mengejar objek pemain sampai jarak sentuh, lalu memperbarui animasi. |
| `Musuh.serang(timer, target)` | Memeriksa jarak dan jeda serangan, lalu memberi damage sentuh jika syaratnya terpenuhi. Dipanggil setelah gerakan musuh. |
| `Musuh.terserang(dmg)` | Mengurangi HP musuh. Dipanggil ketika serangan pemain mengenai musuh. |
| `Musuh.gambar(layar, cam)` | Menggambar musuh hidup yang terlihat kamera. |
| `Spawn.__init__(data_musuh, jeda=1.5, limit_musuh=6, total=None)` | Menyiapkan satu pengatur spawn untuk sebuah run. `total=None` berarti kuota keseluruhan tidak dibatasi. |
| `Spawn.pos_spawn(posisi_player, ukuran_layar)` | Memilih koordinat dunia acak di luar layar. Dipakai oleh `Spawn.update()`. |
| `Spawn.update(timer, player, list_musuh, ukuran_layar)` | Memeriksa timer dan kuota. Mengembalikan `[]` atau `[musuh_baru]`. `Game` menambahkan hasilnya dengan `extend()`. |

### Pistol dan peluru · `senjata/pistol.py` dan `senjata/peluru.py`

| Method | Fungsi dan kapan dipanggil |
| --- | --- |
| `Pistol.__init__(damage, dur, range=600, speed=450)` | Menyiapkan damage, jeda, jangkauan, dan kecepatan peluru. Dipanggil oleh `start_game()`. |
| `Pistol.update(timer, player, list_musuh, mode)` | Memperbarui peluru, memeriksa hit, lalu mencoba menembak sesuai bidikan. Menghasilkan `True` saat peluru baru dibuat dan `None` jika tidak menembak. |
| `Pistol.gambar(layar, cam)` | Meminta setiap peluru aktif menggambar dirinya saat gameplay ditampilkan. |
| `Peluru.__init__(posisi, arah, damage, speed, range)` | Membuat peluru dari salinan posisi awal dan arah tembakan. Dipanggil oleh pistol setelah arah tembakan tersedia. |
| `Peluru.update(timer)` | Menggerakkan peluru dan mengurangi sisa jarak tempuh. |
| `Peluru.hit(target)` | Mengembalikan `True` jika lingkaran peluru menyentuh target. Pistol memakai hasilnya untuk menerapkan damage. |
| `Peluru.gambar(layar, cam)` | Menggambar peluru saat posisinya terlihat kamera. |

### Menu dan HUD · `ui/`

| Method | Fungsi dan kapan dipanggil |
| --- | --- |
| `Menu.__init__(title="Curiousity", select=None)` | Menyiapkan judul dan daftar pilihan. Dipakai untuk Main Menu, Settings, Mode, Pause, dan Game Over. |
| `Menu.slide(step)` | Memindahkan pilihan dan berputar ketika melewati ujung daftar. Gunakan `-1` untuk naik dan `1` untuk turun. |
| `Menu.active_select()` | Mengembalikan teks pilihan saat ini. Biasanya dibaca ketika Enter ditekan. |
| `Menu.gambar(layar)` | Menggambar judul dan menyorot pilihan aktif. |
| `PilihKarakter.__init__(data_char)` | Membuat menu dari entri karakter yang punya objek sprite dan konfigurasi senjata. |
| `PilihKarakter.active_select()` | Mengembalikan ID karakter di JSON, misalnya `"nara"`. Dipakai untuk memilih data karakter saat mulai. |
| `PilihKarakter.gambar(layar)` | Menggambar menu beserta statistik karakter aktif. Navigasinya memakai `Menu.slide()`. |
| `HUD.__init__(lebar)` | Menyiapkan font dan posisi tombol Pause. Dipanggil setelah Pygame siap. |
| `HUD.set_char(player)` | Membuat ikon dari frame idle pertama. Dipanggil ketika mulai atau mengulang run. |
| `HUD.teks(layar, isi, posisi, tengah=False, besar=False)` | Menggambar label. Dipakai oleh HUD untuk nama, angka, dan informasi permainan. |
| `HUD.bar(layar, area, nilai, maks, color, teks)` | Menggambar bar dan label berdasarkan rasio nilai terhadap maksimum. Dipakai untuk HP dan XP. |
| `HUD.gambar(layar, player, xp, xp_limit, level, skor, time, stage)` | Menggambar HUD dengan data run terkini. Dipanggil setelah gambar pemain, musuh, dan peluru. |

`ui/tema.py` berisi konstanta warna. `curiousity.py` membuat objek `Game` dan memanggil `running()` ketika dijalankan langsung.
