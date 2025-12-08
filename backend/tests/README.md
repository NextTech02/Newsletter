# Testes Unitários - Newsletter FCP Backend

Este diretório contém todos os testes unitários para os serviços do backend.

## 📋 Estrutura dos Testes

```
tests/
├── __init__.py
├── conftest.py                    # Fixtures compartilhadas
├── test_auth_service.py           # Testes do serviço de autenticação
├── test_email_service.py          # Testes do serviço de email
├── test_supabase_service.py       # Testes do serviço Supabase
├── test_template_service.py       # Testes do serviço de templates
└── test_user_service.py           # Testes do serviço de usuários
```

## 🚀 Como Executar os Testes

### 1. Instalar Dependências

```bash
cd backend
pip install -r requirements.txt
```

### 2. Executar Todos os Testes

```bash
# Executar todos os testes
pytest

# Executar com output mais detalhado
pytest -v

# Executar com cobertura de código
pytest --cov=app --cov-report=html
```

### 3. Executar Testes Específicos

```bash
# Executar testes de um arquivo específico
pytest tests/test_auth_service.py

# Executar uma classe de testes específica
pytest tests/test_auth_service.py::TestAuthService

# Executar um teste específico
pytest tests/test_auth_service.py::TestAuthService::test_verify_password_correct

# Executar testes que contenham uma palavra no nome
pytest -k "password"
```

### 4. Executar com Diferentes Níveis de Verbosidade

```bash
# Quiet mode (apenas resumo)
pytest -q

# Verbose mode (mais detalhes)
pytest -v

# Very verbose mode (máximo detalhe)
pytest -vv
```

## 📊 Cobertura de Código

Após executar os testes com cobertura, você pode visualizar o relatório HTML:

```bash
# Executar testes com cobertura
pytest --cov=app --cov-report=html

# Abrir relatório HTML (Windows)
start htmlcov/index.html

# Linux/Mac
open htmlcov/index.html
```

## 🧪 Testes por Serviço

### Auth Service (test_auth_service.py)
- ✅ Geração de hash de senha
- ✅ Verificação de senha correta/incorreta
- ✅ Criação de tokens JWT
- ✅ Verificação de tokens válidos/inválidos/expirados
- ✅ Testes com chave secreta incorreta

### Email Service (test_email_service.py)
- ✅ Envio de email individual
- ✅ Envio em massa (bulk)
- ✅ Processamento em lotes
- ✅ Tratamento de falhas parciais
- ✅ Tratamento de exceções

### Supabase Service (test_supabase_service.py)
- ✅ Busca de todos os leads
- ✅ Busca de leads inscritos
- ✅ Paginação automática
- ✅ Criação de leads
- ✅ Deleção de leads
- ✅ Cancelamento de inscrição
- ✅ Busca por email

### Template Service (test_template_service.py)
- ✅ Geração de HTML com uma notícia
- ✅ Geração de HTML com múltiplas notícias
- ✅ Validação de estrutura HTML
- ✅ Teste com caracteres especiais
- ✅ Teste com conteúdo longo
- ✅ Validação de links de unsubscribe

### User Service (test_user_service.py)
- ✅ Busca de todos os usuários
- ✅ Busca por username
- ✅ Criação de usuário
- ✅ Atualização de usuário
- ✅ Deleção de usuário
- ✅ Autenticação de usuário
- ✅ Validações de duplicidade (username/email)

## 🎯 Metas de Cobertura

- **Cobertura mínima**: 80%
- **Cobertura ideal**: 90%+

## 🔧 Fixtures Disponíveis (conftest.py)

- `mock_supabase_client`: Mock do cliente Supabase
- `sample_lead_data`: Dados de exemplo de um lead
- `sample_leads_list`: Lista de leads de exemplo
- `sample_user_data`: Dados de exemplo de um usuário
- `sample_newsletter_data`: Dados de exemplo de uma newsletter
- `mock_smtp_client`: Mock do cliente SMTP

## 📝 Convenções de Nomenclatura

- Arquivos de teste: `test_*.py`
- Classes de teste: `Test*`
- Métodos de teste: `test_*`
- Use nomes descritivos: `test_<funcao>_<cenario>_<resultado_esperado>`

Exemplos:
- `test_create_user_success`
- `test_verify_password_incorrect`
- `test_send_email_failure`

## 🐛 Debug de Testes

```bash
# Executar com output de print
pytest -s

# Parar no primeiro erro
pytest -x

# Parar após N falhas
pytest --maxfail=2

# Executar apenas testes que falharam anteriormente
pytest --lf

# Modo interativo (abre debugger em falhas)
pytest --pdb
```

## 📈 Executar Testes Continuamente

```bash
# Instalar pytest-watch
pip install pytest-watch

# Executar testes automaticamente quando arquivos mudarem
ptw
```

## ✅ CI/CD

Os testes podem ser executados automaticamente em pipelines CI/CD:

```yaml
# Exemplo para GitHub Actions
- name: Run tests
  run: |
    cd backend
    pytest --cov=app --cov-report=xml
```

## 📞 Suporte

Se encontrar problemas ao executar os testes:
1. Verifique se todas as dependências estão instaladas
2. Verifique se o Python 3.11+ está instalado
3. Execute `pip install -r requirements.txt` novamente
4. Limpe o cache do pytest: `pytest --cache-clear`
