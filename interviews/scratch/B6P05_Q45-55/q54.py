N=1_000_000; wrong=0.30
big_c,big_acc=0.020,0.92
small_c,small_acc=0.002,0.80
esc=0.35; keep=1-esc
small_keep_acc=0.90; big_esc_acc=0.88
def total(c,acc): return c+(1-acc)*wrong
large=total(big_c,big_acc); small=total(small_c,small_acc)
inf_c=small_c+esc*big_c           # small model runs on every query; large model only on escalated
casc_acc=keep*small_keep_acc+esc*big_esc_acc
casc=total(inf_c,casc_acc)
print(f"large-only: infer {big_c:.4f} + error {(1-big_acc)*wrong:.4f} = {large:.4f} per query")
print(f"small-only: infer {small_c:.4f} + error {(1-small_acc)*wrong:.4f} = {small:.4f} per query")
print(f"cascade:    infer {inf_c:.4f} + error {(1-casc_acc)*wrong:.4f} = {casc:.4f} per query; accuracy {casc_acc:.4f}")
assert round(large,4)==0.0440 and round(small,4)==0.0620 and round(inf_c,4)==0.0090
assert round(casc_acc,3)==0.893 and round(casc,4)==0.0411
print("per month:",round(large*N),round(small*N),round(casc*N),"; cascade saves vs large:",round((large-casc)*N),f"({(large-casc)/large:.1%})")
assert round((large-casc)*N)==2900
# break-even cost of a wrong answer
w=(inf_c-big_c)/((1-big_acc)-(1-casc_acc))  # inf_c+(1-casc_acc)w = big_c+(1-big_acc)w
print(f"wrong-answer cost at which cascade = large-only: {w:.4f}")
assert round(w,4)==0.4074
for ww in (0.2,0.3,w,0.5,1.0):
    l=big_c+(1-big_acc)*ww; c=inf_c+(1-casc_acc)*ww
    print(f"  wrong costs {ww:.4f}: large {l:.4f}, cascade {c:.4f}, cheaper: {'cascade' if c<l-1e-9 else 'large' if l<c-1e-9 else 'tie'}")
assert (inf_c+(1-casc_acc)*0.5)>(big_c+(1-big_acc)*0.5)
# implied accuracy of each model on the other slice (consistency with the overall rates)
small_on_esc=(small_acc-keep*small_keep_acc)/esc
big_on_keep=(big_acc-esc*big_esc_acc)/keep
print(f"\nimplied small-model accuracy on escalated queries: {small_on_esc:.3f}; large on kept queries: {big_on_keep:.3f}")
assert 0<small_on_esc<big_esc_acc and big_on_keep<1
print("value of 1 accuracy point per month:",round(0.01*wrong*N))
assert round(0.01*wrong*N)==3_000
print("slice accuracy sum check:",round(keep*small_keep_acc,3),round(esc*big_esc_acc,3))
assert round(small_on_esc,3)==0.614 and round(big_on_keep,3)==0.942
