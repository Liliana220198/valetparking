# linear_congruential:
print("\nlinear_congruential: ")


def linear_Congruential_Method(Xo, a, c, m, randomNums, noOfRandomNums):
    randomNums[0] = Xo

    for i in range(1, noOfRandomNums):
        randomNums[i] = ((randomNums[i - 1] * a) + c) % m


if __name__ == '__main__':
    Xo = 37
    a = 19
    c = 33
    m = 100
    noOfRandomNums = 7
    randomNums = [0] * (noOfRandomNums)

    linear_Congruential_Method(Xo, a, c, m, randomNums, noOfRandomNums)

    for i in randomNums:
        print(i, end=" ")
