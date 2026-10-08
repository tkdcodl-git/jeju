# 제주 2박 3일 · 9명 가족여행 일정표

빌드 과정이 없는 **정적 사이트**입니다. **이 저장소의 루트가 그대로 배포 루트**이고, `index.html` 이 최상단에 있습니다.

---

## GitHub 에 올리기

### 방법 A — 웹에서 드래그 (터미널 없이)

1. GitHub 에서 새 저장소를 만듭니다. **README·.gitignore·라이선스는 체크하지 마세요.** (빈 저장소여야 업로드 화면이 바로 나옵니다)
2. 빈 저장소 화면의 **uploading an existing file** 을 누릅니다.
3. 압축을 푼 `jeju-itinerary` 폴더를 **연 다음**, 폴더 자체가 아니라 **안에 있는 항목을 전부 선택**해서(⌘A / Ctrl+A) 드래그합니다.
   `assets` 같은 하위 폴더도 함께 끌면 경로가 유지됩니다.
4. **Commit changes** 를 누릅니다.

> ⚠️ **폴더를 통째로 끌면 안 됩니다.** `jeju-itinerary/index.html` 처럼 한 겹 더 들어가서 Vercel 이 404 를 냅니다.
> ⚠️ 웹 업로드는 **한 번에 100개**까지입니다. 이 저장소는 74개라 한 번에 들어갑니다.
> ⚠️ 웹 드래그는 `.gitignore` · `.vercelignore` 같은 **점으로 시작하는 파일을 건너뜁니다.** 없어도 사이트는 정상 동작합니다. 필요하면 **Add file → Create new file** 로 이름을 직접 입력해 만드세요.

### 방법 B — 터미널 (폴더 통째로, 가장 확실함)

```bash
cd jeju-itinerary          # ← 반드시 이 폴더 안에서
git init -b main
git add -A
git commit -m "제주 가족여행 일정표"
git remote add origin https://github.com/<아이디>/<저장소>.git
git push -u origin main
```

점 파일까지 그대로 올라가고 폴더 구조도 어긋나지 않습니다.

---

### 바뀐 파일만 올리기 (이미 저장소가 있을 때)

업로드용 zip 을 풀고, 안에 있는 항목을 전부 선택해 저장소 첫 화면에 드래그 → **Commit changes**.
같은 경로의 파일은 덮어써지고 나머지는 그대로 남습니다. `index.html` 과 `assets/app.*.js` 는 꼭 함께 올리세요.

---

## Vercel 에 배포하기

**1. 도메인 먼저 넣기** — OG 태그와 canonical 은 절대 URL 이 필요합니다.

```bash
./set-domain.sh https://내도메인.com    # index.html, sitemap.xml, robots.txt 일괄 치환
```

**2. Vercel 에서 Import** — Add New → Project → 이 저장소 선택 → Deploy.

`vercel.json` 에 `framework: null`, `buildCommand: null`, `outputDirectory: "."` 를 명시해 두었으니 설정은 건드릴 것이 없습니다.

CLI 로 올린다면 **반드시 `index.html` 이 있는 폴더 안에서** 실행하세요.

```bash
vercel --prod
```

---

## 404: NOT_FOUND 가 났다면

Vercel 이 `index.html` 을 **루트에서 찾지 못한 것**입니다. 거의 항상 아래 둘 중 하나입니다.

**1) 폴더가 한 겹 더 들어가 있다**

```
저장소/
└── jeju-itinerary/     ← 한 겹 더 들어감
    └── index.html
```

해결은 둘 중 하나입니다.

- 저장소 루트로 파일을 옮긴다
- 또는 Vercel → **Settings → Build and Deployment → Root Directory** 에 `jeju-itinerary` 를 입력하고 재배포

**2) 프레임워크 프리셋이 잘못 잡혔다**

Vercel 이 Vite·Next 등으로 오인하면 빌드를 돌리고 비어 있는 `dist` 를 서빙해 404 가 납니다.
Settings → **Framework Preset = Other**, **Build Command 비움**, **Output Directory 비움** 으로 두세요.

---

## 로컬에서 확인하기

`index.html` 만 따로 내려받으면 **열리지 않습니다.** `assets/` 폴더가 같은 위치에 있어야 합니다.

```bash
python3 -m http.server 4000    # http://localhost:4000
```

모든 경로가 **상대 경로**라서 `index.html` 을 그냥 더블클릭해도 열립니다.

---

## 구성

```
index.html                  6KB   껍데기 + 메타태그 + 부팅 가드
assets/app.*.js           204KB   React 앱 (해시 파일명 → 영구 캐시)
assets/styles.*.css        57KB   Tailwind + 회색 테마 + 데스크톱 레이아웃
assets/img/*.webp                 장소 사진 10장 (상세창 열 때만 로드)
assets/menu/*.webp                메뉴 사진 45장
og.jpg                    244KB   카카오톡·슬랙 공유 미리보기 (1200×630)
favicon.svg / icon-*.png          파비콘, 홈 화면 아이콘
site.webmanifest                  홈 화면에 추가하면 앱처럼 실행
vercel.json                       캐시·보안 헤더, 루트 폴백
robots.txt / sitemap.xml
set-domain.sh                     도메인 일괄 치환
.vercelignore                     build/ · HANDOVER.md 는 배포 제외

build/                            일정·지도 계산 스크립트 (legs.py · geomap.py)
HANDOVER.md                       데이터 구조와 수정 규칙 — 이어서 작업할 때 이 문서부터
```

첫 화면 전송량 약 **222KB** (gzip 후 60KB 내외). 사진은 상세창을 열 때만 내려받습니다.

---

## 고칠 때 반드시 지킬 것

`assets/` 는 **1년 immutable 캐시**입니다. 파일을 고치면 **파일명 해시를 바꾸고 `index.html` 의 두 곳(preload, script src)도 함께** 바꿔야 합니다. 이름이 같으면 방문자 브라우저에 옛 파일이 계속 남습니다.

자세한 내용은 `HANDOVER.md` 를 보세요.
