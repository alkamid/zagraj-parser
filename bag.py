from collections import OrderedDict


class Bag(object):
    def __init__(self, language='polish'):
        self.bag = OrderedDict()
        with open('{}.quackle_alphabet'.format(language)) as f:
            for line in f.readlines():
                lsp = line.split('\t')
                if lsp[0] == 'blank':
                    self.bag['_'] = {'val': int(lsp[1]), 'left': int(lsp[2])}
                    continue
                self.bag[lsp[0]] = {'val': int(lsp[2]), 'left': int(lsp[3])}

    def remove(self, letter):
        self.bag[letter]['left'] -= 1

    def __str__(self):
        bs = ''
        for let in self.bag.keys():
            if self.bag[let]['left'] != 0:
                bs += '{} {}\n'.format(let, self.bag[let]['left'])

        return bs
