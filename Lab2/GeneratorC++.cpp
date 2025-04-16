#include <iostream>
#include <bitset>
#include <random>

std::bitset<128> generateRandomBinarySequence() {
    std::random_device rd;
    std::mt19937_64 gen(rd());
    std::uniform_int_distribution<uint64_t> dis(0, UINT64_MAX);

    std::bitset<128> result;
    for (int i = 0; i < 2; ++i) {
        result |= (std::bitset<128>(dis(gen)) << (i * 64));
    }

    return result;
}

int main() {
    std::bitset<128> randomSequence = generateRandomBinarySequence();
    std::cout << "Случайная 128-битная бинарная последовательность: " << randomSequence << std::endl;
    return 0;
}
