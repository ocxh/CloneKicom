#압축 헤더만 추가되기에 오히려 크키가 늘어나는 모습
import zlib

s = "abcdefg"
print(len(s))


t = zlib.compress(s.encode(encoding='utf-8'))
print(len(t))