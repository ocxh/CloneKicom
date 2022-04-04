import re

p_text = re.compile(r'/[a-z0-9]|[ \[\]{}()<>?|`~!@#$%^&*-_+=,.;:\"\'\]/g')

def is_textfile(buf):
	n_buf = len(buf)
	n_text = len(p_text.findall(buf))
	
	if n_text / float(n_buf) > 0.8: #80% 이상 글자일 경우
		return True
	return False