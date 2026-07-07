# Notas de desenvolvimento

## Itens concluídos

- [x] Ajustar o fluxo de fechamento da conversa para permitir a mensuração de estados de encerramento de forma separada do fechamento em si.

## Pendências prioritárias

- [ ] Implementar o tratamento de erros em pontos críticos do fluxo, incluindo falhas de autenticação, exceções de processamento e respostas inesperadas.
- [ ] Refatorar as funções de edição do usuário, com foco especial na lógica de intenção, para melhorar a manutenção e a clareza do código.
- [ ] Criar e integrar os métodos de métricas necessários para registrar e acompanhar indicadores de desempenho do agente.
- [ ] Revisar e refatorar os filtros utilizados no sistema, garantindo maior consistência e facilidade de manutenção.
- [ ] Implementar e revisar os métodos de root, verificando se estão bem estruturados e alinhados com a arquitetura atual.

## Pendências de integração e interface

- [ ] Finalizar o desenvolvimento do front-end, incluindo a experiência de uso e a integração com os fluxos do back-end.
- [ ] Implementar o consumo do front-end para armazenar corretamente o sistema de token e garantir a persistência da sessão do usuário.

## Métricas a serem implementadas

O sistema deve passar a registrar e acompanhar um conjunto de métricas para avaliar o desempenho do agente de atendimento automatizado. As principais métricas a serem incorporadas são:

- Taxa de resolução no primeiro contato: percentual de atendimentos concluídos com sucesso sem necessidade de intervenção humana.
- Taxa de escalonamento para humano: percentual de conversas transferidas para um atendente humano devido à incapacidade do agente de concluir a demanda.
- Taxa de entendimento correto: percentual de interações em que o agente compreendeu corretamente a intenção do usuário.
- Tempo médio de resposta: tempo médio gasto pelo agente para responder às mensagens do usuário.
- Tempo médio de atendimento: tempo total médio necessário para concluir uma conversa até a resolução.
- Taxa de abandono da conversa: percentual de atendimentos encerrados sem resolução, por desistência do usuário ou falha do fluxo.
- Satisfação do usuário: indicador obtido por avaliações, feedbacks ou sinais de aprovação/desaprovação ao final da interação.
- Taxa de sucesso por intenção: desempenho do agente em categorias específicas, como reembolso, consulta de pedido, cadastro ou suporte técnico.
- Taxa de fallback ou erro: percentual de vezes em que o agente não conseguiu responder adequadamente e precisou recorrer a uma resposta genérica ou a um humano.
- Qualidade das respostas: avaliação da utilidade, clareza e correção das respostas fornecidas pelo agente.
- Conversão de objetivo: percentual de conversas que culminam em uma ação desejada, como agendamento, compra, abertura de chamado ou conclusão de um fluxo.
- Custo por atendimento: indicador de eficiência operacional, especialmente relevante quando o agente substitui parte do trabalho de atendimento humano.

Essas métricas devem ser acompanhadas de forma histórica, permitindo analisar tendências, identificar falhas por tipo de solicitação e prever o comportamento do agente ao longo do tempo.

## Observação

Estas pendências representam os próximos passos principais para consolidar o funcionamento do sistema, melhorar a qualidade do código e garantir a coleta adequada de métricas e dados de uso.
