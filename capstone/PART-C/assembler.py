#!/usr/bin/env python3
"""Two-pass Hack assembler for Nand2Tetris. K=33 variant writes symbols.txt."""
from pathlib import Path
import argparse
import re
import sys

PREDEFINED = {
    "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4,
    **{f"R{i}": i for i in range(16)},
    "SCREEN": 16384, "KBD": 24576,
}
DEST = {
    "": "000", "M": "001", "D": "010", "MD": "011",
    "A": "100", "AM": "101", "AD": "110", "AMD": "111",
}
JUMP = {
    "": "000", "JGT": "001", "JEQ": "010", "JGE": "011",
    "JLT": "100", "JNE": "101", "JLE": "110", "JMP": "111",
}
COMP = {
    "0": "0101010", "1": "0111111", "-1": "0111010",
    "D": "0001100", "A": "0110000", "!D": "0001101",
    "!A": "0110001", "-D": "0001111", "-A": "0110011",
    "D+1": "0011111", "A+1": "0110111", "D-1": "0001110",
    "A-1": "0110010", "D+A": "0000010", "D-A": "0010011",
    "A-D": "0000111", "D&A": "0000000", "D|A": "0010101",
    "M": "1110000", "!M": "1110001", "-M": "1110011",
    "M+1": "1110111", "M-1": "1110010", "D+M": "1000010",
    "D-M": "1010011", "M-D": "1000111", "D&M": "1000000",
    "D|M": "1010101",
}

def read_source(path):
    lines = []
    for number, raw in enumerate(Path(path).read_text(encoding="utf-8").splitlines(), 1):
        line = raw.split("//", 1)[0].strip()
        if line:
            lines.append((number, re.sub(r"\s+", "", line)))
    return lines

def assemble(source_path, output_path=None, symbols_path=None):
    source = read_source(source_path)
    symbols = dict(PREDEFINED)
    label_lines = []
    rom = 0

    # Pass 1: labels
    for line_no, line in source:
        if line.startswith("(") and line.endswith(")"):
            label = line[1:-1]
            if not label or not re.fullmatch(r"[A-Za-z_.$:][\w.$:]*", label):
                raise ValueError(f"Line {line_no}: invalid label declaration")
            if label in symbols:
                print(f"Warning: Line {line_no}: duplicate label '{label}'")
            else:
                symbols[label] = rom
            label_lines.append(line_no)
        else:
            rom += 1

    # Pass 2: instructions and variables
    output = []
    next_variable = 16
    for line_no, line in source:
        if line.startswith("(") and line.endswith(")"):
            continue
        try:
            if line.startswith("@"):
                token = line[1:]
                if token.isdigit():
                    value = int(token)
                else:
                    if not re.fullmatch(r"[A-Za-z_.$:][\w.$:]*", token):
                        raise ValueError("invalid A-instruction symbol")
                    if token not in symbols:
                        symbols[token] = next_variable
                        next_variable += 1
                    value = symbols[token]
                if not 0 <= value <= 32767:
                    raise ValueError("A-instruction value must be 0..32767")
                output.append(f"{value:016b}")
            else:
                if line.count(";") > 1 or line.count("=") > 1:
                    raise ValueError("malformed C-instruction")
                if ";" in line:
                    left, jump = line.split(";")
                else:
                    left, jump = line, ""
                if "=" in left:
                    dest, comp = left.split("=")
                else:
                    dest, comp = "", left
                if dest not in DEST:
                    raise ValueError(f"invalid destination '{dest}'")
                if comp not in COMP:
                    raise ValueError(f"invalid computation '{comp}'")
                if jump not in JUMP:
                    raise ValueError(f"invalid jump '{jump}'")
                output.append("111" + COMP[comp] + DEST[dest] + JUMP[jump])
        except ValueError as exc:
            raise ValueError(f"Line {line_no}: {exc}") from None

    if output_path is None:
        output_path = str(Path(source_path).with_suffix(".hack"))
    Path(output_path).write_text("\n".join(output) + "\n", encoding="utf-8")
    if symbols_path is None:
        symbols_path = str(Path(source_path).with_name("symbols.txt"))
    with open(symbols_path, "w", encoding="utf-8") as f:
        for name, address in sorted(symbols.items(), key=lambda item: (item[1], item[0])):
            f.write(f"{name}={address}\n")
    return output

def main():
    parser = argparse.ArgumentParser(description="Assemble Hack .asm into .hack")
    parser.add_argument("input", help="input .asm file")
    parser.add_argument("-o", "--output", help="output .hack file")
    parser.add_argument("--symbols", default=None, help="symbols output (default: symbols.txt)")
    args = parser.parse_args()
    try:
        result = assemble(args.input, args.output, args.symbols)
        print(f"Assembly successful: {len(result)} instructions")
    except (OSError, ValueError) as exc:
        print(exc, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
