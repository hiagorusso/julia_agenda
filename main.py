import streamlit as st
import sqlite3
from db.connection import criar_tabelas
from db.servicos import cadastrar_servico, listar_servicos, deletar_servico, deletar_atendimento
from db.atendimentos import adicionar_atendimento
from db.servicos import atualizar_valor_servico
from services.resumo import consultar_resumo
from datetime import datetime

st.title("Gerenciamento de Atendimentos do Ateliê")
criar_tabelas()

menu = st.sidebar.selectbox("Escolha uma opção", [
    "Registrar Atendimento",
    "Excluir Atendimento",
    "Cadastrar Serviço",
    "Listar Serviços",
    "Deletar Serviço",
    "Alterar Valor do Serviço",
    "Consultar Resumo",
])


if menu == "Cadastrar Serviço":
    st.header("Cadastrar Serviço")
    nome = st.text_input("Nome do Serviço")
    valor = st.number_input("Valor do Serviço", min_value=0.0, step=0.01)
    if st.button("Cadastrar"):
        if nome and valor > 0:
            try:
                cadastrar_servico(nome, valor)
                st.success(f"Serviço '{nome}' cadastrado com sucesso!")
            except Exception:
                st.error("Erro ao cadastrar o serviço. Verifique se já existe.")

elif menu == "Listar Serviços":
    st.header("Serviços Disponíveis")
    servicos = listar_servicos()
    if servicos:
        for servico in servicos:
            st.write(f"ID: {servico[0]} | Nome: {servico[1]} | Valor: R${servico[2]:.2f}")
    else:
        st.info("Nenhum serviço cadastrado.")

elif menu == "Registrar Atendimento":
    st.header("Registrar Atendimento")
    servicos = listar_servicos()
    if servicos:
        servico_selecionado = st.selectbox(
            "Selecione o Serviço",
            options=[(s[0], f"{s[1]} - R${s[2]:.2f}") for s in servicos],
            format_func=lambda x: x[1]
        )
        data = st.date_input("Data do Atendimento", datetime.now().date())
        if st.button("Registrar"):
            adicionar_atendimento(data.strftime("%Y-%m-%d"), servico_selecionado[0])
            st.success("Atendimento registrado com sucesso!")
    else:
        st.warning("Nenhum serviço disponível para registro.")

elif menu == "Consultar Resumo":
    st.header("Consultar Resumo Mensal")
    mes = st.selectbox("Mês", options=list(range(1, 13)), format_func=lambda x: f"{x:02}")
    ano = st.number_input("Ano", min_value=2000, max_value=2100, value=datetime.now().year)
    if st.button("Consultar"):
        atendimentos, total = consultar_resumo(mes, ano)
        total_liquido = total * 0.7
        if atendimentos:
            for servico, quantidade, total_servico in atendimentos:
                st.write(f"Serviço: {servico} | Quantidade: {quantidade} | Total: R${total_servico:.2f}")
            st.write(f"**Valor total do mês:** R${total:.2f}")
            st.write(f"**Valor líquido (após 30%):** R${total_liquido:.2f}")
        else:
            st.info("Nenhum atendimento encontrado para o período selecionado.")

elif menu == "Deletar Serviço":
    st.header("Deletar Serviço")
    servicos = listar_servicos()
    if servicos:
        servico_nomes = [s[1] for s in servicos]
        servico_selecionado = st.selectbox("Selecione o Serviço para Deletar", servico_nomes)
        if st.button("Deletar"):
            deletar_servico(servico_selecionado)
            st.success(f"Serviço '{servico_selecionado}' deletado com sucesso!")
    else:
        st.info("Nenhum serviço disponível para deletar.")


elif menu == "Alterar Valor do Serviço":
    st.header("Alterar Valor do Serviço")
    servicos = listar_servicos()
    if servicos:
        servico_selecionado = st.selectbox(
            "Selecione o Serviço",
            options=servicos,
            format_func=lambda x: f"{x[1]} - R${x[2]:.2f}"
        )
        novo_valor = st.number_input(
            "Novo Valor do Serviço",
            min_value=0.0,
            step=0.01,
            value=servico_selecionado[2]
        )
        if st.button("Atualizar Valor"):
            try:
                atualizar_valor_servico(servico_selecionado[0], novo_valor)
                st.success(f"Valor do serviço '{servico_selecionado[1]}' atualizado para R${novo_valor:.2f}.")
            except Exception as e:
                st.error(f"Erro ao atualizar o valor: {e}")
    else:
        st.info("Nenhum serviço cadastrado.")

elif menu == "Excluir Atendimento":
    st.header("Excluir Atendimento")
    conexao = sqlite3.connect("atelier.db")
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT a.id, s.nome, a.data
        FROM atendimentos a
        JOIN servicos s ON a.servico_id = s.id
    """)
    atendimentos = cursor.fetchall()
    conexao.close()

    if atendimentos:
        atendimento_selecionado = st.selectbox(
            "Selecione o Atendimento para excluir",
            options=atendimentos,
            format_func=lambda x: f"ID: {x[0]} | Serviço: {x[1]} | Data: {x[2]}"
        )

        if st.button("Excluir Atendimento"):
            deletar_atendimento(atendimento_selecionado[0])
    else:
        st.info("Nenhum atendimento registrado para excluir.")
