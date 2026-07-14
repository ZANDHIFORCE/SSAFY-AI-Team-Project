# 🚀 LocalHub 백엔드 역할 분배 명세서 (BE_RULE.md)

> **프로젝트**: 공공데이터 기반 지역 정보 공유 커뮤니티 (LocalHub)
> **기간**: 3일 (타임어택)
> **기술 스택**: FastAPI, SQLite, SQLAlchemy, OpenAI API
> **최고 규칙(Master Rule)**: 모든 API URL, 데이터 모델, JSON 필드명, 에러 코드는 반드시 루트 디렉토리의 **`RULE.md`**를 100% 준수합니다.
> **협업 전략**: 파일 단위 물리적 격리를 통한 깃(Git) 충돌 방지 및 바이브 코딩(AI 코드 생성) 효율 극대화

---

## 🎯 기본 개발 원칙 (For Human & AI)
1. **도메인 분리**: BE 1은 장소/지도/순위 조회(`GET /api/places`) 및 시드 데이터 관리 위주, BE 2는 장소별 게시판 CRUD(`GET/POST/PUT/DELETE /api/places/{place_id}/posts`) 및 AI 챗봇 연동(`POST /api/chatbot/summary`) 위주로 개발한다.
2. **라우터 격리**: 각자의 담당 라우터 파일(`routers/places.py`, `routers/posts.py`, `routers/chat.py` 등) 안에서만 코드를 작성하며, 타인의 도메인 파일을 직접 수정하지 않는다.
3. **CORS & 배포**: 인프라 충돌을 막기 위해 환경 세팅(`.env`), CORS 설정(Netlify 및 `http://localhost:5173`), Render 서버 배포는 BE 2가 전담한다.

---

## 🧑‍💻 BE 1: 장소, 지도, 랭킹 데이터 담당 (Data & Place Master)
SigunguCode/Place 마스터 시드 데이터를 관리하고, 지도 핀 시각화 및 실시간 핫플 랭킹을 위한 장소 목록 조회 API를 제공하는 역할입니다.

* **주요 담당 라벨**: `[BE-01]`, `[BE-02]`, SigunguCode 마스터 시드 삽입, Place 시드 삽입
* **주요 작업 파일**: `main.py` (Lifespan 시드 로딩 부분), `utils/data_loader.py`, `routers/places.py` (또는 `routers/map.py`)
* **세부 담당 업무**:
  * **[시드 데이터 로드]** FastAPI Lifespan 이벤트 또는 유틸리티(`utils/data_loader.py`)를 활용하여 구동 시 `SigunguCode`(법정동 시군구 마스터) 및 `Place`(최소 3곳 이상, `sigungu_code` 매핑 포함) 테이블의 초기 시드 데이터를 SQLite DB에 적재
  * **[장소 목록 & 랭킹 API (`BE-01`)]** `GET /api/places` 구현. 전체 장소 목록을 반환하되, 각 장소에 속한 게시글 총 개수(`post_count`)를 계산하여 **`post_count` 기준 내림차순으로 정렬** 반환 (지도 핀 렌더링 및 메인 화면 우측 실시간 핫플 순위 위젯 공용)
  * **[장소 단건 조회 API (`BE-02`)]** `GET /api/places/{place_id}` 구현 (`post_count` 포함, 존재하지 않는 ID 조회 시 `404 Not Found`)

---

## 🤖 BE 2: 게시판 코어, AI 챗봇, 인프라 담당 (Core & AI Wizard)
커뮤니티의 핵심인 장소별 게시판 DB 통신을 처리하고, OpenAI API를 연동해 챗봇 동향 요약 기능을 구현하며 서버 환경을 책임지는 역할입니다.

* **주요 담당 라벨**: `[BE-03]`, `[BE-04]`, `[BE-05]`, `[BE-06]`, `[BE-07]`, `[BE-08]`
* **주요 작업 파일**: `database.py`, `models.py`, `routers/posts.py` (또는 `routers/board.py`), `routers/chat.py`, `main.py` (CORS 세팅)
* **세부 담당 업무**:
  * **[인프라 & CORS]** CORS 설정(Netlify 배포 도메인 + `http://localhost:5173`), `.env` 환경 변수 관리, Render 서버 배포 세팅 전담
  * **[코어 DB ORM]** SQLite DB 및 SQLAlchemy ORM 스키마 설계 (`Post` 테이블 - `id`, `place_id`, `nickname`, `password` 해시, `title`, `content`, `created_at` 등 `RULE.md` 3번 섹션 준수)
  * **[장소별 게시판 CRUD (`BE-03`~`BE-07`)]**
    * `BE-03 GET /api/places/{place_id}/posts`: 특정 장소 게시글 목록 조회 (페이지네이션 `page`, `size` 지원, 응답에서 `content` 필드 제외)
    * `BE-04 GET /api/places/{place_id}/posts/{post_id}`: 게시글 상세 조회 (`content` 포함, `password` 필드 절대 노출 금지)
    * `BE-05 POST /api/places/{place_id}/posts`: 게시글 작성 (`password`는 정확히 4자리 숫자 검증 후 해시 저장)
    * `BE-06 PUT /api/places/{place_id}/posts/{post_id}`: 게시글 수정 (평문 비밀번호 검증 필요, 불일치 시 `403 Forbidden`)
    * `BE-07 DELETE /api/places/{place_id}/posts/{post_id}`: 게시글 삭제 (평문 비밀번호 검증 필요, 불일치 시 `403 Forbidden`)
  * **[AI 챗봇 (`BE-08`)]** `POST /api/chatbot/summary` 엔드포인트 구현. `place_id`(특정 장소 또는 `null`)와 `question`을 받아 백엔드가 OpenAI API 프록시 호출, 2~3문장 이내 실용적 동향 요약 응답 프롬프트 구현

---

## 🤝 인터페이스 약속 (Cross-Domain 연동 포인트)
AI 챗봇(BE 2, `BE-08`)이 서울 전역 또는 특정 장소의 관광지 정보와 최신 랭킹/동향을 기반으로 대답해야 하므로, 아래의 함수 1개를 BE 1이 생성하여 BE 2에게 제공합니다.

* **요청 함수명**: `get_local_context_for_ai(place_id: Optional[int] = None) -> str`
* **구현자**: BE 1
* **사용자**: BE 2 (챗봇 프롬프트에 시스템 컨텍스트로 주입)
* **목적**: `place_id`가 주어지면 해당 장소의 정보 및 핫플 상태를, `None`이면 서울 전역 상위 핫플 랭킹 결과를 **AI가 읽기 편한 압축된 문자열(String) 포맷**으로 반환.

---

## 🛑 AI 프롬프트 가이드 (System Instruction)
이 문서를 읽고 있는 AI Assistant는 코드를 생성할 때 다음 규칙을 절대적으로 준수할 것:
1. **최고 규약 준수**: 모든 엔드포인트 URL, 요청/응답 JSON 스펙, 에러 응답(`400`, `403`, `404`)은 반드시 루트 디렉토리의 **`RULE.md`**를 정확히 따라야 하며, 요구사항에 없는 기능(댓글, 좋아요, 로그인/JWT, 스레드 등)은 절대 구현하지 마시오.
2. **역할 및 라벨 준수**: 사용자가 BE 1 역할을 수행 중일 때 `database.py`의 `Post` 모델이나 `routers/posts.py`를 수정하지 마시오. 사용자가 BE 2 역할을 수행 중일 때 시드 로딩 로직이나 `routers/places.py`를 직접 수정하지 마시오.
3. **모듈화 유지**: FastAPI 라우터 코드를 생성할 때는 반드시 `APIRouter()`를 사용한 모듈화된 형태를 유지하며, API 구현 완료 시 `RULE.md`의 구현 체크리스트(`[x]`) 갱신을 잊지 마시오.
4. **보안 규칙**: 비밀번호는 어떠한 경우에도 평문으로 DB에 저장하거나 API 응답에 반환해서는 안 됩니다(해시 저장 필수).