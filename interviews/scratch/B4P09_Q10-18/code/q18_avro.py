# Real fastavro run. No Schema Registry server was run: compatibility is checked by the reader/writer resolution only.
import io, fastavro
from fastavro import schemaless_writer, schemaless_reader
old = {"type":"record","name":"Txn","fields":[{"name":"card","type":"string"},{"name":"amount","type":"double"}]}
new_ok = {"type":"record","name":"Txn","fields":[{"name":"card","type":"string"},{"name":"amount","type":"double"},
          {"name":"channel","type":"string","default":"unknown"}]}
new_bad = {"type":"record","name":"Txn","fields":[{"name":"card","type":"string"},{"name":"amount","type":"double"},
          {"name":"channel","type":"string"}]}
renamed = {"type":"record","name":"Txn","fields":[{"name":"card_id","type":"string"},{"name":"amount","type":"double"}]}
retyped = {"type":"record","name":"Txn","fields":[{"name":"card","type":"string"},{"name":"amount","type":"string"}]}
buf = io.BytesIO(); schemaless_writer(buf, old, {"card":"c1","amount":12.5}); data = buf.getvalue()
print("fastavro", fastavro.__version__, "| bytes written with OLD schema:", len(data))

def read(label, reader, writer=old, payload=data):
    try:
        print(f"{label:34s} ->", schemaless_reader(io.BytesIO(payload), writer, reader))
    except Exception as e:
        print(f"{label:34s} -> FAIL {type(e).__name__}: {e}")
read("new reader, field with default", new_ok)
read("new reader, field NO default", new_bad)
read("reader renamed card->card_id", renamed)
read("reader retyped amount->string", retyped)
# forward direction: new writer, old reader (old consumer ignores the extra field)
buf2 = io.BytesIO(); schemaless_writer(buf2, new_ok, {"card":"c2","amount":3.0,"channel":"upi"})
read("old reader of NEW data (forward)", old, writer=new_ok, payload=buf2.getvalue())
# reader that drops a field the writer had
only_card = {"type":"record","name":"Txn","fields":[{"name":"card","type":"string"}]}
read("reader removes amount field", only_card)
# promotion: int -> long is allowed by the Avro spec
w = {"type":"record","name":"N","fields":[{"name":"x","type":"int"}]}; r = {"type":"record","name":"N","fields":[{"name":"x","type":"long"}]}
b = io.BytesIO(); schemaless_writer(b, w, {"x": 7})
read("int -> long promotion", r, writer=w, payload=b.getvalue())
