"""
Функция-обработчик строки с разделителями '/n' для её вывода на дисплей 4х20:

1) Удаляет символы после 20-ого в каждой строке и символы '/n'
2) Заполняет все пустые знакоместа пробелами

"""

def strFit_4x20 (in_str:str):
    s = 0 #Счетчик символов в текущей строке
    l = 0 #Счетчик строк
    i = 0 #Счетчик символов в in_str
    out_str = ''

    for symbol in in_str:
        if l <=3:
            if s <= 19 and symbol != '\n': #Запись при отсутствии переполнения
                out_str += in_str[i]
                s += 1
            i += 1
            if symbol == '\n': #Признак конца строки по символу перехода
                while s <= 19:  #Заполняем пробелами оставшееся место
                    out_str += ' '
                    s += 1
                s = 0
                l += 1
    while len(out_str)<80:
        out_str += ' '
    
    return out_str

#Tests
if __name__ == "__main__":
    input_string = "AAA45678901234567890AAA\nBBB45678901234567890AAA\nCCC45678901234567890AAA\nDDD45678901234567890AAA\nEEE45678901234567890AAA"
    output_string = strFit_4x20(input_string)
    print(output_string)
    print (type(input_string))
    input_string = "AAA\nBBB\nCCC\nDDD\nEEE"
    output_string = strFit_4x20(input_string)
    print(output_string)
    input_string = "AAA\nBBB"
    output_string = strFit_4x20(input_string)
    print(output_string)
    print("А теперь вызовем ошибку")
    input_string = 100
    output_string = strFit_4x20(input_string)

