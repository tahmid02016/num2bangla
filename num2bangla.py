#!/usr/bin/env python

"""Provides functionality to convert numbers into bangla words

-------------------------------------------------------------------------------

`num2bangla` is a module that provides functionality to convert numbers like `123` to Bangla words like `এক শত তেইশ`. Just call `num2word` function with the number as argument.

num2word takes only one argument as input, the number to convert to word. Input can be int or float or str type.

Example:
    >>> print (num2word(123))
    'এক শত তেইশ'

"""


import json


with open('BanglaWords.json') as fp:
    bangla_words = json.load(fp)


numeric_words = bangla_words['numeric_words']
units = bangla_words['units']


def sanitize(raw_input):
    """Convert raw input into int or float object so that other functions can handle it easily"""
    if isinstance(raw_input, str):
        if '.' in num:
            number = float(raw_input)
        else:
            number = int(raw_input)
        return number
    elif isinstance(raw_input, (int, float)):
        return raw_input
    else:
        raise ValueError('Input must be int or float or str that can be converted into int or float')

def smallint2word(num):
    """Convert integers numbers less than 10^7 into Bangla words"""
    if num < 0:
        word = 'ঋণাত্মক '
        num = abs(num)
    else:
        word = ''
    segments = dict()
    segments['কোটি'] = num//10000000
    num = num % 10000000
    segments['লক্ষ'] = num//100000
    num = num % 100000
    segments['হাজার'] = num//1000
    num = num % 1000
    segments['শতক'] = num//100
    num = num % 100
    segments['একক'] = num
    
    for segment in segments:
        if segments[segment]:
            word = word + numeric_words[str(segments[segment])] + \
                " " + units[segment] + " "
    return word.strip()

def int2word(num):
    """Convert integer numbers into Bangla words"""
    num = str(num)[::-1]
    low = 0
    high = 7
    length = len(num)
    splited = []
    if length > high:
        splited.append(num[low:high])
        low = high
        high += 7
    if low < length:
        splited.append(num[low:])
    result = ''
    for part in splited:
        tmp = smallint2word(int(part[::-1]))
        if tmp and part is splited[0]:
            result = tmp
        elif tmp:
            result = tmp + ' কোটি ' + result
    return result
    
def float2word(num):
    """Convert floating point numbers into Bangla words"""
    _num = str(num)
    p1, p2 = map(int, _num.split('.'))
    p1_word = int2word(p1)
    p2_word = int2word(p2)
    full_word = p1_word + ' দশমিক ' + p2_word
    return full_word.strip()

def num2word(number):
    """Convert number into Bangla words.
    
    @input number
    @input_type: int/float/str
    """
    num = sanitize(number)
    if isinstance(num, int):
        word = int2word(num)
    else:
        word = float2word(num)
    return word


if __name__ == '__main__':
    # code here
