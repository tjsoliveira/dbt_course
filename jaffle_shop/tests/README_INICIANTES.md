# Guia de Testes para Iniciantes

Este guia explica os testes de forma simples para quem está começando com dbt.

## 🎯 O que são Testes?

Testes são verificações que garantem que seus dados estão corretos. É como uma "prova" que seus dados passam.

## 📋 Tipos de Testes Simples

### 1. **Teste de Unicidade** (`test_simple_uniqueness.sql`)
**O que faz:** Verifica se não há IDs duplicados
**Exemplo:** Garante que cada cliente tenha um ID único

```sql
-- Se retornar 0 linhas = ✅ Tudo certo
-- Se retornar > 0 linhas = ❌ Há duplicatas
```

### 2. **Teste de Validação** (`test_simple_validation.sql`)
**O que faz:** Verifica se os valores fazem sentido
**Exemplo:** Garante que pedidos não tenham valores negativos

```sql
-- Se retornar 0 linhas = ✅ Todos os valores são válidos
-- Se retornar > 0 linhas = ❌ Há valores problemáticos
```

### 3. **Teste de Consistência** (`test_simple_consistency.sql`)
**O que faz:** Verifica se os números batem entre tabelas
**Exemplo:** Garante que o total de pedidos esteja correto

```sql
-- Se retornar 0 linhas = ✅ Os números estão consistentes
-- Se retornar > 0 linhas = ❌ Há inconsistências
```

## 🚀 Como Executar

```bash
# Executar todos os testes
dbt test

# Executar apenas testes simples
dbt test --select singular

# Executar um teste específico
dbt test --select test_simple_uniqueness
```

## 📊 Como Interpretar os Resultados

### **✅ Teste Passou (0 linhas):**
- Seu teste funcionou
- Não há problemas nos dados
- Pode continuar com confiança

### **❌ Teste Falhou (> 0 linhas):**
- Há problemas nos dados
- As linhas retornadas mostram o que está errado
- Precisa investigar e corrigir

## 🔍 Exemplo Prático

Imagine que você executou `test_simple_validation` e recebeu:

```sql
| order_id | total_amount | issue_type    |
|----------|--------------|---------------|
| 1001     | -50.00       | Negative amount |
| 1002     | 0.00         | Zero amount     |
```

**O que significa:**
- Pedido 1001 tem valor negativo (não deveria)
- Pedido 1002 tem valor zero (pode ser problema)

## 🎓 Conceitos Importantes

### **LEFT JOIN:**
- Conecta duas tabelas
- Mantém todos os registros da primeira tabela
- Útil para encontrar registros "órfãos"

### **GROUP BY:**
- Agrupa registros por uma coluna
- Permite contar, somar, etc.

### **HAVING:**
- Filtra resultados de agregações
- Como WHERE, mas para grupos

### **CASE WHEN:**
- Cria condições lógicas
- Útil para categorizar dados

## 🔧 Como Criar Seu Próprio Teste

1. **Pense no que quer testar**
2. **Escreva uma query SQL simples**
3. **Salve com nome descritivo**
4. **Execute com `dbt test`**

### **Exemplo de Teste Simples:**
```sql
-- Verifica se há produtos sem preço
SELECT product_id, product_name
FROM {{ ref('stg_products') }}
WHERE price IS NULL
```

## 📚 Próximos Passos

1. **Execute os testes existentes**
2. **Entenda os resultados**
3. **Crie testes simples para suas necessidades**
4. **Aprenda testes mais avançados gradualmente**

## 💡 Dicas para Iniciantes

- **Comece simples:** Teste uma coisa por vez
- **Use nomes descritivos:** `test_verifica_precos.sql`
- **Comente seu código:** Explique o que está testando
- **Teste pequeno:** Execute testes frequentemente
- **Não desanime:** Falhas são oportunidades de aprender!

## 🎉 Lembre-se

Testes são seus amigos! Eles ajudam a:
- **Encontrar problemas** antes que afetem usuários
- **Ganhar confiança** nos seus dados
- **Aprender SQL** de forma prática
- **Ser mais profissional** no trabalho com dados
