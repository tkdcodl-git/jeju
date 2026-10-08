# -*- coding: utf-8 -*-
"""TASK 시작 → 차량 출발 → 다음 장소 도착 타임라인"""
DAYS = {
 'd1':[
  ('ulsan_arrival','12:35', 25, 10,'차량'),
  ('jamae',        '13:10', 60, 10,'차량'),
  ('seoul_join',   '14:35', 15, 60,'차량'),
  ('activekart',   '16:00',120, 25,'차량'),
  ('suksungdo',    '18:25', 90,  5,'차량'),
  ('hanaro',       '20:00', 30,  5,'차량'),
  ('stay_night',   '20:35',  0,  0, None),
 ],
 'd2':[                                       # 2026-10-08 (4차): 10시 출발, 동화마을 먼저
  ('breakfast2',   '09:30', 30, 65,'차량'),   # 애월 → 송당 약 1시간 5분
  ('seongsanbom',  '11:05', 60,  5,'도보'),   # 동화마을 안이라 걸어서 바로
  ('donghwa',      '12:10',120, 15,'차량'),   # 2시간 · 에코랜드까지 번영로 15분
  ('ecoland',      '14:25',120, 50,'차량'),   # 2시간 (매표마감 16:30) · 서귀포까지 50분
  ('ssangdungi',   '17:15', 90,  5,'도보'),   # 올레시장 입구라 걸어서
  ('olle_market',  '18:50', 45, 60,'차량'),
  ('stay_night2',  '20:35',  0,  0, None),
 ],
 'd3':[                                       # 2026-10-08: 전체 30분 늦춤
  ('breakfast3',   '09:00', 40,  0, None),
  ('checkout3',    '09:40', 10, 40,'차량'),
  ('oneandonly',   '10:30', 35,  5,'도보'),
  ('sanbangsan',   '11:10', 40, 22,'차량'),
  ('donsuyug',     '12:15', 45, 70,'차량'),   # 13:00 까지 식사 → 바로 공항
  ('airport',      '14:10', 50,  0, None),
  ('departure',    '15:55',  0,  0, None),
 ],
}
SHORT={'jamae':'자매국수','seoul_join':'제주공항','activekart':'액티브카트','rainyday':'숙소',
 'suksungdo':'숙성도 애월점','hanaro':'하나로마트','stay_night':'숙소','stay_night2':'숙소',
 'ecoland':'에코랜드','seongsanbom':'성산봄','donghwa':'동화마을','ssangdungi':'쌍둥이횟집','checkout3':'체크아웃','sanbangsan':'산방산',
 'oneandonly':'원앤온리','donsuyug':'돈수육','olle_market':'올레시장','airport':'제주공항',
 'departure':'탑승게이트'}
SHORT_SELF={'ulsan_arrival':'제주공항','jamae':'자매국수','seoul_join':'제주공항',
 'activekart':'액티브카트','suksungdo':'숙성도','hanaro':'하나로마트','breakfast2':'숙소',
 'ecoland':'에코랜드','seongsanbom':'성산봄','donghwa':'동화마을','ssangdungi':'쌍둥이횟집','breakfast3':'숙소','checkout3':'숙소',
 'oneandonly':'원앤온리','sanbangsan':'산방산','donsuyug':'돈수육','olle_market':'올레시장',
 'airport':'제주공항'}
COLOR={'d1':('#E0906B','#F0BE9E'),'d2':('#5FAE99','#93CDBB'),'d3':('#7C9FD1','#AEC6E4')}

import geomap as _g
def m(t): h,i=t.split(':'); return int(h)*60+int(i)
def hm(v): return f'{v//60:02d}:{v%60:02d}'
def lab(v): return (f'{v//60}시간 {v%60}분' if v>=60 and v%60 else (f'{v//60}시간' if v>=60 else f'{v}분'))

def build():
    out={}
    for day,rows in DAYS.items():
        c=COLOR[day]
        for i,(pid,st,dur,mv,mode) in enumerate(rows):
            nxt=rows[i+1] if i+1<len(rows) else None
            if nxt:
                gap=m(nxt[1])-m(st); slack=max(0,gap-dur-mv); total=dur+slack+mv
                segs=[(k,v,l,round(v*100.0/total,2)) for k,v,l in
                      (('stay',dur,'머무는 시간'),('slack',slack,'여유'),
                       ('move',mv,(mode or '')+' 이동')) if v>0]
                e=nxt[1]; n=SHORT.get(nxt[0],nxt[0])
                if mv>0:
                    d=hm(m(nxt[1])-mv)
                    dm=(mode or '차량')+' 출발'
                    dp=round((dur+slack)*100.0/total,2)
                    dl=round(min(max(dp,9.0),91.0),2)      # 라벨은 살짝 안쪽으로 제한
                else:
                    d=dp=dl=dm=None
            else:
                if dur<=0: continue
                segs=[('stay',dur,'머무는 시간',100.0)]; e=n=d=dp=dl=dm=None
            mp=None
            if nxt and mv>0 and pid in _g.GEO and nxt[0] in _g.GEO:
                GA,GB=_g.GEO[pid],_g.GEO[nxt[0]]
                A=_g.prj(*GA); B=_g.prj(*GB)
                dkm=_g.km(GA,GB)
                near = (mode=='도보') or (dkm < _g.NEAR_KM)
                mp={'k':'near' if near else 'map','vi':'🚶' if mode=='도보' else '🚐',
                    'an':SHORT_SELF.get(pid,pid),'mvm':(mode or '차량'),'mvt':lab(mv),
                    'km':_g.dist_label(dkm),
                    'nl':'바로 옆' if mode=='도보' else '아주 가까움'}
                if near:
                    # 가까운 거리는 지도 대신 짧은 트랙 — 멀어 보이지 않게
                    mp.update(ax=292,ay=52,bx=408,by=52,rd='M292,52 Q350,34 408,52',
                              vb='0 0 700 132',z=1,tx=0,ty=0)
                else:
                    d0=((B[0]-A[0])**2+(B[1]-A[1])**2)**.5 or 1
                    z=min(6.0,max(1.0,200.0/d0))          # 두 점이 화면에서 충분히 벌어지게
                    cx,cy=(A[0]+B[0])/2,(A[1]+B[1])/2
                    tf=lambda q:(round((q[0]-cx)*z+350,1), round((q[1]-cy)*z+204,1))
                    ad=tf(A); bd=tf(B)
                    # 바다를 지나지 않는 경로를 섬 좌표계에서 구한 뒤 화면 좌표로 변환
                    pts=[tf(q) for q in _g.route_pts(A,B)]
                    rd='M'+str(pts[0][0])+','+str(pts[0][1])+''.join(
                        'L%s,%s'%(q[0],q[1]) for q in pts[1:])
                    mp.update(ax=ad[0],ay=ad[1],bx=bd[0],by=bd[1],rd=rd,
                              vb='0 0 700 408',z=round(z,4),
                              tx=round(350-cx*z,1),ty=round(204-cy*z,1))
            out[pid]={'s':st,'d':d,'dm':dm,'e':e,'n':n,'dp':dp,'dl':dl,'g':segs,'c':c,'mp':mp}
    return out

def js(o):
    parts=[]
    for pid,x in o.items():
        g=','.join('{k:"%s",l:"%s",m:"%s",w:"%s%%"}'%(k,l,lab(v),w) for k,v,l,w in x['g'])
        s=f's:"{x["s"]}"'
        if x['e']: s+=f',e:"{x["e"]}",n:"{x["n"]}"'
        if x['d']: s+=f',d:"{x["d"]}",dm:"{x["dm"]}",dp:"{x["dp"]}%",dl:"{x["dl"]}%"'
        if x.get('mp'):
            p_=x['mp']
            s+=(',mp:{k:"%s",ax:%s,ay:%s,bx:%s,by:%s,rd:"%s",vb:"%s",z:%s,tx:%s,ty:%s,vi:"%s",an:"%s",mvm:"%s",mvt:"%s",km:"%s",nl:"%s"}'
                % (p_['k'],p_['ax'],p_['ay'],p_['bx'],p_['by'],p_['rd'],p_['vb'],
                   p_['z'],p_['tx'],p_['ty'],p_['vi'],p_['an'],p_['mvm'],p_['mvt'],p_['km'],p_['nl']))
        s+=f',c:["{x["c"][0]}","{x["c"][1]}"],g:[{g}]'
        parts.append(f'{pid}:{{{s}}}')
    return 'var LEG={'+','.join(parts)+'};'

if __name__=='__main__':
    o=build()
    for pid,x in o.items():
        seg=' + '.join(f'{l}{v}분' for k,v,l,w in x['g'])
        print(f'{pid:14s} {x["s"]} →{x["d"] or " -  "}({x["dp"] or "-"}%) →{x["e"] or " -  "} {x["n"] or "":10s} | {seg}')
