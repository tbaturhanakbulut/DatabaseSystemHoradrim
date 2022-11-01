Project is written with Python and used cachetools, rwlock and bplustree libraries.
Our code is auto runnable. 
You need to install some requirements before you build
Make sure you have python 3 on your computer and run the commands below:
	pip install cachetools
	pip install rwlock
	pip install bplustree
If these commands do not work, you can try again by typing pip3 instead of pip.

Then find tree.py where the library is installed. Then change the _iter_slice function from the code in it as follows.

def _iter_slice(self, slice_: slice) -> Iterator[Record]:
        if slice_.step is not None:
            raise ValueError('Cannot iterate with a custom step')

        if (slice_.start is not None and slice_.stop is not None and
                slice_.start >= slice_.stop):
            raise ValueError('Cannot iterate backwards')

        if slice_.start is None:
            node = self._left_record_node
        else:
            node = self._search_in_tree(slice_.start, self._root_node)

        while True:
            for entry in node.entries:
                if slice_.start is not None and entry.key < slice_.start:
                    continue

                if slice_.stop is not None and entry.key >= slice_.stop:
                    return

                yield entry

            if node.next_page:
                node = self._mem.get_node(node.next_page)
            else:
                return

Steps to run:
	1) First create an input and output file.
	Input file has some operations in it. 
	create type <type-name><number-of-fields><primary-key-order><field1-name><field1-type><field2-name>..
	delete type <type-name>
	list type
	create record <type-name><field1-value><field2-value>...
	delete record <type-name><primary-key>
	update record <type-name><primary-key><field1-value><field2-value>
	search record <type-name><primary-key> 
	list record <type-name>
	filter record <type-name><condition>


	Sample Input File
	create type angel 3 1 name str alias str affiliation str 
	create type evil 4 1 name str type str alias str spell str
	create record angel Tyrael ArchangelOfJustice HighHeavens
	create record angel Itherael ArchangelOfFate HighHeavens
	update record angel Tyrael Tyrael AspectOfWisdom Horadrim
	list record angel
	list record evil
	list type

	2) python3 main.py <input.txt(with path)> <output file>
 
    

