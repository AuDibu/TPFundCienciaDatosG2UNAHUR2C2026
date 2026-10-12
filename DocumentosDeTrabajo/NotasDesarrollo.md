# Limpieza

## Fase 1

### Limpieza inicial

#### Observaciones

*Repetidos*:

- 50 filas repetidas

*Vacios*:

- salary_after_usd: 754
- salary_before_usd: 753
- automation_risk_percent: 752
- industry: 751

*Objectos (Strings) con posibles issues*:

- job_role: ok
- industry: repetidos con distintos tipos de mayús y minús
- county: ok
- salary_before_usd y salary_after_usd: pasara a decimal, simbolo "$" inconsistente, verificar conversión
- automation_risk_category: ok

#### Decisiones

- Colapsar filas repetidas
- Subsanado de strings:
  - industry: pasar a lower
  - salary_before_usd y salary_after_usd: convertir a float
  - validar conversión
- Estrategia de subsanado de nulos:
  - Analizar los job_roles y su correlación con industry, si los mismos pueden usarse para inferir la industria se usaran esos. Si no se puede inferir se llenara con "unknown"
  - Obtener la mediana a nivel rol/industria y aplicar la misma a nulos de salary_after_usd, salary_before_usd y automation_risk_percent.
  - Validar cantidad de nulos post arreglo. 