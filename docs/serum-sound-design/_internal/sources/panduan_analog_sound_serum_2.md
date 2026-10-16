# Panduan Merancang Karakter Suara Analog di Xfer Serum 2

Panduan ini merangkum lima teknik desain suara (*sound design*) dari video tutorial ["You can throw away your analog synths now"](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U) oleh kanal YouTube **Undulae Music** untuk mengubah karakter digital [Xfer Records Serum 2](https://www.google.com/search?q=https%3A%2F%2Fxferrecords.com%2Fproducts%2Fserum-2) menjadi hangat, organik, dan dinamis layaknya *synthesizer* analog perangkat keras.

## Ringkasan 5 Teknik Utama Emulasi Analog

Tabel perbandingan di bawah memetakan setiap teknik dengan modul yang digunakan, parameter kunci, serta fungsi akustiknya:

| Teknik Emulasi | Modul & Lokasi | Parameter Kunci | Karakter & Hasil Suara | Timestamp Video |
| :--- | :--- | :--- | :--- | :--- |
| **1. Voice Chip Drift** | Tab **Global** → Panel *Voice Control* | Voice Count (6–8), Detune, Pan, Cutoff, Randomizer | Variasi *pitch*, posisi stereo, dan warna filter antar not saat memainkan akor | [00:00:44](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D44s) |
| **2. Noise FM Flutter** | **Oscillator C** → **Oscillator A** (FM) | Low-Pass Filter, Pitch Track *Off*, FM from Osc C | Ketidakstabilan *pitch* mikro (*flutter*) hingga efek synth analog tua/rusak | [00:03:10](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D190s) |
| **3. S&H Pitch Drift** | **LFO 1** → **Matrix** (*Global Tuning*) | Gelombang *Sample & Hold*, Smoothing, Bipolar ~1% | Pergeseran *pitch* acak yang lebih lambat, mulus, dan bebas desis (*noiseless*) | [00:04:47](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D287s) |
| **4. Audio-Rate Noise Mod** | **Oscillator A** → **Noise Level** (Matrix) | Mode Monophonic, Stereo Noise, Kurva Remap Matrix | Tekstur *bass* yang *gritty* dan berkarakter tanpa kesan *white noise* statis | [00:05:44](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D344s) |
| **5. Asymmetrical Drive & Tape** | Tab **FX** & Rantai Efek DAW | Asymmetrical Distortion, Fast Compressor, Analog Clip, Tape | Mengubah gelombang *saw* digital yang kaku menjadi bulat, hangat, dan responsif terhadap resonansi | [00:07:09](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D429s) |

## 1. Panel Kontrol Voice di Tab Global Meniru Pergeseran Kalibrasi Voice Chip

Polysynth analog klasik memiliki komponen perangkat keras bernama *voice chips*—di mana setiap *chip* memuat jalur suara mandiri (osilator, filter, *envelope generator*, dan VCA). Seiring waktu, kalibrasi antar *voice chip* mengalami pergeseran (*drift*) sehingga tiap not yang dimainkan berurutan memiliki sedikit perbedaan *tuning*, bukaan filter, atau kecepatan *envelope* ([00:00:51](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D51s)).

Langkah pengaturan di halaman **Global** [Serum 2](https://www.google.com/search?q=https%3A%2F%2Fxferrecords.com%2Fproducts%2Fserum-2):

* **Atur Jumlah *Voice Chips***: Tentukan jumlah alokasi suara hingga maksimal 8 *voices*. Sebagai contoh, pilih **6 voices** untuk meniru arsitektur 6-suara pada [Sequential Prophet-6](https://www.google.com/search?q=https%3A%2F%2Fsequential.com%2Fmodern-analog%2Fprophet-6%2F) ([00:02:04](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D124s)).
* **Gambar Variasi *Detune* (*D-Tune*)**: Masuk ke sub-halaman **D-Tune** dan gambar sedikit perbedaan tinggi-rendah pada tiap batang suara. Saat not dimainkan secara berurutan, [Serum 2](https://www.google.com/search?q=https%3A%2F%2Fxferrecords.com%2Fproducts%2Fserum-2) akan berputar melewati tiap *voice chip* (*voice cycling*) sehingga tidak ada dua not berurutan yang terdengar identik ([00:01:41](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D101s)).
* **Buat Pola Penyebaran Stereo (*Pan Spread*)**: Buka sub-halaman **Pan** dan gambar pola menyebar secara bertahap dari kiri ke kanan untuk mereplikasi perilaku *pan spreading* khas [Prophet-6](https://www.google.com/search?q=https%3A%2F%2Fsequential.com%2Fmodern-analog%2Fprophet-6%2F) ketika memainkan akor penuh ([00:02:11](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D131s)).
* **Bedakan Bukaan Filter (*Cutoff*) Tiap Suara**: Masuk ke sub-halaman **Cutoff** dan atur nilai yang sedikit berbeda untuk tiap *voice*. Bahkan saat memainkan satu nada yang sama berulang kali, warna kecerahan filter akan berubah secara organik ([00:02:30](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D150s)).
* **Aktifkan *Randomizer* untuk Perilaku Tak Terduga**: Jika tidak ingin pola pergeseran yang berulang secara tetap, naikkan nilai persentase pada kontrol **Randomizer** di sisi kanan panel untuk mengacak parameter tiap *voice* secara dinamis ([00:02:51](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D171s)).

## 2. Modulasi FM dari Filtered Noise Menciptakan Flutter Pitch Mikro

Osilator analog tidak pernah menghasilkan frekuensi yang terkunci secara kaku. Menggunakan sumber *noise* yang telah difilter sebagai modulator FM menghasilkan getaran *pitch* mikro (*fluttering*) yang menghidupkan gelombang statis ([00:03:11](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D191s)).

Langkah konfigurasi menggunakan **Oscillator C**:

1. **Muat Gelombang *Noise* di Oscillator C**: Gunakan **Oscillator C** sebagai sumber *noise* modulasi agar modul *Noise Oscillator* utama tetap tersedia untuk kebutuhan *white noise* biasa ([00:03:16](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D196s)).
2. **Pasang *Low-Pass Filter* pada Oscillator C**: Aktifkan filter *low-pass* khusus untuk menyaring frekuensi tinggi dari *noise* pada Oscillator C agar fluktuasi modulasinya tidak terlalu kasar ([00:03:26](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D206s)).
3. **Matikan *Pitch Tracking***: Nonaktifkan opsi *Pitch Tracking* pada Oscillator C supaya kecepatan fluktuasi *noise* tetap seragam di nada rendah maupun tinggi ([00:03:31](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D211s)).
4. **Terapkan *FM from Osc C* secara Halus**: Pada osilator utama (**Oscillator A**), pilih mode warp **FM from Osc C**. Naikkan nilainya perlahan hingga efek getaran berada tepat di ambang batas pendengaran (*almost inaudible*) untuk memberi kesan hangat alami ([00:03:38](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D218s)).
5. **Eksplorasi Karakter *Broken Synth***: Jika menginginkan tekstur *lo-fi* atau karakter synth analog tua yang rusak, naikkan persentase **FM from Osc C** lebih tinggi dan padukan dengan filter utama ([00:04:36](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D276s)).

## 3. LFO Sample & Hold Menghasilkan Ketidakstabilan Pitch yang Lebih Halus

Apabila teknik FM *noise* masih terasa terlalu berdesis untuk *patch* yang bersih, modulator **Sample & Hold (S&H)** yang diperhalus dapat memberikan efek *pitch drift* serupa namun jauh lebih lambat dan mulus ([00:04:47](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D287s)).

Langkah pengaturan di **LFO 1** dan **Modulation Matrix**:

* **Pilih Gelombang *Sample & Hold***: Ubah bentuk gelombang **LFO 1** menjadi *Sample & Hold* ([00:04:58](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D298s)).
* **Naikkan Parameter *Smoothing***: Putar *knob* **Smoothing** pada LFO 1 untuk melandaikan lompatan tangga sinyal acak menjadi kurva bergelombang yang mulus ([00:05:01](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D301s)).
* **Hubungkan ke *Global Tuning* secara Bipolar**: Di **Modulation Matrix**, arahkan **LFO 1** ke **Global Tuning** (*Master Tune*), ubah arahnya menjadi **Bipolar**, dan atur nilainya sangat kecil sekitar **1%** ([00:05:04](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D304s)).
* **Perhalus Skala Modulasi**: Gunakan pengatur skala (*Output/Aux scaling*) pada baris Matrix tersebut untuk memperkecil rentang goyangannya hingga pergeseran nada terasa organik tanpa terdengar sumbang ([00:05:16](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D316s)).

## 4. Modulasi Audio-Rate pada Level Noise Menambah Tekstur Bass yang Gritty

Menambahkan *white noise* biasa secara langsung di atas suara *bass* sering kali terdengar terlalu bersih dan terpisah dari osilator utama. Dengan menjadikan gelombang **Oscillator A** sebagai sumber modulasi (*audio-rate modulation*) terhadap volume *noise*, fluktuasi gelombang osilator akan memompa level *noise* secara *real-time* ([00:05:44](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D344s)).

Langkah merancang *bassline* analog yang *gritty*:

1. **Siapkan Fondasi *Bass Monophonic***: Turunkan nada osilator ke oktaf rendah (*low end*) dan aktifkan mode **Monophonic** ([00:05:49](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D349s)).
2. **Aktifkan *Stereo Noise* dengan Level Dasar Rendah**: Nyalakan modul **Noise** dan aktifkan mode **Stereo**, tetapi tahan *knob* **Level** agar tidak berbunyi secara konstan ([00:05:59](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D359s)).
3. **Gunakan Oscillator A sebagai *Mod Source***: Buka **Modulation Matrix**, pilih **Oscillator A** sebagai sumber modulasi (*Mod Source*), dan hubungkan ke **Noise Level**. Turunkan jumlah modulasinya secukupnya agar tidak terdengar terlalu tajam (*abrasive*) ([00:06:20](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D380s)).
4. **Bentuk Karakter dengan *Modulation Remap Curve***: Di jendela kurva pemetaan Matrix, sesuaikan bentuk lengkungan kurva. Menekankan bagian kurva tertentu akan mengubah tekstur *noise* dari desiran halus (*smooth*) menjadi dengungan harmonik yang renyah (*buzzy*) ([00:06:41](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D401s)).

## 5. Distorsi Asimetris, Kompresi Cepat, dan Saturasi Pita Menyempurnakan Kehangatan

Gelombang *sawtooth* digital memiliki bentuk simetris sempurna yang terdengar kaku. Memodifikasi bentuk puncak dan lembah gelombang secara tidak simetris serta menambahkan pemrosesan dinamika membuat filter bereaksi layaknya sirkuit analog sungguhan ([00:07:10](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D430s)).

Rantai pemrosesan akhir di dalam [Serum 2](https://www.google.com/search?q=https%3A%2F%2Fxferrecords.com%2Fproducts%2Fserum-2) dan DAW:

* **Gunakan *Tube* atau *Asymmetrical Distortion***: Pada tab **FX**, aktifkan modul **Distortion**. Mode **Tube** membulatkan ujung gelombang secara lembut, sedangkan mode **Asymmetrical** mendistorsi sisi atas (*top*) dan sisi bawah (*bottom*) gelombang secara berbeda sehingga menghasilkan karakter harmonik yang dinamis ([00:07:20](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D440s)).
* **Dorong *Resonance* Filter Setelah Distorsi**: Setelah distorsi asimetris aktif, menaikkan **Resonance** dan menggerakkan *Cutoff* filter akan menghasilkan sapuan frekuensi yang lembut sekaligus memberi efek *crunch* alami pada komponen *noise* ([00:08:48](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D528s)).
* **Tambahkan Kompresor Cepat**: Aktifkan modul **Compressor** di tab FX dengan pengaturan respon yang cepat (*fast compressor*) untuk menjaga kepadatan dinamika sinyal ([00:08:09](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D489s)).
* **Jinakkan Puncak Sinyal dengan *Analog Clip***: Jika muncul *clipping* akibat dorongan distorsi dan kompresor, tambahkan efek [Ableton Live Saturator](https://www.google.com/search?q=https%3A%2F%2Fwww.ableton.com%2Fen%2Fmanual%2Flive-audio-effect-reference%2F) dengan mode **Analog Clip** di jalur audio DAW untuk memotong puncak gelombang secara hangat ([00:08:28](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D508s)).
* **Beri Dimensi Ruang dan Saturasi Pita**: Lengkapi rantai sinyal dengan *reverb* [Eventide Blackhole Immersive](https://www.google.com/search?q=https%3A%2F%2Fstore.eventideaudio.com%2Fproducts%2Fblackhole-immersive) untuk ruang akustik yang luas ([00:09:02](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D542s)), lalu tutup dengan plugin gratis [Airwindows ToTape](https://www.google.com/search?q=https%3A%2F%2Fwww.airwindows.com%2Ftotape9%2F) untuk merekatkan seluruh spektrum menggunakan saturasi pita magnetik ([00:09:38](https://www.google.com/search?q=https%3A%2F%2Fwww.youtube.com%2Fwatch%3Fv%3DEWrwVgzyu6U%26t%3D578s)).
