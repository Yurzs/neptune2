from dns2 import datatypes


class MessageDomainStorage:
    def __init__(self, message: 'Message'):
        self.message = message
        self.storage = []

    storage = []

    def push(self, domain: 'Domain'):
        self.storage.append(domain)
        # for x in self.storage:
        #     print(x.__dict__)

    def search(self, position):
        for domain in self.storage:
            if domain.position == position:
                return domain
        return None

    def search_label(self, label):
        for domain in self.storage:
            if domain.label == label:
                return domain
        return None

    def inject(self):
        pass

    def reset(self):
        self.storage = []


class Domain:
    def __init__(self, storage: MessageDomainStorage, label, position, shortening_allowed=True):
        self._storage = storage
        self._injected = False
        self.label = label
        self.position = position
        self.sa = shortening_allowed

    # @classmethod
    # def parse(cls, storage, label, position, shortening_allowed=True):
    #     if shortening_allowed and len(label.split('.')) > 1:
    #
    #     else:
    #
    #         return [cls(label, position, shortening_allowed)]

    @property
    def binary(self):
        binstring = ''
        search_result = self._storage.search_label(self.label)
        if isinstance(search_result, Domain):
            if search_result._injected and self.sa:
                binstring += f'11{datatypes.int14(int(search_result.position) / 8).binary}'
            else:
                binstring += datatypes.DomainName(self.label).binary
        else:
            resulting_label = ''
            for x in ['.'.join(self.label.split('.')[n:]) for n, x in enumerate(self.label.split('.'))]:
                subsearch_result = self._storage.search_label(x)
                if subsearch_result:
                    binstring += datatypes.DomainName(resulting_label).binary
                    binstring += f'11{datatypes.int14(int(subsearch_result.position) / 8).binary}'
                    return binstring
                else:
                    dmn = Domain(self._storage, x, self.position + len(binstring) + (len(resulting_label) + 1) * 8 )
                    dmn._injected = True
                    self._storage.push(dmn)
                    resulting_label += x.split('.')[0]
            binstring += datatypes.DomainName(self.label).binary
            # for x in self._storage.storage:
            #     print(x.__dict__)
            return binstring
            # binstring += datatypes.DomainName(self.label).binary
        self._injected = True
        self._storage.push(self)
        return binstring

    def __repr__(self):
        return str(self.label)
