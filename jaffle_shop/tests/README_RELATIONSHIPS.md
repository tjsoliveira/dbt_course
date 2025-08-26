# Testes de Relacionamento (Referential Integrity)

Este documento explica como usar os testes de relacionamento nativos do dbt para garantir a integridade referencial entre os modelos.

## 🎯 O que são os Testes de Relacionamento?

Os testes de relacionamento (`relationships`) são testes nativos do dbt que verificam se as chaves estrangeiras em um modelo têm correspondência nas tabelas pai. Eles são mais eficientes e padronizados que testes customizados.

## 📋 Sintaxe Básica

```yaml
columns:
  - name: foreign_key_column
    data_tests:
      - relationships:
          arguments:
            to: ref('parent_model')
            field: primary_key_field
```

## 🔗 Relacionamentos Configurados no Projeto

### 1. **stg_items → stg_orders**
```yaml
- name: order_id
  data_tests:
    - relationships:
        arguments:
          to: ref('stg_orders')
          field: order_id
```
**O que testa:** Verifica se todos os `order_id` em `stg_items` existem em `stg_orders`

### 2. **stg_items → stg_products**
```yaml
- name: product_id
  data_tests:
    - relationships:
        arguments:
          to: ref('stg_products')
          field: product_id
```
**O que testa:** Verifica se todos os `product_id` em `stg_items` existem em `stg_products`

### 3. **stg_orders → stg_customers**
```yaml
- name: customer_id
  data_tests:
    - relationships:
        arguments:
          to: ref('stg_customers')
          field: customer_id
```
**O que testa:** Verifica se todos os `customer_id` em `stg_orders` existem em `stg_customers`

### 4. **fct_orders → stg_customers**
```yaml
- name: customer_id
  data_tests:
    - relationships:
        arguments:
          to: ref('stg_customers')
          field: customer_id
```
**O que testa:** Verifica se todos os `customer_id` em `fct_orders` existem em `stg_customers`

## 🚀 Como Executar

```bash
# Executar todos os testes de relacionamento
dbt test --select relationships

# Executar testes para um modelo específico
dbt test --select stg_items

# Executar apenas testes de relacionamento para um modelo
dbt test --select stg_items+relationships
```

## 📊 Resultados Esperados

### **Quando o teste passa (0 linhas retornadas):**
- ✅ Todos os relacionamentos estão íntegros
- ✅ Não há chaves estrangeiras órfãs

### **Quando o teste falha (> 0 linhas retornadas):**
- ❌ Existem chaves estrangeiras sem correspondência
- 📋 As linhas retornadas mostram os registros problemáticos

## 🔍 Exemplo de Saída de Falha

```sql
| order_id | customer_id | product_id |
|----------|-------------|------------|
| 1001     | 999         | 501        |
| 1002     | 998         | 502        |
```

**Interpretação:** Os `customer_id` 999 e 998 não existem na tabela `stg_customers`

## 🎓 Benefícios para o Curso

1. **Padrão da Indústria:** Usa testes nativos do dbt
2. **Performance:** Mais eficiente que testes customizados
3. **Manutenibilidade:** Menos código para manter
4. **Documentação:** Automática através do dbt docs
5. **Configuração:** Fácil de configurar e entender

## 🔧 Configurações Avançadas

### **Configurar Severidade**
```yaml
- relationships:
    arguments:
      to: ref('parent_model')
      field: primary_key_field
    config:
      severity: warn  # ou error
```

### **Configurar Nome do Teste**
```yaml
- relationships:
    arguments:
      to: ref('parent_model')
      field: primary_key_field
    config:
      test_name: "fk_to_parent_table"
```

### **Configurar Descrição**
```yaml
- relationships:
    arguments:
      to: ref('parent_model')
      field: primary_key_field
    config:
      description: "Verifica se customer_id existe em stg_customers"
```

## 📚 Próximos Passos no Curso

1. **Ativar mais testes de relacionamento** conforme necessário
2. **Adicionar testes de unicidade** para chaves primárias
3. **Implementar testes de business logic** para validações complexas
4. **Configurar alertas** para falhas de teste
5. **Integrar com CI/CD** para validação automática

## 🎉 Vantagens sobre Testes Customizados

| Aspecto | Testes Nativos | Testes Customizados |
|---------|----------------|---------------------|
| **Performance** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Manutenção** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| **Padrão** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| **Flexibilidade** | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Documentação** | ⭐⭐⭐⭐⭐ | ⭐⭐ |
