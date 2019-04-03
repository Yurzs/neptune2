import bitstring


class ParserMixin:

    def parse_byte_rr(self, name_datatype, name_length):
        """

        :param name_datatype:
        :param name_length:
        :return:
        """
        bin_counter = 0
        for item in name_datatype:
            if name_length[item] == 'REST':
                setattr(self, item, name_datatype[item](self.data))
                self.byte_counter += int(len(self.data) / 8)
                break
            elif name_length[item] == 'DYNAMIC':
                obj, self.data, self.byte_counter, self.domain_links = name_datatype[item].decode(
                    byte_data=self.data,
                    byte_counter=self.byte_counter,
                    domain_links=self.domain_links
                )
                setattr(self, item, obj)
            elif item == 'rdata':
                data = self.data
                obj, self.data, self.byte_counter, self.domain_links = name_datatype[item][self.atype].decode(
                    byte_data=self.data[:getattr(self, name_length[item][0]) * 8],
                    byte_counter=self.byte_counter,
                    domain_links=self.domain_links
                )
                self.data = data[getattr(self, name_length[item][0]) * 8:]
                setattr(self, item, obj)
            elif isinstance(name_length[item], list):
                if not getattr(self, name_length[item][0]) == 0:
                    setattr(self, item, name_datatype[item](self.data[:getattr(self, name_length[item][0])]))
                    self.data = self.data[getattr(self, name_datatype[item][0]):]
            elif issubclass(name_datatype[item], int) and isinstance(self.data, bitstring.BitArray):
                setattr(self, item, name_datatype[item](self.data.bin[:name_length[item]], base=2))
                self.data = bitstring.BitArray(bin=self.data.bin[name_length[item]:])
                if name_length[item] >= 8:
                    self.byte_counter += int(name_length[item] / 8)
                else:
                    bin_counter += name_length[item]
            else:
                setattr(self, item, name_datatype[item](self.data[:name_length[item]]))
                self.data = self.data[name_length[item]:]
                if name_length[item] >= 8:
                    self.byte_counter += int(name_length[item] / 8)
                else:
                    bin_counter += name_length[item]
            if bin_counter >= 8:
                self.byte_counter += bin_counter // 8
                bin_counter = bin_counter % 8

    def parse_dict_rr(self, dict_data, name_datatype):
        for item in name_datatype:
            if item == 'rdlength':
                rdata = name_datatype['rdata'][self.atype](dictionary=dict_data['rdata'],
                                                           domain_links=self.domain_links,
                                                           byte_counter=self.byte_counter)
                setattr(self, item, name_datatype[item](len(rdata.encode()) / 8))
                continue
            elif item == 'rdata':
                setattr(self, item, name_datatype[item][self.atype](dictionary=dict_data[item],
                                                                    domain_links=self.domain_links,
                                                                    byte_counter=self.byte_counter))
                continue
            else:
                try:
                    setattr(self, item, name_datatype[item](dict_data[item]))
                except TypeError:
                    setattr(self, item, name_datatype[item](dict_data[item]))
