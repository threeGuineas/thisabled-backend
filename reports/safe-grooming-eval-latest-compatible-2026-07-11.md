# SAFE 최신 호환 서빙 재평가

평가일: 2026-07-11

## 실행 기준

- 최신 GitHub 서빙 branch: `origin/feature/grooming-augmentation` (`8949388`)
- 적용 파일: `thisabled-ai/serving/safety_server/app.py` — 원격 파일 hash `0f36b3000ccf5099132f0c4de93a6c0c0186bbf1`
- 모델: `soyuncj/thisabled-safety-kcelectra`
- Hugging Face revision: `3e9c0b800661db9ce099782a76fbe181e8b23ab5`
- 실제 health: `num_labels=2`, labels=`정상/주의`
- threshold: 성인 `0.85`, 미성년 `0.69`, rule assist `off`

## 결과

38건 합성셋은 38건 모두 정상 응답했다.

- 그루밍 위험 Recall: `23/26 = 88.46%`
- 그루밍 위험 FNR: `11.54%`
- 정상 반례 FPR: `4/12 = 33.33%`
- 미성년 위험 Recall: `15/17 = 88.24%`
- 성인 위험 Recall: `8/9 = 88.89%`
- 기존 3a holdout: `50/50 = 100%` (반례 없음)

하위범주별 Recall은 combined/isolation/dependency/secrecy가 100%, intimacy가 80%, minimal single-signal이 0%였다.

## 결론

최신 HF 2-class 모델과 최신 GitHub 서빙 코드는 호환된다. 이전 HEAD의 `range(4)` 고정으로 발생하던 HTTP 500은 사라졌고, `/health`에서 실제 label 수와 HF revision을 확인할 수 있다. 다만 단일 신호 그루밍 미탐과 정상 반례 오탐은 모델 데이터·임계값 측면의 별도 문제로 남아 있다.
