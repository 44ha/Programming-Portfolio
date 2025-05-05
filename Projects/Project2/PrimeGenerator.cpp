#include <iostream>
#include <cmath>
#include <cstdlib>
#include <ctime>
#include <vector>

using namespace std;

bool checkDivisibilityBySmallPrimes(long long n) {
    vector<long long> smallPrimes = {3, 5, 7, 11, 13, 17, 19, 23, 29};
    for (long long prime : smallPrimes) {
        if (n % prime == 0) {
            return true;
        }
    }
    return false;
}

long long modExp(long long base, long long exp, long long mod) {
    long long result = 1;
    while (exp > 0) {
        if (exp % 2 == 1) {
            result = (result * base) % mod;
        }
        base = (base * base) % mod;
        exp /= 2;
    }
    return result;
}

bool isProbablyPrime(long long n, int k = 10) { 
    if (n <= 1) return false;
    if (n == 2 || n == 3) return true;

    long long r = 0, d = n - 1;
    while (d % 2 == 0) {
        r++;
        d /= 2;
    }

    for (int i = 0; i < k; ++i) {
        long long a = rand() % (n - 4) + 2;
        long long x = modExp(a, d, n);
        if (x == 1 || x == n - 1) continue;

        bool composite = true;
        for (long long j = 0; j < r - 1; ++j) {
            x = (x * x) % n;
            if (x == n - 1) {
                composite = false;
                break;
            }
        }
        if (composite) return false;
    }
    return true;
}

long long generateRandomNumber(int digits) {
    long long min = pow(10, digits - 1);
    long long max = pow(10, digits) - 1;
    return rand() % (max - min + 1) + min;
}

int main() {
    srand(time(0));

    int digits;
    cout << "Enter the number of digits for the prime number (max 10 digits): ";
    cin >> digits;

    if (digits < 1 || digits > 10) {
        cout << "Please enter a valid number of digits (1 to 10)." << endl;
        return 1;
    }

    long long prime;
    bool foundPrime = false;

    while (!foundPrime) {
        prime = generateRandomNumber(digits);

        if (prime % 2 == 0) {
            prime++;
        }

        if (isProbablyPrime(prime)) {
            if (!checkDivisibilityBySmallPrimes(prime)) {
                foundPrime = true;
            }
        }
    }

    cout << "Generated prime number: " << prime << endl;

    return 0;
}
