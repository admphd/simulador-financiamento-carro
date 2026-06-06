# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

# Configuração inicial da página web
st.set_page_config(page_title="Simulador de Financiamento de Carros", page_icon="🚗", layout="centered")

# --- FUNÇÃO DO POP-UP DE BLOQUEIO (MODAL OBRIGATÓRIO) ---
@st.dialog("Aviso Importante")
def mostrar_aviso_legal():
    st.write(
        "Os valores mostrados durante a simulação são **valores estimados** e podem variar conforme o mercado (tanto para mais, como para menos). "
        "O valor de cada veículo utilizado no cálculo, segue a tabela base disponibilizada por cada fabricante em seu site oficial. Ao entrar em contato com a concessionária, o valor pode variar. "
        "Os valores mostrados neste simulador servem apenas de referência para o planejamento de uma possível compra."
    )
    if st.button("OK, entendi", type="primary"):
        st.session_state["confirmou_aviso"] = True
        st.rerun()

# Se for a primeira vez abrindo o programa, bloqueia a tela e exige o clique no OK
if "confirmou_aviso" not in st.session_state:
    mostrar_aviso_legal()
    st.stop()


# --- FUNÇÕES DE CARREGAMENTO DE DADOS ---

def carregar_dados_carros():
    try:
        df = pd.read_excel("lista_carros.xlsx")
        df.columns = df.columns.str.strip()
        
        mapa_colunas = {}
        for col in df.columns:
            col_lower = col.lower()
            if "marca" in col_lower: mapa_colunas[col] = "Marca"
            elif "modelo" in col_lower: mapa_colunas[col] = "Modelo"
            elif "vers" in col_lower: mapa_colunas[col] = "Versão"
            elif "ano" in col_lower: mapa_colunas[col] = "Ano"
            elif "est" in col_lower: mapa_colunas[col] = "Estado"
            elif "val" in col_lower or "pre" in col_lower: mapa_colunas[col] = "Valor"
                
        df = df.rename(columns=mapa_colunas)
        df = df.reset_index(drop=True)
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo 'lista_carros_custos.xlsx': {e}")
        return None

def carregar_dados_taxas():
    try:
        df = pd.read_excel("taxas_bancos.xlsx")
        df.columns = df.columns.str.strip()
        if "Banco" in df.columns:
            df["Banco"] = df["Banco"].astype(str).str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo 'taxas_bancos.xlsx': {e}")
        return None

def carregar_dados_ipva():
    try:
        df = pd.read_excel("IPVA.xlsx")
        df.columns = df.columns.str.strip()
        
        mapa_colunas = {}
        for col in df.columns:
            col_lower = col.lower()
            if "uf" in col_lower or "estado" in col_lower: mapa_colunas[col] = "UF"
            elif "aliquota" in col_lower or "alíquota" in col_lower: mapa_colunas[col] = "Aliquota"
            elif "licenciamento" in col_lower or "licenc" in col_lower: mapa_colunas[col] = "Licenciamento"
            
        df = df.rename(columns=mapa_colunas)
        if "UF" in df.columns:
            df["UF"] = df["UF"].astype(str).str.strip()
            
        return df
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo 'IPVA.xlsx': {e}")
        return None

# Fórmula matemática da Tabela Price
def calcular_price(valor_financiado, taxa_juros_mensal, num_parcelas):
    taxa_decimal = taxa_juros_mensal / 100
    if taxa_decimal == 0: return valor_financiado / num_parcelas
    fator = (1 + taxa_decimal) ** num_parcelas
    return valor_financiado * (taxa_decimal * fator) / (fator - 1)

# Função auxiliar para formatação de moeda brasileira (R$)
def formatar_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# --- INTERFACE WEB ---

st.title("🚗 Simulador Avançado de Financiamento & Custos")
st.markdown("Selecione um veículo da base de dados ou insira os dados manualmente para prever as parcelas e encargos.")

# Alerta fixo discreto no topo
st.caption("⚠️ Projeções estatísticas e simuladas baseadas em históricos de mercado.")
st.divider()

df_carros = carregar_dados_carros()
df_taxas = carregar_dados_taxas()
df_ipva = carregar_dados_ipva()

# Inicializa as variáveis de controle globalmente
taxa_final = None
banco_info = ""
pode_calcular = False

if df_carros is not None and df_ipva is not None:
    st.subheader("1. Seleção do Veículo")
    
    # Puxa as marcas do Excel e injeta a opção customizada no topo da lista
    lista_marcas_cru = df_carros["Marca"].dropna().unique().tolist()
    lista_marcas = ["Negociar com a concessionária"] + sorted(lista_marcas_cru)
    
    marca_sel = st.selectbox("Marca", lista_marcas, index=None, placeholder="Escolha uma marca ou selecione para negociar...")
    
    if marca_sel:
        # Inicialização das variáveis de dados do carro para o escopo
        modelo_sel = ""
        texto_exibicao_versao = ""
        ano_veiculo = 2026
        estado_veiculo = "usado"
        valor_total_carro = 0.0
        veiculo_valido = False

        # --- CAMINHO A: INSERÇÃO MANUAL ---
        if marca_sel == "Negociar com a concessionária":
            col_m1, col_m2 = st.columns(2)
            with col_m1:
                modelo_sel = st.text_input("Modelo do Veículo", placeholder="Ex: Onix, Civic, 308...")
                texto_exibicao_versao = st.text_input("Versão / Opcionais", placeholder="Ex: 1.4 LTPS, Sport, Griffe THP...")
            with col_m2:
                ano_veiculo = st.number_input("Ano de Fabricação", min_value=1900, max_value=2030, value=2026, step=1)
                estado_veiculo = st.selectbox("Condição do Veículo", ["Novo", "Usado"])
                estado_veiculo = estado_veiculo.lower()
            
            # Campo de valor que aceita APENAS números de ponto flutuante
            valor_total_carro = st.number_input("Valor do Veículo (R$)", min_value=0.0, value=0.0, step=5000.0, format="%.2f")
            
            # Validação básica para liberar o próximo passo
            if modelo_sel.strip() != "" and valor_total_carro > 0:
                veiculo_valido = True
                st.success(f"🚘 **Veículo Customizado:** {modelo_sel} {texto_exibicao_versao} | **Valor Informado:** {formatar_real(valor_total_carro)}")
            else:
                st.info("ℹ️ Preencha o nome do modelo e insira um valor válido maior que R$ 0,00 para continuar.")

        # --- CAMINHO B: SELEÇÃO DA PLANILHA ---
        else:
            df_filtrado = df_carros[df_carros["Marca"] == marca_sel]
            
            modelo_sel = st.selectbox("Modelo", sorted(df_filtrado["Modelo"].dropna().unique().tolist()))
            df_filtrado = df_filtrado[df_filtrado["Modelo"] == modelo_sel]
            
            if "Versão" in df_filtrado.columns:
                lista_versoes = df_filtrado["Versão"].dropna().unique().tolist()
                lista_versoes = [v for v in lista_versoes if str(v).strip() != "" and str(v).lower() != "nan"]
                if len(lista_versoes) > 0:
                    texto_exibicao_versao = st.selectbox("Versão", sorted(lista_versoes))
                    df_filtrado = df_filtrado[df_filtrado["Versão"] == texto_exibicao_versao]
            
            df_filtrado_copy = df_filtrado.copy().reset_index(drop=True)
            col_ano_id = "Ano" if "Ano" in df_filtrado_copy.columns else df_filtrado_copy.columns[0]
            col_est_id = "Estado" if "Estado" in df_filtrado_copy.columns else df_filtrado_copy.columns[0]
            
            labels_geradas = []
            for idx, row in df_filtrado_copy.iterrows():
                ano_cru = str(row[col_ano_id]).strip()
                ano_limpo = ano_cru.split('/')[0] if '/' in ano_cru else ano_cru
                estado_limpo = str(row[col_est_id]).strip()
                labels_geradas.append(f"{ano_limpo} - ({estado_limpo})")
                
            df_filtrado_copy["Label_Exibicao"] = labels_geradas
            dict_opcoes = dict(zip(df_filtrado_copy["Label_Exibicao"], df_filtrado_copy.index))
            
            ano_estado_sel = st.selectbox("Ano e Condição", sorted(list(dict_opcoes.keys())))
            
            id_linha_copy = dict_opcoes[ano_estado_sel]
            carro_selecionado = df_filtrado_copy.loc[id_linha_copy]
            estado_veiculo = str(carro_selecionado[col_est_id]).strip().lower()
            
            try:
                ano_str_cru = str(carro_selecionado[col_ano_id]).strip().split('/')[0]
                ano_veiculo = int(''.join(filter(str.isdigit, ano_str_cru)))
            except ValueError:
                ano_veiculo = 2026

            try:
                if isinstance(carro_selecionado, pd.DataFrame): valor_cru = carro_selecionado["Valor"].values[0]
                elif isinstance(carro_selecionado["Valor"], pd.Series): valor_cru = carro_selecionado["Valor"].values[0]
                else: valor_cru = carro_selecionado["Valor"]
                valor_total_carro = float(valor_cru)
                veiculo_valido = True
            except (KeyError, ValueError, IndexError):
                st.error("❌ Não foi possível identificar o preço correto na coluna de valor do carro.")
                st.stop()
                
            st.success(f"🚘 **Veículo Definido:** {marca_sel} {modelo_sel} {texto_exibicao_versao} | **Valor:** {formatar_real(valor_total_carro)}")

        # --- SEÇÃO 2: LOCALIDADE (Só abre se houver veículo válido) ---
        if veiculo_valido:
            st.divider()
            st.subheader("2. Localidade de Emplacamento")
            lista_ufs = sorted(df_ipva["UF"].dropna().unique().tolist())
            uf_sel = st.selectbox("Selecione o Estado (UF) para calcular o IPVA e Licenciamento", lista_ufs, index=None, placeholder="Escolha a UF de destino...")
            
            if uf_sel:
                linha_ipva = df_ipva[df_ipva["UF"] == uf_sel]
                
                if not linha_ipva.empty:
                    aliquota_cru = linha_ipva["Aliquota"].values[0]
                    aliquota_ipva = float(aliquota_cru) / 100 if float(aliquota_cru) > 1 else float(aliquota_cru)
                    
                    try:
                        licenciamento_cru = linha_ipva["Licenciamento"].values[0]
                        valor_licenciamento = float(licenciamento_cru) if not pd.isna(licenciamento_cru) else 274.61
                    except (KeyError, ValueError, IndexError):
                        valor_licenciamento = 274.61
                        st.warning("⚠️ Coluna 'Licenciamento' não encontrada ou inválida. Usando taxa padrão.")
                else:
                    aliquota_ipva = 0.0375
                    valor_licenciamento = 274.61
                    st.warning(f"⚠️ Dados tributários não localizados para '{uf_sel}'. Aplicando taxas padrões.")

                st.caption(f"📍 **Estado Ativo:** {uf_sel} | IPVA: **{aliquota_ipva*100:.2f}%** | Licenciamento: **{formatar_real(valor_licenciamento)}**")
                
                st.divider()
                st.subheader("3. Condições do Financiamento & Custos Variáveis")
                
                col_valores, col_prazo, col_extras = st.columns(3)
                with col_valores:
                    valor_entrada = st.number_input("Valor da Entrada (R$)", min_value=0.0, value=0.0, step=1000.0, format="%.2f")
                with col_prazo:
                    num_parcelas = st.number_input("Quantidade de Parcelas (Meses)", min_value=1, max_value=120, value=60, step=1)
                with col_extras:
                    gastos_extras = st.number_input("Gastos Extras Mensais (R$)", min_value=0.0, value=0.0, step=50.0, format="%.2f")
                    
                valor_financiado = valor_total_carro - valor_entrada

                st.write("**Como deseja definir a taxa de juros?**")
                tipo_taxa = st.radio("Escolha uma opção:", ["Selecionar Banco da Lista", "Digitar Taxa Manualmente"], label_visibility="collapsed")
                
                if tipo_taxa == "Selecionar Banco da Lista":
                    if df_taxas is not None:
                        df_taxas = df_taxas.dropna(subset=["Banco"])
                        lista_bancos = sorted(df_taxas["Banco"].unique().tolist())
                        banco_sel = st.selectbox("Selecione o Banco", lista_bancos, index=None, placeholder="Escolha um banco da lista...")
                        
                        if banco_sel:
                            linha_banco = df_taxas[df_taxas["Banco"] == banco_sel]
                            colunas_existentes = df_taxas.columns.tolist()
                            if "TAXA" in colunas_existentes: taxa_final = float(linha_banco["TAXA"].values[0])
                            elif "Taxa" in colunas_existentes: taxa_final = float(linha_banco["Taxa"].values[0])
                            elif "Taxas" in colunas_existentes: taxa_final = float(linha_banco["Taxas"].values[0])
                            else: taxa_final = float(linha_banco.iloc[:, 1].values[0])
                            banco_info = f"via **{banco_sel}**"
                            pode_calcular = True
                        else:
                            st.info("ℹ️ Selecione um banco acima para visualizar as taxas e gerar as projeções financeiras.")
                    else:
                        st.warning("⚠️ Base de dados de bancos não encontrada. Digite a taxa manualmente.")
                        taxa_final = st.number_input("Taxa de Juros (% a.m.)", min_value=0.0, value=0.0, step=0.1)
                        pode_calcular = True
                else:
                    taxa_final = st.number_input("Digite a Taxa de Juros (% a.m.)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
                    banco_info = "(Definida Manualmente)"
                    pode_calcular = True

                st.divider()

                if pode_calcular and taxa_final is not None:
                    # --- MEMÓRIA DE CÁLCULO DE CUSTOS ---
                    if "novo" in estado_veiculo:
                        base_calculo_custos = valor_total_carro * 0.95
                        is_carro_novo = True
                        custo_manutencao_mensal = 60.0
                    else:
                        base_calculo_custos = valor_total_carro
                        is_carro_novo = False
                        if ano_veiculo >= 2020: custo_manutencao_mensal = 75.0
                        else: custo_manutencao_mensal = 100.0

                    valor_ipva = base_calculo_custos * aliquota_ipva
                    
                    total_impostos_com_ipva = valor_ipva + valor_licenciamento
                    impostos_mensal_com_ipva = total_impostos_com_ipva / 12
                    impostos_mensal_sem_ipva = valor_licenciamento / 12

                    valor_seguro_anual = base_calculo_custos * 0.055
                    seguro_mensal = valor_seguro_anual / 12

                    parcela_mensal = 0.0
                    if valor_financiado > 0:
                        parcela_mensal = calcular_price(valor_financiado, taxa_final, num_parcelas)

                    if is_carro_novo:
                        custo_mensal_1_ano = parcela_mensal + impostos_mensal_sem_ipva + seguro_mensal + custo_manutencao_mensal + gastos_extras
                        custo_mensal_geral = parcela_mensal + impostos_mensal_com_ipva + seguro_mensal + custo_manutencao_mensal + gastos_extras
                    else:
                        custo_mensal_geral = parcela_mensal + impostos_mensal_com_ipva + seguro_mensal + custo_manutencao_mensal + gastos_extras

                    # --- EXIBIÇÃO DAS ABAS DE RESULTADOS ---
                    tab_financiamento, tab_custos_adicionais = st.tabs(["📋 Financiamento", "💰 Custos de Propriedade Mensais"])

                    with tab_financiamento:
                        if valor_financiado <= 0:
                            st.warning("⚠️ O valor da entrada é maior ou igual ao valor de mercado do veículo. Não há saldo a financiar.")
                        else:
                            total_pago = parcela_mensal * num_parcelas
                            total_juros = total_pago - valor_financiado

                            st.info(f"📊 Taxa aplicada: **{taxa_final:.2f}% a.m.** {banco_info}. Fonte: Banco Central.")
                            
                            c_res1, c_res2 = st.columns(2)
                            with c_res1:
                                st.metric(label="Valor da Parcela Mensal", value=formatar_real(parcela_mensal))
                                st.metric(label="Valor Efetivamente Financiado", value=formatar_real(valor_financiado))
                            with c_res2:
                                st.metric(label="Total de Juros Pagos", value=formatar_real(total_juros))
                                st.metric(label="Custo Total do Financiamento", value=formatar_real(total_pago))

                    with tab_custos_adicionais:
                        st.subheader("📊 Resumo do Custo Mensal Consolidado")
                        
                        if is_carro_novo:
                            c_total1, c_total2 = st.columns(2)
                            with c_total1:
                                st.metric(label="💰 CUSTO TOTAL (Mensal - No 1º Ano)", value=formatar_real(custo_mensal_1_ano))
                            with c_total2:
                                st.metric(label="💰 CUSTO TOTAL (Mensal - Do 2º Ano em Diante)", value=formatar_real(custo_mensal_geral))
                        else:
                            st.metric(label="💰 CUSTO TOTAL DO VEÍCULO (Por Mês)", value=formatar_real(custo_mensal_geral))
                        st.divider()
                        
                        if is_carro_novo:
                            st.success(f"✨ **Veículo Zero Km:** Nos estados de GO e MS, veículos novos são livres de imposto de IPVA no 1º ano! Para os demais estados, considerar o valor de imposto de IPVA a partir do segundo ano. Projeções refletem a alíquota de {aliquota_ipva*100:.2f}% e taxa de licenciamento de {formatar_real(valor_licenciamento)} ({uf_sel}) a partir do 2º ano.")
                            st.warning("⚠️ **Alíquota de IPVA:** Para os estados com Alíquota de IPVA variável, está sendo considerada a alíquota de maior valor para este cálculo.")
                            st.warning("⚠️ **Lembrete de Custos Extras (Falta incluir):** Lembre-se que para rodar com o veículo Novo você deverá levar em consideração os valores de **registro no Detran** e o **primeiro emplacamento**, que não estão inclusos nas contas automáticas acima.")
                        else:
                            st.info(f"ℹ️ **Veículo Usado ({ano_veiculo}):** IPVA, Licenciamento e Seguro calculados com base no valor integral atual e tabela regional de {uf_sel}.")
                            st.warning("⚠️ **Lembrete de Custos Extras (Falta incluir):** Lembre-se que para veículos usados você deverá levar em consideração as custas de **taxas de vistoria** e **transferência do veículo** junto ao Detran, que não estão inclusas no cálculo.")
                        
                        col_ipva, col_seguro, col_manutencao = st.columns(3)
                        
                        with col_ipva:
                            st.markdown(f"### 🏛️ Impostos Estaduais")
                            st.metric(label=f"Valor do IPVA ({aliquota_ipva*100:.2f}%)", value=formatar_real(valor_ipva))
                            st.metric(label="Licenciamento (Tabela)", value=formatar_real(valor_licenciamento))
                            st.markdown("---")
                            st.metric(label="Total Impostos (Anual)", value=formatar_real(total_impostos_com_ipva))
                            st.metric(label="Custo Mensal Impostos", value=formatar_real(impostos_mensal_com_ipva))
                            if is_carro_novo:
                                st.metric(label="Custo Mensal Impostos (1º Ano)", value=formatar_real(impostos_mensal_sem_ipva))
                            else: st.metric(label="Custo Mensal Impostos", value=formatar_real(impostos_mensal_com_ipva))
                                
                        with col_seguro:
                            st.markdown("### 🛡️ Seguro Estimado")
                            st.metric(label="Seguro Médio (Anual)", value=formatar_real(valor_seguro_anual))
                            st.write("") 
                            st.markdown("---")
                            st.metric(label="Custo Mensal Seguro", value=formatar_real(seguro_mensal))
                            st.caption("⚠️ **Nota Informativa:** O valor do seguro depende de muitas variáveis reais (idade do condutor, gênero, local de residência histórica, presença de garagem, histórico de sinistros, uso diário do carro, etc.). O valor acima é meramente ilustrativo e estatístico baseado no perfil do veículo.")
                                
                        with col_manutencao:
                            st.markdown("### 🔧 Manutenção & Extras")
                            st.metric(label="Custo Médio de Manutenção", value=formatar_real(custo_manutencao_mensal), help=f"Perfil: {'Novo' if is_carro_novo else 'Usado'} ano {ano_veiculo}.")
                            st.metric(label="Seus Gastos Extras", value=formatar_real(gastos_extras))
                            st.markdown("---")
                            st.metric(label="Financiamento (Parcela)", value=formatar_real(parcela_mensal))
            else:
                st.info("💡 Por favor, selecione o **Estado (UF)** acima para carregar as regras tributárias regionais.")