# 🚀 LocalHub 프론트 전달용 API 명세서

> **버전**: 1.0.1 (시드 데이터 반영 업데이트)  
> **대상 프로젝트**: 공공데이터 기반 지역 정보 공유 커뮤니티 **LocalHub**  
> **Base URL (개발 환경)**: `http://localhost:8000`  
> **Base URL (배포 환경)**: Render 백엔드 배포 도메인 (`VITE_API_BASE_URL` 사용 권장)  
> **공통 규칙**:
> - 모든 API 엔드포인트는 `/api`로 시작합니다.
> - 모든 요청/응답 JSON 필드명은 **snake_case** (예: `place_id`, `created_at`, `post_count`)를 사용합니다.
> - 별도의 인증/인가 헤더(Token, Cookie, Session 등)는 사용하지 않습니다 (익명 서비스).
> - **★ 중요 (장소 데이터 스펙)**: 실제 백엔드 시드 데이터 로더(`utils/data_loader.py`)에 의해 초기 적재되는 장소(`Place`)의 `name`은 동 단위(예: 성수동, 홍대)가 아닌 **서울시 25개 자치구 이름(예: `성동구`, `마포구`, `강남구` 등 `~구` 단위)**으로 구성되어 있습니다. 프론트 UI 구성 및 지도 핀 표기 시 '구' 단위임을 참고해 주세요.

---

## 📋 API 엔드포인트 목록 요약

| 라벨 | 메소드 & URL | 화면 / 기능 (`FE-xx` 매핑) | 상태 코드 |
| :--- | :--- | :--- | :---: |
| **`[BE-01]`** | `GET /api/places` | `FE-01` 지도 핀 표시 / `FE-02` 우측 핫플 순위 위젯 | `200` |
| **`[BE-02]`** | `GET /api/places/{place_id}` | 장소 단건 상세 조회 및 핫플 상태 확인 | `200` / `404` |
| **`[BE-03]`** | `GET /api/places/{place_id}/posts` | `FE-04` 특정 장소의 게시판 목록 조회 (페이지네이션) | `200` / `404` |
| **`[BE-04]`** | `GET /api/places/{place_id}/posts/{post_id}` | `FE-05` 게시글 상세 조회 (`content` 포함) | `200` / `404` |
| **`[BE-05]`** | `POST /api/places/{place_id}/posts` | `FE-06` 게시글 작성 (4자리 숫자 비밀번호 설정) | `201` / `400` |
| **`[BE-06]`** | `PUT /api/places/{place_id}/posts/{post_id}` | `FE-07` 게시글 수정 (비밀번호 대조 필요) | `200` / `403` / `404` |
| **`[BE-07]`** | `DELETE /api/places/{place_id}/posts/{post_id}` | `FE-07` 게시글 삭제 (비밀번호 대조 필요) | `204` / `403` / `404` |
| **`[BE-08]`** | `POST /api/chatbot/summary` | `FE-08` AI 챗봇 실시간 동향 요약 위젯 | `200` / `500` |

---

## 1. 📍 장소 / 지도 / 랭킹 API

### `[BE-01]` 장소 목록 및 핫플 랭킹 조회
지도 화면(`FE-01`)에 핀을 렌더링하거나, 메인 화면 우측의 실시간 핫플 순위 위젯(`FE-02`)을 구성할 때 호출합니다.

- **URL**: `GET /api/places`
- **Path/Query Parameters**: 없음
- **주의 및 연동 팁**:
  - 응답 배열은 해당 장소(구)에 등록된 게시글 수(`post_count`)를 기준으로 **내림차순 정렬**되어 반환됩니다.
  - 랭킹 위젯(`FE-02`)을 구성할 때는 별도의 정렬 없이 배열의 상위 N개(`res.data.slice(0, 5)` 등)를 바로 활용하시면 됩니다.
  - `sigungu_code`는 공공데이터 법정동 시군구 코드 (`lDongSignguCd`, 예: `"200"`은 성동구, `"440"`은 마포구)를 의미합니다.
  - 백엔드 시드 데이터 상의 `name`은 반드시 **서울시 25개 구 이름(`성동구`, `마포구`, `강남구` 등)**만 들어있습니다.

#### 🟢 성공 응답 (`200 OK`)
```json
[
  {
    "id": 4,
    "name": "성동구",
    "lat": 37.5633,
    "lng": 127.0371,
    "description": "서울특별시 성동구 지역 정보 공유",
    "sigungu_code": "200",
    "post_count": 12
  },
  {
    "id": 14,
    "name": "마포구",
    "lat": 37.5663,
    "lng": 126.9016,
    "description": "서울특별시 마포구 지역 정보 공유",
    "sigungu_code": "440",
    "post_count": 8
  },
  {
    "id": 23,
    "name": "강남구",
    "lat": 37.5172,
    "lng": 127.0473,
    "description": "서울특별시 강남구 지역 정보 공유",
    "sigungu_code": "680",
    "post_count": 5
  }
]
```

---

### `[BE-02]` 장소 단건 조회
특정 장소(구)의 기본 정보 및 최신 게시글 개수(`post_count`)를 조회합니다.

- **URL**: `GET /api/places/{place_id}`
- **Path Parameter**:
  - `place_id` (`int`, 필수): 조회할 장소 ID (예: `4` -> 성동구)

#### 🟢 성공 응답 (`200 OK`)
```json
{
  "id": 4,
  "name": "성동구",
  "lat": 37.5633,
  "lng": 127.0371,
  "description": "서울특별시 성동구 지역 정보 공유",
  "sigungu_code": "200",
  "post_count": 12
}
```

#### 🔴 실패 응답 (`404 Not Found`)
```json
{
  "detail": "존재하지 않는 장소입니다."
}
```

---

## 2. 📝 게시판 CRUD API (장소별)

### `[BE-03]` 장소별 게시글 목록 조회 (페이지네이션)
특정 장소(구)에 속한 게시판 목록(`FE-04`)을 조회합니다. 최신 작성순(`id` 내림차순)으로 반환됩니다.

- **URL**: `GET /api/places/{place_id}/posts`
- **Path Parameter**:
  - `place_id` (`int`, 필수): 소속 장소 ID (예: `4` -> 성동구)
- **Query Parameters**:
  - `page` (`int`, 선택, 기본값: `1`): 페이지 번호 (`1` 이상)
  - `size` (`int`, 선택, 기본값: `20`): 한 페이지당 항목 수 (`1` ~ `100` 사이)
- **주의 및 연동 팁**:
  - 목록 응답의 `items` 배열 내부 객체에는 **`content`(본문) 필드가 포함되지 않습니다.** (`title`, `nickname`, `created_at` 등 목록 표시에 필요한 필드만 제공)

#### 🟢 성공 응답 (`200 OK`)
```json
{
  "items": [
    {
      "id": 10,
      "place_id": 4,
      "nickname": "익명",
      "title": "성동구 성수역 주변 포켓몬 행사로 인파 밀집 중",
      "created_at": "2026-07-14T15:30:00"
    },
    {
      "id": 9,
      "place_id": 4,
      "nickname": "성동구주민",
      "title": "이번 주말 왕십리역 주변 교통 통제 안내",
      "created_at": "2026-07-14T14:15:22"
    }
  ],
  "total": 12,
  "page": 1,
  "size": 20
}
```

#### 🔴 실패 응답 (`404 Not Found`)
```json
{
  "detail": "존재하지 않는 장소입니다."
}
```

---

### `[BE-04]` 게시글 상세 조회
게시글 본문(`content`)을 포함한 단건 상세 정보(`FE-05`)를 조회합니다.

- **URL**: `GET /api/places/{place_id}/posts/{post_id}`
- **Path Parameters**:
  - `place_id` (`int`, 필수): 장소 ID (예: `4`)
  - `post_id` (`int`, 필수): 게시글 ID (예: `10`)
- **주의 및 연동 팁**:
  - 보안상 응답 JSON에 **`password` 필드는 절대 반환되지 않습니다.**

#### 🟢 성공 응답 (`200 OK`)
```json
{
  "id": 10,
  "place_id": 4,
  "nickname": "익명",
  "title": "성동구 성수역 주변 포켓몬 행사로 인파 밀집 중",
  "content": "성수역 3번 출구 쪽 줄이 너무 깁니다. 오실 분들은 4번 출구 쪽 골목이나 뚝섬역에서 걸어오는 길로 우회하는 걸 추천드려요!",
  "created_at": "2026-07-14T15:30:00"
}
```

#### 🔴 실패 응답 (`404 Not Found`)
```json
{
  "detail": "게시글을 찾을 수 없습니다."
}
```

---

### `[BE-05]` 게시글 작성
선택한 장소(구)에 새로운 게시글(`FE-06`)을 등록합니다.

- **URL**: `POST /api/places/{place_id}/posts`
- **Path Parameter**:
  - `place_id` (`int`, 필수): 장소 ID
- **Request Body** (`application/json`):
  ```json
  {
    "nickname": "익명",
    "password": "1234",
    "title": "성동구 실시간 동네 소식입니다",
    "content": "서울숲 출입구 근처 주차장이 현재 만차입니다."
  }
  ```
- **필드 유효성 및 제약사항 (★ 중요)**:
  - `password`: **정확히 4자리 숫자 문자열**이어야 합니다 (예: `"1234"`, `"0000"` 등). 영문/특수문자가 포함되거나 4자리가 아닐 경우 `400 Bad Request` 에러가 발생합니다.
  - `nickname`: 빈 문자열(`""`)이나 `null` 전송 시 백엔드에서 자동으로 `"익명"`으로 지정됩니다.
- **주의 및 연동 팁**:
  - 백엔드 DB에는 비밀번호가 bcrypt 해시되어 저장되며, 응답 결과에 `password`는 반환되지 않습니다.

#### 🟢 성공 응답 (`201 Created`)
```json
{
  "id": 11,
  "place_id": 4,
  "nickname": "익명",
  "title": "성동구 실시간 동네 소식입니다",
  "content": "서울숲 출입구 근처 주차장이 현재 만차입니다.",
  "created_at": "2026-07-14T16:40:00"
}
```

#### 🔴 실패 응답 (`400 Bad Request` - 비밀번호 형식 오류)
```json
{
  "detail": "비밀번호는 정확히 4자리 숫자 문자열이어야 합니다."
}
```

---

### `[BE-06]` 게시글 수정
게시글 수정 화면(`FE-07`)에서 사용자가 입력한 평문 비밀번호를 대조하여 일치할 경우 제목과 본문을 수정합니다.

- **URL**: `PUT /api/places/{place_id}/posts/{post_id}`
- **Path Parameters**:
  - `place_id` (`int`, 필수): 장소 ID
  - `post_id` (`int`, 필수): 수정할 게시글 ID
- **Request Body** (`application/json`):
  ```json
  {
    "password": "1234",
    "title": "수정된 게시글 제목",
    "content": "수정된 본문 내용입니다"
  }
  ```

#### 🟢 성공 응답 (`200 OK`)
```json
{
  "id": 10,
  "place_id": 4,
  "nickname": "익명",
  "title": "수정된 게시글 제목",
  "content": "수정된 본문 내용입니다",
  "created_at": "2026-07-14T15:30:00"
}
```

#### 🔴 실패 응답 (`403 Forbidden` - 비밀번호 불일치)
```json
{
  "detail": "비밀번호가 일치하지 않습니다."
}
```

#### 🔴 실패 응답 (`404 Not Found`)
```json
{
  "detail": "게시글을 찾을 수 없습니다."
}
```

---

### `[BE-07]` 게시글 삭제
게시글 삭제 모달/화면(`FE-07`)에서 사용자가 입력한 평문 비밀번호를 대조하여 일치할 경우 게시글을 삭제합니다.

- **URL**: `DELETE /api/places/{place_id}/posts/{post_id}`
- **Path Parameters**:
  - `place_id` (`int`, 필수): 장소 ID
  - `post_id` (`int`, 필수): 삭제할 게시글 ID
- **Request Body** (`application/json`):
  ```json
  {
    "password": "1234"
  }
  ```
- **주의 및 연동 팁 (★ 중요)**:
  - 삭제가 성공하면 HTTP 상태 코드 **`204 No Content`**가 반환되며, **응답 Body(텍스트나 JSON)가 아예 없습니다.**
  - 프론트엔드(`axios` 또는 `fetch`)에서 응답 데이터를 `response.json()`으로 파싱하려 하면 Syntax Error가 발생할 수 있으므로, **`response.status === 204` 확인만으로 성공 여부를 판단**해 주세요.

#### 🟢 성공 응답 (`204 No Content`)
```http
HTTP/1.1 204 No Content
(응답 본문 없음)
```

#### 🔴 실패 응답 (`403 Forbidden` - 비밀번호 불일치)
```json
{
  "detail": "비밀번호가 일치하지 않습니다."
}
```

#### 🔴 실패 응답 (`404 Not Found`)
```json
{
  "detail": "게시글을 찾을 수 없습니다."
}
```

---

## 3. 🤖 AI 챗봇 API

### `[BE-08]` 실시간 동향 및 핫플 요약
모든 화면에 공통으로 노출되는 플로팅 위젯(`FE-08`)에서 AI 챗봇에게 동향 분석을 요청할 때 호출합니다. 백엔드가 프록시로 OpenAI API와 통신하므로, API 키는 프론트엔드에 절대 노출되지 않습니다.

- **URL**: `POST /api/chatbot/summary`
- **Request Body** (`application/json`):
  ```json
  {
    "place_id": null,
    "question": "지금 어디가 붐벼?"
  }
  ```
  - `place_id` (`int | null`, 선택):
    - `null` 전송 시: **서울 전역 핫플레이스(자치구 단위)**의 게시글 및 랭킹 데이터를 종합하여 답변합니다.
    - 특정 `id`(예: `4` -> 성동구) 전송 시: **해당 구(성동구)의 최신 게시글 10건과 정보**를 집중적으로 분석하여 답변합니다.
  - `question` (`string | null`, 선택):
    - 사용자가 입력한 질문. 미입력(`null`) 또는 생략 시 `"전반적인 실시간 동향과 인파/이벤트 이슈를 간결하게 요약해 주세요."` 프롬프트로 작동합니다.

#### 🟢 성공 응답 (`200 OK`)
```json
{
  "summary": "성동구 성수역 주변에 포켓몬 행사 때문에 사람이 대거 몰려있습니다. 성수역 3번 출구 인파가 집중되고 있으니 골목 쪽 우회를 추천합니다."
}
```

#### 🔴 실패 응답 (`500 Internal Server Error`)
```json
{
  "detail": "OpenAI 챗봇 요약 생성 중 오류가 발생했습니다: ..."
}
```

---

## 4. 💡 프론트엔드 연동 체크리스트 & 공통 에러 대응

1. **CORS 설정 확인**
   - 백엔드는 기본적으로 `http://localhost:5173` (Vite 기본 포트) 및 `.env`의 `FRONTEND_ORIGIN`을 허용하고 있습니다.
   - 혹시 다른 포트(`3000`, `5174` 등)에서 프론트가 실행 중이라면 백엔드 담당자에게 origin 추가를 요청하세요.

2. **HTTP Error Handling (`axios` / `fetch`)**
   | 상태 코드 | 대표 사유 | 프론트엔드 권장 UX 동작 |
   | :---: | :--- | :--- |
   | **`400`** | `POST` 시 비밀번호가 4자리 숫자가 아님 | 입력창 하단 경고 메시지 표시 또는 alert 모달 노출 |
   | **`403`** | `PUT`/`DELETE` 시 비밀번호 불일치 | `"비밀번호가 일치하지 않습니다."` 경고 후 비밀번호 재입력 유도 |
   | **`404`** | 존재하지 않는 장소/게시글 ID 접근 | `"존재하지 않거나 삭제된 게시글입니다."` 안내 후 목록으로 리다이렉트 |
   | **`500`** | AI 챗봇 또는 DB 처리 중 서버 오류 | `"현재 일시적인 오류로 요약을 불러올 수 없습니다."` 폴백 메시지 표시 |

3. **비밀번호 입력 UI 팁**
   - 게시글 작성/수정/삭제 폼의 비밀번호 input에는 `maxlength="4"` 및 숫자만 입력받는 유효성 검증(`inputmode="numeric"`, 정규식 등)을 프론트 단에서도 적용해주시면 훌륭한 사용자 경험을 제공할 수 있습니다.
