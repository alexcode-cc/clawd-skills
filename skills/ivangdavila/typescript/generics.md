# Generic Traps

## Inference Failures

- `useState<User>()` infiere `User | undefined` — olvido manejar el undefined inicial
- `Array.filter(x => x.active)` no narrowea el tipo — necesita type guard: `.filter((x): x is Active => x.active)`
- `Promise.all([fetchA(), fetchB()])` infiere tupla solo con `as const` — sin él es union array
- Generic con default `<T = any>` escapa el `any` silenciosamente al resto del código

## Constraint Mistakes

- `<T extends object>` permite arrays — usar `<T extends Record<string, unknown>>` para solo objetos planos
- `<T extends string>` no acepta literals directamente — `fn("hello")` infiere `string`, no `"hello"`
- `keyof T` en función genérica es `string | number | symbol` — no solo strings

## Variance Traps

- Arrays son covariantes: `Dog[] assignable to Animal[]` pero push de `Cat` rompe en runtime
- Function params son contravariantes — `(animal: Animal) => void` NO es assignable a `(dog: Dog) => void`
- `readonly` arrays evitan el problema de covarianza — preferir para inputs

## Return Type Widening

```typescript
// Devuelve string, no "hello"
function greet() { return "hello" }

// Fix: anotar explícitamente
function greet(): "hello" { return "hello" }

// O usar as const en el return
function greet() { return "hello" as const }
```

## Mapped Type Gotchas

- `{ [K in keyof T]: X }` pierde modificadores — usar `-?` o `-readonly` explícitamente
- `Partial<T>` hace TODO opcional, incluso nested — usar DeepPartial custom si necesitas profundidad
- `Required<T>` no funciona con nested — igual, necesitas versión deep
