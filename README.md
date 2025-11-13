# 📖 FEIFOOD

## 🍔 Sobre o projeto
O **FEIFOOD** é um sistema em Python que simula um aplicativo de pedidos de comida.  
Ele permite que usuários se cadastrem, façam login, busquem alimentos, adicionem itens ao carrinho, finalizem pedidos e avaliem seus próprios pedidos.

---

## ⚙️ Funcionalidades
- Cadastro de usuários  
- Login com verificação de credenciais  
- Menu logado com opções personalizadas  
- Busca de alimentos em um catálogo (`alimentos.txt`)  
- Carrinho de compras com opção de remover itens  
- Finalização de pedidos com IDs independentes por usuário (`pedidos.txt`)  
- Avaliação de pedidos feita apenas pelo usuário que realizou o pedido (`avaliacoes.txt`)  

---

## 📂 Estrutura de arquivos
⚠️ IMPORTANTE: Todos os arquivos `.txt` devem ser criados manualmente com os nomes exatos e na mesma pasta onde está o arquivo `menu.py`.  
Cada arquivo deve seguir a estrutura correta:

- **cadastros.txt** → armazena nome, usuário e senha  
- **alimentos.txt** → armazena os alimentos disponíveis  
- **pedidos.txt** → armazena os pedidos realizados  
- **avaliacoes.txt** → armazena as avaliações dos pedidos  

---

## ▶️ Como executar
1. Certifique-se de ter **Python 3** instalado.  
2. Clone ou baixe este repositório.  
3. Crie os arquivos `.txt` conforme descrito acima na mesma pasta do `menu.py`.  
4. Execute o programa:
   ```bash
   python menu.py

---

## 🖥️ Fluxo de uso

### Menu principal  
1 → Cadastro  
2 → Login  
0 → Sair  

### Menu logado  
1 → Buscar alimentos  
2 → Carrinho  
3 → Avaliar pedido  
0 → Logout  

### Carrinho  
1 → Remover item  
2 → Finalizar pedido  
0 → Voltar  

### Finalização de pedido  
O pedido é salvo em `pedidos.txt`.  
O usuário pode avaliar imediatamente.  

---

## 📝 Observações

- Cada usuário possui sua própria sequência de pedidos (IDs independentes).  
- Apenas o dono de um pedido pode avaliá-lo.  
- As avaliações usam `;` como separador para evitar problemas com vírgulas nos comentários.  
- Todos os arquivos `.txt` devem estar na mesma raiz do arquivo `menu.py`.  

