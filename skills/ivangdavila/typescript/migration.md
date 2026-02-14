# Migration Traps

## Implicit Any

- `noImplicitAny: false` inicial esconde MUCHOS errores — el código "compila" pero tipos son wrong
- Callback params sin tipo son `any` silencioso — `arr.map(x => x.foo)` no falla aunque x sea number
- Event handlers heredan any del DOM — `onClick={e => e.target.value}` es any

## Strict Mode Gotchas

- `strictNullChecks: true` rompe MUCHO código existente — localStorage.getItem devuelve `string | null`
- `strictPropertyInitialization` requiere inicializar en constructor — o usar `!` assertion
- Habilitar strict incrementalmente es más trabajo que empezar strict

## Type Assertions

- `as Type` no valida nada — `"hello" as number` compila
- `as unknown as Type` es escape hatch total — evitar a toda costa
- JSON.parse devuelve `any` — necesita assertion o validación runtime

## Third Party Types

- `@types/x` puede estar desactualizado vs el paquete real
- Algunos @types tienen errores — a veces necesitas augmentar o ignorar
- `skipLibCheck: true` esconde errores en node_modules pero también en tus .d.ts

## CommonJS Interop

- `import x from "cjs"` vs `import * as x from "cjs"` — comportamiento diferente
- `esModuleInterop: true` cambia cómo se importan CJS — puede romper código existente
- `allowSyntheticDefaultImports` solo afecta tipos, no runtime — confuso

## Gradual Adoption Mistakes

- Renombrar .js a .ts de golpe = miles de errores — mejor usar allowJs y checkJs gradual
- `// @ts-ignore` se propaga y nunca se quita — usar `// @ts-expect-error` que falla si ya no hay error
- `any` temporal se queda para siempre — mejor `unknown` desde el inicio

## Build Configuration

- `outDir` no limpia archivos viejos — .js huérfanos causan bugs
- `declaration: true` sin `declarationDir` mezcla .d.ts con código
- `composite` y `references` para monorepos son confusos pero necesarios
