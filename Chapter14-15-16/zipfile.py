import zipfile

if zipfile.is_zipfile('1.zip'):
    print("===zip파일===")
    zf = zipfile.ZipFile('1.zip', 'r')
    
    zip_li = zf.namelist()
    print(zip_li)
    print(zf[0:4]) #zip파일 헤더('PK\x03\x04')

    buf = zf.read('test1.txt') #압축 파일 내부의 test1.txt 파일 읽기
    print(buf) 

    #zf.write (ZIP파일로 압축)
