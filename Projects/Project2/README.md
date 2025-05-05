# Prime Number Generator Using Miller-Rabin Test

This program generates **random prime numbers** with a specified number of digits (up to 10 digits). It uses a method called the **Miller-Rabin Primality Test** to check if a number is prime. This method is much faster than older methods, especially for larger numbers.

The program works by:
- Checking if a number is divisible by small primes like 3, 5, 7, 11, etc.
- Using the **Miller-Rabin Test** to make sure the number is prime.

This method is really useful when you need to generate large primes quickly, like for cryptography or random number generation.

## Features

- You can specify how many digits you want the prime number to have (up to 10 digits).
- The program uses the **Miller-Rabin Test** to check if the number is prime.
- It also checks divisibility by small primes to speed up the process.
- It's **faster** than older methods for checking primes, especially for big numbers.

## How It Works

### Miller-Rabin Primality Test

The **Miller-Rabin Test** is a smart way to check if a number is prime, but it's not 100% guaranteed—it's probabilistic. However, the chances of it being wrong are really, really small.

Here’s how it works:
1. It takes the number $n-1$, and splits it into two parts: $2^r \times d$, where $d$ is odd.
2. It picks a random number \( a \) and checks if it meets certain conditions by doing some calculations with it.
3. It repeats this check **k times** (in our case, 10 times) to make sure the number is probably prime.

The more times it repeats, the more confident we are that the number is prime.

### Divisibility Check

Before doing the **Miller-Rabin Test**, the program checks if the number is divisible by small primes (like 3, 5, 7, etc.). If it is, we know right away that it’s not prime, and we can skip the test for that number.

## Why It's Fast

The **Miller-Rabin Test** is much quicker than old methods, like trial division or the Sieve of Eratosthenes, especially when working with large numbers. The test does a lot of checks in just a few steps.

### Time Complexity:

- The Miller-Rabin Test runs in $O(k \log n)$, where $k$ is the number of rounds (10 in this case) and $n$ is the number being checked.

- Checking divisibility by small primes takes \( O(1) \) time, which is pretty fast.

So, the time it takes to generate a prime is mainly based on the **Miller-Rabin Test**.

### Chance of Error

The **probability of error** in the test depends on how many rounds we run. With **10 rounds**, the chance of making a mistake is super small:

$$P(\text{error}) = \left( \frac{1}{4} \right)^{10} \approx 0.000000000095$$




In other words, the chance that it says a non-prime number is prime is **about 0.0000001%**.

## How It Works (Step-by-Step)

1. You enter the number of digits you want for your prime number (1 to 10 digits).
2. The program generates a random number with that many digits.
3. It first checks if the number is divisible by small primes (like 3, 5, 7, etc.).
4. Then, it runs the **Miller-Rabin Test** to check if the number is prime.
5. If the number passes all checks, it’s shown as a prime number!

## Example

Here’s an example of how it works:

```bash
Enter the number of digits for the prime number (max 10 digits): 7
Generated prime number: 2163911
