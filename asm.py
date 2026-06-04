#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
# SPDX-FileCopyrightText: 2026 prostochelovek097
import sys
import struct
import re

# полный набор опкодов Pulse 
OPCODES_PULSE = {
    'nop': 0x00, 'mov': 0x01, 'add': 0x02, 'load_frame': 0x03, 
    'sub': 0x04, 'and': 0x05, 'or': 0x06, 'xor': 0x07, 
    'cmp': 0x08, 'jmp': 0x09, 'jz': 0x0A, 'jnz': 0x0B, 
    'load': 0x0C, 'store': 0x0D, 'halt': 0x0E, 'inc': 0x0F, 
    'dec': 0x10, 'movi': 0x21, 'ldrb': 0x22, 'strb': 0x23, 
    'ldrh': 0x24, 'strh': 0x25
}

# опкоды Z80 
OPCODES_Z80 = {
    'nop': 0x00, 'ld_a': 0x3E, 'ld_b': 0x06, 'add_a_b': 0x80, 'jp': 0xC3, 'halt': 0x76, 'load_frame': 0xDF
}

def encode_imm32(val): return struct.pack('<I', val)
def encode_imm16(val): return struct.pack('<H', val)

def parse_reg(s):
    s = s.strip().lower()
    if s.startswith('r'): return int(s[1:])
    raise ValueError(f"неправильный регистр: {s}")

def parse_val(s):
    s = s.strip()
    return int(s, 16) if s.lower().startswith('0x') else int(s)

def compile_pulse(lines):
    labels = {}
    pc = 0
    
    # проход 1: считаем байты и ищем метки
    for line in lines:
        line = line.split(';')[0].strip()
        if not line: continue
        if ':' in line:
            lbl, rest = line.split(':', 1)
            labels[lbl.strip().lower()] = pc
            line = rest.strip()
        if not line: continue

        tokens = re.split(r'[,\s]+', line)
        op = tokens[0].lower()
        if op not in OPCODES_PULSE: raise ValueError(f"неизвестный опкод: {op}")

        if op in ('mov', 'load', 'ldrb', 'ldrh'): pc += 6 # op(1) + reg(1) + addr/imm(4)
        elif op in ('store', 'strb', 'strh'): pc += 6     # op(1) + addr(4) + reg(1)
        elif op in ('add', 'sub', 'cmp', 'and', 'or', 'xor'): pc += 3 # op(1) + r1(1) + r2(1)
        elif op in ('jmp', 'jz', 'jnz'): pc += 5          # op(1) + addr(4)
        elif op == 'movi': pc += 4                        # op(1) + reg(1) + imm16(2)
        elif op in ('nop', 'load_frame', 'halt'): pc += 1
        elif op in ('inc', 'dec'): pc += 2

    # проход 2: генерим байткод
    out = bytearray()
    for line in lines:
        line = line.split(';')[0].strip()
        if ':' in line: line = line.split(':', 1)[1].strip()
        if not line: continue

        tokens = re.split(r'[,\s]+', line)
        op = tokens[0].lower()
        out.append(OPCODES_PULSE[op])

        if op in ('mov', 'load', 'ldrb', 'ldrh'):
            out.append(parse_reg(tokens[1]))
            out.extend(encode_imm32(parse_val(tokens[2])))
        elif op in ('store', 'strb', 'strh'):
            out.extend(encode_imm32(parse_val(tokens[1])))
            out.append(parse_reg(tokens[2]))
        elif op in ('add', 'sub', 'cmp', 'and', 'or', 'xor'):
            out.append(parse_reg(tokens[1]))
            out.append(parse_reg(tokens[2]))
        elif op in ('jmp', 'jz', 'jnz'):
            addr = labels.get(tokens[1], parse_val(tokens[1]) if tokens[1].isdigit() or tokens[1].startswith('0x') else 0)
            out.extend(encode_imm32(addr))
        elif op == 'movi':
            out.append(parse_reg(tokens[1]))
            out.extend(encode_imm16(parse_val(tokens[2])))
        elif op in ('inc', 'dec'):
            out.append(parse_reg(tokens[1]))
            
    return bytes(out)

def compile_z80(lines):
    labels = {}
    pc = 0
    for line in lines:
        line = line.split(';')[0].strip()
        if not line: continue
        if ':' in line:
            lbl, rest = line.split(':', 1)
            labels[lbl.strip().lower()] = pc
            line = rest.strip()
        if not line: continue

        tokens = re.split(r'[,\s]+', line)
        op = tokens[0].lower()
        if op in ('ld_a', 'ld_b'): pc += 2
        elif op == 'add_a_b': pc += 1
        elif op == 'jp': pc += 3
        elif op in ('nop', 'halt', 'load_frame'): pc += 1

    out = bytearray()
    for line in lines:
        line = line.split(';')[0].strip()
        if ':' in line: line = line.split(':', 1)[1].strip()
        if not line: continue

        tokens = re.split(r'[,\s]+', line)
        op = tokens[0].lower()
        out.append(OPCODES_Z80[op])

        if op in ('ld_a', 'ld_b'):
            out.append(parse_val(tokens[1]) & 0xFF)
        elif op == 'jp':
            addr = labels.get(tokens[1], parse_val(tokens[1]) if tokens[1].isdigit() else 0)
            out.extend(encode_imm16(addr))
            
    return bytes(out)

if __name__ == '__main__':
    args = sys.argv[1:]
    arch = "pulse"
    
    if args and args[0].startswith("--arch="):
        arch = args[0].split("=")[1]
        args.pop(0)

    if len(args) != 2:
        print("использование: python3 asm.py [--arch=pulse|z80] <in.asm> <out.bin>")
        sys.exit(1)

    with open(args[0], 'r') as f:
        lines = f.readlines()

    if arch == "z80":
        binary = compile_z80(lines)
    else:
        binary = compile_pulse(lines)

    with open(args[1], 'wb') as f:
        f.write(binary)
        
    print(f"[asm] собрано {len(binary)} байт под {arch.lower()} -> {args[1]}")
