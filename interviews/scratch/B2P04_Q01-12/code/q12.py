BOS, EOS = "<s>", "</s>"
def render(messages, add_generation_prompt=False):
    out = BOS
    for m in messages: out += f"<|{m['role']}|>\n{m['content']}{EOS}\n"
    if add_generation_prompt: out += "<|assistant|>\n"
    return out
msgs = [{"role": "user", "content": "2+2?"}, {"role": "assistant", "content": "4"}]
train = render(msgs)
infer_ok = render(msgs[:1], add_generation_prompt=True)
infer_bad = "User: 2+2?\nAssistant:"          # hand-written, different from training
print("TRAIN string :", repr(train)); print("INFER (match):", repr(infer_ok)); print("INFER (bad)  :", repr(infer_bad))
print("train prefix == inference prompt:", train.startswith(infer_ok), "| bad:", train.startswith(infer_bad))
# EOS check: which positions are supervised in the response?
print("response label text with EOS   :", repr("4" + EOS))
print("response label text WITHOUT EOS:", repr("4"), "-> model never sees a stop signal, rambles on")
# toy generation: model that learned a stop token only if it was trained with it
def generate(trained_with_eos, max_tokens=8):
    out = []
    for i in range(max_tokens):
        if trained_with_eos and i == 1: out.append(EOS); break
        out.append("4" if i == 0 else "...more text")
    return out
print("with EOS   :", generate(True)); print("without EOS:", generate(False))
