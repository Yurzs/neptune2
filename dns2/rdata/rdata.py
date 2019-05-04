

class Rdata:
    binary_instructions = []

    @property
    def binary(self):
        binstring = ''
        for item in self.binary_instructions:
            binstring += item.binary
        return binstring

    @property
    def binary_instructions(self):
        return self.__dict__.values()
