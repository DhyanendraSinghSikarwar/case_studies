def out(n,k,s=1,p=0): return (n+2*p-k)//s+1
print(out(224,3,1,1), out(224,3,2,1), out(224,7,2,3), out(32,2,2,0))
# params: conv 3x3, 64->128 vs dense on same 32x32 maps
print("conv params",3*3*64*128+128)
print("dense equiv",(32*32*64)*(32*32*128))
# receptive field: stacked 3x3 stride-1 convs
rf=1
for _ in range(3): rf+=2
print("RF of 3 stacked 3x3:",rf)
