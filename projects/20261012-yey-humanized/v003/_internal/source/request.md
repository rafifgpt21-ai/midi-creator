# Yey — tiga piano stereo, v003

- Revisi asal: v002, tanpa mengubah atau menimpa revisi itu.
- Tanggal: 2026-10-15.

## Permintaan asli

> di projek ini, tulis ulang hanya part pianonya, saya ingin menggunakan 3 piano, piano center, piano left dan piano righ
> ini di stereo placement akan ditempatkan sesuai namanya, tulis ulang ini dengan memanfaatkan 3 layer piano berbeda dengan permainan yang berbeda antara ketinganya tapi saling melengkapi dan terdengar harmonis dan memanfaatkan stereoplacement untuk effek yang megah tanpa merubah struktur chord dan lagu
>
> gunakan skill yang menurutmu sesuai
> gunakan skill skill dari music-composition-skills

## Keputusan musik

- 120 BPM, 4/4, 76 bar / 152 detik, 480 PPQN; F# Dorian dengan D natural pada D6.
- Seluruh timeline chord dan slash bass, bagian, empat bar pembuka kosong, serta B/D# terakhir dikunci dari v002.
- Center: fondasi bass dan tiga suara chord dengan upper contour yang terhubung; serangan jarang, touch utama. Register bass dipindahkan naik saat BBC bass masuk.
- Left: broken chord register menengah, figur naik-turun dengan aksen lembut. Tidak membawa sub-bass ke sisi kiri.
- Right: jawaban melodis lebih tinggi, lebih pendek dan jarang daripada figur left; onset saling mengisi, bukan salinan atau delay.
- Center / left / right memakai CC10 64 / 20 / 108; kira-kira center / L69 / R70. Piano samping lebih tenang daripada center.
- Bars 13–16 lebih lapang; bars 49–52 dan 57–60 lebih terbuka; bars 33–48 dan 61–72 menahan aktivitas di bawah cello; bars 73–76 mengurangi figur dan touch.
- Piano right mengosongkan bar berisi flute atau clarinet dan bar awal tema cello. Semua piano baru tetap chord tone sepanjang gate; tidak ada reharmonisasi, anticipatory chord, swing, atau offset acak.
- Timing strict 1/32 dipertahankan; permainan baru memakai grid straight 1/8, ekspresi melalui velocity dan gate.
- Keenam layer BBC dipertahankan identik: nada, timing, velocity, CC, program hint, volume, pan, dan byte MIDI.

| Layer ID | Instrumen | Fungsi | GM hint |
| --- | --- | --- | --- |
| piano-center | Piano akustik pilihan pengguna | Fondasi dan upper contour | 0 |
| piano-left | Instance piano akustik terpisah | Broken-chord accompaniment | 0 |
| piano-right | Instance piano akustik terpisah | Jawaban tinggi / ruang stereo | 0 |

## Asumsi dan referensi

Lanjutkan pengecualian piano akustik pilihan pengguna yang tercatat pada v001/v002; jangan menggantinya dengan sintesis piano Serum. Ketiga part dapat memakai tiga instance patch piano yang sama; perbedaan utamanya ada pada permainan, register, touch, dan posisi. Tidak membuat sound atau preset baru, audio, combined MIDI, drum, atau proyek Cubase.

Sumber kebenaran asal: `v002/_internal/composition.json`, `v002/_internal/source/performance-design.json`, dan sumber MIDI asli di `_internal/references/yey.mid`. Script mencari root proyek dari lokasi dirinya, sehingga tetap dapat dijalankan setelah publikasi. Tidak memakai randomness atau seed.

Skill dari music-composition-skills: mc-workflow (intent dan self-audit), mc-harmony (identitas chord/inversi), mc-counterpoint (ritme dan arah yang saling mengisi), mc-orchestration dan referensi piano (register/touch/gate), mc-texture-layering (pemisahan register dan pengurangan di bawah tema), mc-mix-intent (center/left/right dan kedalaman konsisten), mc-development (motif dan variasi antarbagian), mc-symbolic-score (ekspor deterministik), mc-ai-tell-audit (audit akhir simbolik). Panduan workspace dan permintaan mempertahankan chord/form mengalahkan saran generik untuk reharmonisasi, perubahan bentuk atau onset jitter.

## Kriteria penerimaan

- Sembilan MIDI terpisah, masing-masing satu track SMF-1, 145920 ticks; tepat tiga piano mengganti piano v002.
- Validate, generate, verify exit 0 dan ok:true.
- Keenam layer non-piano identik spesifikasi dan byte MIDI terhadap v002.
- 72 bar piano mempunyai chord pitch-class lengkap yang sama, lowest piano pitch sesuai bass/inversi; tidak ada gate ke chord yang tidak mendukung.
- Onset side piano berbeda dan tidak serempak; ada pengurangan densitas saat tema dan penutup.
- README menautkan semua MIDI, menjelaskan penggantian piano saja, pan di Cubase, patch manual, dan pemisahan verifikasi MIDI dari playback/listening aktual.
