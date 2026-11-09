
import sys,json,re
src=open(sys.argv[1]).read()
tests=json.load(open(sys.argv[2]))
ns={}
out=[]
try:
    exec(compile(src,'<artifact>','exec'),ns)
except SyntaxError as e:
    print(json.dumps({'load_error':'SyntaxError: %s'%e})); sys.exit()
except Exception as e:
    print(json.dumps({'load_error':'%s: %s'%(type(e).__name__,e)})); sys.exit()
for expr,expected in tests:
    try:
        val=eval(expr,ns)
        got=repr(val)
        out.append({'expr':expr,'expected':expected,'got':got,'ok':got==expected})
    except Exception as e:
        out.append({'expr':expr,'expected':expected,'got':None,'error':'%s: %s'%(type(e).__name__,e),'ok':False})
print(json.dumps({'tests':out}))
