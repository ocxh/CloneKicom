#html패턴
import re

pat = r"<\s*html\b|\bdoctype\b<\s*head\b|<\s*meta\b|\bhref\b|\blink\b<\s*body\b|<\s*script\b|<\s*iframe\b|<\?(php\b)?"
p_html = re.compile(pat, re.IGNORECASE)
#script패턴
pat = '<script.*?>[\d\D]*?</script>|<iframe.*?>[\d\D]*?</iframe>\<\?(php\b)?[\d\D]*?\?>'
p_script = re.compile(pat, re.IGNORECASE)

def format(filehandler, filename):
	fileformat = {}
	
	mm = filehandler
	
	buf = mm[:4096] #4096byte 읽기
	if is_textfile(buf): #텍스트 파일 여부 확인
		ret = p_html.findall(buf) #html 키워드 찾기
		
		if len(ret) >= HTML_KEY_CNT:
			fileformat['keyword'] = list(set(ret)) #존재하는 HTML키워드
			
			ret = {'ff_html':fileformat}
	
return ret