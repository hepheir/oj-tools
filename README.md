# oj-tools

[QingdaoU/OnlineJudge](https://github.com/QingdaoU/OnlineJudge) 를 위한 테스트케이스 생성기입니다.


## Install

```shell
pip install --upgrade oj-tools
```


## Example

아래는 $N \leq 100$ 인 $N$ 번째 소수를 구하는 문제의 테스트 케이스를 생성하는 예시 입니다.

```python
def prime_generator(hi):
    # Sieve of Eratosthenes
    # https://en.wikipedia.org/wiki/Sieve_of_Eratosthenes
    sieve = [True] * (hi+1)
    for p in range(2, hi+1):
        if sieve[p]:
            for j in range(2*p, hi+1, p):
                sieve[j] = False
            yield p


if __name__ == '__main__':
    import oj

    # 100번째 소수들까지 사전에 구해둡니다.
    # 100번째 소수는 541 입니다. (https://prime-numbers.info/number/100th-prime)
    primes = list(prime_generator(hi=541))

    # 1. Problem 객체를 생성합니다.
    problem = oj.Problem('prime_numbers')

    # 입력 데이터로는 1이상 100 이하의 정수를 일부 사용하며, 테스트케이스 번호는 1부터 세어봅니다.
    for testcase_no, input_data in enumerate(range(1, 101, 3), start=1):
        # 2-1. input_data에 대한 올바른 output_data를 구합니다.
        output_data = primes[input_data-1] # 1-base에서 0-base로 보정

        # 2-2. TestCase 객체를 생성합니다.
        tc = oj.TestCase(
            id=str(testcase_no),
            input=str(input_data),
            output=str(output_data),
        )

        # 2-3. 테스트케이스를 문제에 추가합니다.
        problem.add_testcase(tc)

    # 3. 문제의 정보와 테스트케이스를 prime_numbers.zip 파일로 출력합니다.
    problem.extract_as_zip()
```
