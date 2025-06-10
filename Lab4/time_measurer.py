import time
import multiprocessing


from card_finder import CardFinder


class TimeMeasurer:
    def __init__(self):
        self.cpu_count = multiprocessing.cpu_count()

    def measure_performance(self, card_hash, bin_prefixes, last4_digits):
        """
        Measure performance with different numbers of processes
        :param card_hash: hash value
        :param bin_prefixes: list of BINs
        :param last4_digits: last 4 digits
        :return: Table of time dependence on the number of processes
        """
        max_processes = int(1.5 * self.cpu_count)
        results = []

        for num_processes in range(1, max_processes + 1):
            start_time = time.time()
            card = CardFinder()
            card.find_card_number(bin_prefixes, last4_digits, card_hash, num_processes)
            elapsed = time.time() - start_time
            results.append((num_processes, elapsed))

        return results
