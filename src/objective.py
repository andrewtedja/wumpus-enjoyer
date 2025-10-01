
from collections import defaultdict

'''
> NOTES
# state -> dict { (hari, jam, ruangan): kelas }
# data -> dict { "kelas_mata_kuliah": [...], "ruangan": [...], "mahasiswa": [...] }

OBJ FUNCTION: 
- Bentrok Mahasiswa (mahasiswa punya >= 2 matkul di jam & hari yg sama)
asumsi 2 bentrok = +2 score

- Bentrok Ruangan (>= 2 matkul di ruangan & waktu yg sama)
asumsi slot = jam,hari,ruangan sama
1 slot ada N kode matkul -> score += N

- Overcapacity Ruangan (jumlah mahasiswa > kuota ruangan)
asumsi slot = jam,hari,ruangan sama
jika jumlah mahasiswa>kuota -> score += (jumlah mahasiswa - kuota) * sks
'''

def get_bentrok_mahasiswa(state, data) -> int:
    score = 0

    for mahasiswa in data["mahasiswa"]:
        jadwal_mahasiswa = defaultdict(list)
        for mk in mahasiswa["daftar_mk"]:
            for (hari, jam, ruang), kode in state.items():
                if kode == mk:
                    jadwal_mahasiswa[(hari, jam)].append(kode)

        for slot, kelas in jadwal_mahasiswa.items():
            if len(kelas) > 1:
                score += len(kelas)

    return score


def get_bentrok_ruangan(state) -> int:
    score = 0
    slot_counter = defaultdict(list)
    for (hari, jam, ruang), kode in state.items():
        slot_counter[(hari, jam, ruang)].append(kode)
    for slot, kelas in slot_counter.items():
        if len(kelas) > 1:
            score += len(kelas)

    return score

def get_overcapacity(state, data) -> int:
    score = 0

    kelas_mata_kuliah = data["kelas_mata_kuliah"]
    ruangan_dict = {ruang["kode"]: ruang["kuota"] for ruang in data["ruangan"]}

    for (hari, jam, ruang), kode in state.items():
        for kelas in kelas_mata_kuliah:
            if kelas["kode"] == kode:
                kapasitas = ruangan_dict[ruang]
                if kelas["jumlah_mahasiswa"] > kapasitas:

                    # print(f"[DEBUG OVERCAP] ", kelas["jumlah_mahasiswa"], ">", kapasitas)
                    score += (kelas["jumlah_mahasiswa"] - kapasitas) * kelas["sks"]

    return score

# ===================== TOTAL SCORE =====================
def evaluate(state, data) -> int:
    print("[DEBUG] bentrok mahasiswa:", get_bentrok_mahasiswa(state, data))
    print("[DEBUG] bentrok ruangan:", get_bentrok_ruangan(state))
    print("[DEBUG] overcap:", get_overcapacity(state, data))

    return (get_bentrok_mahasiswa(state, data) + get_bentrok_ruangan(state) + get_overcapacity(state, data))