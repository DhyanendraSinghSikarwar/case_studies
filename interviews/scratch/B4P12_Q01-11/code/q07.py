import unittest
GATES=["lineage","development","validation","approval","shadow","deployment","monitoring","retired"]
EVID={"development":["lineage_id"],"validation":["dev_report","lineage_id"],
 "approval":["validation_report","validator","approver"],
 "shadow":["approval_id","approver"],
 "deployment":["shadow_report","deployer"],
 "monitoring":["deploy_id"],"retired":["retire_reason","approver"]}
class Refused(Exception): pass
class Model:
    def __init__(s): s.state="lineage"; s.log=[]; s.ev={}
    def promote(s,to,**ev):
        i=GATES.index(s.state)
        if to!=GATES[i+1] if i+1<len(GATES) else True: raise Refused(f"cannot skip {s.state}->{to}")
        for k in EVID.get(to,[]):
            if not ev.get(k): raise Refused(f"missing evidence '{k}' for {to}")
        # separation of duties
        if to=="approval" and ev["approver"] in (ev["validator"],ev.get("builder")): raise Refused("approver must differ from validator/builder")
        if to=="deployment" and ev["deployer"]==s.ev.get("approver"): raise Refused("deployer must differ from approver")
        s.state=to; s.ev.update(ev); s.log.append((to,dict(ev)))
class T(unittest.TestCase):
    def full(s):
        m=Model()
        m.promote("development",lineage_id="L1"); m.promote("validation",dev_report="D",lineage_id="L1")
        m.promote("approval",validation_report="V",validator="vera",approver="al",builder="bo")
        return m
    def test_happy(s):
        m=s.full(); m.promote("shadow",approval_id="A1",approver="al")
        m.promote("deployment",shadow_report="S",deployer="dee"); m.promote("monitoring",deploy_id="X"); s.assertEqual(m.state,"monitoring")
    def test_missing(s):
        m=Model()
        with s.assertRaises(Refused): m.promote("development")
    def test_skip(s):
        m=Model()
        with s.assertRaises(Refused): m.promote("approval",validation_report="V",validator="v",approver="a")
    def test_sod_approver(s):
        m=Model(); m.promote("development",lineage_id="L"); m.promote("validation",dev_report="D",lineage_id="L")
        with s.assertRaises(Refused): m.promote("approval",validation_report="V",validator="vera",approver="vera")
    def test_sod_deployer(s):
        m=s.full(); m.promote("shadow",approval_id="A",approver="al")
        with s.assertRaises(Refused): m.promote("deployment",shadow_report="S",deployer="al")
    def test_state_unchanged_on_refusal(s):
        m=Model()
        try: m.promote("development")
        except Refused: pass
        s.assertEqual(m.state,"lineage")
if __name__=="__main__": unittest.main(verbosity=2)
