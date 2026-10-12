# Penilaian musikal — Afterglow Circuit

Audit berdasarkan event MIDI dan rancangan aransemen. Audio belum didengarkan.

- Harmoni: Fm9–Dbmaj9–Abmaj9–Ebadd9, dua bar per chord, voicing bergerak dekat; semua instrumen bernada berada dalam F natural minor. Dua bar terakhir kembali ke tonic.
- Register: bass MIDI 25–44; chord/pad menengah; arp dan lead di atas. Bass, arp dan lead diperiksa monofonik; chord/pad memang polifonik.
- Groove: kick four-on-the-floor, clap beat 2/4, open hat offbeat, closed hat dengan aksen ringan, ride hadir di puncak drop. Bass offbeat menyisakan ruang bagi kick.
- Tema: motif lead orisinal delapan bar mengikuti progression. Drop pertama membuka dengan chord/arp, lead masuk setelah delapan bar; final drop memberi hook langsung dan register arp lebih tinggi menjelang puncak.
- Bentuk: intro 16 bar, groove 16, theme 16, breakdown 16, build 8, drop 24, interlude 16, build 8, final drop 24, outro 16.
- Build: snare dipercepat dari not 1/8 ke 1/16 lalu 1/32; velocity naik. Kick/bass dihilangkan pada dua bar terakhir dan satu beat hening tepat sebelum kedua drop.
- Frase/dinamika: lead mempunyai jeda di akhir kalimat empat bar; breakdown memberi nada panjang; outro mengurangi jumlah layer, velocity dan densitas arp; tonic penutup dibiarkan berbunyi.
- Sound: arah saw chord, plucked arp, sub bass dan pad ditentukan melalui instrumen DAW. Sweeps filter dan efek pumping perlu automation/sidechain DAW; audit tidak mengklaim bunyi efek tersebut sudah dirender.

## Layer dan register

| Layer | Nada | Pitch MIDI min–max | Velocity min–max |
| --- | ---: | --- | --- |
| Electronic kick | 493 | 36–36 | 96–116 |
| Electronic clap | 200 | 39–39 | 83–101 |
| Snare build and fills | 264 | 38–38 | 38–98 |
| Closed hi-hat | 1170 | 42–42 | 36–74 |
| Open hi-hat | 414 | 46–46 | 75–82 |
| Ride cymbal | 96 | 51–51 | 47–63 |
| Shaker / maracas | 432 | 70–70 | 31–48 |
| Deep mono synth bass | 429 | 25–44 | 61–101 |
| Wide saw poly synth | 1616 | 53–79 | 52–104 |
| Plucked synth arpeggio | 2100 | 63–80 | 58–92 |
| Warm atmospheric pad | 400 | 49–67 | 37–59 |
| Melodic saw lead | 209 | 72–84 | 51–91 |

## Densitas per bagian

| Bagian | Bar (1-based) | Nada drum | Nada instrumen bernada |
| --- | --- | ---: | ---: |
| Intro | 1–16 | 96 | 200 |
| Groove | 17–32 | 272 | 424 |
| Theme | 33–48 | 454 | 648 |
| Breakdown | 49–64 | 16 | 212 |
| Build 1 | 65–72 | 280 | 292 |
| Drop 1 | 73–96 | 713 | 1018 |
| Interlude | 97–112 | 16 | 228 |
| Build 2 | 113–120 | 280 | 292 |
| Final drop | 121–144 | 745 | 1118 |
| Outro | 145–160 | 197 | 322 |

Audit event lulus: scale, batas timeline, pitch overlap, monofoni bass/arp/lead, gap sebelum drop, dan keberadaan nada tiap layer.
