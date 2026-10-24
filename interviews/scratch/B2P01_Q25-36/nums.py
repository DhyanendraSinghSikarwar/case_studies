# Q25/26
d,L,H,Hkv,hd,ffn,V=4096,32,32,8,128,14336,128256
emb=V*d
attn=d*H*hd+2*d*Hkv*hd+H*hd*d
mlp=3*d*ffn
norms=2*d
per=attn+mlp+norms
tot=2*emb+L*per+d
print("emb",emb/1e6,"attn/layer",attn/1e6,"mlp/layer",mlp/1e6,"total",tot/1e9)
print("attn share",L*attn/tot,"mlp share",L*mlp/tot,"emb share",2*emb/tot)
print("tied total",(tot-emb)/1e9)
# 7B old vocab 32000
print("v32k emb",32000*4096/1e6)
print("lm head flops/token",2*d*V/1e9,"GFLOP; body flops/token",2*(L*per)/1e9)
# Q32
F=1000e12; BW=3.35e12
print("ridge",F/BW)
P=8e9; wbytes=2*P
for B in [1,8,32,64,128,256,512]:
    flops=2*P*B; t_c=flops/F; t_m=wbytes/BW
    t=max(t_c,t_m)
    print(B,"AI",flops/wbytes,"t_mem ms",t_m*1e3,"t_cmp ms",t_c*1e3,"tok/s",B/t, "bound","mem" if t_m>t_c else "compute")
# with KV cache: ctx 4096 per seq, Llama3-8B GQA kv bytes/token
kvtok=2*L*Hkv*hd*2
print("kv bytes/token",kvtok, "per seq 4k MB",kvtok*4096/1e6)
for B in [1,8,32,64,128,256,512]:
    bytes_=wbytes+B*kvtok*4096
    t_m=bytes_/BW; t_c=2*P*B/F
    print(B,"with KV: t_mem ms",t_m*1e3,"t_cmp ms",t_c*1e3,"tok/s",B/max(t_m,t_c))
# Q33
dc,dr,nh,dh,Lm=512,64,128,128,60
mha=2*nh*dh; gqa8=2*8*dh; mla=dc+dr
print("per tok per layer elems MHA",mha,"GQA8",gqa8,"MLA",mla, "MHA/MLA",mha/mla,"GQA/MLA",gqa8/mla,"equiv groups",mla/(2*dh))
ctx=128000
for n,e in [("MHA",mha),("GQA8",gqa8),("MLA",mla)]:
    print(n,"KB/token",e*Lm*2/1e3,"GB for 128k",e*Lm*2*ctx/1e9)
