# Panduan detail sound analog dan retro di Serum 2

Panduan ini menjadi **default saat brief meminta sound analog, vintage, retro analog, atau pendekatan gear analog nyata**, termasuk saat memilih sound tiap layer komposisi. Instruksi atau referensi pengguna yang lebih spesifik tetap diutamakan. Untuk brief analog tanpa model gear, mulai dari instrumen yang terawat dengan variasi kecil; tentukan keluarga arsitektur menurut peran sound dan catat asumsi. Istilah retro saja belum menentukan arsitektur: rekaman retro juga bisa memakai FM digital, sampler, atau instrumen akustik.

Tujuannya ialah meniru perilaku instrumen: sumber, interaksi oscillator, filter, envelope, alokasi voice, respons permainan, dan jalur audio. Kelima teknik dari lampiran pengguna menjadi pilihan yang dipakai sesuai penyebab bunyinya. Noise FM, stereo noise, kompresi cepat, tape, dan reverb besar **tidak otomatis aktif** pada setiap patch analog.

Semua angka resep di sini merupakan **titik awal rancangan**, bukan hasil ukur hardware atau preset yang sudah didengarkan. Nilai cents/Hz/ms/dB menjelaskan target fisik atau musikal; konversikan ke parameter Serum/tool yang benar dan verifikasi. Persentase sebuah knob bukan satuan universal.

## Isi dan jalur baca

- [1. Pilih target dan arsitektur](#1-pilih-target-dan-arsitektur)
- [2. Bangun sumber dan fase](#2-bangun-sumber-dan-fase)
- [3. Filter, envelope, dan permainan](#3-filter-envelope-dan-permainan)
- [4. Teknik 1: variasi antar voice](#4-teknik-1-variasi-antar-voice)
- [5. Teknik 2: filtered-noise FM](#5-teknik-2-filtered-noise-fm)
- [6. Teknik 3: drift S&H yang dihaluskan](#6-teknik-3-drift-sh-yang-dihaluskan)
- [7. Teknik 4: oscillator ke level noise](#7-teknik-4-oscillator-ke-level-noise)
- [8. Teknik 5: drive, dinamika, dan tape](#8-teknik-5-drive-dinamika-dan-tape)
- [9. Resep menurut keluarga instrumen](#9-resep-menurut-keluarga-instrumen)
- [10. Macro dan spesifikasi implementasi](#10-macro-dan-spesifikasi-implementasi)
- [11. Implementasi native dan batas tool](#11-implementasi-native-dan-batas-tool)
- [12. Verifikasi dan perbaikan](#12-verifikasi-dan-perbaikan)
- [13. Sumber dan koreksi lampiran](#13-sumber-dan-koreksi-lampiran)

Untuk patch baru, baca bagian 1–4, bagian teknik yang diperlukan, resep terkait, lalu 10–12. Untuk memperbaiki sound yang sudah ada, mulai dari gejala di bagian 12 dan pertahankan karakter yang diminta pengguna.

## 1. Pilih target dan arsitektur

Catat peran, rentang MIDI, panjang gate, mono/poly, legato/retrigger, model/revisi gear bila ada, keadaan kalibrasi, dan apakah target ialah output synth kering atau rekaman yang sudah diproses. Suara hardware pada rekaman dapat mengandung chorus, amplifier, konsol, tape, EQ, dan ruang; pisahkan hipotesis instrumen dari hipotesis rekamannya.

| Target | Fondasi yang diprioritaskan | Perlakuan variasi dan stereo |
|---|---|---|
| Monosynth VCO, misalnya keluarga Minimoog | Beberapa oscillator terpisah, mixer, low-pass resonan, envelope dan glide | Offset dan gerakan relatif oscillator; pusat mono; tidak memerlukan pola enam voice |
| Polysynth VCO, misalnya pendekatan Prophet | Oscillator per voice, filter/envelope per voice, batas polyphony | Offset kalibrasi antar voice dan drift kecil; pan spread hanya bila target memiliki/memerlukan fitur itu |
| Polysynth DCO, misalnya Juno-106 | Satu inti pitch per voice dengan saw/pulse/sub terkait, filter/envelope, chorus | Pitch relatif stabil; PWM, filter dan chorus menyediakan gerakan; hindari detune dua VCO bebas sebagai fondasi |
| String ensemble atau organ analog | Generator/register dan pembagian envelope sesuai target, ensemble sebagai pembentuk utama | Gerakan ensemble tidak sama dengan drift VCO; jangan menganggap semua alat memakai VCF dan ADSR per nada |
| Rekaman tua atau synth rusak | Fondasi instrumen dahulu, kemudian kerusakan/medium rekaman | Wow/flutter, hiss, dropouts, pitch wander lebih besar hanya bila brief memerlukannya |

Nama keluarga merupakan arah rancangan. Filter bernama mirip atau jumlah oscillator yang sama belum membuktikan emulasi sirkuit. Jika target gear tertentu, cocokkan manual/model/revisi dan referensi audio bila tersedia; beri label **terinspirasi** atau **pendekatan** sampai pembandingan mendukung klaim yang lebih kuat.

Default keputusan untuk brief analog umum:

1. Gunakan waveform sederhana yang tepat, satu unison voice per oscillator sebagai fondasi, dan jalur subtractive yang mudah diperiksa.
2. Cocokkan attack, body, release, respons filter, serta mode permainan sebelum memperbesar ketidakstabilan.
3. Tambahkan variasi antar voice untuk poly atau drift relatif untuk beberapa VCO bila diperlukan. Pada DCO, mulai dengan drift pitch nol atau sangat kecil.
4. Pertahankan low end dan pusat stereo. Lebarkan lewat mekanisme yang sesuai target, misalnya chorus atau pan spread yang memang diminta.
5. Tambahkan nonlinearitas secukupnya dengan perbandingan level setara. Pilih noise FM atau modulasi noise hanya jika masih ada sifat tekstur yang belum terpenuhi.
6. Pisahkan lapisan instrumen dari warna rekaman. Simpan FX eksternal sebagai langkah opsional dengan dependency yang jelas.

## 2. Bangun sumber dan fase

### Waveform, jumlah oscillator, dan tuning

Mulai dari saw, pulse/square, triangle, atau campurannya menurut target. Pilih tabel/frame yang benar-benar diperiksa; nama tabel saja tidak menjamin bentuknya. WT position tetap merupakan awal yang wajar untuk sumber subtractive, kecuali perubahan bentuk/PWM memang diperlukan. Warp kompleks dipakai untuk sifat yang bernama dan teruji.

Gunakan A/B/C sebagai oscillator terpisah saat perlu mengatur interval, level, fase, dan drift masing-masing. Unison menumpuk salinan oscillator; ia bukan pengganti otomatis arsitektur dua atau tiga VCO. Hard sync, ring modulation, atau cross-mod dapat menjadi ciri hardware tertentu, sehingga gunakan bila target meminta, bukan sebagai hiasan semua patch retro.

Untuk dua VCO pada interval unison, coba selisih tuning total 3–8 cents. Bedakan **offset tetap antar oscillator**, **offset antar voice**, dan **drift sepanjang waktu**. Ketiganya dijumlahkan pada pitch akhir dan dapat menghasilkan beating berlebihan bila dinaikkan bersama-sama. Pada bass, mulai lebih kecil dan dengarkan sustain panjang.

Hubungan pitch dan beating untuk dua sinus terdekat:

`f2 = f1 × 2^(cents/1200)`; `beat_Hz ≈ |f2 − f1|`.

Contoh: selisih 5 cents sekitar 0,29 Hz pada 100 Hz, tetapi sekitar 2,89 Hz pada 1 kHz. Kedalaman cents yang sama tidak menghasilkan kecepatan beating yang sama di semua register. Bunyi kompleks juga dipengaruhi partial dan filter.

Pada pendekatan DCO, saw/pulse/sub yang berasal dari satu inti bukan oscillator bebas yang terus bergeser relatif. Gunakan relasi pitch dan fase yang terkendali, atau sumber gabungan/template terverifikasi bila relasi persis diperlukan. Memainkan saw dan pulse di slot terpisah tanpa detune hanya pendekatan; verifikasi relasi fase dan artikulasinya.

### Fase: random, memory, dan kontinuitas

Manual S2 pp. 41–44 membedakan PHASE, RAND, dan Phase Memory. RAND mengacak fase awal voice baru; ia tidak membuat pitch bergerak selama nada ditahan. Phase Memory menyediakan All Voices, Contiguous, dan Per Voice dengan perilaku berbeda. Pilih dari perilaku note-on yang dibutuhkan, bukan berdasarkan anggapan bahwa RAND maksimum selalu lebih analog.

- Ulangi satu nada dengan gate pendek. Jika attack selalu menghasilkan sapuan fase identik yang tidak sesuai target, periksa reset fase, RAND, dan Phase Memory.
- Untuk kesan oscillator berlanjut, evaluasi Contiguous sesuai manual dan uji note overlap/voice stealing. Jangan menyamakan opsi itu dengan simulasi lengkap semua VCO hardware yang terus berosilasi.
- Untuk bass tajam dengan fase terkontrol, pertahankan attack konsisten bila dibutuhkan musik; tambah variasi di filter atau sustain tanpa merusak pukulan awal.
- Bila ada klik, periksa diskontinuitas fase, attack/release, envelope retrigger, dan DC. Mengacak fase bukan penyelesaian universal.

### PWM

Pilih pulse dan metode perubahan duty cycle yang benar menurut UI/template. LFO lambat sekitar 0,1–0,6 Hz dengan perubahan duty cycle terbatas adalah percobaan awal untuk pad; jangan menganggap WT scan saw-ke-square sebagai PWM yang setara. Batasi agar pulse tidak hilang pada ekstrem, dan periksa apakah body tetap jelas pada register rendah. Sumber PWM bersama dapat sesuai hardware dengan satu LFO bersama; sumber per voice memberi perilaku berbeda.

## 3. Filter, envelope, dan permainan

### Filter dan jalur gain

Pilih slope dan karakter respons menurut target: low-pass 24 dB/oct untuk sebagian keluarga, 12 dB/oct atau multimode untuk keluarga lain. Bandingkan cutoff, resonance, key tracking, level input, dan respons saat didorong. Nama mode Serum tidak menjadi bukti kecocokan dengan ladder, OTA, atau rangkaian hardware tertentu.

Pastikan semua sumber yang seharusnya difilter benar-benar melewati filter; periksa Sub/Direct dan jalur paralel agar tidak menambah fundamental yang tidak ada di target. Sebaliknya, bila dibutuhkan sub bersih dalam produksi, tulis sebagai adaptasi musikal. Resonance dapat mengubah level fundamental menurut model filter; jangan selalu mengompensasinya bila justru itu ciri target.

Nyatakan cutoff sebagai endpoint yang bisa diuji, misalnya base 300 Hz menuju sekitar 2 kHz saat envelope mencapai puncak. Pada skala logaritmik, octave lebih berguna daripada penjumlahan Hz: `cutoff_baru = cutoff_dasar × 2^(offset_octave)`. Offset ±0,02 octave kira-kira ±1,4% frekuensi. Jangan menyalin persentase cutoff UI langsung ke rumus ini tanpa kalibrasi.

### Envelope dan artikulasi

Pisahkan Env 1 untuk amplitude dan envelope timbre bila target memerlukannya. Samakan kurva, gate, sustain, dan perilaku retrigger. Angka attack 10 ms pada dua synth belum tentu menghasilkan transient yang sama karena kurva dan level awal berbeda.

| Peran | Amp: attack / decay / sustain / release | Titik awal envelope filter |
|---|---|---|
| Bass pendek | 3 ms / 250 ms / 65% / 70 ms | Attack 2 ms, decay 180 ms, sustain rendah |
| Pluck/key | 4 ms / 650 ms / 0–15% / 180 ms | Decay 200–400 ms; brightness turun lebih cepat dari body |
| Brass poly | 25 ms / 500 ms / 70% / 250 ms | Attack 35 ms, decay 450 ms, sustain sedang |
| Pad | 500 ms / 1 s / 80% / 1,5 s | Attack 900 ms, release 1,8 s; rentang cutoff terbatas |
| Lead legato | 8 ms / 350 ms / 80% / 130 ms | Attack cepat, body bertahan; test legato dan detached |

Angka ini tidak mewakili kalibrasi hardware. Sesuaikan tempo dan gate nyata; note-off bisa terjadi sebelum decay selesai. Untuk meniru panel ADS/decay-release bersama, ikuti keterkaitan kontrol target; ADSR bebas pada Serum adalah kemudahan implementasi, bukan bukti fitur asli.

### Polyphony, note priority, dan expression

Atur batas polyphony secara terpisah dari sequence Voice Control. Pertimbangkan release overlap: akor enam nada diikuti akor baru dapat mencuri voice walaupun masing-masing akor hanya enam nada. Untuk mono, tentukan note priority, legato/retrigger dan glide; jika priority yang diminta tidak didukung schema, verifikasi melalui UI/template atau laporkan celahnya.

Velocity, aftertouch, atau MPE mengikuti target. Hardware lama tertentu tidak merespons velocity seperti synth modern. Saat mengejar perilaku asli, jangan otomatis menambahkan velocity-ke-cutoff besar; jika berguna untuk produksi, labeli sebagai adaptasi performa. Tuning drift di dalam synth tidak mengubah timing MIDI: kontrak on-grid/no-swing workspace tetap berlaku.

## 4. Teknik 1: variasi antar voice

**Tujuan:** memberi identitas kalibrasi pada tiap voice, sehingga pengulangan nada/akor mempunyai variasi kecil tanpa membuat sustain seluruh akor bergoyang bersama.

Manual S2 pp. 316–318 menjelaskan Global → Voice Control, pilihan oscillator yang terkena, sequence 1–8, serta RANDOM untuk PAN, DETUNE, CUTOFF, dan ENVS. Angka 1–8 mengatur **panjang sequence**; ia bukan batas maksimum polyphony Serum dan bukan oscillator unison count. Nama `voice_unison` pada tool juga bukan alasan untuk menyamakan ketiganya.

Langkah UI:

1. Mulai dari konfigurasi Init pada panel dan pilih oscillator yang memang harus terkena. Catat pilihan A/B/C/Noise/Sub.
2. Pilih panjang sequence sesuai desain, misalnya enam langkah untuk percobaan polysynth enam voice. Atur batas polyphony di bagian Voicing secara terpisah.
3. Isi variasi DETUNE kecil, rata-rata dekat nol; periksa hasil dalam cents memakai UI yang sesuai atau pengukuran. Jangan menganggap batang SEQ memakai satuan cents.
4. Tambahkan CUTOFF dan ENVS sedikit bila target perlu perbedaan timbre/artikulasi. Mulai dari nol agar dampak setiap kelompok terdengar.
5. PAN tetap tengah untuk instrumen mono atau target tanpa pan spread. Bila dibutuhkan, gunakan pola kecil kiri/kanan dan periksa mono sum. Sifat pan spread pada Prophet-6 bukan ciri wajib semua synth retro.
6. RANDOM mulai nol, lalu naikkan sedikit jika pola tetap terlalu kentara. Manual mencantumkan RANDOM DETUNE dalam cents, sedangkan parameter random lain dalam persen; tool memiliki ketidakpastian skala tertentu, jadi cocokkan readout sebelum menulis angka.
7. Uji 16–24 note-on nada sama secara detached, akor ditahan, lalu overlap/voice stealing. Pastikan sifat yang berulang benar berasal dari alokasi/sequence, bukan LFO retrigger atau variasi velocity.

Contoh **target musikal enam langkah** untuk kalibrasi; bukan array JSON tool:

| Langkah | Target pitch offset | Target cutoff relatif | Target waktu envelope relatif | Pan bila diperlukan |
|---|---|---|---|---|
| 1 | −2 cents | −1% frekuensi | +1% waktu | sedikit kiri |
| 2 | +1 cent | +1% frekuensi | −1% waktu | sedikit kanan |
| 3 | −1 cent | 0% | +2% waktu | dekat tengah |
| 4 | +2 cents | +2% frekuensi | 0% | sedikit kiri |
| 5 | 0 cents | −2% frekuensi | −2% waktu | sedikit kanan |
| 6 | 0 cents | 0% | 0% | tengah |

Jangan memberi pola identik pada semua parameter tanpa alasan: setiap voice menjadi selalu sekaligus paling tinggi, terang, cepat, dan kanan. Korelasi seperti itu mungkin dibutuhkan target tertentu, tetapi bukan default umum. Offset note-on tidak menggantikan drift selama sustain; gunakan bagian 6 untuk gerak tersebut.

## 5. Teknik 2: filtered-noise FM

**Tujuan:** menambah ketidakstabilan cepat atau tekstur kasar yang sangat kecil. Default **mati**; coba setelah fondasi dan drift lambat memadai. Noise FM menghasilkan sideband/pelebaran spektrum; ia tidak identik dengan perubahan kalibrasi VCO atau wow/flutter tape.

Langkah percobaan:

1. Gunakan Osc C sebagai modulator noise jika memang diperlukan agar slot Noise tetap tersedia. Pilih engine/source yang menghasilkan noise berkelanjutan. Tabel satu siklus yang diulang dapat menghasilkan pola periodik; jangan mengklaimnya noise acak broadband yang sama dengan sumber kontinu.
2. Terapkan low-pass **pada sinyal modulator sebelum titik FM**. Warp LPF pada C sebelum warp/modulasi berikutnya dapat menjadi jalur yang dievaluasi; urutan warp dan titik tap harus diperiksa pada UI/manual/template.
3. Nonaktifkan key tracking sumber jika bandwidth/fluktuasi dimaksudkan tetap saat nada carrier berubah. Jika kontrol engine itu tidak tersedia, gunakan sumber yang sudah difilter atau jalur filter terverifikasi dan catat perbedaannya.
4. Pada A pilih sumber FM yang benar-benar C. Sumber harus aktif, tetapi level audionya dapat diturunkan menjadi nol untuk modulasi saja menurut S2 p. 54. Solo/bypass untuk memeriksa bahwa C tidak bocor sebagai hiss langsung dan FM tetap bekerja.
5. Mulai amount dari nol. Naikkan sampai perbedaannya mudah dikenali, lalu turunkan sampai efek sesuai brief. Uji nada rendah, tengah, tinggi; amount persen yang sama belum tentu memberi pergeseran cents yang sama.
6. Bila ingin B turut mengalami perilaku ini, rancang route B secara eksplisit; FM A tidak otomatis memodulasi B. Periksa apakah sumber bersama membuat keduanya terlalu berkorelasi.

Sebagai eksperimen, mulai modulator yang didominasi frekuensi sangat rendah, misalnya low-pass sekitar 5–30 Hz, bila engine/filter sungguh mendukungnya. Naikkan bandwidth hanya bila perlu tekstur cepat; hasilnya dapat berubah menjadi roughness/noise daripada drift. Ini rentang percobaan, bukan nilai video atau ukuran flutter hardware.

Menaruh low-pass di audio utama setelah carrier tidak menyaring noise yang sudah masuk ke titik FM. Alternatif `FM (Filter 1/2)` hanya sah bila sumber filter dan routing ke carrier terkonfirmasi; jangan mengubah nama destination dan menganggap graph selesai.

Tanda terlalu jauh: pusat pitch bergeser, sustain berdesis, transient kasar, nada atas berbunyi seperti FM metalik. Turunkan amount/bandwidth, periksa mode FM dan tracking; jika hanya butuh pitch wander bersih, gunakan S&H halus. Untuk broken synth, kenaikan amount merupakan pilihan kreatif tersendiri dan harus dilabeli.

## 6. Teknik 3: drift S&H yang dihaluskan

**Tujuan:** pitch bergerak pelan selama nada ditahan tanpa menambahkan noise audio langsung. S&H bertangga yang belum dihaluskan bisa menghasilkan lompatan/zipper; modulasi pitch juga mengubah spektrum. Istilah tanpa hiss bukan jaminan tanpa artefak.

1. Pilih LFO bertipe S&H di UI; pada schema yang diperiksa nama algoritmenya `random_sh`. Penggunaan algoritme tersebut pada generation masih memiliki batas verifikasi yang dijelaskan tool.
2. Gunakan rate bebas dalam Hz, mode Free dan konfigurasi HOST yang sesuai. Untuk gerak bebas antar playback, evaluasi HOST off; jika reproduksibilitas diperlukan, catat perilaku host/reset yang dipakai. S2 pp. 191–193 membedakan FREE, MONO, BPM/HZ dan HOST.
3. Naikkan Smooth sampai peralihan cukup landai. Smoothing mengubah kedalaman dan respons efektif; periksa output serta periode aktual.
4. Untuk drift tiap voice, pilih sumber poly dan destination oscillator pitch yang benar. Untuk goyangan bersama seluruh instrumen, gunakan sumber mono bersama dan Main Tuning bila destination tersedia. Ini dua model berbeda.
5. Gunakan route bipolar yang terpusat. Mulai sekitar ±1–3 cents dan rate pembaruan 0,05–0,3 Hz untuk VCO terawat. Pada bass/DCO mulai nol atau lebih kecil; ubah berdasarkan target.
6. Kurangi amount/OUTPUT dan gunakan AUX scaling bila diperlukan untuk kalibrasi halus. Angka sekitar 1% pada Matrix dalam lampiran tidak menentukan besar pitch tanpa destination, rentang, curve, dan scaling.
7. Tahan nada 20–30 detik, lalu mainkan akor. Jika semua nada akor membengkok bersamaan, periksa source MONO dan destination global. Jika nada pendek terdengar sama setiap kali, periksa retrigger dan host phase.

Gerakan relatif dua oscillator membutuhkan route yang tidak seluruhnya identik. Gabungkan komponen bersama kecil dan komponen independen bila target menuntutnya; jangan menambahkan random sumber sebanyak mungkin. Sumber Main Tuning hanya menggeser keseluruhan pitch dan tidak otomatis meniru ketidaksepakatan antar VCO.

Pedoman **target pitch akhir**, termasuk penjumlahan semua route:

| Keadaan | Titik awal drift kontinu | Pilihan awal |
|---|---|---|
| DCO terawat/bass sangat stabil | 0 hingga sekitar ±1 cent | Utamakan PWM/filter/chorus |
| VCO terawat | sekitar ±1–3 cents | Gerak lambat kecil; offset antar oscillator terpisah |
| VCO vintage lebih longgar | sekitar ±3–6 cents | Periksa intonasi akor dan beating lintas register |
| Rusak/rekaman aus | Ditentukan brief dan pembandingan | Wander/wow/flutter bukan default analog umum |

Rentang tersebut bukan karakterisasi semua hardware. Pitch wander dapat berada pada banyak skala waktu; vibrato sinus reguler mudah terdengar seperti pemain/LFO, sehingga bukan pengganti otomatis drift acak. Bila memakai kurva periodik sebagai fallback, sebutkan bahwa perilakunya berulang.

## 7. Teknik 4: oscillator ke level noise

**Tujuan:** memberi grit yang mengikuti gerak waveform, bukan menambahkan hiss statis. Ini modulasi amplitude noise pada audio rate, bukan metode utama membuat pitch analog.

1. Siapkan bass mono dengan oscillator utama yang sudah tepat dan low end terpusat. Dengarkan versi tanpa noise sebagai pembanding.
2. Aktifkan Noise dengan sumber yang diketahui, level dasar sangat rendah atau nol. Pastikan jalurnya ke filter/output sesuai desain.
3. Di Matrix pilih output Osc A sebagai SOURCE dan Noise Level sebagai DESTINATION, sebagaimana kemampuan oscillator/filter sebagai mod source pada S2 p. 208 dan pp. 210–212.
4. Tentukan polarity dan base dengan sengaja: sinyal bipolar menuju level nonnegatif dapat terpotong pada nol. Bentuk remap dapat menghasilkan respons satu sisi atau rectified; base, amount, curve, dan clamping bersama-sama menentukan hasil.
5. Mulai amount kecil; uji apakah tekstur mengikuti body tanpa menutupi fundamental. Bypass route, lalu bypass Noise untuk membedakan kontribusi modulasi dari level dasar.
6. Gunakan Editable Curve dengan RISE/FALL bila tersedia untuk membentuk remap. Tool friendly belum menyediakan semua kurva remap ini; kurva yang hanya dideskripsikan dalam spec belum terimplementasi.
7. Stereo Noise adalah opsi tekstur bagian atas. Untuk bass, mulai mono dan gunakan stereo hanya bila target memerlukannya serta mono sum tetap baik. Jangan melebarkan fundamental hanya agar terdengar vintage.

Noise yang levelnya mengikuti oscillator tetap noise bermodulasi; jangan menjanjikan perubahan menjadi harmonik murni. Jika grit mendominasi, turunkan amount, batasi spektrum noise, atau gunakan saturasi ringan sebagai alternatif yang dinilai terhadap brief. Untuk pad bersih atau emulasi gear tanpa gejala tersebut, route ini boleh tetap mati.

## 8. Teknik 5: drive, dinamika, dan tape

### Nonlinearitas dan posisi dalam rantai

Saw ideal tidak otomatis terdengar buruk karena digital. Bentuk saw juga bukan sinus simetris; daftar harmoniknya berbeda. Warna analog berasal dari perilaku spesifik sumber, rangkaian, filter, kontrol, dan interaksi level. Waveshaping asimetris dapat mengubah kandungan harmonik dan DC, tetapi bukan syarat semua analog.

Bandingkan Tube, soft clipping/saturation, atau mode asimetris yang benar-benar tersedia. Manual membedakan warp Asym pada oscillator (p. 53) dan FX Distortion dengan mode termasuk X-Shaper (Asym) (pp. 167–168). Jangan mengasumsikan keduanya mempunyai nama enum, kurva, lokasi, atau respons yang sama.

| Lokasi nonlinearitas | Yang berubah | Penggunaan |
|---|---|---|
| Warp/saturasi oscillator sebelum voice filter | Harmonik sumber masuk filter dan mengikuti artikulasi voice | Membentuk excitation; berbeda dari bus drive |
| Input/drive voice filter | Interaksi level, resonance, dan model filter | Mendekati perilaku driven filter bila model mendukung |
| FX sesudah penjumlahan voice | Seluruh akor berinteraksi di nonlinearitas yang sama | Warna bus; dapat menimbulkan intermodulasi antar nada |
| FX sebelum/di dalam/sesudah ruang | Serangan, repeats, atau tails yang terdistorsi berbeda | Pilihan warna rekaman/produksi |

Pilih satu tahap dahulu. Mulai drive rendah, trim output, bandingkan level setara. Jika butuh drive sebelum filter tetapi hanya memakai FX setelah voice filter, catat bahwa hasilnya pendekatan berbeda. Urutan internal PRE/POST filter milik modul Distortion juga tidak sama dengan memindahkan seluruh modul ke depan voice filter.

### Kompresi dan headroom

Kompresor cepat bukan default untuk analog. Ia dapat mengurangi punch, mengangkat hiss, atau meratakan perbedaan voice yang baru dibuat. Jika dibutuhkan, mulai single-band dengan gain reduction kecil sekitar 1–3 dB pada bagian paling keras; sesuaikan attack/release terhadap transient dan tempo. Multiband agresif dipakai bila memang targetnya demikian.

Saat level overload, kurangi gain di tahap yang mengalami overload; trim akhir tidak menghapus clipping sebelumnya. Soft clip adalah warna tambahan yang dipilih, bukan perbaikan universal. Uji akor padat dan release overlap, bukan hanya satu nada. Sisakan headroom output yang memadai dan catat peak hasil render bila tersedia.

### Chorus, tape, dan ruang

Untuk keluarga DCO dengan chorus, chorus dapat menentukan identitas sound dan layak dirancang lebih awal. Chorus generik Serum merupakan pendekatan; ia belum membuktikan replika BBD tertentu. Hiss chorus hanya ditambahkan jika penting bagi target atau referensi; noise bukan syarat kehangatan.

Tape merupakan **lapisan medium rekaman**. Pisahkan saturasi, pembatasan bandwidth, wow, flutter, dan noise; satu mode Tape Sat tidak otomatis mengimplementasikan seluruh perilaku tape machine. Pitch modulation di dalam voice Serum tidak sama dengan memproses keseluruhan rekaman beserta tails sesudah synth.

Mulai reverb/delay dari bypass kecuali efek itu bagian identitas target. Blackhole Immersive, Airwindows ToTape, dan Ableton Saturator dalam lampiran adalah contoh rantai tutorial, bukan dependency wajib, bukan bagian preset native Serum, dan bukan instruksi default untuk Cubase. Jika memakai FX eksternal yang diminta, catat plugin/versi/order/settings dan cara memuatnya; preset Serum saja tidak membawa insert DAW tersebut.

## 9. Resep menurut keluarga instrumen

Resep berikut adalah prototipe authored yang **belum dirender/didengarkan**. Target register memakai angka MIDI agar label oktaf DAW tidak membingungkan. Sesuaikan parameter dan nilai akhir melalui [verifikasi](verification.md).

### A. Bass mono VCO yang terawat

- Rentang percobaan MIDI 28–55; mono, pusat stereo, unison 1 per oscillator.
- A saw sebagai body; B saw atau pulse dengan selisih 2–5 cents dan level lebih rendah. C hanya bila fungsi oscillator ketiga diperlukan. Sub bukan tambahan wajib bila target tidak memilikinya.
- Jalur mixer → low-pass 24 dB/oct yang paling cocok → amp. Mulai cutoff 150–400 Hz dengan envelope menuju sekitar 1–2 kHz, resonance rendah/sedang, key tracking sesuai rentang.
- Amp A/D/S/R sekitar 3 ms / 250 ms / 65% / 70 ms; filter decay sekitar 180 ms dengan sustain rendah. Drift mulai ±1 cent, noise FM/noise AM mati.
- Glide mulai 40–90 ms hanya bila brief menginginkan; tentukan legato dan priority. Drive ringan sebelum/di filter bila terimplementasi; chorus/reverb mati sebagai awal.
- Uji nada panjang, overlap, lompatan oktaf, dan level fundamental. Tidak ada klaim replika Minimoog hanya dari konfigurasi ini.

### B. Brass polysynth VCO

- Rentang percobaan MIDI 48–84; dua saw, selisih 4–7 cents; unison 1. Polyphony misalnya 6 sesuai target.
- Filter low-pass sesuai keluarga; base sekitar 500–900 Hz, envelope menuju 2–5 kHz. Amp dan filter mengikuti baris brass pada bagian 3.
- Voice Control enam langkah dengan variasi kecil pitch/cutoff/env; konversikan target bagian 4 melalui UI/readback. Drift kontinu mulai ±1–2 cents; FM noise mati.
- Pan spread ringan hanya bila sesuai target. Mulai saturasi rendah; reverb pendek opsional setelah karakter dry tercapai.
- Uji akor rapat, transposisi, note repeats, dan release overlap. Jika vibrato kolektif muncul, evaluasi route Main Tuning dan LFO MONO.

### C. Pad keluarga DCO/chorus

- Rentang percobaan MIDI 48–84; satu inti saw/pulse dengan square sub terkait jika perlu. Jangan memulai dari dua saw detuned lebar.
- PWM lambat sekitar 0,2–0,5 Hz dengan duty cycle moderat; low-pass dan high-pass sesuai kebutuhan target; satu envelope bersama bila target mengaitkan VCA/VCF.
- Amp attack 400–800 ms, release 1–2 s; envelope filter memberi bukaan lambat. Drift pitch nol dahulu; variasi timbre antar voice sangat kecil bila dibutuhkan.
- Chorus menjadi pembentuk utama lebar/gerak, dengan level wet yang masih menjaga body di mono. Noise FM dan oscillator→Noise Level mati.
- Uji versi chorus off/on pada level setara. Jika ingin meniru Juno tertentu, periksa source/fase/sub/chorus dengan referensi; generic chorus dan routing ADSR bebas belum merupakan replika sirkuit.

### D. Pluck/key retro poly

- Rentang MIDI 48–84; satu pulse atau dua oscillator dengan selisih 2–4 cents. Amp decay 500–900 ms, sustain 0–15%, release 100–250 ms.
- Filter decay 180–350 ms; cutoff menutup lebih cepat daripada amplitude. Buat variasi antar voice kecil pada cutoff dan envelope, bukan pitch besar pada setiap attack.
- Fase dipilih agar attack tidak berbunyi zap identik bila tidak sesuai target. Drift sangat kecil; chorus tipis atau delay gelap opsional.
- Uji repeats cepat dan sustain pedal/release overlap bila dipakai. Kompresi terlalu cepat dan reverb besar dapat menghapus artikulasi.

### E. Lead VCO ekspresif

- Rentang MIDI 55–88; saw/pulse, mono, retrigger untuk detached dan legato sesuai brief. Glide 50–120 ms sebagai percobaan.
- Amp attack 5–15 ms, release 80–180 ms; filter mengikuti permainan. Drift mulai ±1–2 cents.
- Vibrato pemain dipisah dari drift: sekitar 4–6 Hz dengan depth dari nol via mod wheel/aftertouch, batas atas ditentukan brief. Jangan memberi vibrato besar permanen lalu menyebutnya VCO drift.
- Uji note priority, bend range, overlap, dan perpindahan register. Fitur expression tambahan yang tidak ada di gear asli diberi label adaptasi.

### F. Varian aged/broken

Mulai dari salah satu resep yang sudah stabil, lalu simpan revisi baru. Tambahkan satu penyebab dahulu: drift lebih besar, noise FM kecil, noise AM untuk grit, atau pemrosesan tape setelah instrumen. Pisahkan macro **Age** dari **Drift** agar pengguna bisa memperoleh warna spektrum tua tanpa pitch rusak. Uji pusat pitch, dropout level, stereo/mono, dan tails. Varian ini dipilih hanya bila brief meminta kerusakan/rekaman aus.

## 10. Macro dan spesifikasi implementasi

Nama macro menjelaskan hasil dengar. Gunakan yang berguna untuk patch; tidak harus seluruh daftar.

| Macro | Kandidat tujuan | Batas yang diperiksa |
|---|---|---|
| Drift | Depth gerak pitch, bukan interval dasar | Nol sampai batas cents yang tetap musikal; total semua route diperhitungkan |
| Voice Character | Variasi cutoff/env dan offset voice jika bisa dimodulasi | Tidak merusak intonasi/attack; bila kontrol statis tak dapat dimodulasi, gunakan route alternatif terverifikasi atau varian preset |
| Drive | Drive dan trim kompensasi | Tidak sekadar lebih keras; periksa chord overload |
| Tone | Cutoff/envelope amount | Endpoint terukur di register target |
| Width | Chorus atau pan spread yang sesuai | Body mono terjaga; jangan otomatis menggeser bass |
| Age | Warna rekaman, noise/bandwidth/wow bila diterapkan | Mekanisme bernama, tidak mengaktifkan semua kerusakan sekaligus |
| Space | Wet delay/reverb | Tail, feedback, dan gain tetap terkendali |

Tambahkan catatan berikut pada design spec internal, terpisah dari JSON tool:

```yaml
analog_target:
  family: "VCO mono | VCO poly | DCO poly | ensemble | lainnya"
  model_revision: "model/revisi atau asumsi keluarga"
  condition: "terawat | lebih longgar | aged/broken sesuai brief"
  claim: "terinspirasi | pendekatan | pembandingan terhadap referensi"
  reference_scope: "instrumen dry atau rantai rekaman"
  oscillator_relationship: "jumlah, waveform, interval, relasi fase/sub"
  polyphony_and_priority: "batas voice, legato/retrigger, glide, note priority"
  voice_sequence: "panjang, oscillator terkena, target offset dan kalibrasi"
  continuous_drift: "shared/per-voice/per-oscillator, rate, target cents, smoothing"
  optional_techniques: "noise FM / noise AM / nonlinearitas / tape: alasan on/off"
  signal_path: "titik modulasi dan urutan pemrosesan yang sesungguhnya"
  historical_adaptations: "velocity/MPE/sub/stereo tambahan bila ada"
  calibration: "target fisik -> field/unit tool -> readback/UI/audio"
  unmet_requirements: []
```

Untuk setiap route tulis sumber, destination, base, amount, polarity, curve, AUX, OUTPUT, trigger, dan endpoint efektif. Catat state macro min/default/max serta interaksinya. Jangan memasukkan blok metadata rancangan ini sebagai field tambahan ke schema preset.

## 11. Implementasi native dan batas tool

Ikuti [native build](native-build.md), [tool capabilities](tool-capabilities.md), serta panduan Serum MCP workspace sebelum membuat preset. Panggil `list_parameters()` setiap build dan baca semantic schema terkini. Panduan ini tidak mengesahkan raw key/enum yang belum diketahui.

Inspeksi dokumentasi ini pada 2026-10-16 menggunakan runtime `list_parameters()` dan checkout lokal. Ada beberapa batas penting:

| Kebutuhan | Jalur yang tersedia | Yang masih harus dibuktikan pada build |
|---|---|---|
| Pola voice dan random | `voice_unison` dengan daftar pan/detune/filter_cutoff/env_time serta field random | Skala cents/cutoff/env; arti sequence `voice_count` masih ditandai uncertain oleh upstream |
| Jumlah suara | Voicing/polyphony, oscillator unison, dan Voice Control adalah state berbeda | Jangan memakai satu angka untuk ketiganya; periksa native state dan UI |
| Fase/RAND/Phase Memory | Template/UI/raw state yang sudah terverifikasi | Friendly OscillatorSpec tidak mengekspos semua opsi fase |
| Drift S&H | `lfos` dengan `shape: random_sh`, smooth, mode/rate/sync; route pitch yang tersedia | Upstream membatasi bukti generation algoritmik; periksa output dan distribusi/polarity |
| Shared versus poly LFO | Field mono dan pengaturan mode/HOST menurut kemampuan | MONO, FREE, dan HOST punya fungsi terpisah; schema belum tentu menyediakan semua switch |
| Noise C → FM A | Engine/source + warp/mod-source yang terverifikasi | Generic `fm` tidak menjamin sumber C; periksa tap sebelum/sesudah filter dan tracking |
| Audio-rate A → Noise Level | Source/destination Matrix yang didukung | Remap curve arbitrary dan noise stereo belum tentu dapat ditulis friendly schema |
| Drive per voice versus bus | Warp/filter drive atau FX chain sesuai kemampuan | Topologi, point of summing, PRE/POST dan output gain |
| Tape/FX eksternal | Workflow DAW terpisah jika diminta | Tidak tersimpan otomatis di `.SerumPreset` |

Ada ketidakselarasan dokumentasi unit: manual menyebut RANDOM DETUNE dalam cents; deskripsi semantic tool menggunakan konvensi yang sebagian masih uncertain/percentage-like. Batang SEQ DETUNE juga belum dikalibrasi cents oleh inspeksi upstream. Simpan target cents dan lakukan readout/ukur; jangan mengarang konversi. Nama `voice_count` yang diterima schema belum membuktikan setting enam langkah sudah benar di plugin.

Jika kontrol wajib belum tersedia: pakai template yang terverifikasi, atau UI yang tersedia, simpan native baru, lalu readback. Jika tidak ada jalur, nyatakan detail yang belum terpenuhi dan status kandidat. Jangan mengklaim emulasi gear selesai hanya karena JSON lolos schema. File `.SerumPreset`, dependency, spesifikasi/binding/receipt dan status pengujian mengikuti kontrak workspace.

## 12. Verifikasi dan perbaikan

### Uji terarah

Gunakan [verification](verification.md) untuk struktur, load, render dan listening. Untuk sound analog, tambah pemeriksaan berikut dengan MIDI, velocity, gate, tempo, quality, dan state macro yang dicatat:

1. **Dry baseline:** bypass proses opsional dan samakan level terhadap versi berkarakter. Attack/body/release serta jenis filter harus sudah mendekati tujuan.
2. **Repeat:** mainkan nada sama 16–24 kali dengan velocity/gate identik. Amati pola voice, attack fase, cutoff dan level. Sesuaikan jumlah ulangan jika sequence lebih panjang.
3. **Held note:** tahan 20–30 detik pada register rendah/tengah/tinggi. Untuk gerak lebih lambat, perpanjang sampai beberapa pembaruan/siklus tercakup. Pisahkan pusat tuning, deviasi cents, beating, vibrato reguler, dan hiss.
4. **Chord:** akor 3/4/6 nada sesuai target, termasuk release overlap. Periksa apakah drift per voice atau shared bekerja seperti spesifikasi, voice stealing sesuai batas, dan drive bus tidak mengaburkan akor.
5. **Artikulasi:** detached, legato, note overlap, lompatan register, velocity dan gesture yang benar-benar digunakan. Uji note priority/glide di mono.
6. **Mono/stereo:** periksa body, keseimbangan kanal, fundamental bass, dan chorus/pan spread. Korelasi meter membantu tetapi tidak menggantikan listening mono.
7. **Isolasi teknik:** bypass voice offsets, drift LFO, noise FM, noise AM dan drive secara terpisah. Nilai apakah tiap teknik menyelesaikan kebutuhan tertentu.
8. **Macro/level/tail:** min/default/max dan kombinasi ekstrem, peak saat akor, hiss sesudah release, feedback delay/reverb. Reload preset final dan cek dependency.

Jika mengukur pitch dari audio, mulai dengan oscillator tunggal bersih. FM, noise, harmonik kuat, chorus dan akor dapat menyesatkan tracker. Konversi deviasi frekuensi dengan `cents = 1200 × log2(f_ukur / f_target)`; pisahkan offset median dari deviasi terhadap median. Bandingkan referensi dengan nada/gate dan level yang setara, lalu nilai konteks musik.

### Diagnosis

| Gejala | Dugaan dan tindakan terarah |
|---|---|
| Masih statis meski pitch bergoyang | Periksa bentuk/relasi sumber, envelope, respons filter, fase; menambah drift tidak memperbaiki arsitektur yang salah |
| Terdengar sumbang/chorused berlebihan | Kurangi total offset + drift + unison + chorus; ukur per sumber; cek mean pitch dan polarity |
| Semua nada bergoyang bersama | Main Tuning/shared MONO LFO; gunakan destination/source per voice jika itulah target |
| Setiap attack identik seperti zap | Periksa reset fase/RAND/memory serta LFO retrigger; sesuaikan tanpa merusak pukulan bass |
| Hiss/roughness berlebih | Solo sumber, cek kebocoran C, noise level, bandwidth dan amount FM; bypass kompresor yang mengangkat noise |
| Patch DCO terlalu goyah | Kurangi drift/detune; kembalikan relasi pitch inti; gunakan PWM/chorus untuk gerak |
| Bass kehilangan body di mono | Kurangi chorus/stereo noise/pan pada komponen rendah; cek fase, jalur Sub dan resonance |
| Akor pecah padahal solo bersih | Cek gain sebelum bus nonlinear, jumlah voice aktif, release overlap dan intermodulasi |
| Drift terasa terlalu cepat/lambat | Cek Hz versus BPM, HOST/retrigger, `rate10x`, global scaling dan smoothing; ukur periodenya |
| Warna vintage hanya terasa saat lebih keras | Ulangi bypass pada level setara dan dengarkan transient/spektrum, bukan loudness |

Laporan akhir tetap memisahkan **struktur/readback**, **plugin berhasil memuat**, **render/analisis**, dan **listening aktual**. Panduan ini adalah dokumen rancangan; penulisannya tidak berarti resepnya telah diuji pada plugin atau didengarkan.

## 13. Sumber dan koreksi lampiran

Dasar teknik: lampiran pengguna *panduan_analog_sound_serum_2.md*, yang mengaitkan lima teknik dengan video Undulae Music [You can throw away your analog synths now](https://www.youtube.com/watch?v=EWrwVgzyu6U). Penanda waktu yang diberikan lampiran: [voice 0:44](https://www.youtube.com/watch?v=EWrwVgzyu6U&t=44s), [noise FM 3:10](https://www.youtube.com/watch?v=EWrwVgzyu6U&t=190s), [S&H 4:47](https://www.youtube.com/watch?v=EWrwVgzyu6U&t=287s), [noise modulation 5:44](https://www.youtube.com/watch?v=EWrwVgzyu6U&t=344s), [drive 7:09](https://www.youtube.com/watch?v=EWrwVgzyu6U&t=429s). **Video/transkrip tidak berhasil diakses saat penyusunan; judul, kanal, urutan dan timestamp tersebut berasal dari lampiran, belum diverifikasi langsung.**

Perilaku kontrol diperiksa terhadap *Serum 2 User Guide* yang tersedia lokal, plugin 2.0.18/manual 1.0.3: phase pp. 41–44; warp/LPF/FM pp. 49–55; filter/routing pp. 133–151; distortion pp. 167–168; envelope pp. 183–187; LFO pp. 191–193; audio mod source p. 208; Matrix pp. 209–214; voicing pp. 215–218; Voice Control pp. 316–318. Lihat [indeks sumber](sources.md) untuk provenance. Rancangan dan angka tambahan ditulis untuk panduan ini, bukan kutipan atau hasil ukur dari manual/video.

Rujukan primer gear dan konteks:

- [Roland JUNO-106 owner's manual](https://cdn.roland.com/assets/media/pdf/JUNO-106_OM.pdf): enam voice dan DCO dengan pitch stabil; [artikel teknis Roland](https://www.roland.com/uk/blog/roland-icon-series-juno-106-synthesizer/) menerangkan sumber DCO dan peran chorus. Ini mendasari pemisahan pendekatan DCO dari drift VCO.
- [Sequential Prophet-6 operation manual](https://www.sequential.com/wp-content/uploads/2019/03/Prophet-6-Operation-Manual.pdf): pan spread per voice. Pemakaian pola pan pada Serum adalah pendekatan rancangan, bukan bukti alokasi voice identik.
- [Moog Minimoog Model D manual](https://api.moogmusic.com/sites/default/files/2018-01/Minimoog_Model_D_Manual.pdf): jalur oscillator/mixer, ladder low-pass 24 dB/oct dan kontrol envelope/key tracking. Contoh Serum di sini tidak mengklaim simulasi rangkaiannya.
- [Halaman resmi Serum 2](https://xferrecords.com/products/serum-2): konteks oscillator dan routing produk. Detail UI panduan ini menggunakan versi manual yang disebut di atas; cocokkan dengan versi terpasang.

Koreksi utama dari lampiran: sequence Voice Control bukan batas polyphony; tidak semua gear analog memakai voice chips terintegrasi; RAND fase bukan pitch drift; random antar note berbeda dari drift kontinu; noise FM bukan model universal VCO/tape; saw digital tidak otomatis kaku karena simetri; urutan drive/filter harus eksplisit; clipping diperbaiki di tahap penyebabnya; kompresi, stereo noise, tape dan reverb eksternal merupakan pilihan sesuai target.
