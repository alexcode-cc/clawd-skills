# Declaration File Traps

## Module Augmentation

- `declare module "x"` requiere path EXACTO — `"lodash"` no es igual que `"lodash/index"`
- Augmentation en archivo sin imports se vuelve global — añadir `export {}` para forzar módulo
- No puedes añadir nuevos exports, solo extender existentes — limitación del sistema

## Ambient Declarations

- `declare const` sin valor crea variable global — puede colisionar con otros
- `declare function` en archivo de módulo no es global — necesita `declare global {}`
- Archivos .d.ts sin import/export son scripts globales — comportamiento legacy confuso

## Type vs Interface en .d.ts

- `interface` se puede extender/merge desde otros archivos — útil para augmentation
- `type` no se puede reabrir — si necesitas que usuarios extiendan, usar interface
- `declare class` crea valor Y tipo — `declare type` solo tipo

## Path Mapping

- `paths` en tsconfig solo afecta compilación — bundler necesita config separada
- `baseUrl` es requerido para que `paths` funcione — fácil de olvidar
- Los paths no se transforman en output — solo son aliases de compilación

## Export Patterns

```typescript
// MAL: export default en .d.ts es problemático
declare module "x" {
  export default function(): void  // Problemas con esModuleInterop
}

// BIEN: named exports
declare module "x" {
  export function doThing(): void
}
```

## Wildcards

- `declare module "*.svg"` afecta TODOS los .svg — no puedes tener tipos específicos
- Los wildcards tienen menor prioridad que matches exactos
- No puedes usar wildcards para augmentar, solo para declarar nuevos módulos
