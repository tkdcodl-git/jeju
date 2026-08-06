# 제주 2박 3일 · 9명 가족여행 일정표

빌드 없는 **정적 사이트**입니다. `index.html`이 있는 이 폴더가 그대로 배포 루트입니다.

---

## ⚠️ 404: NOT_FOUND 가 났다면

Vercel이 `index.html`을 **루트에서 찾지 못한 것**입니다. 거의 항상 아래 둘 중 하나입니다.

**1) 폴더가 한 겹 더 들어가 있다**

깃 저장소나 업로드한 폴더가 이런 모양이면 루트에 `index.html`이 없어서 404가 납니다.

```
저장소/
└── jeju-vercel/        ← 한 겹 더 들어감
    └── index.html
```

해결은 두 가지 중 하나입니다.

- 저장소 루트로 파일을 옮긴다 (`jeju-vercel/` 안의 내용을 한 단계 위로)
- 또는 Vercel → **Settings → Build and Deployment → Root Directory**에 `jeju-vercel` 을 입력하고 재배포

CLI로 올릴 때는 **반드시 `index.html`이 있는 폴더 안에서** `vercel` 을 실행하세요.

```bash
cd jeju-vercel      # ← 이 폴더 안에서
vercel --prod
```

**2) 프레임워크 프리셋이 잘못 잡혔다**

Vercel이 Vite·Next 등으로 오인하면 빌드를 돌리고 비어 있는 `dist`를 서빙해 404가 납니다.
Settings → **Framework Preset = Other**, **Build Command 비움**, **Output Directory 비움**으로 두세요.
이번 `vercel.json`에 `framework: null`, `buildCommand: null`, `outputDirectory: "."`를 명시해 두었으니 새로 배포하면 자동으로 교정됩니다.

---

## 로컬에서 그냥 열어 보고 싶을 때

`index.html`만 따로 내려받으면 **열리지 않습니다.** `assets/` 폴더가 같은 위치에 있어야 합니다.

```
같은 폴더에 나란히 ↓
index.html
assets/
```

폴더 없이 파일 하나로 보려면 **`jeju-single.html`** 을 쓰세요. CSS·JS·사진이 모두 안에 들어 있어서
어디에 두고 더블클릭해도 열리고, 카카오톡·메일로 파일 자체를 보내도 상대방이 바로 볼 수 있습니다.
(단, 이 파일은 배포용이 아닙니다. Vercel에는 `jeju-vercel` 폴더를 올리세요.)

---

## 구성

```
index.html                  6KB   껍데기 + 메타태그 + 부팅 가드
assets/app.*.js           169KB   React 앱 (해시 파일명 → 영구 캐시)
assets/styles.*.css        47KB   Tailwind + 회색 테마 + 데스크톱 레이아웃
assets/img/*.webp         371KB   만장굴·에코랜드 사진 (상세창 열 때만 로드)
og.jpg                    244KB   카카오톡·슬랙 공유 미리보기 (1200×630)
favicon.svg / icon-*.png          파비콘, 홈 화면 아이콘
site.webmanifest                  홈 화면에 추가하면 앱처럼 실행
vercel.json                       캐시·보안 헤더, 루트 폴백
robots.txt / sitemap.xml
set-domain.sh                     도메인 일괄 치환
```

첫 화면 전송량 약 **222KB** (gzip 후 60KB 내외). 사진은 상세창을 열 때만 내려받습니다.

모든 경로가 **상대 경로**라서, 배포 전에 `index.html`을 그냥 더블클릭해도 그대로 열립니다.

---

## 배포 순서

**1. 도메인 먼저 넣기** — OG 태그와 canonical은 절대 URL이 필요합니다.

```bash
./set-domain.sh https://jeju.mydomain.com
```

`index.html`, `sitemap.xml`, `robots.txt`가 한 번에 교체됩니다.
(윈도우면 세 파일에서 `https://jeju.example.com`을 찾아 바꿔 주세요.)

**2. 배포**

```bash
npm i -g vercel
vercel login
cd jeju-vercel     # index.html이 있는 폴더
vercel --prod
```

`Which directory is your code located in?` → 그냥 엔터.
Framework는 **Other**, Build Command는 **비움**.

또는 GitHub 연동:

```bash
git init && git add . && git commit -m "제주 일정표"
git branch -M main
git remote add origin https://github.com/<계정>/<저장소>.git
git push -u origin main
```

**3. 도메인 연결** — Settings → Domains

| 대상 | 레코드 | 값 |
|---|---|---|
| 루트 (`mydomain.com`) | A | `76.76.21.21` |
| 서브도메인 (`jeju.mydomain.com`) | CNAME | `cname.vercel-dns.com` |

도메인을 붙인 뒤 **1번을 다시 실행하고 재배포**해야 공유 미리보기가 정상 동작합니다.

**4. 확인**

- 아이폰 Safari → 공유 → **홈 화면에 추가** (주소창 없이 앱처럼 열립니다)
- 카카오톡에 링크 붙여 미리보기 확인. 안 보이면 [카카오 디버거](https://developers.kakao.com/tool/debugger/sharing)에서 캐시를 초기화하세요.

---

## 내용 수정

일정 데이터는 `assets/app.*.js` 안의 `var ts={...},ff={...},JA=[...]` 세 곳에 모여 있습니다.

- `ts` — 장소별 설명·주소·운영시간·팁
- `ff` — 장소별 이모지와 색
- `JA` — 날짜별 시간표 (`time`, `placeId`, `dur`)
- `WI` — 날짜별 컨셉 색 (호버·NOW 강조에 그대로 쓰입니다)

**파일을 고치면 파일명의 해시를 바꾸고 `index.html`의 두 곳(`preload`, `script src`) 참조도 함께 바꿔 주세요.**
`assets/`는 1년 immutable로 캐싱되므로, 이름이 같으면 방문자 브라우저에 옛 파일이 남습니다.

## 참고

- 화면이 안 그려지면 흰 화면 대신 **오류 내용과 실패한 파일 경로**가 표시되고 '다시 시도' 버튼이 나옵니다.
- 데스크톱(1024px↑)에서는 3일치가 **3단으로 나란히** 보이고, 상세창은 화면 중앙 모달로 뜹니다.
- "지금" 강조는 방문자 기기 시각 기준입니다. 10/9·10/10·10/11이면 해당 날짜 한 곳만, 그 밖의 날짜에는 세 날짜의 현재 시각 위치를 함께 표시합니다.
- `robots.txt`는 검색 노출을 **허용**합니다. 가족만 볼 페이지면 파일 안의 두 줄을 서로 바꿔 주세요.
