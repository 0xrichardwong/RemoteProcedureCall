import math

# floor(double x): 10 進数 x を最も近い整数に切り捨て、その結果を整数で返す。
def floor(x):
    return math.floor(x)

# nroot(int n, int x): 方程式 rn = x における、r の値を計算する。
def nroot(n, x):
    if x < 0 and n % 2 == 0:
        raise ValueError("Error")
    return x ** (1 / n)

# reverse(string s): 文字列 s を入力として受け取り、入力文字列の逆である新しい文字列を返す。
def reverse(s):
    reversed = ''
    for i in range(len(s)-1, -1, -1):
        reversed += s[i]
    return reversed
    
# validAnagram(string str1, string str2): 2 つの文字列を入力として受け取り，2 つの入力文字列が互いにアナグラムであるかどうかを示すブール値を返す。
def validAnagram(s1, s2):
    if len(s1) != len(s2):
        return False

    count1 = {}
    count2 = {}

    for char in s1:
        count1[char] = count1.get(char, 0) + 1
    
    for char in s2:
        count2[char] = count2.get(char, 0) + 1

    return count1 == count2

# sort(string[] strArr): 文字列の配列を入力として受け取り、その配列をソートして、ソート後の文字列の配列を返す。
def sort(s):
    return sorted(s) 