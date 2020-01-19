# Ch 06. 디스크립터로 더 멋진 객체 만들기

## 디스크립터 (Descriptor)
### 디스크립터 메커니즘
- 클라이언트 클래스: 디스크립터 구현의 기능을 활용할 도메인 모델로서 솔루션을 위해 생성한 일반적인 추상화 객체
- 디스크립터 클래스: 디스크립터 로직의 구현체 .디스크립터 프로토콜을 구현한 클래스의 인스턴스

**주의사항: 이 프로토콜이 동작하려면 디스크립터 객체가 클래스 속성으로 정의되어야 함**

### 디스크립터 프로토콜
디스크립터 클래스는 다음 매직 메서드 중에 최소한 개 이상을 포함해야 한다. ([Descriptor Protocol](https://docs.python.org/3/howto/descriptor.html#descriptor-protocol))
- `descr.__get__(self, obj, type=None) -> value`
- `descr.__set__(self, obj, value) -> None`
- `descr.__delete__(self, obj) -> None`

