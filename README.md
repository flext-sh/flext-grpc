# FLEXT gRPC

Camada gRPC para comunicacao service-to-service de baixa latencia entre componentes FLEXT.

Descricao oficial atual: "FLEXT gRPC - High-Performance gRPC Services".

## O que este projeto entrega

- Padroniza contratos RPC para integracao interna.
- Apoia exposicao de endpoints binarios para workloads tecnicos.
- Melhora performance de troca de mensagens entre servicos.

## Contexto operacional

- Entrada: requests gRPC conforme contrato protobuf.
- Saida: responses gRPC para consumidores internos.
- Dependencias: flext-core e definicoes de contrato RPC.

## Estado atual e risco de adocao

- Qualidade: **Alpha**
- Uso recomendado: **Nao produtivo**
- Nivel de estabilidade: em maturacao funcional e tecnica, sujeito a mudancas de contrato sem garantia de retrocompatibilidade.

## Diretriz para uso nesta fase

Aplicar este projeto somente em desenvolvimento, prova de conceito e homologacao controlada, com expectativa de ajustes frequentes ate maturidade de release.
