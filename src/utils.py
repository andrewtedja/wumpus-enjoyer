from typing import List, Dict, Tuple, Any
from state import init_state, get_empty_slots, generate_slots, hari_list, jam_list

def get_slots(state: Dict[Tuple[str,int,str], str], kode: str) -> List[Tuple[str,int,str]]:
    slots = [slot for slot, k in state.items() if k == kode]
    hari_index = {h: i for i, h in enumerate(hari_list)}
    slots.sort(key=lambda s: (hari_index[s[0]], s[1], s[2]))
    return slots

def find_initial_position(slots_all: List[Tuple[str,int,str]],
                               state: Dict[Tuple[str,int,str], str],
                               sks: int) -> List[Tuple[str,int,str]]:
    used = set(state.keys())
    valid_starts = []
    max_jam = max(jam_list)
    for hari, jam, ruang in slots_all:
        if jam + sks - 1 > max_jam:
            continue
        ok = True
        for offset in range(sks):
            slot = (hari, jam + offset, ruang)
            if slot in used:
                ok = False
                break
        if ok:
            valid_starts.append((hari, jam, ruang))
    return valid_starts

def is_valid_duration(state, data):
    kelas_dict = {k["kode"]: k["sks"] for k in data["kelas_mata_kuliah"]}
    for kode, sks in kelas_dict.items():
        slots = [s for s, v in state.items() if v == kode]
        if not slots:
            return False
        hari = {s[0] for s in slots}
        ruang = {s[2] for s in slots}
        jam = sorted([s[1] for s in slots])
        if len(hari) > 1 or len(ruang) > 1 or len(jam) != sks or \
           not all(jam[i+1] - jam[i] == 1 for i in range(len(jam)-1)):
            return False
    return True


def add_code(state: Dict[Tuple[str,int,str], str],
                   kode: str,
                   start: Tuple[str,int,str],
                   sks: int) -> None:
    hari, jam, ruang = start
    for offset in range(sks):
        state[(hari, jam + offset, ruang)] = kode

def remove_code(state: Dict[Tuple[str,int,str], str], kode: str) -> None:
    to_del = [slot for slot, k in state.items() if k == kode]
    for slot in to_del:
        del state[slot]

def move_code(state, kode, new_hari, new_jam, new_ruang, sks):
    for key in list(state.keys()):
        if state[key] == kode:
            del state[key]

    for offset in range(sks):
        slot = (new_hari, new_jam + offset, new_ruang)
        state[slot] = kode