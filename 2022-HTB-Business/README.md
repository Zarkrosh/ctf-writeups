# Write-up HTB Business CTF 2022

- [Write-up HTB Business CTF 2022](#write-up-htb-business-ctf-2022)
  - [Forensics - SquatBot](#forensics---squatbot)
    - [Unintended solution: search for crypted received data](#unintended-solution-search-for-crypted-received-data)
    - [Intended solution: dump inode of anonymous file](#intended-solution-dump-inode-of-anonymous-file)

## Forensics - SquatBot 
🩸 **First Blood**

> An AWS development company that provides full-scale cloud consulting and AWS application development services has recently been compromised. They try to maintain cyber hygiene by applying numerous procedures and safe development practices. To this day, they are unaware of how malware could penetrate their defenses. We have managed to obtain a memory dump and isolate the compromised server. Can you analyze the dump and examine the malware's behavior?

The challenge download included a memory dump and a ZIP file from a custom Ubuntu profile for Volatility. After putting the custom Volatility profile on the volatility/plugins/overlays/linux directory, I could analyze the memory dump.

The linux_bash command showed that the repository https://github.com/bootooo3/boto3 was cloned and installed with Python. 



<p align="center">
  <img src="images/squatbot_1.png"><br>
  <code>vol.py -f dump.mem --profile=LinuxUbuntu_4_15_0-184-generic_profilex64 linux_bash</code>
</p>


Taking a look at the repository, I saw that it was new and had no stars. However, it had a nice formatted README claiming:

> Boto3 is the Amazon Web Services (AWS) Software Development Kit (SDK) for Python, which allows Python developers to write software that makes useof services like Amazon S3 and Amazon EC2. You can find the latest, mostup to date, documentation at our doc site, including a list of services that are supported.

I found that the original boto3 project was located on https://github.com/boto/boto3, so it appeared to be a clone with some malicious code inside that tried to exploit a typosquatting error from a developer. The file CHANGELOG.rst from the fake repository said that the last version was 1.24.9. I cloned the original repository and went back to a commit from that version (original was on 1.24.31).

```
git clone https://github.com/boto/boto3
git reset --hard 39aa8e2ebe26105a3153f1df01e27bf7fad4fe74
```

Now I can compare the contents from both fake and original repositories with tools like Meld, for example.

<p align="center">
  <img src="images/squatbot_2.png">
</p>

Apart from some git related differences, setup.py was detected to have different contents: on the first line, some B64 was being decoded and executed.

<p align="center">
  <img src="images/squatbot_3.png">
</p>
<p align="center">
  <img src="images/squatbot_4.png">
</p>


Analyzing the code, I see that a connection to a certain host and port is made. Then, syscall 319 is called. Taking a look into the documentation, I see that it's memfd_create.

<p align="center">
  <img src="images/squatbot_5.png">
</p>


Then, the malware enters a loop where it receives data from the connection, XOR that data with decimal key 239 and writes the resulting bytes to the created anonymous file on memory. Finally it does a C2 callback to files.pypi-install.com with some info of the compromised host and runs the malware if C2 returns "Ok".

The host from where the XORed malware was received was down, so the only way to see what was run on the machine was to recover it from memory.






<br>

### Unintended solution: search for crypted received data

At this point I blocked for a while, enumerating files looking for file descriptors in /proc, listing and dumping proc_maps from the python3 and other processes, looking for loaded ELFs in dynamic sections, unsuccessfully.

After some time, the idea that the received data connection might still be available in the memory came to my mind, as the python3 process was still running. This data should be encrypted with key 239, and instead of keep dumping things I just decided to XOR the entire memory dump with that key. If the data was still there, I should be able to find some data like ELF headers, strings and so. And I did.

<p align="center">
  <img src="images/squatbot_6.png">
</p>


However, the found ELF was not complete. Instead several pieces were scattered in blocks of 0x5A0 bytes with some rubbish bytes in middle (0x1E0 blocks), apparently in reverse order:


<p align="center">
  <img src="images/squatbot_7.png">
</p>

<p align="center">
  <img src="images/squatbot_8.png">
</p>

So I recovered these blocks and write them to a file.

<p align="center">
  <img src="images/squatbot_9.png">
</p>

Then I loaded it on IDA, apart from an error seemed to be correct and I analyzed the function that referenced the "/bin/sh" string. There I found a loop that XORed some data with the 0x1F key.

<p align="center">
  <img src="images/squatbot_10.png">
</p>

That decrypted data was the flag:

<p align="center">
  <img src="images/squatbot_11.png">
</p>






<br>

### Intended solution: dump inode of anonymous file

After the end of the CTF, I talked with the challenge's creator ([thewildspirit](https://twitter.com/_thewildspirit)) about my unintended solution, and told me that the intended solution was even easier than what I did 😂.

At the beginning I was on the right way, trying to recover the content from the anonymous file created by the malware, but I struggled with Volatility's functionalities and didn't go low level.

The intended solution was to locate the anonymous file descriptor, parse its structure and use the inode number of the file to dump it using the find_files plugin.

For it, I used linux_lsof plugin to dump all the open file descriptors for all the processes:

<code>vol.py -f dump.mem --profile=LinuxUbuntu_4_15_0-184-generic_profilex64 linux_lsof > linux_lsof.txt</code>

I saw that the python3 process had 4 file descriptors opened: 0-2 (stdin/stdout/stderr on pseudo-terminal) and a 4th file descriptor with no path (the anonymous file created). It seems that on a memory dump, the path of file descriptors for anonymous files matches the regex <code>\\/:\\[\d+\\]</code>.

Then I spawned a volshell on the memory dump, changed the context to the python3 process (PID 1451) and dumped the inode of all the files referenced by the file descriptors. The commands I used were deduced from [Volatility's code](https://github.com/volatilityfoundation/volatility/blob/master/volatility/plugins/linux/lsof.py). Using the last inode value, I could dump the content of the anonymous file:

<p align="center">
  <img src="images/squatbot_12.png">
</p>

This ELF was completely correct, unlike the one that I dumped my way (function names were shown):
<p align="center">
  <img src="images/squatbot_13.png">
</p>