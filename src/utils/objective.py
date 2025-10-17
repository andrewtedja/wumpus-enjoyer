
from collections import defaultdict

'''
> NOTES
# state -> dict { (hari, jam, ruangan): kelas }
# data -> dict { "kelas_mata_kuliah": [...], "ruangan": [...], "mahasiswa": [...] }

OBJ FUNCTION: 
- Bentrok Mahasiswa (mahasiswa punya >= 2 matkul di jam & hari yg sama)

- Bentrok Ruangan (>= 2 matkul di ruangan & waktu yg sama)
asumsi slot = jam,hari,ruangan sama

- Overcapacity Ruangan (jumlah mahasiswa > kuota ruangan)
asumsi slot = jam,hari,ruangan sama
'''
# Factor 1 - mhs punya 2+ kelas di waktu sama
def get_bentrok_mahasiswa(state, data) -> int:
    score = 0
    for mhs in data["mahasiswa"]:
        jadwal = defaultdict(list)
        for (hari, jam, ruang), kode in state.items():
            if kode in mhs["daftar_mk"]:
                jadwal[(hari, jam)].append(kode)
        # 1 mahasiswa punya 2+ kelas di waktu sama -> penalti
        for slot, kelas in jadwal.items():
            if len(kelas) > 1:
                score += len(kelas) - 1
    return score

# Factor 2 - bentrok state, itung weighted priority
# default weight = 1
PRIO_WEIGHT = {
                1: 1.75,
                2: 1.5,
                3: 1.25
            }

def get_bentrok_ruangan_berbobot(state, data) -> float:
    score = 0.0
    # group by (hari, jam, ruang)
    slot_dict = defaultdict(list)
    for (hari, jam, ruang), kode in state.items():
        slot_dict[(hari, jam, ruang)].append(kode)

    for (hari, jam, ruang), kelas_list in slot_dict.items():
        if len(kelas_list) <= 1:
            continue
        # if lebih dari 1 kelas di slot sama -> hitung weight prioritas
        for kelas in kelas_list:
            for mhs in data["mahasiswa"]:
                for mk, prio in zip(mhs["daftar_mk"], mhs["prioritas"]):
                    if mk == kelas:
                        score += PRIO_WEIGHT.get(prio, 1.0)
    return score

# Factor 3 - jml mhs > kuota
def get_overcapacity(state, data) -> int:
    score = 0
    kuota_ruang = {r["kode"]: r["kuota"] for r in data["ruangan"]}
    info_kelas = {k["kode"]: k for k in data["kelas_mata_kuliah"]}

    for (hari, jam, ruang), kode in state.items():
        jmhs = info_kelas[kode]["jumlah_mahasiswa"]
        cap = kuota_ruang[ruang]
        if jmhs > cap:
            score += (jmhs - cap) * info_kelas[kode]["sks"]
    return score

# ===================== DOSEN =====================

def get_bentrok_dosen(state, data) -> int:
    score = 0
    if "dosen" not in data:
        return 0

    dosen_blocks = {d["nama"]: d.get("waktu_sibuk", []) for d in data["dosen"]}
    dosen_map = {kode: d["nama"] for d in data["dosen"] for kode in d.get("mengajar", [])}

    for (hari, jam, ruang), kode in state.items():
        dosen = dosen_map.get(kode)
        if not dosen:
            continue

        for block in dosen_blocks.get(dosen, []):
            if block["hari"] == hari and jam in block["jam"]:
                score += 5 
                break  
    return score


# ===================== TOTAL SCORE =====================
def evaluate(state, data) -> int:
    f1 = get_bentrok_mahasiswa(state, data)
    f2 = get_bentrok_ruangan_berbobot(state, data)
    f3 = get_overcapacity(state, data)
    f4 = get_bentrok_dosen(state, data)
    total = f1 + f2 + f3 + f4

    # print(f"[DEBUG] f1={f1}, f2={f2}, f3={f3}, f4={f4}, total={total}")
    return total