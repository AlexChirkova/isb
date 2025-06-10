import hashlib
import multiprocessing
from functools import partial


class CardFinder:
    def __init__(self):
       self.cpu_count = multiprocessing.cpu_count()

    def find_card_number(self, bins, last4_digits, card_hash, processes=0):
        """
        Find card number matching the hash with given BIN and last 4 digits
        :param processes: Count of processes
        :param bins: list of BINs
        :param last4_digits: last 4 digits
        :param card_hash: hash value
        :return: found card number
        """
        if not processes: processes = self.cpu_count

        with multiprocessing.Pool(processes=processes) as pool:
            for bin_prefix in bins:
                result = self._process_bin(pool, card_hash, bin_prefix, last4_digits)
                if result:
                    return result

        raise ValueError("No matching card number found")

    def _process_bin(self, pool, card_hash, bin_prefix, last4_digits):
        """
        Processing of a single BIN
        :param pool: the current process
        :param card_hash: hash value
        :param bin_prefix: BIN
        :param last4_digits: last 4 digits
        :return: found card number according to current BIN
        """
        # The card number has 16 digits: BIN (6) + middle (6) + last4 (4)
        middle_length = 6
        middle_digits = [str(i).zfill(middle_length) for i in range(10**middle_length)]

        chunk_size = len(middle_digits) // self.cpu_count
        chunks = [
            middle_digits[i : i + chunk_size]
            for i in range(0, len(middle_digits), chunk_size)
        ]

        worker = partial(self._find_in_chunk, bin_prefix, last4_digits, card_hash)
        for found in pool.map(worker, chunks):
            if found:
                return found

    def _find_in_chunk(self, bin_prefix, last4_digits, target_hash, chunk):
        """
        Check a chunk of middle digits for matching hash
        :param bin_prefix: BIN
        :param last4_digits: last 4 digits
        :param target_hash: hash value
        :param chunk: the chunk for check
        :return:
        """
        for middle in chunk:
            card_number = bin_prefix + middle + last4_digits
            if self._hash_matches(card_number, target_hash):
                return card_number
        return ""

    @staticmethod
    def _hash_matches(card_number, target_hash):
        """
        Check if the card number hashes to the target hash
        :param card_number: found card number
        :param target_hash: hash value
        :return: do the nash values match or not
        """

        hashed = hashlib.sha3_384(card_number.encode()).hexdigest()
        return hashed == target_hash
