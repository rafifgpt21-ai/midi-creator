"""Complete producer documentation and audit the exported arrangement."""
from pathlib import Path
import json
import math
import re
import mido
from midi_creator.export import verify_export
from midi_creator.spec import compile_composition

HERE=Path(__file__).resolve().parent
PROJECT=next(p for p in HERE.parents if p.name=="20261014-the-lantern-gate")
OUT=PROJECT/"v001"
SOURCE=json.loads((HERE/"composition.json").read_text(encoding="utf-8"))
BINDINGS=json.loads((HERE/"bbcso-bindings.json").read_text(encoding="utf-8"))
COMP=compile_composition(SOURCE)
REPORT=verify_export(OUT)
assert REPORT["ok"] and REPORT["timing"]["on_grid"]

SECTIONS=[("Whispering Lanterns",1,12,"fragment",2,
    "Harp dan viola membuka ruang; flute masuk bar 5, oboe menjawab bar 9."),
    ("The Hidden Path",13,16,"new",4,"Tema lengkap pada flute, lalu oboe; pizzicato memberi langkah ringan."),
    ("The Quest",29,16,"vary",6,"Tema pindah ke Violins 1; ostinato masuk bertahap, horn muncul bar 39."),
    ("Sanctuary",45,10,"vary",2,"Brass, percussion, dan short strings keluar; clarinet, harp, viola, cello mengisi ruang."),
    ("The Gate Awakens",55,16,"fragment",7,"Tema kembali pada strings lalu horn; tremolo, flute pendek dan roll membangun antisipasi."),
    ("Banner of Dawn",71,16,"recap",9,"Tema heroik pada violin/horn; trumpet mengambil alih paruh kedua, low brass dan drum bergabung."),
    ("The Lantern Gate",87,8,"extend",10,"Tema diperlebar; puncak B6 lalu final D minor tutti pada bar 93."),
    ("Hall Release",95,2,"contract",0,"Tidak ada serangan nada baru; ruang release sekitar 3,3 detik."),
]


def pitch_name(p):
    return ["C","C#","D","D#","E","F","F#","G","G#","A","Bb","B"][p%12]+str(p//12-1)


rows=[]
stats=[]
for raw,layer in zip(SOURCE["layers"],COMP.layers):
    binding=BINDINGS[layer.id]
    lo=min(n.pitch for n in layer.notes); hi=max(n.pitch for n in layer.notes)
    first=min(n.start for n in layer.notes)/COMP.ppqn/3+1
    last=max(n.end for n in layer.notes)/COMP.ppqn/3+1
    controls={c: [e.value for e in layer.control_changes if e.control==c] for c in [1,11]}
    stats.append(dict(id=layer.id,patch=binding["patch"],articulation=binding["articulation"],
        first_bar=first,last_note_off_bar=last,pitch_min=lo,pitch_max=hi,
        velocity_min=min(n.velocity for n in layer.notes),velocity_max=max(n.velocity for n in layer.notes),
        cc1_range=[min(controls[1]),max(controls[1])],cc11_range=[min(controls[11]),max(controls[11])],
        note_count=len(layer.notes),cc_events=len(layer.control_changes)))
    rows.append(f'| {layer.name} | {binding["patch"]} | {binding["articulation"]} | '
        f'[{layer.id}.mid](MIDI/{layer.id}.mid) | {pitch_name(lo)}–{pitch_name(hi)} ({lo}–{hi}) | {math.floor(first)} | {raw["role"]} |')

section_stats=[]
for name,start,bars,development,energy,_ in SECTIONS:
    a=(start-1)*3*COMP.ppqn;b=a+bars*3*COMP.ppqn
    notes=[n for layer in COMP.layers for n in layer.notes if a<=n.start<b]
    active=[layer.id for layer in COMP.layers if any(n.start<b and n.end>a for n in layer.notes)]
    section_stats.append(dict(section=name,start_bar=start,bars=bars,development=development,
        intended_energy=energy,note_on_count=len(notes),active_layers=len(active),
        median_velocity=sorted(n.velocity for n in notes)[len(notes)//2] if notes else None))
assert section_stats[3]["active_layers"] < section_stats[2]["active_layers"]
assert section_stats[5]["active_layers"] > section_stats[1]["active_layers"]
assert section_stats[-1]["note_on_count"]==0
assert all(n.pitch%12 in {0,2,4,5,7,9,11} for layer in COMP.layers if layer.kind!="drums" for n in layer.notes)
assert all(n.pitch%12 in {2,5,9} for layer in COMP.layers if layer.kind!="drums"
           for n in layer.notes if n.start==276*COMP.ppqn)
assert all(c.start<=COMP.end_tick for layer in COMP.layers for c in layer.control_changes)

AUDIT=dict(structural=REPORT["ok"],on_grid=REPORT["timing"]["on_grid"],
    mode="D Dorian",all_pitched_notes_in_mode=True,final_tonic="D minor",
    all_final_downbeat_pitched_notes_in_tonic=True,seed=20261014,
    layers=stats,sections=section_stats,
    musical_review={
        "motif":"D-E-F / A-G-F-E; G-B-A-G emphasizes the natural sixth. Variants preserve this contour.",
        "register":"Written pitches are concert/sounding MIDI pitches; no transposition applied to winds, brass, piccolo or basses.",
        "voice_leading":"Long inner voices use nearby chord tones; open low voicing; no dense low triads. D pedal retains modal centre.",
        "phrasing":"Long melodic pitches are connected with short note-off gaps. Breaths at phrase ends; no claim of sampled legato.",
        "articulation":"35 fixed-articulation instances. String Long plus short layers can imply divisi; mix down the supporting layers.",
        "dynamic_arc":"Quiet opening, growing quest, 10-bar retreat, rebuild, heroic recap, expanded final arrival.",
        "percussion":"Phrased 6/8 accents, irregular fills at 68/70/78/85/92; no persistent pop backbeat; sparse piatti.",
        "timing":"Strict 1/16 note-on grid, CC sampling at 1/32; velocity/gate shaping instead of timing jitter.",
        "library_limits":"Discover has one dynamic sample layer and no true legato/round robins. CC dynamics adjust level; realism is constrained by the library.",
    },
    verification_status={"midi_structure":"passed","cc_readback":"passed", "bbcso_patch_loading":"not tested",
        "percussion_plugin_trigger":"not tested live; documented map and local C4 preference used",
        "cubase_import":"not tested live","audio_render":"not requested/not performed","actual_listening":"not performed"})
(OUT/"_internal/musical-audit.json").write_text(json.dumps(AUDIT,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

readme="""# The Lantern Gate

Aransemen orkestra fantasy menuju final epic, dibuat untuk **BBC Symphony Orchestra Discover (gratis)**. **35 MIDI terpisah**, satu instrumen dan satu artikulasi tetap per track. Buat satu instance BBCSO untuk setiap baris tabel di bawah.

**Tempo:** 108 BPM quarter note · **Meter:** 6/8 (rasa dua pulsa, dotted-quarter = 72) · **Mode:** D Dorian — D E F G A B C · **Panjang:** 96 bar / 2:40 · **Resolusi:** 960 PPQN.

## Mulai di Cubase

1. Buat project dengan tempo **108 BPM**, meter **6/8**, dan instrument track pada **Musical Time Base**. Semua MIDI harus mulai pada **1.1.1.0**, meskipun not pertama baru muncul belakangan.
2. Muat **BBC Symphony Orchestra**, pilih mode **Discover**, lalu pilih instrumen dan artikulasi dari tabel. Nama browser mungkin memakai prefiks “Discover -”. Pilih hanya satu artikulasi; jangan Shift-select beberapa teknik sekaligus. Kunci Technique Selector bila diperlukan.
3. Buat satu instance/track khusus per artikulasi, termasuk instrument yang sama: Violins 2 Long, Spiccato dan Pizzicato adalah tiga track terpisah. Tidak ada keyswitch atau pergantian program dalam MIDI.
4. Gunakan **File > Import > MIDI File**, left locator **1.1.1.0**, **Import to Left Locator**. Dengan tempo project sudah benar, **Ignore Master Track Events on Merge** mempertahankan tempo project. Untuk drag-and-drop, **Import Dropped File as Single Part**, lalu tempatkan setiap part pada bar 1. Pertahankan keheningan awal.
5. MIDI melodic menggunakan channel **1**; Untuned Percussion menggunakan channel **10**. Set MIDI channel BBCSO ke **All** atau channel yang sesuai. Instance percussion juga terpisah per baris agar dinamika dan pan independen.
6. Pertahankan **CC1 Dynamics** dan **CC11 Expression** saat impor. Dengan mapping default BBCSO, kurva ini membentuk swell dan frase. Pada preset Long gunakan respons velocity normal; hindari velocity-to-dynamics yang menimpa kurva CC1. Periksa lane CC1/CC11 di Key Editor.
7. File juga membawa level awal **CC7** dan pan **CC10** yang moderat. BBCSO memiliki posisi panggung dalam sampel; pan MIDI di sini hanya tambahan kecil. Jika Anda memakai pan/gain mixer sendiri, filter CC7/CC10 sesuai kebutuhan, sambil mempertahankan CC1/CC11.

## Track, patch, dan MIDI

Rentang memakai **C4 = MIDI 60**. Cubase biasanya menamai MIDI 60 sebagai C3; angka MIDI pada tabel tetap otoritatif. Semua pitch sudah berupa concert/sounding pitch: jangan transposisi tambahan untuk clarinet, horns, piccolo, atau double bass.

| Track | Patch BBCSO Discover | Artikulasi tetap | MIDI | Rentang aktual | Masuk bar | Fungsi |
| --- | --- | --- | --- | --- | --- | --- |
"""+"\n".join(rows)+"""

Long dipakai untuk garis menyambung dengan gate hampir penuh dan swell, bukan patch Legato yang tidak tersedia di Discover. Spiccato adalah nama teknik short strings di Discover; woodwind/brass pendek memakai Staccatissimo. Timpani dan snare roll cepat di part Hits ditulis sebagai pukulan ulang, bukan sebagai pergantian ke mode Rolls. Suspended Cymbal Roll mendapat track khusus dan trigger khusus.

Saat Long dan short strings dari seksi yang sama berjalan bersamaan, perlakukan sebagai pembagian fungsi/divisi secara musikal. Sampel Discover tetap merupakan seksi penuh: turunkan level short/harmony pendukung bila keseimbangan terdengar terlalu besar.

## Bentuk lagu

| Bar | Waktu mulai | Bagian | Perkembangan |
| --- | --- | --- | --- |
"""
for name,start,bars,_,_,detail in SECTIONS:
    seconds=(start-1)*3/108*60
    readme+=f'| {start}–{start+bars-1} | {int(seconds)//60}:{int(seconds)%60:02d} | {name} | {detail} |\n'
readme+="""

Harmoni menggunakan Dm/add9/6, G, F, C, Am/Am7 dan Em7, dengan inversion dan pedal D. **B natural** pada G dan Dm6 mempertahankan warna Dorian; tidak ada Bb atau C# yang menggeser ke natural/harmonic minor. Kecepatan ganti harmoni berubah dari dua/empat bar menjadi per bar; tema juga berpindah register dan instrumen. Final kembali ke **D minor pada bar 93**, ditahan hampir dua bar, lalu bar 95–96 memberi ruang release. Penutup musikal tetap besar; ruang akhir bukan fade-out yang panjang.

## Percussion yang dipakai

Semua memakai patch bawaan pilihan Anda: **BBCSO Discover**, bukan kit GM atau Cubase Sampler. **Jangan remap semua pitch ke MIDI 60.** Load **Untuned Percussion** untuk baris drum/cymbal/triangle; load **Timpani** untuk track bertonal.

| Part | Pitch MIDI | Nama pada manual (C4 = 60) | Nama Cubase (C3 = 60) | Peran |
| --- | --- | --- | --- | --- |
| Bass Drum Hits | 36 | C2 | C1 | Pukulan konser dalam dan jarang; menegaskan kedatangan frase. |
| Snare Hits | 40 | E2 | E1 | March 6/8, ghost notes dan repeated-hit rolls. |
| Suspended Cymbal Hits | 41 | F2 | F1 | Satu tanda transisi lembut, bukan crash di setiap bar. |
| Suspended Cymbal Roll | 43 | G2 | G1 | Dua swell sebelum klimaks dan penutup. |
| Piatti Hits | 59 | B3 | B2 | Crash orkestral pada bar 71, 79, 87, 93. |
| Triangle Hits | 52 | E3 | E2 | Kilau kecil di pembukaan. |
| Timpani Hits | 38 / 45 | D2 / A2 | D1 / A1 | Nada D dan A; tidak memakai map Untuned Percussion. |

Mapping nama nada mengikuti [daftar resmi Untuned Percussion Discover](https://support.spitfireaudio.com/en/articles/11815993-what-are-the-untuned-percussion-instruments-used-in-bbc-so-discover). Konversi numerik memakai middle C = 60 dan preferensi lokal BBCSO `defaultMiddleCIsC4=1`; pemicu plugin belum diuji live. Pada keyboard BBCSO, pastikan pitch 36 menampilkan Bass Drum dan 40 Snare sebelum playback lengkap. Perubahan label octave di DAW tidak memerlukan transposisi file.

Timpani mengunci pulsa 3+3, bass drum memberi bobot pada batas frase, snare mengisi perkembangan tanpa backbeat pop, dan cymbal hanya memberi tanda besar. Hindari tambahan kick/hat elektronik atau compression yang menghapus kontras sanctuary–epic. Sampel sudah dipilih melalui library Anda; tidak ada file sample yang disalin.

## Dinamika dan batas Discover

Velocity berbeda menurut aksen dan tujuan frase; gate dipendekkan untuk short notes dan hampir penuh untuk Long. CC1 membentuk perkembangan besar, sedangkan CC11 memberi swell ringan dalam frase. Kedua kurva tidak memakai atenuasi dalam yang identik. Semua note-on **on-grid 1/16, straight, tanpa swing atau random timing jitter**; perubahan panjang nada dan velocity menghasilkan variasi performa.

Discover hanya memiliki satu dynamic layer, tanpa true legato atau round robins. Karena itu CC1 di Discover bertindak sebagai pengatur level tambahan; kurvanya tidak menghasilkan perubahan timbre pp–ff seperti Core/Professional. Pembagian frase, register dan orkestrasi sudah disusun untuk batas tersebut. Lihat [manual Discover, bagian controls dan Appendix B/C](https://d1t3zg51rvnesz.cloudfront.net/p/files/product-manuals/4924/1688057212/BBC%20Symphony%20Orchestra%20Discover_User%20Manual.pdf) dan [perbandingan resmi edisi](https://support.spitfireaudio.com/en/articles/11815936-which-features-are-different-between-editions-of-bbc-so).

## Instrumen eksternal dan asumsi

Semua track menggunakan **BBC Symphony Orchestra Discover by Spitfire Audio**, sesuai permintaan Anda. Alasan: sampel orkestral Anda menentukan artikulasi dan karakter permainan. Cara muat, register dan mapping ada pada tabel. Tidak diperlukan Serum, plugin tambahan, file preset, instrument Core/Professional, atau file gabungan. Harp, Celeste, Glockenspiel dan Tubular Bells memakai patch Discover bawaan; tidak perlu keyswitch maupun pedal.

Durasi, D Dorian, tempo dan meter dipilih karena tidak ditentukan secara spesifik. Penyusunan memakai seed **20261014** yang tetap. Skill yang diterapkan: `mc-workflow`, `mc-development`, `mc-melody`, `mc-harmony`, `mc-orchestration`, `mc-arrangement-arch`, dan pemeriksaan `mc-ai-tell-audit` pada struktur/performa MIDI. Pemaksaan chord di luar Dorian serta timing offset dari contoh skill dikecualikan untuk mengikuti mode dan kontrak timing workspace.

## Status verifikasi

- **Validate / generate / verify: PASS (`ok: true`).** 35 file SMF format 1, tepat satu track per file; semua 960 PPQN, 6/8, tempo 108, akhir tick **276480**, durasi **160.000128 detik** akibat pembulatan tempo MIDI.
- **1.966 nada dan 7.024 event CC1/CC11**; readback posisi/channel/controller/value sesuai spesifikasi; tidak ada stuck note atau overlap pitch yang sama. Semua 1.966 note-on on-grid.
- Audit offline: seluruh nada bertonal berada di D Dorian; serangan final bertonal membentuk D minor; register diperiksa; sanctuary mengurangi jumlah layer; klimaks memperluas register dan instrumentasi; bar release tanpa note-on baru.
- Pengujian generator: **46 tes dijalankan, 45 lulus dan 1 integrasi Serum opt-in dilewati**; contoh single-layer dan multi-layer juga diperiksa.
- **Pemuatan patch BBCSO, pemicu percussion dan impor Cubase live: belum diuji. Audio tidak dirender dan belum didengarkan melalui VST Anda.** Verifikasi struktur MIDI tidak membuktikan hasil bunyi atau keseimbangan mixing.

Semua MIDI siap diimpor dari bar 1. Bahan sumber, binding, spesifikasi, seed, laporan verifikasi dan audit berada dalam `_internal/`; folder kerja produser berisi README dan MIDI.
"""
(OUT/"README.md").write_text(readme,encoding="utf-8")
(PROJECT/"README.md").write_text("# The Lantern Gate\n\nOrkestra D Dorian untuk BBC Symphony Orchestra Discover; pembukaan fantasy dan final epic.\n\n**Revisi siap pakai terbaru: [v001 — README dan 35 MIDI](v001/README.md).**\n\n108 BPM · 6/8 · 96 bar · 2:40 · satu artikulasi tetap per track.\n",encoding="utf-8")

roster=[]
for stat,raw in zip(stats,SOURCE["layers"]):
    bind=BINDINGS[stat["id"]]
    roster.append(dict(id=stat["id"],instrument=bind["patch"]+" / "+bind["articulation"],
        midi=dict(program=raw.get("program",0),bank=0,channel=bind["channel"]),
        role=raw["role"],band=bind["family"],entry=f'bar {stat["first_bar"]:g}',
        exit=f'bar {stat["last_note_off_bar"]:.3f}',note="See authoritative composition.json and bbcso-bindings.json."))
PLAN=dict(spec_version="1.0",meta=dict(title="The Lantern Gate",style_layer="none",style_layers=[],
    fusion_note="",key="D minor",mode="dorian",meter="6/8",tempo=108,target_duration="2:40",deliverable=["midi"],
    upstream=dict(brief="request.md",lyrics={},picture={})),
    intent=dict(one_thing="Turn a small Dorian lantern motif into a heroic orchestral arrival.",
        reference_pair=[],listener_situation="Producer imports independent BBCSO Discover parts in Cubase.",
        emotional_arc=[dict(section=n,mood=d,value=e) for n,s,b,dev,e,d in SECTIONS]),
    material=dict(motif="D5-E5-F5 (1.5,.5,1 quarter beats), then A5-G5-F5-E5; G5-B5-A5-G5 carries Dorian sixth.",
        character="Curious ascending gesture that answers itself in descending steps.",stated_in=["The Hidden Path"],
        development_mode="thematic variation"),
    form=[dict(id=n,name="Intro" if s==1 else "Outro" if s>=87 else "Instrumental",bars=b,start_bar=s,
        harmony="i / IV / bIII / bVII / v / ii in D Dorian; see harmony.json for full bar map",
        harmony_letters="Dm / G / F / C / Am / Em7; Dmadd9 and Dm6; see harmony.json",
        melody_register="high" if s>=71 else "middle-high" if s!=45 else "middle",
        development=dev,energy=e,events=[],note=d) for n,s,b,dev,e,d in SECTIONS],
    arrangement=dict(roster=roster,depth_map={r["id"]:"foreground" if r["role"].startswith("tema") else "support" for r in roster},
        bass_kick_relation=dict(mode="combined accents",detail="D/A timpani and sparse concert bass drum articulate large phrases."),
        spectrum_budget=[],energy_curve={n:e for n,s,b,dev,e,d in SECTIONS},
        subtraction_events=[dict(at=dict(section="Sanctuary",bar_offset=0),what="Remove brass, short strings, basses and percussion",why="Expose clarinet/harp and rebuild contrast.")],
        hooks=dict(vocal_hook={},arrangement_hook=dict(what="D-E-F to A, answered by descending steps and natural-sixth B",first_at="bar 5 fragment",recurs_at=[13,29,55,71,87])),
        groove=dict(feel="straight",push_pull=[dict(part="all",offset_ms=0,note="Workspace requires strict on-grid.")],
            fill_policy=dict(bars=[68,70,78,85,92],rationale="Phrase arrivals rather than every four bars."))),
    vocal={},mix_intent=dict(mood="Intimate lantern light opening into broad heroic arrival.",
        sound_stage=[dict(id=r["id"],pan=round((raw["pan"]-64)/63*100),depth="support") for r,raw in zip(roster,SOURCE["layers"])],
        dynamics=dict(notes=["Sanctuary withdraws layers; preserve this contrast."],target_DR_dB=None),
        width_map={"Whispering Lanterns":"small occupied stage","Banner of Dawn":"full occupied stage"},
        loudness_target="No audio mastering requested"),
    render=dict(midi=dict(instrument_map=BINDINGS)),
    checks=dict(self_audit=["Dorian note inventory and final tonic checked", "Unequal section lengths and subtractive sanctuary", "35 fixed articulation parts", "Theme recap and expanded final six-bar arc", "Actual audio/listening still untested"],
        exemptions=["No borrowed reference works: original brief without an audio reference.",
            "No out-of-mode chord: user specifically requests Dorian throughout.",
            "No onset push/pull: strict timing contract; variation through gates/velocity/CC.",
            "No vocals/Suno/audio: MIDI-only request.",
            "Peak deliberately near the ending: user specifically requests an epic ending.",
            "Plan is a descriptive MIDI handoff; repo composition schema remains authoritative."]),messages=[])
(HERE/"arrangement-plan.json").write_text(json.dumps(PLAN,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")

request="""# Brief komposisi

- Proyek: The Lantern Gate / 20261014-the-lantern-gate
- Revisi: v001
- Revisi asal: komposisi baru
- Tanggal: 2026-10-14

## Permintaan asli

“buatkan musik orchestra yang terdengar dinamic dan natural; gunakan dorian mode untuk musiknya, vibe nya fantasy di awal dan di akhir terdengar epic; saya menggunakan BBC Symphony Orchestra sebagai VST, kamu tinggal buat midi per track nya saja.”

Pengguna memberi kategori Strings, Woodwinds, Brass, Percussion & Keyboards serta contoh instrumen/artikulasi. Klarifikasi: **versi gratis (Discover)**. “jika ingin menggunakan mode berbeda dari instrumen yang sama, buat track khusus untuk mode berbeda.” Instruksi tambahan: “gunakan skill yang tersedia dan yang cocok.”

## Keputusan musik

- Gaya/mood: fantasy orkestra, kemudian heroik, dengan sanctuary yang tenang di tengah.
- Tempo quarter-note: 108 BPM. Meter: 6/8, dotted-quarter 72.
- Pusat tonal: D Dorian (D E F G A B C). Final D minor.
- Panjang: 96 bar, sekitar 160 detik; 94 bar musik dan 2 bar release.
- Bentuk: intro 12 / tema 16 / quest 16 / sanctuary 10 / ascent 16 / epic recap 16 / coda 8 / release 2.
- Harmoni: chord modal, inversion dekat dan pedal D; ganti harmoni dua/empat bar maupun per bar. B natural menegaskan sixth Dorian.
- Natural: rests/breaths, aksen, variasi velocity/gate, smooth CC1/CC11, handoff instrumen, rentang konser yang wajar. Tanpa random onset jitter/swing, sesuai kontrak timing.
- Plugin: BBC Symphony Orchestra Discover, semua 35 instrumen-artikulasi memakai instance terpisah; lihat bbcso-bindings.json dan README.
- Drum: Discover Untuned Percussion; numeric 36 Bass Drum, 40 Snare, 41 Sus Cymbal Hit, 43 Sus Cymbal Roll, 59 Piatti, 52 Triangle. Timpani Hits bertonal 38/45 pada patch sendiri. Mapping merujuk manual; middle C lokal = C4/MIDI60; live trigger belum diuji.

## Asumsi dan referensi

Durasi/tempo/key/meter dipilih agent. Harp dan Celeste tersedia pada Discover menurut manual. Tidak memakai Legato, Marcato, Col Legno atau solo winds Core/Professional. Long digunakan untuk garis connected tanpa mengklaim sampled legato. Long+short seksi strings dapat berjalan sebagai fungsi divisi; README menjelaskan dampak full-section samples.

Skill: mc-workflow, mc-development, mc-melody, mc-harmony, mc-orchestration, mc-arrangement-arch, mc-ai-tell-audit. Internal arrangement-plan.json mencatat motif, perkembangan, roster, arc serta alasan pengecualian chromatic chords/timing offsets. composition.json tetap sumber nada/CC yang otoritatif.

Seed 20261014; build_composition.py mereproduksi nada, velocity, gate dan CC. Gate retrigger harp diselesaikan sebelum ekspor, disimpan di gate-adjustments.json. Generator ditambah field CC1/CC11 untuk memenuhi dinamika Long; schema, compiler, render, readback, dokumentasi serta tes diubah bersama. 46 tes: 45 passed, 1 opt-in Serum skipped; single/multi-layer examples covered.

Sumber primer: manual Discover Appendix B/C, artikel Spitfire tentang perbedaan edisi dan map Untuned Percussion. Tautan ada di README. Tidak ada karya musik atau audio pengguna yang ditiru.

## Perubahan revisi

Komposisi baru, belum ada revisi asal; proyek pengguna lain dan revisi lama dipertahankan.

## Kriteria penerimaan dan hasil

- 35 MIDI dengan satu track format 1/instrumen-artikulasi per file; tanpa combined atau preset/audio sesuai request.
- 108 BPM, 6/8, 960 PPQN, EOT tick 276480 sama; semua posisi awal global tetap bar 1.
- Validate, generate, verify PASS; on_grid true.
- Readback 1.966 nada, 7.024 CC sesuai komposisi; tidak ada note stuck/overlap pitch sama.
- Seluruh nada bertonal dalam D Dorian; final D minor; retreat tengah dan epic final diperiksa pada data komposisi.
- Output: v001/README.md, v001/MIDI/*.mid.
- Pemuatan patch, live Cubase import, render dan actual listening: belum dilakukan; tidak diklaim.
"""
(HERE/"request.md").write_text(request,encoding="utf-8")
for target in re.findall(r'\]\(([^)]+)\)',readme):
    if not target.startswith("https://"):
        assert (OUT/target).is_file(),target
assert {p.name for p in OUT.iterdir()}=={"README.md","MIDI","_internal"}
(OUT/"_internal/final-verification.json").write_text(json.dumps(REPORT,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print(json.dumps(dict(ok=True,midi_files=len(COMP.layers),notes=sum(len(l.notes) for l in COMP.layers),
    cc_events=sum(len(l.control_changes) for l in COMP.layers),duration=COMP.seconds,
    sections=section_stats),indent=2))
