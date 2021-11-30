from pwn import *
import time

def add_tree(facing,x,y,moves, new_depth, known_pos):
    if(facing == "D"):
        new_x = x + 1
        new_y = y
    elif(facing == "R"):
        new_x = x
        new_y = y + 1
    else:
        new_x = x
        new_y = y - 1

    if lines[new_x][new_y] == "O" and [new_x, new_y] not in known_pos:
        known_pos.append([new_x, new_y])
        new_moves = moves
        new_moves += facing
        new_depth.append([new_moves,new_x,new_y])
        return False, new_moves

    elif lines[new_x][new_y] == "F":
        moves += facing
        return True, moves

    else:
        return False, False

p = remote("209.97.132.64",30750)
p.recvuntil(b"> ")
p.sendline(b"2")
# Remove first line and last two because they dont belong to the map.

while True:
    res = p.recvuntil("> ")
    lines = res.decode("utf-8").split("\n")[1:-2]
    new_lines = []
    for l in lines:
        new_l = l.replace("☠️ ","X")
        new_l = new_l.replace("🔩","O")
        new_l = new_l.replace("💎","F")
        new_l = new_l.replace("🤖","S")
        new_l = new_l.replace(" ", "")
        new_lines.append(new_l)

    lines = new_lines

    for (l, line) in enumerate(lines):
        try:
            start_pos = (l, line.index("S"))
            break
        except ValueError:
            pass

    x, y = start_pos
    tree = [["",x,y]]
    known_pos = [[x,y]]
    

    while True:
        new_depth = []
        sol = False
        for mov in tree:
            #print("Mov: ", mov)
            sol, moves = add_tree("D",mov[1], mov[2], mov[0], new_depth,known_pos)
            if sol:
                break
            sol, moves = add_tree("L",mov[1], mov[2], mov[0], new_depth,known_pos)
            if sol:
                break
            sol, moves = add_tree("R",mov[1], mov[2], mov[0], new_depth,known_pos)
            if sol:
                break
            #lines[mov[1]][mov[2]].replace("O",X)
        if(sol):
            print("Sol:", moves)
            p.sendline(moves)
            res = p.recvuntil(b"!")
            if(b"500" in res):
                p.interactive()
            print(res)
            res = p.recvuntil(b"!")
            break

        #print("new_depth:", new_depth)

        tree = new_depth.copy()
