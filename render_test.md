# Markdown Bold Rendering Test

Testing the rendering of bold text with various lengths and the "Strict Spacing" rule.

## 1. Term: **컨텍스트 주입(Context Injection)**

- 기본: **컨텍스트 주입(Context Injection)** 입니다. (No extra space after bold, before '입니다')
- 규정 준수 (Strict Spacing): **컨텍스트 주입(Context Injection)** 이라 합니다. (Space after bold)

## 2. Length Tests (Strict Spacing Applied)

- 10 chars: **ABCDEFGHIJ** 입니다.
- 20 chars: **ABCDEFGHIJKLMNOPQRST** 입니다.
- 30 chars: **ABCDEFGHIJKLMNOPQRSTUVWXYZ1234** 입니다.
- 40 chars: **ABCDEFGHIJKLMNOPQRSTUVWXYZ12345678901234** 입니다.
- 50 chars: **ABCDEFGHIJKLMNOPQRSTUVWXYZ123456789012345678901234** 입니다.
- 60 chars: **ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890123456789012345678901234** 입니다.
- 100 chars: **ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890ABCDEFGHIJKLMNOPQRST1234567890** 입니다.

## 3. Korean + English Complex String (Strict Spacing)

- **컨텍스트 주입(Context Injection)** 의 개념
- **가나다라마바사아자차카타파하(Alphabet-abcdefg-1234567890)** 의 테스트

## 4. No Spacing vs Strict Spacing Comparison

- No Spacing: **컨텍스트 주입**입니다. (Error prone)
- Strict Spacing: **컨텍스트 주입Context Injection**입니다. (Stable)
