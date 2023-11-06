from array import array
import sys

MAX_NUMBER=32767
MODULO = REGOFFSET = MAX_NUMBER + 1

def process(file: str) -> array:
    with open(file, "rb") as f:
        data = array("H", f.read())
    return data

class VM:
    def __init__(self, data: array):
        self.__memory = data
        self.__ptr = 0
        self.__registers = array("H",[0]*8)
        self.__stack = []
        self.__input_buffer = []
    
    def run(self, ptr = 0):
        self.__ptr = ptr
        while True:
            self.__ptr = self.__run_instruction(self.__ptr)

    def memory(self, address:int):
        value = self.__memory[address]
        if value > MAX_NUMBER:
            regindex = value - REGOFFSET
            value = self.__registers[regindex]
        return value
    
    def get_register(self, address:int):
        register = self.__memory[address]
        return  register - REGOFFSET if register > MAX_NUMBER else register

    def set_register(self, register:int, value:int):
        self.__registers[register] = value

    def get_input(self):
        if len(self.__input_buffer) == 0:
            self.__input_buffer = [ord(x) for x in f'{input("-> ")}\n']
        return self.__input_buffer.pop(0)

    def __run_instruction(self, address:int):
        op = self.__memory[address]
        match(op):
            case 0:  # halt: 0
                # stop execution and terminate the program
                exit(0)
            case 1: # set: 1 a b
                # set register <a> to the value of <b>
                regindex = self.get_register(address + 1)
                value = self.memory(address + 2)
                self.set_register(regindex, value)
                return address + 3
            case 2: # push: 2 a
                # push <a> onto the stack
                self.__stack.append(self.memory(address + 1))
                return address + 2
            case 3: # pop: 3 a
                # remove the top element from the stack and write it into <a>; empty stack = error
                value = self.__stack.pop()
                regindex = self.get_register(address + 1)
                self.set_register( regindex, value)
                return address + 2
            case 4: # eq: 4 a b c
                # set <a> to 1 if <b> is equal to <c>; set it to 0 otherwise
                regindex = self.get_register(address + 1)
                value = 1 if self.memory(address+2) == self.memory(address + 3) else 0
                self.set_register(regindex, value)
                return address + 4
            case 5: # gt: 5 a b c
                # set <a> to 1 if <b> is greater than <c>; set it to 0 otherwise
                regindex = self.get_register(address + 1)
                value = 1 if self.memory(address + 2) > self.memory(address + 3) else 0
                self.set_register(regindex, value)
                return address + 4
            case 6: # jmp: 6 a
                # jump to <a>
                return self.memory(address+1)
            case 7: # jt: 7 a b
                # if <a> is nonzero, jump to <b>
                return self.memory(address+2) if self.memory(address+1) > 0 else address + 3
            case 8: # jf: 8 a b
                # if <a> is zero, jump to <b>
                return self.memory(address+2) if self.memory(address+1) == 0 else address + 3
            case 9: # add: 9 a b c
                # assign into <a> the sum of <b> and <c> (modulo 32768)
                regindex = self.get_register(address+1)
                value = (self.memory(address+2) + self.memory(address+3)) % MODULO
                self.set_register(regindex, value)
                return address + 4
            case 10: # mult: 10 a b c
                # store into <a> the product of <b> and <c> (modulo 32768)
                regindex = self.get_register(address+1)
                value = (self.memory(address + 2) * self.memory(address + 3))%MODULO
                self.set_register(regindex, value)
                return address + 4
            case 11: # mod: 11 a b c
                # store into <a> the remainder of <b> divided by <c>
                regindex = self.get_register(address+1)
                value = self.memory(address+2) % self.memory(address+3)
                self.set_register(regindex, value)
                return address + 4
            case 12: # and: 12 a b c   
                # stores into <a> the bitwise and of <b> and <c>
                regindex = self.get_register(address+1)
                value = self.memory(address+2) & self.memory(address+3)
                self.set_register(regindex, value)
                return address + 4
            case 13: # or: 13 a b c
                # stores into <a> the bitwise or of <b> and <c>
                regindex = self.get_register(address+1)
                value = self.memory(address+2) | self.memory(address+3)
                self.set_register(regindex, value)
                return address + 4
            case 14: # not: 14 a b
                # stores 15-bit bitwise inverse of <b> in <a>
                value = self.memory(address+2)
                regindex = self.get_register(address+1)
                self.set_register(regindex, MAX_NUMBER-value)
                return address + 3
            case 15: # rmem: 15 a b
                # read memory at address <b> and write it to <a>
                value = self.memory(self.memory(address+2))
                regindex = self.get_register(address+1)
                self.set_register(regindex, value)
                return address + 3
            case 16: # wmem: 16 a b
                # write the value from <b> into memory at address <a>
                value = self.memory(address+2)
                newaddress = self.memory(address+1)
                self.__memory[newaddress] = value
                return address + 3
            case 17: # call: 17 a
                # write the address of the next instruction to the stack and jump to <a>
                self.__stack.append(address + 2)
                return self.memory(address+1)
            case 18: # ret: 18
                # remove the top element from the stack and jump to it; empty stack = halt
                return self.__stack.pop()
            case 19: # out: 19 a
                # write the character represented by ascii code <a> to the terminal
                sys.stdout.write(chr(self.memory(address+1)))
                return address + 2
            case 20: # in: 20 a
                # read a character from the terminal and write its ascii code to <a>; it can be assumed that once input starts, it will continue until a newline is encountered; this means that you can safely read whole lines from the keyboard and trust that they will be fully read
                regindex = self.get_register(address+1)
                value = self.get_input()
                self.set_register(regindex, value)
                return address + 2
            case 21: # noop: 21
                # no operation
                return address + 1
            case _:
                # panic
                assert("panic")

def disassemble(data, outfile):
    ops = [
        {"name":"halt", "args":0},
        {"name":"set", "args":2},
        {"name":"push", "args":1},
        {"name":"pop", "args":1},
        {"name":"eq", "args":3},
        {"name":"gt", "args":3},
        {"name":"jmp", "args":1},
        {"name":"jt", "args":2},
        {"name":"jf", "args":2},
        {"name":"add", "args":3},
        {"name":"mult", "args":3},
        {"name":"mod", "args":3},
        {"name":"and", "args":3},
        {"name":"or", "args":3},
        {"name":"not", "args":2},
        {"name":"rmem", "args":2},
        {"name":"wmem", "args":2},
        {"name":"call", "args":1},
        {"name":"ret", "args":0},
        {"name":"out", "args":1},
        {"name":"in", "args":1},
        {"name":"noop", "args":0}
    ]
    with open(outfile, "w") as f:
        end = len(data)
        i = 0
        while i < end:
            opidx = data[i]
            i += 1
            if opidx <= 21:
                op = ops[opidx]
                f.write(f"{i-1}: {op['name']}")
                for j in range(op['args']):
                    arg = data[i]
                    if 32768 <= arg <= 32775: # registers
                        arg = f"${arg - REGOFFSET}"
                    elif (opidx == 19) and (32 <= arg <= 126): # char
                        arg = f"{arg}   \t# '{chr(arg)}'"
                    f.write(f" {arg}")
                    i += 1
                f.write("\n")
            else: # not instuction, just memory value?
                f.write(f"{i-1}: {opidx}\t [raw] \n")


data = process("./challenge.bin")
# disassemble(data, "./challenge.asm")
# testdata = array("H", [9,32768,32769,4,19,32768])
vm = VM(data)
vm.run()