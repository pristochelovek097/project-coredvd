#!/usr/bin/env python3
# файл asm.py - ассемблер для процессоров

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
    'ldrh': 0x24, 'strh': 0x25, 'shl': 0x26, 'shr': 0x27,
    'mul': 0x28, 'div': 0x29, 'push': 0x2A, 'pop': 0x2B,
    'call': 0x2C, 'ret': 0x2D
}

# опкоды Z80
OPCODES_Z80 = {
    'nop': 0x00, 'ld_a': 0x3E, 'ld_b': 0x06, 'add_a_b': 0x80,
    'jp': 0xC3, 'halt': 0x76, 'load_frame': 0xDF
}

def encode_imm32(val): return struct.pack('<I', val)
def encode_imm16(val): return struct.pack('<H', val)

def parse_reg(s):
    s = s.strip().lower()
    if s.startswith('r'):
        return int(s[1:])
    raise ValueError(f"invalid register: {s}")

def parse_val(s):
    s = s.strip()
    if s.lower().startswith('0x'):
        return int(s, 16)
    return int(s)

def compile_pulse(lines):
    labels = {}
    pc = 0
    
    # проход 1: считаем байты и ищем метки
    for line in lines:
        line = line.split(';')[0].strip()
        if not line:
            continue
        if ':' in line:
            lbl, rest = line.split(':', 1)
            labels[lbl.strip().lower()] = pc
            line = rest.strip()
        if not line:
            continue

        tokens = re.split(r'[,\s]+', line)
        op = tokens[0].lower()
        if op not in OPCODES_PULSE:
            raise ValueError(f"unknown opcode: {op}")

        # размеры инструкций
        if op in ('mov', 'load', 'ldrb', 'ldrh'):
            pc += 6  # op(1) + reg(1) + addr/imm(4)
        elif op in ('store', 'strb', 'strh'):
            pc += 6  # op(1) + addr(4) + reg(1)
        elif op in ('add', 'sub', 'cmp', 'and', 'or', 'xor', 'shl', 'shr', 'mul'):
            pc += 3  # op(1) + rd(1) + rs(1)
        elif op == 'div':
            pc += 3  # op(1) + rd(1) + rs(1)
        elif op in ('jmp', 'jz', 'jnz', 'call'):
            pc += 5  # op(1) + addr(4)
        elif op == 'movi':
            pc += 4  # op(1) + reg(1) + imm16(2)
        elif op in ('inc', 'dec', 'push', 'pop'):
            pc += 2  # op(1) + reg(1)
        elif op == 'ret':
            pc += 1  # op(1)
        elif op in ('nop', 'load_frame', 'halt'):
            pc += 1
        else:
            raise ValueError(f"unsupported opcode size: {op}")

    # проход 2: генерим байткод
    out = bytearray()
    for line in lines:
        line = line.split(';')[0].strip()
        if ':' in line:
            line = line.split(':', 1)[1].strip()
        if not line:
            continue

        tokens = re.split(r'[,\s]+', line)
        op = tokens[0].lower()
        out.append(OPCODES_PULSE[op])

        if op in ('mov', 'load', 'ldrb', 'ldrh'):
            out.append(parse_reg(tokens[1]))
            out.extend(encode_imm32(parse_val(tokens[2])))
        elif op in ('store', 'strb', 'strh'):
            out.extend(encode_imm32(parse_val(tokens[1])))
            out.append(parse_reg(tokens[2]))
        elif op in ('add', 'sub', 'cmp', 'and', 'or', 'xor', 'shl', 'shr', 'mul', 'div'):
            out.append(parse_reg(tokens[1]))
            out.append(parse_reg(tokens[2]))
        elif op in ('jmp', 'jz', 'jnz', 'call'):
            if tokens[1] in labels:
                addr = labels[tokens[1]]
            else:
                addr = parse_val(tokens[1])
            out.extend(encode_imm32(addr))
        elif op == 'movi':
            out.append(parse_reg(tokens[1]))
            out.extend(encode_imm16(parse_val(tokens[2])))
        elif op in ('inc', 'dec', 'push', 'pop'):
            out.append(parse_reg(tokens[1]))
        elif op == 'ret':
            pass  # already added opcode
        elif op in ('nop', 'load_frame', 'halt'):
            pass  # already added opcode

    return bytes(out)

def compile_z80(lines):
    labels = {}
    pc = 0
    
    # проход 1: метки
    for line in lines:
        line = line.split(';')[0].strip()
        if not line:
            continue
        if ':' in line:
            lbl, rest = line.split(':', 1)
            labels[lbl.strip().lower()] = pc
            line = rest.strip()
        if not line:
            continue

        tokens = re.split(r'[,\s]+', line)
        op = tokens[0].lower()
        
        if op in ('ld_a', 'ld_b'):
            pc += 2
        elif op == 'add_a_b':
            pc += 1
        elif op == 'jp':
            pc += 3
        elif op in ('nop', 'halt', 'load_frame'):
            pc += 1

    # проход 2: генерация
    out = bytearray()
    for line in lines:
        line = line.split(';')[0].strip()
        if ':' in line:
            line = line.split(':', 1)[1].strip()
        if not line:
            continue

        tokens = re.split(r'[,\s]+', line)
        op = tokens[0].lower()
        out.append(OPCODES_Z80[op])

        if op in ('ld_a', 'ld_b'):
            out.append(parse_val(tokens[1]) & 0xFF)
        elif op == 'jp':
            if tokens[1] in labels:
                addr = labels[tokens[1]]
            else:
                addr = parse_val(tokens[1])
            out.extend(encode_imm16(addr))

    return bytes(out)

def print_usage():
    print("Usage:")
    print("  python3 asm.py --arch=pulse <input.asm> <output.bin>")
    print("  python3 asm.py --arch=z80 <input.asm> <output.bin>")
    print("\nPulse instructions:")
    print("  nop, halt, load_frame")
    print("  mov rd, imm32")
    print("  movi rd, imm16")
    print("  add rd, rs, sub rd, rs, mul rd, rs, div rd, rs")
    print("  and rd, rs, or rd, rs, xor rd, rs, cmp rd, rs")
    print("  shl rd, rs, shr rd, rs")
    print("  inc rd, dec rd")
    print("  push rd, pop rd")
    print("  load rd, addr, store addr, rd")
    print("  jmp addr, jz addr, jnz addr")
    print("  call addr, ret")
    print("\nZ80 instructions:")
    print("  nop, halt, load_frame")
    print("  ld_a imm8, ld_b imm8")
    print("  add_a_b")
    print("  jp addr")

if __name__ == '__main__':
    args = sys.argv[1:]
    arch = "pulse"
    
    if args and args[0].startswith("--arch="):
        arch = args[0].split("=")[1]
        args.pop(0)

    if len(args) != 2 or args[0] in ('-h', '--help'):
        print_usage()
        sys.exit(1)

    try:
        with open(args[0], 'r') as f:
            lines = f.readlines()

        if arch == "z80":
            binary = compile_z80(lines)
            print(f"[asm] Z80 mode")
        else:
            binary = compile_pulse(lines)
            print(f"[asm] Pulse mode (extended)")

        with open(args[1], 'wb') as f:
            f.write(binary)

        print(f"[asm] assembled {len(binary)} bytes -> {args[1]}")
        
        # вывод hexdump для маленьких файлов
        if len(binary) <= 64:
            print("\n[asm] hexdump:")
            for i in range(0, len(binary), 16):
                chunk = binary[i:i+16]
                hex_part = ' '.join(f'{b:02x}' for b in chunk)
                ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
                print(f"  {i:04x}: {hex_part:<48} {ascii_part}")

    except Exception as e:
        print(f"[error] {e}")
        sys.exit(1)
