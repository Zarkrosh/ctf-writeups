import sys

def resolve(w, tags, regs, ins):
    if w in tags:
        return hex(int(tags[w]))[2:].zfill(2)
    elif w in regs:
        return regs[w]
    elif w in ins:
        return ins[w]
    elif "0x" == w[0:2]:
        return w[2:].zfill(2)
    else:
        try:
            # Remove the 0x and pad to two characters.
            return hex(int(w))[2:].zfill(2)
        except (TypeError, ValueError):
            print(w)
            print(tags, regs, ins)
            sys.exit(0)

if len(sys.argv) < 2:
    print("Supply one arg for the assembly")
    sys.exit(-1)
with open(sys.argv[1], "r") as fp:
    lines = list(fp)

res = []
# In bytes.
position = 0
tags = {}
regs = {"ax": "00", "bx": "01", "cx": "02", "dx": "03"}
ins = {
       "sub" : "01",
       "clr" : "030000",
       "rst" : "040000",
       "jmp" : "05",
       "jg"  : "080000",
       "jge" : "090000",
       "jl"  : "0a0000",
       "jle" : "0b0000",
       "je"  : "0c0000",
       "jz"  : "0d0000",
       "jnz" : "0e0000",
       "movl": "10",
       "call": "11",
       "ret" : "120000",
       "cmp" : "13",
       "push": "14",
       "pop" : "15",
       "mmiv": "17",
       "mmov": "18",
       "msk" : "1a0000",
       "mskb": "1b0000"}

position = 0
# Add all the tags first.
for l in lines:
    if ":" == l[0]:
        tags[l.split()[0]] = position
        continue
    # Tags refer to the instruciton, not the byte.
    position += 1

# Regs are 32 bits.
for l in lines:
    if ":" == l[0]:
        # Discard line if tag.
        continue
    # Discard the first \t.
    l_ins = l.replace(",", "").split()
    if l_ins[0] == "sub" and len(l_ins) == 2:
        l_ins.append("0")
    # print(l_ins)
    l_ins = list(map(lambda x: resolve(x, tags, regs, ins), l_ins))
    # print(len("".join(l_ins)))

    res.append("".join(l_ins))
print("v2.0 raw")
print(" ".join(res))
