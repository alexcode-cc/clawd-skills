# Utility Type Traps

## Partial/Required

- `Partial<T>` es shallow — objetos nested siguen siendo required
- `Required<T>` no quita `undefined` del union — `{ a?: string | undefined }` sigue teniendo undefined
- Ambos pierden readonly — el resultado es mutable aunque T fuera readonly

## Pick/Omit

- `Omit<T, K>` no verifica que K existe en T — `Omit<User, "typo">` compila sin error
- `Pick` con key que no existe también compila — no hay validación
- Ambos pierden discriminated union narrowing — el resultado ya no es discriminable

## Record

- `Record<string, T>` implica que TODA key existe — acceso a key inexistente devuelve T, no T | undefined
- `Record<K, V>` con K union no garantiza todas las keys — puede faltar alguna
- Para objeto con keys específicas requeridas, usar mapped type explícito

## Extract/Exclude

- `Extract<T, U>` devuelve `never` si no hay match — no error, silenciosamente vacío
- `Exclude` igual — puede devolver never sin avisar
- Ambos distribuyen sobre unions — comportamiento no intuitivo con tipos complejos

## ReturnType/Parameters

- `ReturnType<typeof fn>` falla si fn es overloaded — toma solo la última signature
- `Parameters` igual con overloads — comportamiento inconsistente
- Ambos requieren `typeof` para funciones (no para tipos función)

## NonNullable

- `NonNullable<T>` quita null Y undefined — a veces solo quieres quitar uno
- No funciona deep — nested nullables siguen ahí
- `T & {}` es alternativa que solo quita null/undefined del nivel superior

## Awaited

- `Awaited<T>` unwrapea recursivamente — puede ser sorpresa con Promise<Promise<T>>
- No funciona con PromiseLike custom que no sigue el patrón estándar
